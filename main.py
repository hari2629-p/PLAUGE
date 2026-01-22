"""
PLAUGE - Plagiarism Detection System
Main entry point for running the application.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.ml_models.plagiarism_detector import PlagiarismDetector, download_nltk_resources


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
            from backend.ml_models.check_against_corpus import main as check_main
            check_main()
        elif cmd == 'corpus':
            from backend.database.corpus_builder import main as corpus_main
            corpus_main()
        elif cmd == 'demo':
            from backend.ml_models.plagiarism_detector import main as demo_main
            demo_main()
        else:
            print(f"Unknown command: {cmd}")
    else:
        print("Run with a command to get started!")


if __name__ == "__main__":
    main()
