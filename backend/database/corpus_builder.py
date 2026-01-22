"""
CORPUS BUILDER - Build a comprehensive plagiarism detection corpus

Sources:
1. arXiv API - Free, unlimited academic paper abstracts
2. Semantic Scholar API - Free academic paper database (100 req/5min for unauthenticated)
3. CORE API - Open access research papers (free API key available)
4. CrossRef API - Metadata and abstracts from millions of papers
5. OpenAlex API - Free and open catalog of scholarly papers

Features:
- SQLite database for efficient storage and deduplication
- Multiple academic sources
- Progress tracking and resume capability
- Topic-based downloading

Usage:
    python corpus_builder.py                        # Interactive mode
    python corpus_builder.py --download "machine learning" 50
    python corpus_builder.py --stats               # Show database stats
    python corpus_builder.py --export              # Export to txt files
"""

import urllib.request
import urllib.parse
import json
import xml.etree.ElementTree as ET
import sqlite3
import os
import time
import sys
import hashlib
from datetime import datetime
import ssl


# ============================================================================
# Configuration
# ============================================================================

CORPUS_FOLDER = "corpus"
DATABASE_FILE = "corpus_database.db"

# API Endpoints
ARXIV_API = "http://export.arxiv.org/api/query"
SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1/paper/search"
CROSSREF_API = "https://api.crossref.org/works"
OPENALEX_API = "https://api.openalex.org/works"

# Rate limiting (seconds between requests)
RATE_LIMITS = {
    'arxiv': 3.0,
    'semantic_scholar': 1.0,
    'crossref': 1.0,
    'openalex': 0.1
}


# ============================================================================
# Database Management
# ============================================================================

class CorpusDatabase:
    """SQLite database for managing the corpus."""
    
    def __init__(self, db_file=DATABASE_FILE):
        self.db_file = db_file
        self.conn = None
        self._connect()
        self._create_tables()
    
    def _connect(self):
        self.conn = sqlite3.connect(self.db_file)
        self.conn.row_factory = sqlite3.Row
    
    def _create_tables(self):
        cursor = self.conn.cursor()
        
        # Main papers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS papers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content_hash TEXT UNIQUE,
                title TEXT NOT NULL,
                abstract TEXT NOT NULL,
                source TEXT,
                source_id TEXT,
                authors TEXT,
                year INTEGER,
                topics TEXT,
                url TEXT,
                added_date TEXT,
                word_count INTEGER
            )
        ''')
        
        # Topics index table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS topics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                paper_count INTEGER DEFAULT 0
            )
        ''')
        
        # Download history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS download_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT,
                source TEXT,
                papers_found INTEGER,
                papers_added INTEGER,
                download_date TEXT
            )
        ''')
        
        self.conn.commit()
    
    def content_hash(self, title, abstract):
        """Generate a hash to detect duplicates."""
        content = f"{title.lower().strip()}{abstract.lower().strip()}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def add_paper(self, title, abstract, source, source_id=None, authors=None, 
                  year=None, topics=None, url=None):
        """Add a paper to the database, returns True if added (not duplicate)."""
        
        if not title or not abstract or len(abstract) < 50:
            return False
        
        content_hash = self.content_hash(title, abstract)
        word_count = len(abstract.split())
        
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO papers 
                (content_hash, title, abstract, source, source_id, authors, 
                 year, topics, url, added_date, word_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                content_hash, title, abstract, source, source_id,
                authors, year, topics, url,
                datetime.now().isoformat(), word_count
            ))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Duplicate
            return False
    
    def get_stats(self):
        """Get corpus statistics."""
        cursor = self.conn.cursor()
        
        cursor.execute('SELECT COUNT(*) as total FROM papers')
        total = cursor.fetchone()['total']
        
        cursor.execute('SELECT source, COUNT(*) as count FROM papers GROUP BY source')
        by_source = {row['source']: row['count'] for row in cursor.fetchall()}
        
        cursor.execute('SELECT SUM(word_count) as total_words FROM papers')
        total_words = cursor.fetchone()['total_words'] or 0
        
        cursor.execute('SELECT MIN(year) as min_year, MAX(year) as max_year FROM papers WHERE year IS NOT NULL')
        year_range = cursor.fetchone()
        
        return {
            'total_papers': total,
            'by_source': by_source,
            'total_words': total_words,
            'year_range': (year_range['min_year'], year_range['max_year']) if year_range['min_year'] else None
        }
    
    def get_all_papers(self):
        """Get all papers from database."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM papers ORDER BY id')
        return cursor.fetchall()
    
    def search_papers(self, query):
        """Search papers by title or abstract."""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM papers 
            WHERE title LIKE ? OR abstract LIKE ?
            ORDER BY id
        ''', (f'%{query}%', f'%{query}%'))
        return cursor.fetchall()
    
    def log_download(self, query, source, found, added):
        """Log download activity."""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO download_history (query, source, papers_found, papers_added, download_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (query, source, found, added, datetime.now().isoformat()))
        self.conn.commit()
    
    def close(self):
        if self.conn:
            self.conn.close()


# ============================================================================
# API Fetchers
# ============================================================================

def create_ssl_context():
    """Create SSL context that works on Windows."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def fetch_arxiv(query, max_results=50):
    """Fetch papers from arXiv API."""
    papers = []
    
    query_encoded = urllib.parse.quote(query)
    url = f"{ARXIV_API}?search_query=all:{query_encoded}&start=0&max_results={max_results}"
    
    try:
        response = urllib.request.urlopen(url, timeout=30)
        xml_data = response.read().decode('utf-8')
        
        root = ET.fromstring(xml_data)
        namespace = {'atom': 'http://www.w3.org/2005/Atom'}
        
        for entry in root.findall('atom:entry', namespace):
            title = entry.find('atom:title', namespace)
            summary = entry.find('atom:summary', namespace)
            entry_id = entry.find('atom:id', namespace)
            published = entry.find('atom:published', namespace)
            
            # Get authors
            authors = []
            for author in entry.findall('atom:author', namespace):
                name = author.find('atom:name', namespace)
                if name is not None:
                    authors.append(name.text)
            
            if title is not None and summary is not None:
                year = None
                if published is not None:
                    try:
                        year = int(published.text[:4])
                    except:
                        pass
                
                papers.append({
                    'title': ' '.join(title.text.split()),
                    'abstract': ' '.join(summary.text.split()),
                    'source': 'arxiv',
                    'source_id': entry_id.text if entry_id else None,
                    'authors': ', '.join(authors[:5]),
                    'year': year,
                    'url': entry_id.text if entry_id else None,
                    'topics': query
                })
    
    except Exception as e:
        print(f"   ⚠️  arXiv error: {e}")
    
    return papers


def fetch_semantic_scholar(query, max_results=50):
    """Fetch papers from Semantic Scholar API."""
    papers = []
    
    params = urllib.parse.urlencode({
        'query': query,
        'limit': min(max_results, 100),
        'fields': 'title,abstract,authors,year,externalIds,url'
    })
    
    url = f"{SEMANTIC_SCHOLAR_API}?{params}"
    
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'PlagiarismDetector/1.0')
        
        ctx = create_ssl_context()
        response = urllib.request.urlopen(req, timeout=30, context=ctx)
        data = json.loads(response.read().decode('utf-8'))
        
        for paper in data.get('data', []):
            if paper.get('abstract'):
                authors = [a.get('name', '') for a in paper.get('authors', [])[:5]]
                
                papers.append({
                    'title': paper.get('title', ''),
                    'abstract': paper.get('abstract', ''),
                    'source': 'semantic_scholar',
                    'source_id': paper.get('paperId'),
                    'authors': ', '.join(authors),
                    'year': paper.get('year'),
                    'url': paper.get('url'),
                    'topics': query
                })
    
    except Exception as e:
        print(f"   ⚠️  Semantic Scholar error: {e}")
    
    return papers


def fetch_crossref(query, max_results=50):
    """Fetch papers from CrossRef API."""
    papers = []
    
    params = urllib.parse.urlencode({
        'query': query,
        'rows': min(max_results, 100),
        'filter': 'has-abstract:true'
    })
    
    url = f"{CROSSREF_API}?{params}"
    
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'PlagiarismDetector/1.0 (mailto:user@example.com)')
        
        ctx = create_ssl_context()
        response = urllib.request.urlopen(req, timeout=30, context=ctx)
        data = json.loads(response.read().decode('utf-8'))
        
        for item in data.get('message', {}).get('items', []):
            abstract = item.get('abstract', '')
            # Clean HTML tags from abstract
            import re
            abstract = re.sub(r'<[^>]+>', '', abstract)
            
            if abstract and len(abstract) > 50:
                title = item.get('title', [''])[0] if item.get('title') else ''
                authors = [f"{a.get('given', '')} {a.get('family', '')}".strip() 
                          for a in item.get('author', [])[:5]]
                
                year = None
                if item.get('published-print'):
                    year = item['published-print'].get('date-parts', [[None]])[0][0]
                elif item.get('created'):
                    year = item['created'].get('date-parts', [[None]])[0][0]
                
                papers.append({
                    'title': title,
                    'abstract': abstract,
                    'source': 'crossref',
                    'source_id': item.get('DOI'),
                    'authors': ', '.join(authors),
                    'year': year,
                    'url': item.get('URL'),
                    'topics': query
                })
    
    except Exception as e:
        print(f"   ⚠️  CrossRef error: {e}")
    
    return papers


def fetch_openalex(query, max_results=50):
    """Fetch papers from OpenAlex API (free and open)."""
    papers = []
    
    params = urllib.parse.urlencode({
        'search': query,
        'per-page': min(max_results, 200),
        'filter': 'has_abstract:true'
    })
    
    url = f"{OPENALEX_API}?{params}"
    
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'mailto:user@example.com')
        
        ctx = create_ssl_context()
        response = urllib.request.urlopen(req, timeout=30, context=ctx)
        data = json.loads(response.read().decode('utf-8'))
        
        for work in data.get('results', []):
            abstract_inverted = work.get('abstract_inverted_index', {})
            
            # Reconstruct abstract from inverted index
            if abstract_inverted:
                words = {}
                for word, positions in abstract_inverted.items():
                    for pos in positions:
                        words[pos] = word
                abstract = ' '.join([words[i] for i in sorted(words.keys())])
            else:
                continue
            
            if len(abstract) > 50:
                title = work.get('title', '')
                authors = [a.get('author', {}).get('display_name', '') 
                          for a in work.get('authorships', [])[:5]]
                
                papers.append({
                    'title': title,
                    'abstract': abstract,
                    'source': 'openalex',
                    'source_id': work.get('id'),
                    'authors': ', '.join(authors),
                    'year': work.get('publication_year'),
                    'url': work.get('doi'),
                    'topics': query
                })
    
    except Exception as e:
        print(f"   ⚠️  OpenAlex error: {e}")
    
    return papers


# ============================================================================
# Corpus Builder
# ============================================================================

class CorpusBuilder:
    """Build and manage the plagiarism detection corpus."""
    
    def __init__(self):
        self.db = CorpusDatabase()
        
    def download_topic(self, topic, count_per_source=25, sources=None):
        """Download papers on a topic from multiple sources."""
        
        if sources is None:
            sources = ['arxiv', 'semantic_scholar', 'crossref', 'openalex']
        
        print(f"\n📥 Downloading papers on: '{topic}'")
        print(f"   Sources: {', '.join(sources)}")
        print("-" * 50)
        
        total_found = 0
        total_added = 0
        
        for source in sources:
            print(f"\n   🔍 Fetching from {source}...")
            
            fetcher = {
                'arxiv': fetch_arxiv,
                'semantic_scholar': fetch_semantic_scholar,
                'crossref': fetch_crossref,
                'openalex': fetch_openalex
            }.get(source)
            
            if not fetcher:
                continue
            
            papers = fetcher(topic, count_per_source)
            found = len(papers)
            added = 0
            
            for paper in papers:
                if self.db.add_paper(**paper):
                    added += 1
            
            total_found += found
            total_added += added
            
            print(f"      Found: {found}, New: {added}, Duplicates: {found - added}")
            
            # Rate limiting
            time.sleep(RATE_LIMITS.get(source, 1.0))
        
        self.db.log_download(topic, ','.join(sources), total_found, total_added)
        
        print(f"\n   ✅ Topic complete: {total_added} new papers added")
        return total_added
    
    def bulk_download(self, topics_with_counts):
        """Download multiple topics."""
        print("\n" + "=" * 70)
        print("           BULK CORPUS DOWNLOAD")
        print("=" * 70)
        
        total = 0
        for topic, count in topics_with_counts:
            added = self.download_topic(topic, count_per_source=count)
            total += added
            time.sleep(2)  # Be nice to APIs
        
        print("\n" + "=" * 70)
        print(f"✅ Bulk download complete! {total} new papers added")
        self.print_stats()
    
    def print_stats(self):
        """Print corpus statistics."""
        stats = self.db.get_stats()
        
        print("\n" + "=" * 70)
        print("           📊 CORPUS STATISTICS")
        print("=" * 70)
        
        print(f"\n   Total Papers: {stats['total_papers']:,}")
        print(f"   Total Words:  {stats['total_words']:,}")
        
        if stats['year_range']:
            print(f"   Year Range:   {stats['year_range'][0]} - {stats['year_range'][1]}")
        
        print("\n   Papers by Source:")
        for source, count in stats['by_source'].items():
            bar = "█" * min(count // 5, 30)
            print(f"      {source:20} {count:5} {bar}")
        
        print("=" * 70)
    
    def export_to_files(self, folder=CORPUS_FOLDER):
        """Export database to individual text files."""
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        papers = self.db.get_all_papers()
        
        print(f"\n📤 Exporting {len(papers)} papers to '{folder}/'...")
        
        for paper in papers:
            # Create filename from title
            safe_title = "".join(c if c.isalnum() or c in ' _-' else '' 
                                 for c in paper['title'][:40])
            safe_title = safe_title.replace(' ', '_').lower()
            filename = f"{paper['source']}_{paper['id']:04d}_{safe_title}.txt"
            filepath = os.path.join(folder, filename)
            
            content = f"""Title: {paper['title']}

Source: {paper['source']}
Authors: {paper['authors'] or 'Unknown'}
Year: {paper['year'] or 'Unknown'}
URL: {paper['url'] or 'N/A'}

Abstract:
{paper['abstract']}
"""
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        
        print(f"   ✅ Exported {len(papers)} papers!")
    
    def close(self):
        self.db.close()


# ============================================================================
# Interactive Menu
# ============================================================================

def print_menu():
    print("\n" + "=" * 70)
    print("           📚 CORPUS BUILDER - Main Menu")
    print("=" * 70)
    print("""
   1. 📥 Quick Download (Recommended Topics)
   2. 🔍 Download by Topic (Custom Search)
   3. 📊 Show Corpus Statistics  
   4. 📤 Export to Text Files
   5. 🗑️  Clear and Rebuild Corpus
   6. ❌ Exit
""")


def quick_download():
    """Download a comprehensive set of academic papers."""
    topics = [
        ("machine learning", 20),
        ("deep learning neural networks", 20),
        ("natural language processing NLP", 20),
        ("plagiarism detection", 15),
        ("text similarity", 15),
        ("document comparison", 10),
        ("semantic similarity", 10),
        ("information retrieval", 10),
        ("text mining", 10),
        ("computational linguistics", 10),
        ("artificial intelligence", 15),
        ("data science", 10),
        ("computer vision", 10),
        ("reinforcement learning", 10),
        ("transformer models", 10),
    ]
    
    builder = CorpusBuilder()
    builder.bulk_download(topics)
    builder.export_to_files()
    builder.close()


def custom_download():
    """Download papers on a custom topic."""
    topic = input("\n   Enter topic to search: ").strip()
    if not topic:
        print("   ⚠️  No topic entered.")
        return
    
    try:
        count = int(input("   Papers per source (default 25): ").strip() or "25")
    except ValueError:
        count = 25
    
    builder = CorpusBuilder()
    builder.download_topic(topic, count_per_source=count)
    
    export = input("\n   Export to text files? (y/n): ").strip().lower()
    if export == 'y':
        builder.export_to_files()
    
    builder.close()


def show_stats():
    """Show corpus statistics."""
    builder = CorpusBuilder()
    builder.print_stats()
    builder.close()


def export_corpus():
    """Export corpus to text files."""
    builder = CorpusBuilder()
    builder.export_to_files()
    builder.close()


def clear_corpus():
    """Clear and rebuild corpus."""
    confirm = input("\n   ⚠️  This will delete all papers. Type 'DELETE' to confirm: ")
    if confirm == 'DELETE':
        if os.path.exists(DATABASE_FILE):
            os.remove(DATABASE_FILE)
            print("   ✅ Database cleared!")
        
        # Also clear corpus folder
        if os.path.exists(CORPUS_FOLDER):
            for f in os.listdir(CORPUS_FOLDER):
                if f.endswith('.txt'):
                    os.remove(os.path.join(CORPUS_FOLDER, f))
            print(f"   ✅ Corpus folder cleared!")
    else:
        print("   ❌ Cancelled.")


def interactive_mode():
    """Run interactive menu."""
    while True:
        print_menu()
        choice = input("   Enter choice (1-6): ").strip()
        
        if choice == '1':
            quick_download()
        elif choice == '2':
            custom_download()
        elif choice == '3':
            show_stats()
        elif choice == '4':
            export_corpus()
        elif choice == '5':
            clear_corpus()
        elif choice == '6':
            print("\n   👋 Goodbye!\n")
            break
        else:
            print("   ⚠️  Invalid choice.")


# ============================================================================
# Main
# ============================================================================

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == '--stats':
            show_stats()
        elif sys.argv[1] == '--export':
            export_corpus()
        elif sys.argv[1] == '--download':
            topic = sys.argv[2] if len(sys.argv) > 2 else "machine learning"
            count = int(sys.argv[3]) if len(sys.argv) > 3 else 25
            builder = CorpusBuilder()
            builder.download_topic(topic, count_per_source=count)
            builder.export_to_files()
            builder.close()
        elif sys.argv[1] == '--quick':
            quick_download()
        else:
            print(__doc__)
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
