# ✅ Feature Update: Intelligent Search & AI Detection

## 🎉 Major Upgrades Completed

I've enhanced the PLAUGE system to be smarter and more automated, as per your request!

### **1. Intelligent Web Search 🧠**
- **Auto-Keywords**: You no longer need to type a search query! The system reads your uploaded document, extracts key phrases (using RAKE algorithm), and automatically searches for relevant papers.
- **Wikipedia Support**: Now searches Wikipedia in addition to arXiv and Semantic Scholar for broader context.
- **Expanded Scope**: Checks against 200M+ online sources without manual input.

### **2. AI Content Detection 🤖**
- **New Analysis Module**: Checks your document for patterns typical of AI generation (sentence length variance, vocabulary richness).
- **Visual Gauge**: A new card in the results screen shows the **AI Probability Score** (0-100%) and assessment (e.g., "Likely Human-Written").

### **3. UI / UX Improvements ✨**
- **Home Button**: Added a "Home" icon in the results header to quickly start over.
- **Fixed Actions**:
  - 💾 **Download Report**: Generates a detailed `.txt` report with all matches and scores.
  - 🔗 **Share Results**: Copies a summary to your clipboard for easy sharing.

---

## 🚀 How to Use the New Features

1.  **Open Frontend**: `frontend/index.html`
2.  **Select "Web Search"**: Click the toggle.
3.  **Leave Search Empty**: Just upload your file! The system will say: *"Auto-generating keywords..."*
4.  **Analyze**: Watch it find papers automatically.
5.  **View Results**:
    - See the **AI Detection** card.
    - Check the **Papers Found**.
    - Click **Download Report** to save the analysis.

---

## 🔧 Technical Details

**New Modules:**
- `backend/api/web_search.py`: Contains `KeywordExtractor`, `WikipediaSearcher`, `AIContentScanner`.
- `backend/api/app.py`: Updated `/api/analyze/web` to use auto-query logic.

**Visual Upgrades:**
- **AI Card**: Gradients (Green to Red) based on probability.
- **Icons**: Added Home, Download, and Share icons.

**System is fully operational!** 🚀
