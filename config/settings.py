"""
PLAUGE Configuration
"""

import os

# Paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS_DIR = os.path.join(PROJECT_ROOT, 'corpus')
SUBMIT_DIR = os.path.join(PROJECT_ROOT, 'submit')
DATABASE_PATH = os.path.join(PROJECT_ROOT, 'backend', 'database', 'corpus_database.db')

# Plagiarism Detection Settings
PLAGIARISM_THRESHOLDS = {
    'high': 0.8,      # >= 80% = High plagiarism
    'medium': 0.5,    # >= 50% = Medium plagiarism
    'low': 0.0,       # < 50% = Low plagiarism
}

# TF-IDF Settings
TFIDF_MAX_FEATURES = 5000
TFIDF_NGRAM_RANGE = (1, 2)

# API Settings
API_HOST = '0.0.0.0'
API_PORT = 8000
API_DEBUG = True

# Corpus Builder Settings
RATE_LIMITS = {
    'arxiv': 3.0,
    'semantic_scholar': 1.0,
    'crossref': 1.0,
    'openalex': 0.1,
}
