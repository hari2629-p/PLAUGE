import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def download_nltk_resources():
    resources = ['punkt', 'stopwords', 'wordnet', 'punkt_tab']
    for resource in resources:
        try:
            nltk.download(resource, quiet=True)
        except:
            pass


class TextPreprocessor:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
    
    def to_lowercase(self, text):
        return text.lower()
    
    def remove_punctuation(self, text):
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def tokenize(self, text):
        return word_tokenize(text)
    
    def remove_stopwords(self, tokens):
        return [token for token in tokens if token not in self.stop_words]
    
    def lemmatize(self, tokens):
        return [self.lemmatizer.lemmatize(token) for token in tokens]
    
    def preprocess(self, text):
        text = self.to_lowercase(text)
        text = self.remove_punctuation(text)
        tokens = self.tokenize(text)
        tokens = self.remove_stopwords(tokens)
        tokens = self.lemmatize(tokens)
        return ' '.join(tokens)


class TfidfFeatureExtractor:
    def __init__(self, max_features=5000, ngram_range=(1, 2)):
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=ngram_range,
            lowercase=False,
            token_pattern=r'\b\w+\b'
        )
        self.tfidf_matrix = None
    
    def fit_transform(self, documents):
        self.tfidf_matrix = self.vectorizer.fit_transform(documents)
        return self.tfidf_matrix
    
    def get_feature_names(self):
        return self.vectorizer.get_feature_names_out().tolist()


class SimilarityCalculator:
    @staticmethod
    def compute_cosine_similarity(tfidf_matrix):
        return cosine_similarity(tfidf_matrix)
    
    @staticmethod
    def similarity_to_percentage(similarity):
        return round(similarity * 100, 2)


class PlagiarismDecision:
    HIGH_THRESHOLD = 0.8
    MEDIUM_THRESHOLD = 0.5
    
    @classmethod
    def get_plagiarism_level(cls, similarity):
        if similarity >= cls.HIGH_THRESHOLD:
            return "High plagiarism"
        elif similarity >= cls.MEDIUM_THRESHOLD:
            return "Medium plagiarism"
        else:
            return "Low plagiarism"
    
    @classmethod
    def get_color_code(cls, similarity):
        if similarity >= cls.HIGH_THRESHOLD:
            return "\033[91m"
        elif similarity >= cls.MEDIUM_THRESHOLD:
            return "\033[93m"
        else:
            return "\033[92m"


class PlagiarismDetector:
    def __init__(self, max_features=5000):
        self.preprocessor = TextPreprocessor()
        self.feature_extractor = TfidfFeatureExtractor(max_features=max_features)
        self.similarity_calculator = SimilarityCalculator()
        self.documents = []
        self.preprocessed_docs = []
        self.similarity_matrix = None
    
    def add_documents(self, documents):
        self.documents = documents
        self.preprocessed_docs = [
            self.preprocessor.preprocess(doc) for doc in documents
        ]
    
    def analyze(self):
        if len(self.preprocessed_docs) < 2:
            raise ValueError("At least 2 documents are required for comparison")
        
        tfidf_matrix = self.feature_extractor.fit_transform(self.preprocessed_docs)
        self.similarity_matrix = self.similarity_calculator.compute_cosine_similarity(tfidf_matrix)
        
        pairwise_results = []
        n_docs = len(self.documents)
        
        for i in range(n_docs):
            for j in range(i + 1, n_docs):
                similarity = self.similarity_matrix[i, j]
                percentage = self.similarity_calculator.similarity_to_percentage(similarity)
                level = PlagiarismDecision.get_plagiarism_level(similarity)
                
                pairwise_results.append({
                    'doc1_index': i,
                    'doc2_index': j,
                    'similarity_score': similarity,
                    'similarity_percentage': percentage,
                    'plagiarism_level': level
                })
        
        return {
            'similarity_matrix': self.similarity_matrix,
            'pairwise_results': pairwise_results
        }
    
    def print_results(self, results):
        RESET = "\033[0m"
        BOLD = "\033[1m"
        
        print("\n" + "=" * 70)
        print(f"{BOLD}📄 PLAGIARISM DETECTION RESULTS{RESET}")
        print("=" * 70)
        
        for result in results['pairwise_results']:
            doc1 = result['doc1_index'] + 1
            doc2 = result['doc2_index'] + 1
            percentage = result['similarity_percentage']
            level = result['plagiarism_level']
            color = PlagiarismDecision.get_color_code(result['similarity_score'])
            
            print(f"\n{BOLD}Document {doc1} vs Document {doc2}{RESET}")
            print("-" * 40)
            print(f"  Similarity Score: {color}{percentage}%{RESET}")
            print(f"  Plagiarism Level: {color}{level}{RESET}")
        
        print("\n" + "=" * 70)
        print(f"{BOLD}LEGEND:{RESET}")
        print(f"  \033[91m● High plagiarism (≥80%)\033[0m")
        print(f"  \033[93m● Medium plagiarism (50-79%)\033[0m")
        print(f"  \033[92m● Low plagiarism (<50%)\033[0m")
        print("=" * 70 + "\n")


def main():
    print("📥 Downloading NLTK resources...")
    download_nltk_resources()
    
    sample_documents = [
        """
        Machine learning is a subset of artificial intelligence that enables 
        systems to learn and improve from experience without being explicitly 
        programmed. It focuses on developing computer programs that can access 
        data and use it to learn for themselves.
        """,
        """
        Machine learning is a branch of artificial intelligence which allows 
        systems to learn and improve from experience without being explicitly 
        programmed. It concentrates on developing computer programs that can 
        access data and use it to learn for themselves.
        """,
        """
        Deep learning is a specialized form of machine learning that uses 
        neural networks with multiple layers. These networks can automatically 
        learn representations from data without manual feature engineering.
        """,
        """
        The weather today is sunny and warm. I went to the park to enjoy the 
        beautiful day. Children were playing on the swings while dogs ran 
        around freely.
        """
    ]
    
    print("\n🔧 Initializing Plagiarism Detector...")
    detector = PlagiarismDetector(max_features=5000)
    
    print(f"📄 Loading {len(sample_documents)} documents...")
    detector.add_documents(sample_documents)
    
    print("\n📝 Document Previews:")
    print("-" * 50)
    for i, doc in enumerate(sample_documents, 1):
        preview = ' '.join(doc.split()[:15]) + "..."
        print(f"  Doc {i}: {preview}")
    
    print("\n🔍 Analyzing documents for plagiarism...")
    results = detector.analyze()
    
    detector.print_results(results)
    
    print("\n📊 SIMILARITY MATRIX (as percentages):")
    print("-" * 50)
    sim_matrix = results['similarity_matrix']
    n = len(sample_documents)
    
    header = "      " + "   ".join([f"Doc{i+1}" for i in range(n)])
    print(header)
    
    for i in range(n):
        row = f"Doc{i+1}  "
        for j in range(n):
            percentage = sim_matrix[i, j] * 100
            row += f"{percentage:5.1f}  "
        print(row)
    
    print("\n✅ Analysis complete!")


if __name__ == "__main__":
    main()
