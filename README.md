# 🔍 PLAUGE - Plagiarism Detection System

A comprehensive plagiarism detection system using TF-IDF and cosine similarity, with a large corpus of academic papers from multiple sources.

## 📁 Project Structure

```
PLAUGE/
├── main.py                         # 🚀 Main entry point
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── backend/                        # 🧠 Backend ML Models & Logic
│   ├── __init__.py
│   ├── core/                       # Core ML algorithms
│   │   ├── plagiarism_detector.py  # Main plagiarism detection engine
│   │   ├── check_against_corpus.py # Check papers against corpus
│   │   └── check_my_documents.py   # Check user documents
│   ├── api/                        # REST API endpoints (future)
│   │   └── __init__.py
│   ├── database/                   # Database management
│   │   ├── corpus_builder.py       # Multi-source corpus downloader
│   │   └── corpus_database.db      # SQLite database (575+ papers)
│   └── utils/                      # Utility functions
│       └── __init__.py
│
├── corpus/                         # 📚 Academic Papers Corpus (603 papers)
│   ├── machine_learning/           # 65 papers
│   ├── deep_learning/              # 43 papers
│   ├── nlp/                        # 29 papers
│   ├── plagiarism_detection/       # 34 papers (directly relevant!)
│   ├── text_similarity/            # 41 papers
│   ├── information_retrieval/      # 20 papers
│   ├── ai_general/                 # 25 papers
│   ├── computer_vision/            # 28 papers
│   ├── transformers/               # 39 papers
│   ├── reinforcement_learning/     # 22 papers
│   ├── data_science/               # 10 papers
│   ├── computational_linguistics/  # 14 papers
│   └── other/                      # 233 papers
│
├── config/                         # ⚙️ Configuration
│   ├── __init__.py
│   └── settings.py                 # App settings & thresholds
│
├── scripts/                        # 🔧 Utility Scripts
│   ├── download_corpus.py          # Download from arXiv
│   └── organize_project.py         # Project organization tool
│
├── docs/                           # 📄 Documentation
│   └── DOCUMENTATION.txt           # Detailed documentation
│
├── submit/                         # 📝 Papers to Check
│   └── (place your papers here)
│
├── documents/                      # 📂 User Documents
│
└── frontend/                       # 🌐 Web Interface (future)
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Commands

```bash
# Show help
python main.py

# Check a paper for plagiarism
python main.py check

# Manage corpus (download more papers)
python main.py corpus

# Run demo with sample documents
python main.py demo
```

## 📊 Corpus Statistics

| Category | Papers | Description |
|----------|--------|-------------|
| **Machine Learning** | 65 | ML algorithms, sklearn, classification |
| **Deep Learning** | 43 | Neural networks, CNNs, RNNs |
| **NLP** | 29 | Natural language processing |
| **Plagiarism Detection** | 34 | Directly relevant research! |
| **Text Similarity** | 41 | Cosine, Jaccard, semantic similarity |
| **Transformers** | 39 | BERT, GPT, attention mechanisms |
| **Information Retrieval** | 20 | Search, ranking, indexing |
| **Computer Vision** | 28 | Image processing, object detection |
| **AI General** | 25 | General artificial intelligence |
| **Reinforcement Learning** | 22 | Q-learning, policy gradients |
| **Data Science** | 10 | Analytics, visualization |
| **Computational Linguistics** | 14 | Syntax, semantics, morphology |
| **Other** | 233 | Miscellaneous academic papers |
| **Total** | **603** | |

### Data Sources
- 📚 **arXiv** - Open-access preprints
- 📖 **Semantic Scholar** - AI-curated database
- 🔗 **CrossRef** - Published research with DOIs
- 🌐 **OpenAlex** - Open academic catalog

## 🧠 How It Works

### 1. Text Preprocessing
- Lowercase conversion
- Punctuation removal
- Tokenization
- Stopword removal
- Lemmatization

### 2. Feature Extraction
- TF-IDF vectorization
- N-gram support (unigrams + bigrams)
- Max 5000 features

### 3. Similarity Calculation
- Cosine similarity between document vectors
- Generates similarity matrix

### 4. Plagiarism Classification
| Similarity | Level | Color |
|------------|-------|-------|
| ≥ 80% | 🔴 High Plagiarism | Red |
| 50-79% | 🟡 Medium Plagiarism | Yellow |
| < 50% | 🟢 Low Plagiarism | Green |

## 📥 Building Your Corpus

### Quick Download (Recommended Topics)
```bash
python main.py corpus
# Select option 1 for quick download
```

### Custom Topic Download
```bash
# From command line
python backend/database/corpus_builder.py --download "specific topic" 50

# Or interactive mode
python main.py corpus
# Select option 2
```

### View Corpus Statistics
```bash
python backend/database/corpus_builder.py --stats
```

## 🔍 Checking Documents

### 1. Place your paper in `submit/` folder
```
submit/
└── my_paper.txt
```

### 2. Run the checker
```bash
python main.py check
```

### 3. View Results
The system will compare your paper against all 603 corpus papers and show:
- Overall highest match percentage
- Detailed matches sorted by similarity
- Plagiarism level classification

## 📦 Dependencies

```
nltk>=3.8
scikit-learn>=1.3
numpy>=1.24
```

## 🔮 Future Enhancements

- [ ] Web interface (frontend/)
- [ ] REST API (backend/api/)
- [ ] Real-time document monitoring
- [ ] PDF/DOCX support
- [ ] Citation detection
- [ ] Paraphrase detection with BERT
- [ ] Report generation (PDF)

## 📄 License

MIT License

---

**Built with ❤️ using Python, NLTK, and Scikit-learn**