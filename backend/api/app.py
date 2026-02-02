"""
Flask API for PLAUGE Plagiarism Detection System
Connects the frontend UI to the backend ML models
Supports: Unified analysis with corpus + web search + AI detection
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
import time
import tempfile
import docx
import json
from PyPDF2 import PdfReader
from nltk.tokenize import sent_tokenize

# Add parent directory to path to import backend modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.ml_models.plagiarism_detector import PlagiarismDetector, download_nltk_resources
from backend.api.web_search import WebSearchManager, AIContentScanner

# Initialize Flask to serve frontend
app = Flask(__name__, static_folder='../../frontend', static_url_path='')
CORS(app)

# Corpus path
CORPUS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../corpus'))


def load_corpus():
    """Load all documents from the corpus directory"""
    documents = []
    names = []
    
    if not os.path.exists(CORPUS_PATH):
        print(f"Warning: Corpus path does not exist: {CORPUS_PATH}")
        return documents, names
    
    for category in os.listdir(CORPUS_PATH):
        category_path = os.path.join(CORPUS_PATH, category)
        if os.path.isdir(category_path):
            for filename in os.listdir(category_path):
                if filename.endswith('.txt'):
                    filepath = os.path.join(category_path, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            if content.strip():
                                documents.append(content)
                                names.append({
                                    'title': filename.replace('.txt', '').replace('_', ' ').title(),
                                    'category': category,
                                    'filepath': filepath
                                })
                    except Exception as e:
                        print(f"Error loading {filepath}: {e}")
    
    return documents, names


def extract_text_from_file(file):
    """Extract text from uploaded file (supports .txt, .pdf, .docx)"""
    filename = file.filename.lower()
    
    if filename.endswith('.txt'):
        return file.read().decode('utf-8', errors='ignore')
    
    elif filename.endswith('.pdf'):
        # Save to temp file and read with PyPDF2
        # Use mkstemp to avoid Windows file locking issues
        fd, tmp_path = tempfile.mkstemp(suffix='.pdf')
        os.close(fd) # Close the file handle immediately
        
        try:
            file.save(tmp_path)
            text = ""
            reader = PdfReader(tmp_path)
            for page in reader.pages:
                text += page.extract_text() or ""
            return text
        finally:
            try:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
            except Exception as e:
                print(f"Warning: Could not remove temp file {tmp_path}: {e}")
    
    elif filename.endswith('.docx'):
        # Save to temp file and read with python-docx
        # Use mkstemp to avoid Windows file locking issues
        fd, tmp_path = tempfile.mkstemp(suffix='.docx')
        os.close(fd)
        
        try:
            file.save(tmp_path)
            doc = docx.Document(tmp_path)
            text = ""
            for para in doc.paragraphs:
                text += para.text + "\n"
            return text
        finally:
            try:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
            except Exception as e:
                print(f"Warning: Could not remove temp file {tmp_path}: {e}")
    
    else:
        raise ValueError(f"Unsupported file type: {filename}")


@app.route('/')
def index():
    """Serve the frontend application"""
    return app.send_static_file('index.html')


# History File Path
HISTORY_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../history.json'))

def load_history_data():
    """Load history from JSON file"""
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_to_history(record):
    """Save a new record to history"""
    history = load_history_data()
    # Add timestamp and ID
    record['id'] = str(int(time.time() * 1000))
    record['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
    
    # Prepend new record (newest first)
    history.insert(0, record)
    
    # Keep last 50 records
    history = history[:50]
    
    try:
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"Error saving history: {e}")

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get analysis history"""
    return jsonify(load_history_data())

@app.route('/api/history', methods=['DELETE'])
def clear_history():
    """Clear analysis history"""
    try:
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
        return jsonify({'message': 'History cleared'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_document():
    """
    Unified Analysis Endpoint
    - Auto-detects keywords from submitted document
    - Searches web sources (arXiv, Semantic Scholar, Wikipedia, OpenAlex)
    - Compares against local corpus (600+ papers)
    - Runs AI content detection
    - Returns combined results
    """
    print("\n" + "!"*50)
    print("🔥 API REQUEST RECEIVED: /api/analyze")
    print("!"*50 + "\n")
    start_time = time.time()
    
    # Check for uploaded file
    if 'document' not in request.files:
        return jsonify({'error': 'No document uploaded'}), 400
    
    file = request.files['document']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        # Extract text from uploaded file
        print(f"📄 Processing file: {file.filename}")
        submitted_text = extract_text_from_file(file)
        
        extracted_len = len(submitted_text.strip()) if submitted_text else 0
        print(f"   ✓ Extracted {extracted_len} characters")

        if not submitted_text or extracted_len < 10:
            print("   ❌ Error: Document text is empty or too short.")
            return jsonify({'error': 'Document is empty or contains no selectable text (scanned PDFs not supported).'}), 400
        
        # 1. Load local corpus
        print("📚 Loading corpus...")
        corpus_docs, corpus_names = load_corpus()

        print(f"   ✓ Loaded {len(corpus_docs)} corpus documents")
        
        # 2. Initialize web search and get web documents
        print("🌐 Searching web sources...")
        search_manager = WebSearchManager()
        web_papers = search_manager.search_all(text_content=submitted_text, max_per_source=3)
        web_docs, web_metadata = search_manager.prepare_for_analysis(web_papers)
        print(f"   ✓ Found {len(web_docs)} web documents")
        
        # 3. Run AI content detection
        print("🤖 Running AI content analysis...")
        ai_result = AIContentScanner.analyze(submitted_text)
        print(f"   ✓ AI Score: {ai_result['score']}% ({ai_result['level']})")
        
        # 4. Combine all documents for analysis
        all_docs = [submitted_text] + corpus_docs + web_docs
        all_names = [{'title': 'Submitted Document', 'category': 'User Upload'}] + corpus_names
        
        # Add web metadata
        for meta in web_metadata:
            all_names.append({
                'title': meta['title'],
                'category': f"Web - {meta['source']}",
                'authors': meta.get('authors', ''),
                'url': meta.get('url', '')
            })
        
        # 5. Run plagiarism detection
        print("🔍 Running plagiarism analysis...")
        detector = PlagiarismDetector(max_features=5000)
        detector.add_documents(all_docs)
        results = detector.analyze()
        
        # 6. Calculate results (compare submitted doc against all others)
        matches = []
        for result in results['pairwise_results']:
            # Only get comparisons involving the submitted document (index 0)
            if result['doc1_index'] == 0:
                other_idx = result['doc2_index']
                if other_idx < len(all_names):
                    match_info = all_names[other_idx]
                    match_doc_content = all_docs[other_idx]
                    
                    # Get snippet
                    snippet = get_best_matching_snippet(submitted_text, match_doc_content)
                    
                    matches.append({
                        'title': match_info.get('title', 'Unknown Document'),
                        'category': match_info.get('category', 'Unknown'),
                        'score': int(result['similarity_percentage']),
                        'authors': match_info.get('authors', ''),
                        'url': match_info.get('url', ''),
                        'snippet': snippet
                    })
        
        # Sort by score descending
        matches.sort(key=lambda x: x['score'], reverse=True)
        top_matches = matches[:10]  # Top 10 matches
        
        # Calculate statistics
        all_scores = [m['score'] for m in matches]
        highest_match = max(all_scores) if all_scores else 0
        avg_similarity = round(sum(all_scores) / len(all_scores), 1) if all_scores else 0
        
        # Overall score is the highest match found
        overall_score = highest_match
        
        # Calculate analysis time
        analysis_time = f"{round(time.time() - start_time, 1)}s"
        
        print(f"✅ Analysis complete in {analysis_time}")
        print(f"   ✓ Overall Score: {overall_score}%")
        print(f"   ✓ Top Match: {top_matches[0]['title'] if top_matches else 'None'}")
        
        # 7. Build response
        response_data = {
            'overallScore': overall_score,
            'highestMatch': highest_match,
            'avgSimilarity': avg_similarity,
            'documentsCompared': len(all_docs) - 1,  # Exclude submitted doc
            'analysisTime': analysis_time,
            'matches': top_matches,
            'aiDetection': ai_result
        }
        
        # Save to history
        save_to_history({
            'fileName': file.filename,
            'overallScore': overall_score,
            'aiScore': ai_result['score'],
            'topMatch': top_matches[0]['title'] if top_matches else 'None',
            'matchesCount': len(matches)
        })
        
        return jsonify(response_data)
    
    except Exception as e:
        print(f"❌ Analysis error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


def get_best_matching_snippet(source_text, target_text):
    """Find the sentence in target_text that best matches any part of source_text"""
    try:
        # Basic caching/optimization could go here, but for now direct comparison
        source_sents = sent_tokenize(source_text)[:50] # Check first 50 sentences to save time
        target_sents = sent_tokenize(target_text)
        
        best_match = "No specific text match found."
        max_overlap = 0
        
        # Pre-process source sentences into sets of words
        source_sets = [set(s.lower().split()) for s in source_sents if len(s.split()) > 5]
        
        for t_sent in target_sents:
            words = t_sent.lower().split()
            if len(words) < 5: continue 
            t_set = set(words)
            
            for s_set in source_sets:
                # Jaccard-ish similarity (intersection / smaller_set_len)
                intersection = len(s_set.intersection(t_set))
                if intersection > 0:
                    score = intersection / min(len(s_set), len(t_set))
                    if score > max_overlap:
                        max_overlap = score
                        best_match = t_sent
        
        if max_overlap > 0.3: # Threshold
            return "..." + best_match + "..."
        elif max_overlap > 0:
             return "..." + best_match + "..."
        return "Similar concepts or formatting detected."
    except:
        return "Content analysis unavailable."


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    corpus_docs, _ = load_corpus()
    return jsonify({
        'status': 'healthy',
        'corpus_size': len(corpus_docs),
        'version': '2.0.0-unified'
    })


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Starting PLAUGE API Server (Unified Analysis)")
    print("="*60)
    
    # Download NLTK resources
    print("\n📥 Downloading NLTK resources...")
    download_nltk_resources()
    
    # Check corpus
    corpus_docs, corpus_names = load_corpus()
    print(f"\n📚 Loaded {len(corpus_docs)} documents from corpus")
    
    print("\n✅ Server ready!")
    print("   👉 Open App: http://localhost:5000")
    print("   📊 API Endpoint: POST /api/analyze")
    print("   🏥 Health Check: GET /api/health")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
