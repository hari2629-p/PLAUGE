"""
Check your own documents for plagiarism.
Place your .txt files in the 'documents' folder and run this script.
"""

import os
from backend.ml_models.plagiarism_detector import PlagiarismDetector, download_nltk_resources


def load_documents_from_folder(folder_path):
    documents = []
    filenames = []
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"📁 Created folder: {folder_path}")
        print("   Please add your .txt files there and run again.")
        return [], []
    
    txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    
    if not txt_files:
        print(f"⚠️  No .txt files found in '{folder_path}'")
        print("   Please add your text files and run again.")
        return [], []
    
    for filename in sorted(txt_files):
        filepath = os.path.join(folder_path, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            documents.append(content)
            filenames.append(filename)
            print(f"   ✓ Loaded: {filename}")
    
    return documents, filenames


def print_results_with_filenames(results, filenames):
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    GREEN = "\033[92m"
    
    print("\n" + "=" * 70)
    print(f"{BOLD}📄 PLAGIARISM DETECTION RESULTS{RESET}")
    print("=" * 70)
    
    for result in results['pairwise_results']:
        file1 = filenames[result['doc1_index']]
        file2 = filenames[result['doc2_index']]
        percentage = result['similarity_percentage']
        level = result['plagiarism_level']
        
        if result['similarity_score'] >= 0.8:
            color = RED
        elif result['similarity_score'] >= 0.5:
            color = YELLOW
        else:
            color = GREEN
        
        print(f"\n{BOLD}{file1} vs {file2}{RESET}")
        print("-" * 50)
        print(f"  Similarity Score: {color}{percentage}%{RESET}")
        print(f"  Plagiarism Level: {color}{level}{RESET}")
    
    print("\n" + "=" * 70)
    print(f"{BOLD}LEGEND:{RESET}")
    print(f"  {RED}● High plagiarism (≥80%){RESET}")
    print(f"  {YELLOW}● Medium plagiarism (50-79%){RESET}")
    print(f"  {GREEN}● Low plagiarism (<50%){RESET}")
    print("=" * 70 + "\n")


def main():
    print("\n" + "=" * 70)
    print("        PLAGIARISM CHECKER - Check Your Own Documents")
    print("=" * 70)
    
    download_nltk_resources()
    
    documents_folder = "documents"
    
    print(f"\n📂 Loading documents from './{documents_folder}/' folder...")
    documents, filenames = load_documents_from_folder(documents_folder)
    
    if len(documents) < 2:
        print("\n❌ Need at least 2 documents to compare.")
        print(f"   Add .txt files to the '{documents_folder}' folder.\n")
        return
    
    print(f"\n✅ Loaded {len(documents)} documents")
    
    print("\n🔍 Analyzing for plagiarism...\n")
    detector = PlagiarismDetector()
    detector.add_documents(documents)
    results = detector.analyze()
    
    print_results_with_filenames(results, filenames)
    
    print("✅ Analysis complete!\n")


if __name__ == "__main__":
    main()
