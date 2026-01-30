# 🔌 Backend + Frontend Integration Guide

## ✅ What Was Done

Your PLAUGE system now has a **complete frontend-to-backend integration**! Here's what was connected:

### **Backend API** (`backend/api/app.py`)
- ✅ Flask REST API server
- ✅ `/api/analyze` endpoint for plagiarism detection
- ✅ `/api/health` for health checks
- ✅ `/api/corpus/stats` for corpus statistics
- ✅ Loads all 603 papers from corpus automatically
- ✅ Returns real TF-IDF analysis results

### **Frontend** (`frontend/app.js`)
- ✅ Updated to call Flask API at `http://localhost:5000`
- ✅ Sends files via `FormData`
- ✅ Receives real plagiarism scores
- ✅ Displays actual corpus paper matches
- ✅ Shows true analysis time

---

## 🚀 How to Run the Full System

### **Step 1: Install Dependencies** (One-time)
```bash
cd c:\Users\USER\Documents\PROJECTS\PLAUGE
pip install -r requirements.txt
```

This installs:
- `nltk` - Natural language processing
- `scikit-learn` - TF-IDF vectorization
- `numpy` - Numerical operations
- `flask` - Web API server
- `flask-cors` - Cross-origin requests

---

### **Step 2: Start the Backend Server**

**Option A: Using the batch script** (Easiest)
```bash
# Just double-click:
start_backend.bat

# Or from command line:
start_backend.bat
```

**Option B: Manual start**
```bash
cd c:\Users\USER\Documents\PROJECTS\PLAUGE
python backend\api\app.py
```

You should see:
```
============================================================
🚀 Starting PLAUGE API Server
============================================================

📥 Downloading NLTK resources...
📚 Loaded 603 documents from corpus

✅ Server ready!
   Frontend: Open frontend/index.html in browser
   API URL:  http://localhost:5000
============================================================

 * Serving Flask app 'app'
 * Running on http://0.0.0.0:5000
```

**Keep this terminal open!** The server needs to run in the background.

---

### **Step 3: Open the Frontend**

In a **new terminal** or just double-click:

**Option A: Direct open**
```bash
cd frontend
start index.html
```

**Option B: With local server** (recommended)
```bash
cd frontend
python -m http.server 8000
# Visit: http://localhost:8000
```

---

## 📝 Test It Out!

### **Upload a Test Document**

1. **Drag & Drop** or **Click** to upload a `.txt` file
2. Click **"Analyze Document"**
3. Watch the real analysis happen:
   - Progress bar shows actual processing
   - Backend loads 603 corpus papers
   - TF-IDF vectorization runs
   - Cosine similarity calculated
   - Real results displayed!

### **What You'll See**

**Real Data:**
- ✅ **Overall Score**: Actual highest similarity percentage
- ✅ **Documents Compared**: Real count (603)
- ✅ **Highest Match**: True maximum similarity
- ✅ **Top Matches**: Actual paper titles from your corpus
- ✅ **Categories**: Real categories (machine_learning, nlp, etc.)
- ✅ **Analysis Time**: Actual processing time

**Sample Result:**
```json
{
  "overallScore": 67,
  "highestMatch": 67,
  "avgSimilarity": 38,
  "analysisTime": "2.3s",
  "documentsCompared": 603,
  "matches": [
    {
      "title": "attention_is_all_you_need",
      "category": "transformers",
      "score": 67
    },
    ...
  ]
}
```

---

## 🔍 API Endpoints Reference

### **GET /api/health**
Health check endpoint
```bash
curl http://localhost:5000/api/health
```
Returns:
```json
{
  "status": "healthy",
  "message": "PLAUGE API is running"
}
```

### **GET /api/corpus/stats**
Get corpus statistics
```bash
curl http://localhost:5000/api/corpus/stats
```
Returns:
```json
{
  "total_documents": 603,
  "categories": {
    "machine_learning": 65,
    "deep_learning": 43,
    ...
  }
}
```

### **POST /api/analyze**
Analyze document for plagiarism
```bash
curl -X POST \
  -F "document=@myfile.txt" \
  http://localhost:5000/api/analyze
```

---

## 🛠️ How It Works

### **Backend Flow:**
```
1. Frontend uploads file
   ↓
2. Flask receives file at /api/analyze
   ↓
3. Extract text content
   ↓
4. Load all 603 corpus documents
   ↓
5. Create combined document list [uploaded_doc, corpus_doc1, ...]
   ↓
6. Run PlagiarismDetector:
   - Preprocess all documents
   - TF-IDF vectorization
   - Cosine similarity matrix
   ↓
7. Extract matches for uploaded doc (index 0)
   ↓
8. Sort by similarity, get top 5
   ↓
9. Return JSON response
```

### **Frontend Flow:**
```
1. User drags/uploads file
   ↓
2. File preview shown
   ↓
3. User clicks "Analyze Document"
   ↓
4. FormData created with file
   ↓
5. fetch('http://localhost:5000/api/analyze', {POST})
   ↓
6. Progress animation while waiting
   ↓
7. Receive JSON response
   ↓
8. Display real results:
   - Score circle animation
   - Top matches list
   - Statistics
```

---

## 🐛 Troubleshooting

### **Error: "Failed to fetch"**
**Problem:** Backend server not running

**Solution:**
```bash
# Start the backend:
python backend\api\app.py
```

---

### **Error: "No corpus documents found"**
**Problem:** Corpus folder empty or wrong path

**Solution:**
- Check that `corpus/` folder has subdirectories with .txt files
- Verify you have 603 papers in the corpus
- Path should be `PLAUGE/corpus/machine_learning/*.txt`, etc.

---

### **Error: "Invalid file type"**
**Problem:** Only `.txt` files currently supported

**Solution:**
- For now, upload only `.txt` files
- PDF/DOCX support can be added later with:
  ```bash
  pip install PyPDF2 python-docx
  ```

---

### **Port 5000 already in use**
**Problem:** Another app using port 5000

**Solution:**
Edit `backend/api/app.py`, line 194:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change to 5001
```

Then update `frontend/app.js`, line 162:
```javascript
const response = await fetch('http://localhost:5001/api/analyze', {
```

---

## 📊 File Changes Made

### **New Files:**
1. ✅ `backend/api/app.py` - Flask API server
2. ✅ `start_backend.bat` - Easy startup script

### **Modified Files:**
1. ✅ `frontend/app.js` - Real API calls instead of mock data
2. ✅ `requirements.txt` - Added Flask dependencies

### **What Stays Same:**
- ✅ All ML models (`plagiarism_detector.py`)
- ✅ Corpus loading logic
- ✅ TF-IDF algorithm
- ✅ Frontend UI/styling

---

## ✅ Success Checklist

Before testing, make sure:
- [x] Flask installed (`pip install flask flask-cors`)
- [x] Backend server running (port 5000)
- [x] Frontend open in browser
- [x] Corpus has 603 documents
- [x] `.txt` file ready to upload

---

## 🎯 Next Steps

Now that backend + frontend are connected:

### **Immediate:**
1. ✅ Test with real documents
2. ✅ Verify results match expectations
3. ✅ Try different papers from corpus

### **Soon:**
- [ ] Add PDF/DOCX support
- [ ] Show highlighted matching text
- [ ] Generate downloadable reports
- [ ] Add authentication
- [ ] Deploy to cloud

### **Later:**
- [ ] Add real-time streaming
- [ ] Implement caching for faster repeat checks
- [ ] Create document comparison view
- [ ] Add citation detection

---

## 💡 Pro Tips

### **Faster Testing:**
- Backend stays open - no need to restart
- Just refresh frontend after changes
- Use browser DevTools (F12) to debug

### **Better Results:**
- Longer documents = better analysis
- More unique content = lower scores
- Very short texts may show high similarity

### **Performance:**
- 603 papers analyzes in ~2-5 seconds
- Larger corpus = longer analysis time
- Consider caching for production

---

## 🎉 You're All Connected!

Your system is now **fully operational** with:
- ✨ Beautiful frontend UI
- 🧠 Powerful ML backend
- 🔌 Real-time API connection
- 📊 Actual plagiarism detection

**Test it now and see real results!** 🚀

---

**Questions? Check:**
- `backend/api/app.py` - API implementation
- `frontend/app.js` - Line 142-184 for API calls
- Browser console (F12) for debugging
- Backend terminal for server logs
