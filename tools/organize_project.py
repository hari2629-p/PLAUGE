"""
Organize the PLAUGE project into proper folder structure.
Moves files to appropriate directories based on their function.
"""

import os
import shutil
import re

# Project root
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Folder structure
FOLDERS = {
    'backend': {
        'core': 'Core ML/plagiarism detection algorithms',
        'api': 'REST API endpoints',
        'database': 'Database management',
        'utils': 'Utility functions',
    },
    'corpus': {
        'machine_learning': 'ML papers',
        'deep_learning': 'Deep learning/neural network papers',
        'nlp': 'Natural language processing papers',
        'plagiarism_detection': 'Plagiarism detection papers',
        'text_similarity': 'Text similarity papers',
        'information_retrieval': 'Information retrieval papers',
        'ai_general': 'General AI papers',
        'computer_vision': 'Computer vision papers',
        'transformers': 'Transformer model papers',
        'reinforcement_learning': 'Reinforcement learning papers',
        'data_science': 'Data science papers',
        'computational_linguistics': 'Computational linguistics papers',
        'other': 'Other/uncategorized papers',
    },
    'frontend': 'Web interface files',
    'config': 'Configuration files',
    'scripts': 'Utility scripts',
    'docs': 'Documentation',
    'submit': 'Papers to check for plagiarism',
    'documents': 'User documents',
}

# File categorization rules for corpus
CORPUS_CATEGORIES = {
    'machine_learning': [
        'machine_learn', 'ml_', 'supervised', 'unsupervised', 'sklearn',
        'scikit', 'classification', 'regression', 'clustering'
    ],
    'deep_learning': [
        'deep_learn', 'neural_net', 'cnn', 'rnn', 'lstm', 'deep_neural',
        'convolutional', 'recurrent', 'autoencoder'
    ],
    'nlp': [
        'natural_language', 'nlp', 'language_process', 'text_process',
        'sentiment', 'named_entity', 'pos_tag', 'parsing', 'speech'
    ],
    'plagiarism_detection': [
        'plagiarism', 'plagiaris', 'copy_detect', 'academic_integrity',
        'duplicate_detect', 'source_code_plagia'
    ],
    'text_similarity': [
        'text_similar', 'similarity', 'cosine', 'jaccard', 'levenshtein',
        'edit_distance', 'string_match', 'document_similar'
    ],
    'information_retrieval': [
        'information_retrieval', 'retriev', 'search_engine', 'indexing',
        'query', 'ranking', 'bm25', 'tfidf'
    ],
    'ai_general': [
        'artificial_intellig', 'ai_', '_ai_', 'intelligent', 'reasoning',
        'knowledge', 'expert_system', 'multiagent'
    ],
    'computer_vision': [
        'computer_vision', 'image', 'visual', 'object_detect', 'segmentation',
        'recognition', 'yolo', 'detection'
    ],
    'transformers': [
        'transformer', 'bert', 'gpt', 'attention', 'llm', 'language_model',
        'pre-train', 'pretrain', 'large_language'
    ],
    'reinforcement_learning': [
        'reinforcement', 'q-learning', 'policy', 'reward', 'agent',
        'environment', 'markov', 'rlhf'
    ],
    'data_science': [
        'data_science', 'data_mining', 'analytics', 'visualization',
        'statistics', 'exploratory'
    ],
    'computational_linguistics': [
        'linguistic', 'computational_ling', 'syntax', 'semantics',
        'morpholog', 'phonolog', 'pragmatics'
    ],
}


def categorize_paper(filename):
    """Determine the category of a paper based on its filename."""
    filename_lower = filename.lower()
    
    for category, keywords in CORPUS_CATEGORIES.items():
        for keyword in keywords:
            if keyword in filename_lower:
                return category
    
    return 'other'


def organize_corpus():
    """Organize corpus files into category subfolders."""
    corpus_dir = os.path.join(ROOT, 'corpus')
    
    if not os.path.exists(corpus_dir):
        print("❌ Corpus directory not found!")
        return
    
    # Create category folders
    for category in CORPUS_CATEGORIES.keys():
        cat_path = os.path.join(corpus_dir, category)
        os.makedirs(cat_path, exist_ok=True)
    os.makedirs(os.path.join(corpus_dir, 'other'), exist_ok=True)
    
    # Get all txt files in corpus root
    files = [f for f in os.listdir(corpus_dir) 
             if f.endswith('.txt') and os.path.isfile(os.path.join(corpus_dir, f))]
    
    moved_count = {cat: 0 for cat in list(CORPUS_CATEGORIES.keys()) + ['other']}
    
    print(f"\n📁 Organizing {len(files)} corpus files...\n")
    
    for filename in files:
        category = categorize_paper(filename)
        src = os.path.join(corpus_dir, filename)
        dst = os.path.join(corpus_dir, category, filename)
        
        try:
            shutil.move(src, dst)
            moved_count[category] += 1
        except Exception as e:
            print(f"   ⚠️  Error moving {filename}: {e}")
    
    # Print summary
    print("=" * 60)
    print("📊 CORPUS ORGANIZATION SUMMARY")
    print("=" * 60)
    
    for category, count in sorted(moved_count.items(), key=lambda x: -x[1]):
        if count > 0:
            bar = "█" * min(count // 5, 30)
            print(f"   {category:25} {count:4} papers {bar}")
    
    print("=" * 60)
    print(f"   Total: {sum(moved_count.values())} papers organized\n")


def organize_backend():
    """Move backend/ML files to appropriate locations."""
    moves = [
        # Core ML files
        ('plagiarism_detector.py', 'backend/core/plagiarism_detector.py'),
        ('check_against_corpus.py', 'backend/core/check_against_corpus.py'),
        ('check_my_documents.py', 'backend/core/check_my_documents.py'),
        
        # Database files
        ('corpus_builder.py', 'backend/database/corpus_builder.py'),
        ('corpus_database.db', 'backend/database/corpus_database.db'),
        
        # Scripts
        ('download_corpus.py', 'scripts/download_corpus.py'),
        
        # Docs
        ('DOCUMENTATION.txt', 'docs/DOCUMENTATION.txt'),
    ]
    
    print("\n📦 Organizing backend files...\n")
    
    for src_name, dst_path in moves:
        src = os.path.join(ROOT, src_name)
        dst = os.path.join(ROOT, dst_path)
        
        if os.path.exists(src):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            try:
                shutil.move(src, dst)
                print(f"   ✓ {src_name} → {dst_path}")
            except Exception as e:
                print(f"   ⚠️  Error moving {src_name}: {e}")
        else:
            print(f"   ⚠️  Not found: {src_name}")


def create_init_files():
    """Create __init__.py files for Python packages."""
    packages = [
        'backend',
        'backend/core',
        'backend/api',
        'backend/database',
        'backend/utils',
        'scripts',
    ]
    
    for pkg in packages:
        init_path = os.path.join(ROOT, pkg, '__init__.py')
        os.makedirs(os.path.dirname(init_path), exist_ok=True)
        if not os.path.exists(init_path):
            with open(init_path, 'w') as f:
                f.write(f'"""{pkg.split("/")[-1]} package"""\n')
            print(f"   ✓ Created {pkg}/__init__.py")


def create_main_runner():
    """Create main.py entry point."""
    main_content = '''"""
PLAUGE - Plagiarism Detection System
Main entry point for running the application.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.core.plagiarism_detector import PlagiarismDetector, download_nltk_resources


def main():
    """Main entry point."""
    print("=" * 60)
    print("   PLAUGE - Plagiarism Detection System")
    print("=" * 60)
    print("""
    Commands:
        python main.py check       - Check documents for plagiarism
        python main.py corpus      - Manage corpus database
        python main.py demo        - Run demo with sample documents
    """)
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        
        if cmd == 'check':
            from backend.core.check_against_corpus import main as check_main
            check_main()
        elif cmd == 'corpus':
            from backend.database.corpus_builder import main as corpus_main
            corpus_main()
        elif cmd == 'demo':
            from backend.core.plagiarism_detector import main as demo_main
            demo_main()
        else:
            print(f"Unknown command: {cmd}")
    else:
        print("Run with a command to get started!")


if __name__ == "__main__":
    main()
'''
    
    main_path = os.path.join(ROOT, 'main.py')
    with open(main_path, 'w') as f:
        f.write(main_content)
    print(f"   ✓ Created main.py")


def update_imports():
    """Update import statements in moved files."""
    # Files to update with their new paths
    files_to_update = [
        ('backend/core/check_against_corpus.py', [
            ('from plagiarism_detector import', 'from backend.core.plagiarism_detector import'),
        ]),
        ('backend/core/check_my_documents.py', [
            ('from plagiarism_detector import', 'from backend.core.plagiarism_detector import'),
        ]),
    ]
    
    print("\n🔧 Updating import statements...\n")
    
    for filepath, replacements in files_to_update:
        full_path = os.path.join(ROOT, filepath)
        if os.path.exists(full_path):
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            for old, new in replacements:
                content = content.replace(old, new)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"   ✓ Updated imports in {filepath}")


def create_config():
    """Create configuration file."""
    config_content = '''"""
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
'''
    
    config_path = os.path.join(ROOT, 'config', 'settings.py')
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, 'w') as f:
        f.write(config_content)
    print(f"   ✓ Created config/settings.py")
    
    # Create __init__.py
    init_path = os.path.join(ROOT, 'config', '__init__.py')
    with open(init_path, 'w') as f:
        f.write('from .settings import *\n')


def main():
    """Run all organization tasks."""
    print("\n" + "=" * 60)
    print("   🗂️  PLAUGE PROJECT ORGANIZER")
    print("=" * 60)
    
    # Step 1: Organize corpus into categories
    organize_corpus()
    
    # Step 2: Move backend files
    organize_backend()
    
    # Step 3: Create init files
    print("\n📝 Creating package files...\n")
    create_init_files()
    
    # Step 4: Create main entry point
    create_main_runner()
    
    # Step 5: Create config
    create_config()
    
    # Step 6: Update imports
    update_imports()
    
    print("\n" + "=" * 60)
    print("   ✅ PROJECT ORGANIZATION COMPLETE!")
    print("=" * 60)
    print("""
    New Structure:
    ├── main.py                 # Entry point
    ├── backend/
    │   ├── core/               # ML algorithms
    │   ├── api/                # REST API
    │   ├── database/           # Corpus DB
    │   └── utils/              # Utilities
    ├── corpus/
    │   ├── machine_learning/
    │   ├── deep_learning/
    │   ├── nlp/
    │   ├── plagiarism_detection/
    │   ├── text_similarity/
    │   └── ... (categorized papers)
    ├── config/                 # Settings
    ├── scripts/                # Utility scripts
    ├── docs/                   # Documentation
    ├── submit/                 # Papers to check
    └── frontend/               # Web UI (future)
    """)


if __name__ == "__main__":
    main()
