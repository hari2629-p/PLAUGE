"""
PLAGIARISM CHECKER - Check submitted papers against a corpus of research papers.

Folder Structure:
    corpus/     - Put existing research papers here (your reference database)
    submit/     - Put the paper you want to check here

Usage:
    python check_against_corpus.py
"""

import os
from backend.ml_models.plagiarism_detector import PlagiarismDetector, download_nltk_resources


CORPUS_FOLDER = "corpus"
SUBMIT_FOLDER = "submit"


def setup_folders():
    for folder in [CORPUS_FOLDER, SUBMIT_FOLDER]:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"📁 Created folder: {folder}/")


def load_txt_files(folder_path):
    documents = []
    filenames = []
    
    txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    
    for filename in sorted(txt_files):
        filepath = os.path.join(folder_path, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                documents.append(content)
                filenames.append(filename)
        except Exception as e:
            print(f"   ⚠️  Error reading {filename}: {e}")
    
    return documents, filenames


def check_paper_against_corpus(submitted_doc, submitted_name, corpus_docs, corpus_names):
    all_docs = [submitted_doc] + corpus_docs
    
    detector = PlagiarismDetector()
    detector.add_documents(all_docs)
    results = detector.analyze()
    
    matches = []
    for result in results['pairwise_results']:
        if result['doc1_index'] == 0:
            corpus_idx = result['doc2_index'] - 1
            matches.append({
                'corpus_file': corpus_names[corpus_idx],
                'similarity_score': result['similarity_score'],
                'similarity_percentage': result['similarity_percentage'],
                'plagiarism_level': result['plagiarism_level']
            })
    
    matches.sort(key=lambda x: x['similarity_score'], reverse=True)
    return matches


def get_color(score):
    if score >= 0.8:
        return "\033[91m"  # Red
    elif score >= 0.5:
        return "\033[93m"  # Yellow
    else:
        return "\033[92m"  # Green


def print_results(submitted_name, matches):
    RESET = "\033[0m"
    BOLD = "\033[1m"
    
    print("\n" + "=" * 70)
    print(f"{BOLD}📄 PLAGIARISM CHECK RESULTS{RESET}")
    print(f"   Submitted Paper: {BOLD}{submitted_name}{RESET}")
    print("=" * 70)
    
    if not matches:
        print("\n   No corpus papers to compare against.\n")
        return
    
    highest = matches[0]
    max_score = highest['similarity_percentage']
    max_color = get_color(highest['similarity_score'])
    
    print(f"\n{BOLD}📊 OVERALL RESULT:{RESET}")
    print(f"   Highest Match: {max_color}{max_score}% with '{highest['corpus_file']}'{RESET}")
    
    if highest['similarity_score'] >= 0.8:
        print(f"   Status: {max_color}⚠️  HIGH PLAGIARISM DETECTED{RESET}")
    elif highest['similarity_score'] >= 0.5:
        print(f"   Status: {max_color}⚠️  MEDIUM SIMILARITY - Review Required{RESET}")
    else:
        print(f"   Status: {max_color}✅ LOW SIMILARITY - Likely Original{RESET}")
    
    print(f"\n{BOLD}📋 DETAILED MATCHES (sorted by similarity):{RESET}")
    print("-" * 70)
    
    for i, match in enumerate(matches, 1):
        color = get_color(match['similarity_score'])
        print(f"\n   {i}. {match['corpus_file']}")
        print(f"      Similarity: {color}{match['similarity_percentage']}%{RESET}")
        print(f"      Level: {color}{match['plagiarism_level']}{RESET}")
    
    print("\n" + "=" * 70)
    print(f"{BOLD}LEGEND:{RESET}")
    print(f"   \033[91m● High plagiarism (≥80%) - Likely copied\033[0m")
    print(f"   \033[93m● Medium plagiarism (50-79%) - Needs review\033[0m")
    print(f"   \033[92m● Low plagiarism (<50%) - Likely original\033[0m")
    print("=" * 70 + "\n")


def main():
    print("\n" + "=" * 70)
    print("     PLAGIARISM CHECKER - Check Against Research Paper Corpus")
    print("=" * 70)
    
    download_nltk_resources()
    setup_folders()
    
    print(f"\n📚 Loading corpus from './{CORPUS_FOLDER}/'...")
    corpus_docs, corpus_names = load_txt_files(CORPUS_FOLDER)
    
    if not corpus_docs:
        print(f"\n❌ No papers found in corpus!")
        print(f"   Add .txt files to the '{CORPUS_FOLDER}/' folder.")
        print("   These are the reference papers to check against.\n")
        return
    
    print(f"   ✅ Loaded {len(corpus_docs)} papers in corpus:")
    for name in corpus_names:
        print(f"      • {name}")
    
    print(f"\n📝 Loading submitted paper from './{SUBMIT_FOLDER}/'...")
    submit_docs, submit_names = load_txt_files(SUBMIT_FOLDER)
    
    if not submit_docs:
        print(f"\n❌ No paper found to check!")
        print(f"   Add your .txt file to the '{SUBMIT_FOLDER}/' folder.\n")
        return
    
    for i, (doc, name) in enumerate(zip(submit_docs, submit_names)):
        print(f"\n🔍 Checking: {name}...")
        matches = check_paper_against_corpus(doc, name, corpus_docs, corpus_names)
        print_results(name, matches)
    
    print("✅ All checks complete!\n")


if __name__ == "__main__":
    main()
