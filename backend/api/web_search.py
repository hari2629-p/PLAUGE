"""
Web Search & AI Detection Module for PLAUGE
Features:
- Auto-keyword extraction from documents
- Multi-source search (arXiv, Semantic Scholar, Wikipedia)
- Basic AI content detection patterns
"""

import requests
import json
import time
import re
import wikipedia
from collections import Counter
from typing import List, Dict, Tuple
from rake_nltk import Rake


class KeywordExtractor:
    """Extract search keywords from text"""
    
    def __init__(self):
        self.rake = Rake()
        
    def extract(self, text: str, max_keywords: int = 3) -> str:
        """Extract top keywords to form a search query"""
        try:
            # Extract keywords from the first 2000 chars (intro usually contains key topics)
            self.rake.extract_keywords_from_text(text[:2000])
            phrases = self.rake.get_ranked_phrases()
            
            # Select top 2-3 distinct phrases
            query_phrases = []
            seen_words = set()
            
            for phrase in phrases:
                words = set(phrase.split())
                # Avoid overlapping phrases
                if not words.intersection(seen_words) and len(phrase) > 4:
                    query_phrases.append(phrase)
                    seen_words.update(words)
                
                if len(query_phrases) >= max_keywords:
                    break
            
            # Fallback if RAKE fails or returns empty
            if not query_phrases:
                return text[:100]  # Just return start of text
                
            return " ".join(query_phrases)
        except Exception as e:
            print(f"Keyword extraction error: {e}")
            return text.split()[:5]  # Fallback to first few words


class WikipediaSearcher:
    """Search Wikipedia"""
    
    @staticmethod
    def search(query: str, max_results: int = 3) -> List[Dict]:
        try:
            results = wikipedia.search(query, results=max_results)
            papers = []
            
            for title in results:
                try:
                    page = wikipedia.page(title, auto_suggest=False)
                    papers.append({
                        'title': page.title,
                        'authors': 'Wikipedia Contributors',
                        'abstract': page.summary[:500] + "...",
                        'published': 'N/A',
                        'source': 'Wikipedia',
                        'id': page.pageid,
                        'url': page.url
                    })
                except (wikipedia.DisambiguationError, wikipedia.PageError):
                    continue
                    
            return papers
        except Exception as e:
            print(f"Wikipedia search error: {e}")
            return []


class ArxivSearcher:
    BASE_URL = "http://export.arxiv.org/api/query"
    
    @staticmethod
    def search(query: str, max_results: int = 5) -> List[Dict]:
        params = {
            'search_query': f'all:{query}',
            'start': 0,
            'max_results': max_results,
            'sortBy': 'relevance',
            'sortOrder': 'descending'
        }
        try:
            response = requests.get(ArxivSearcher.BASE_URL, params=params, timeout=10)
            if response.status_code != 200: return []
            
            import xml.etree.ElementTree as ET
            root = ET.fromstring(response.content)
            papers = []
            namespace = {'atom': 'http://www.w3.org/2005/Atom'}
            
            for entry in root.findall('atom:entry', namespace):
                title = entry.find('atom:title', namespace).text.strip()
                summary = entry.find('atom:summary', namespace).text.strip()
                published = entry.find('atom:published', namespace).text[:10]
                authors = [a.find('atom:name', namespace).text for a in entry.findall('atom:author', namespace)]
                arxiv_id = entry.find('atom:id', namespace).text.split('/')[-1]
                
                papers.append({
                    'title': title,
                    'authors': ', '.join(authors[:3]),
                    'abstract': summary,
                    'published': published,
                    'source': 'arXiv',
                    'id': arxiv_id,
                    'url': f'https://arxiv.org/abs/{arxiv_id}'
                })
            return papers
        except Exception as e:
            print(f"arXiv search error: {e}")
            return []


class SemanticScholarSearcher:
    BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
    
    @staticmethod
    def search(query: str, max_results: int = 5) -> List[Dict]:
        params = {'query': query, 'limit': max_results, 'fields': 'title,authors,abstract,year,url'}
        try:
            response = requests.get(SemanticScholarSearcher.BASE_URL, params=params, timeout=10)
            if response.status_code != 200: return []
            
            data = response.json()
            papers = []
            for paper in data.get('data', []):
                if not paper.get('abstract'): continue
                authors = [a.get('name', '') for a in paper.get('authors', [])]
                papers.append({
                    'title': paper.get('title', 'Unknown'),
                    'authors': ', '.join(authors[:3]),
                    'abstract': paper.get('abstract', ''),
                    'published': str(paper.get('year', 'N/A')),
                    'source': 'Semantic Scholar',
                    'id': paper.get('paperId', ''),
                    'url': paper.get('url', '')
                })
            return papers
        except Exception as e:
            print(f"Semantic Scholar error: {e}")
            return []


class AIContentScanner:
    """
    Basic heuristic-based AI content detection.
    Real AI detection requires large transformers (like RoBERTa), 
    but we can check for common statistical patterns:
    - Low perplexity (simulated by repetitive structure)
    - Very uniform sentence lengths
    - Lack of 'burstiness' (variation in vocabulary)
    """
    
    @staticmethod
    def analyze(text: str) -> Dict:
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        
        if not sentences:
            return {'score': 0, 'confidence': 'Low', 'reason': 'Text too short'}
            
        # Feature 1: Sentence Length Variance (AI tends to be more uniform)
        lengths = [len(s.split()) for s in sentences]
        avg_len = sum(lengths) / len(lengths)
        variance = sum((l - avg_len) ** 2 for l in lengths) / len(lengths)
        std_dev = variance ** 0.5
        
        # Feature 2: Vocabulary Richness (Type-Token Ratio)
        words = text.lower().split()
        unique_words = set(words)
        ttr = len(unique_words) / len(words) if words else 0
        
        # Heuristic scoring (Simplified)
        ai_score = 0
        
        # Low variance in sentence length -> Possible AI
        if std_dev < 5: ai_score += 30
        elif std_dev < 8: ai_score += 15
        
        # "Perfect" grammar structure often leads to mid-range TTR
        if 0.4 < ttr < 0.6: ai_score += 20
        
        # Check for common AI phrases (very basic)
        ai_phrases = ["it is important to note", "in conclusion", "furthermore", "moreover", "as an ai language model"]
        count_phrases = sum(1 for p in ai_phrases if p in text.lower())
        ai_score += min(count_phrases * 10, 30)
        
        # Cap at 95%
        ai_score = min(ai_score + 10, 95) # Base probability
        
        level = "High" if ai_score > 70 else "Medium" if ai_score > 40 else "Low"
        
        return {
            'score': int(ai_score),
            'level': level,
            'details': {
                'avg_sentence_len': round(avg_len, 1),
                'vocabulary_richness': round(ttr, 2),
                'std_dev': round(std_dev, 1)
            }
        }


class OpenAlexSearcher:
    BASE_URL = "https://api.openalex.org/works"
    
    @staticmethod
    def search(query: str, max_results: int = 5) -> List[Dict]:
        params = {
            'search': query,
            'per-page': max_results,
            'select': 'title,authorships,abstract_inverted_index,publication_year,id,doi'
        }
        try:
            response = requests.get(OpenAlexSearcher.BASE_URL, params=params, timeout=10)
            if response.status_code != 200: return []
            
            data = response.json()
            papers = []
            
            for work in data.get('results', []):
                # Reconstruct abstract from inverted index (simplified)
                abstract = "Abstract available in full text."
                if work.get('abstract_inverted_index'):
                    # Skip reconstructing full abstract for speed, just use title/meta
                    # Real reconstruction is complex
                    pass
                
                authors = [a.get('author', {}).get('display_name', '') for a in work.get('authorships', [])]
                
                papers.append({
                    'title': work.get('title', 'Unknown'),
                    'authors': ', '.join(authors[:3]),
                    'abstract': work.get('title', '') + " - " + ', '.join(authors), # Fallback text
                    'published': str(work.get('publication_year', 'N/A')),
                    'source': 'OpenAlex',
                    'id': work.get('id', ''),
                    'url': work.get('doi') or f"https://openalex.org/{work.get('id', '')}"
                })
            return papers
        except Exception as e:
            print(f"OpenAlex search error: {e}")
            return []


class WebSearchManager:
    """Unified Search Manager"""
    
    def __init__(self):
        self.extractor = KeywordExtractor()
    
    def generate_query(self, text: str) -> str:
        return self.extractor.extract(text)
    
    def search_all(self, query: str = None, text_content: str = None, max_per_source: int = 3) -> List[Dict]:
        """
        Search using query OR extract query from text
        """
        if not query and text_content:
            print("🤖 Auto-generating search keywords from document...")
            query = self.extractor.extract(text_content)
            print(f"🔑 Generated Query: '{query}'")
            
        if not query:
            return []
            
        all_papers = []
        
        # 1. Wikipedia (General)
        print(f"🔍 Searching Wikipedia...")
        all_papers.extend(WikipediaSearcher.search(query, max_results=2))
        
        # 2. arXiv (Preprints)
        print(f"🔍 Searching arXiv...")
        all_papers.extend(ArxivSearcher.search(query, max_results=max_per_source))
        
        # 3. Semantic Scholar (Academic)
        print(f"🔍 Searching Semantic Scholar...")
        all_papers.extend(SemanticScholarSearcher.search(query, max_results=max_per_source))
        
        # 4. OpenAlex (Global Research)
        print(f"🔍 Searching OpenAlex...")
        all_papers.extend(OpenAlexSearcher.search(query, max_results=max_per_source))
        
        return all_papers

    @staticmethod
    def prepare_for_analysis(papers: List[Dict]) -> tuple:
        documents = []
        metadata = []
        for paper in papers:
            abstract = paper.get('abstract', '')
            if abstract and len(abstract.strip()) > 50:
                documents.append(abstract)
                metadata.append({
                    'title': paper['title'],
                    'authors': paper['authors'],
                    'source': paper['source'],
                    'url': paper.get('url', ''),
                    'published': paper.get('published', '')
                })
        return documents, metadata
