"""
Download research papers from arXiv to build your corpus.
Uses the arXiv API to fetch paper abstracts.

Usage:
    python download_corpus.py                    # Download default topics
    python download_corpus.py "machine learning" # Download specific topic
    python download_corpus.py "deep learning" 20 # Download 20 papers on topic
"""

import urllib.request
import xml.etree.ElementTree as ET
import os
import time
import sys


CORPUS_FOLDER = "corpus"


def search_arxiv(query, max_results=10):
    base_url = "http://export.arxiv.org/api/query?"
    query_encoded = query.replace(" ", "+")
    search_query = f"search_query=all:{query_encoded}&start=0&max_results={max_results}"
    url = base_url + search_query
    
    print(f"🔍 Searching arXiv for: '{query}'...")
    
    try:
        response = urllib.request.urlopen(url, timeout=30)
        data = response.read().decode('utf-8')
        return data
    except Exception as e:
        print(f"❌ Error fetching from arXiv: {e}")
        return None


def parse_arxiv_response(xml_data):
    papers = []
    
    root = ET.fromstring(xml_data)
    namespace = {'atom': 'http://www.w3.org/2005/Atom'}
    
    for entry in root.findall('atom:entry', namespace):
        title = entry.find('atom:title', namespace)
        summary = entry.find('atom:summary', namespace)
        
        if title is not None and summary is not None:
            papers.append({
                'title': ' '.join(title.text.split()),
                'abstract': ' '.join(summary.text.split())
            })
    
    return papers


def save_papers_to_corpus(papers, prefix="arxiv"):
    if not os.path.exists(CORPUS_FOLDER):
        os.makedirs(CORPUS_FOLDER)
    
    existing = len([f for f in os.listdir(CORPUS_FOLDER) if f.endswith('.txt')])
    
    saved = 0
    for i, paper in enumerate(papers, existing + 1):
        safe_prefix = "".join(c if c.isalnum() or c == '_' else '_' for c in prefix)[:15]
        filename = f"{safe_prefix}_{i:03d}.txt"
        filepath = os.path.join(CORPUS_FOLDER, filename)
        
        content = f"Title: {paper['title']}\n\nAbstract:\n{paper['abstract']}"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        saved += 1
        print(f"   ✓ Saved: {filename}")
    
    return saved


def main():
    print("\n" + "=" * 70)
    print("           arXiv CORPUS DOWNLOADER")
    print("=" * 70)
    
    if len(sys.argv) > 1:
        topic = sys.argv[1]
        count = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        topics = [(topic, count)]
    else:
        topics = [
            ("machine learning", 5),
            ("natural language processing", 5),
            ("plagiarism detection", 5),
            ("text similarity", 5),
            ("deep learning", 5)
        ]
    
    total_saved = 0
    
    for topic, count in topics:
        print(f"\n📥 Downloading {count} papers on '{topic}'...")
        
        xml_data = search_arxiv(topic, count)
        
        if xml_data:
            papers = parse_arxiv_response(xml_data)
            if papers:
                prefix = topic.replace(" ", "_")
                saved = save_papers_to_corpus(papers, prefix)
                total_saved += saved
                print(f"   ✅ Downloaded {saved} papers")
            else:
                print(f"   ⚠️  No papers found")
        
        time.sleep(1)
    
    print("\n" + "=" * 70)
    print(f"✅ Download complete! {total_saved} papers saved to '{CORPUS_FOLDER}/'")
    print("=" * 70)
    print("\n📋 Next steps:")
    print("   1. Add your paper to 'submit/' folder")
    print("   2. Run: python check_against_corpus.py")
    print("")


if __name__ == "__main__":
    main()
