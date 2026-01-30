// ============================================
// PLAUGE - Plagiarism Detection System
// Interactive Frontend Application
// ============================================

class PlagiarismDetector {
    constructor() {
        this.currentFile = null;
        this.analysisResults = null;
        // Determine API URL based on where the frontend is loaded from
        const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
        this.apiBaseUrl = isLocalhost ? '' : 'http://localhost:5000';
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupDragAndDrop();
    }

    setupEventListeners() {
        // Upload area click
        const uploadArea = document.getElementById('upload-area');
        const fileInput = document.getElementById('file-input');

        if (uploadArea && fileInput) {
            uploadArea.addEventListener('click', () => {
                fileInput.click();
            });

            // File input change
            fileInput.addEventListener('change', (e) => {
                if (e.target.files.length > 0) {
                    this.handleFileSelect(e.target.files[0]);
                }
            });
        }

        // Remove file button
        const removeFileBtn = document.getElementById('remove-file');
        if (removeFileBtn) {
            removeFileBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.removeFile();
            });
        }

        // Analyze button
        const analyzeBtn = document.getElementById('analyze-btn');
        if (analyzeBtn) {
            analyzeBtn.addEventListener('click', () => {
                this.analyzeDocument();
            });
        }

        // New analysis button
        const newAnalysisBtn = document.getElementById('new-analysis-btn');
        if (newAnalysisBtn) {
            newAnalysisBtn.addEventListener('click', () => {
                this.resetToUpload();
            });
        }

        // Get Started button (Scroll to upload or return to home)
        const getStartedBtn = document.getElementById('getStartedBtn');
        if (getStartedBtn) {
            getStartedBtn.addEventListener('click', (e) => {
                console.log('Get Started button clicked');
                e.preventDefault();

                // Check if we're on the results page
                const analysisSection = document.getElementById('analysis-section');
                const heroSection = document.getElementById('hero-section');

                // If results are showing, go back to home
                if (analysisSection && !analysisSection.classList.contains('hidden')) {
                    console.log('On results page - returning to home');
                    this.resetToUpload();
                } else {
                    // Otherwise, scroll to upload section
                    console.log('On home page - scrolling to upload');
                    const uploadSection = document.getElementById('upload-section');
                    console.log('Upload section found:', uploadSection);
                    if (uploadSection) {
                        uploadSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
                        // Also focus on the upload area for better visibility
                        setTimeout(() => {
                            const uploadArea = document.getElementById('upload-area');
                            if (uploadArea) {
                                uploadArea.style.transform = 'scale(1.02)';
                                setTimeout(() => {
                                    uploadArea.style.transform = 'scale(1)';
                                }, 200);
                            }
                        }, 500);
                    } else {
                        console.error('Upload section not found!');
                    }
                }
            });
        } else {
            console.error('Get Started button not found!');
        }

        // Setup modallisteners
        this.setupModalListeners();

        // New Action Buttons
        const homeBtn = document.getElementById('home-btn');
        if (homeBtn) {
            homeBtn.addEventListener('click', () => this.resetToUpload());
        }

        const downloadBtn = document.getElementById('download-report-btn');
        if (downloadBtn) {
            downloadBtn.addEventListener('click', () => this.downloadReport());
        }

        const shareBtn = document.getElementById('share-results-btn');
        if (shareBtn) {
            shareBtn.addEventListener('click', () => this.shareResults());
        }
    }

    setupModalListeners() {
        const aboutBtn = document.getElementById('aboutBtn');
        const statsBtn = document.getElementById('statsBtn');
        const closeModal = document.getElementById('close-modal');
        const closeStatsModal = document.getElementById('close-stats-modal');
        const modalOverlay = document.getElementById('modal-overlay');
        const statsModalOverlay = document.getElementById('stats-modal-overlay');

        if (aboutBtn) {
            aboutBtn.addEventListener('click', () => this.showModal('about-modal'));
        }

        if (statsBtn) {
            statsBtn.addEventListener('click', () => this.showModal('stats-modal'));
        }

        if (closeModal) {
            closeModal.addEventListener('click', () => this.hideModal('about-modal'));
        }

        if (closeStatsModal) {
            closeStatsModal.addEventListener('click', () => this.hideModal('stats-modal'));
        }

        if (modalOverlay) {
            modalOverlay.addEventListener('click', () => this.hideModal('about-modal'));
        }

        if (statsModalOverlay) {
            statsModalOverlay.addEventListener('click', () => this.hideModal('stats-modal'));
        }

        // History Modal Listeners
        const historyBtn = document.getElementById('historyBtn');
        const closeHistoryModal = document.getElementById('close-history-modal');
        const historyModalOverlay = document.getElementById('history-modal-overlay');
        const clearHistoryBtn = document.getElementById('clear-history-btn');

        if (historyBtn) {
            historyBtn.addEventListener('click', () => {
                this.showModal('history-modal');
                this.loadHistory();
            });
        }

        if (closeHistoryModal) {
            closeHistoryModal.addEventListener('click', () => this.hideModal('history-modal'));
        }

        if (historyModalOverlay) {
            historyModalOverlay.addEventListener('click', () => this.hideModal('history-modal'));
        }

        if (clearHistoryBtn) {
            clearHistoryBtn.addEventListener('click', () => this.clearHistory());
        }
    }

    setupDragAndDrop() {
        const uploadArea = document.getElementById('upload-area');
        if (!uploadArea) return;

        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');

            if (e.dataTransfer.files.length > 0) {
                this.handleFileSelect(e.dataTransfer.files[0]);
            }
        });
    }

    handleFileSelect(file) {
        // Validate file type
        const validTypes = ['.txt', '.pdf', '.docx'];
        const fileExtension = '.' + file.name.split('.').pop().toLowerCase();

        if (!validTypes.includes(fileExtension)) {
            alert('Please upload a .txt, .pdf, or .docx file');
            return;
        }

        this.currentFile = file;
        this.showFilePreview();
    }

    showFilePreview() {
        if (!this.currentFile) return;

        // Hide upload area, show file preview
        const uploadArea = document.getElementById('upload-area');
        const filePreview = document.getElementById('file-preview');

        if (uploadArea) uploadArea.style.display = 'none';
        if (filePreview) filePreview.classList.remove('hidden');

        // Update file info
        const fileName = document.getElementById('file-name');
        const fileSize = document.getElementById('file-size');
        if (fileName) fileName.textContent = this.currentFile.name;
        if (fileSize) fileSize.textContent = this.formatFileSize(this.currentFile.size);
    }

    removeFile() {
        this.currentFile = null;
        const uploadArea = document.getElementById('upload-area');
        const filePreview = document.getElementById('file-preview');
        const fileInput = document.getElementById('file-input');

        if (uploadArea) uploadArea.style.display = 'block';
        if (filePreview) filePreview.classList.add('hidden');
        if (fileInput) fileInput.value = '';
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
    }

    async analyzeDocument() {
        if (!this.currentFile) return;

        // Hide hero section, show analysis section
        const heroSection = document.getElementById('hero-section');
        const analysisSection = document.getElementById('analysis-section');

        if (heroSection) heroSection.classList.add('hidden');
        if (analysisSection) analysisSection.classList.remove('hidden');

        // Reset progress
        this.resetProgress();

        try {
            // Show progress animation
            this.simulateAnalysisProgress();

            // Prepare form data
            const formData = new FormData();
            formData.append('document', this.currentFile);

            // Call backend API (Robust URL handling)
            const response = await fetch(`${this.apiBaseUrl}/api/analyze`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Analysis failed');
            }

            // Get real results
            this.analysisResults = await response.json();

            // Show results
            setTimeout(() => {
                this.showResults();
            }, 500);

        } catch (error) {
            console.error('Analysis error:', error);
            alert('Error analyzing document: ' + error.message + '\n\nMake sure the backend server is running:\n  cd backend/api\n  python app.py');
            this.resetToUpload();
        }
    }

    async simulateAnalysisProgress() {
        // Show progress animation for Unified Analysis
        const steps = [
            { step: 1, text: 'Auto-detecting keywords & searching web...', progress: 30, duration: 2500 },
            { step: 2, text: 'Scanning local corpus (600+ docs)...', progress: 50, duration: 1000 },
            { step: 3, text: 'Analyzing AI patterns & Similarity...', progress: 75, duration: 1500 },
            { step: 4, text: 'Compiling unified report...', progress: 100, duration: 800 }
        ];

        for (const stepData of steps) {
            await this.executeStep(stepData);
        }
    }

    resetProgress() {
        const progressCard = document.getElementById('progress-card');
        const resultsCard = document.getElementById('results-card');
        const progressFill = document.getElementById('progress-fill');

        if (progressCard) progressCard.classList.remove('hidden');
        if (resultsCard) resultsCard.classList.add('hidden');

        // Reset all steps
        document.querySelectorAll('.step').forEach(step => {
            step.classList.remove('active', 'completed');
        });

        // Reset progress bar
        if (progressFill) progressFill.style.width = '0%';
    }

    async executeStep(stepData) {
        return new Promise((resolve) => {
            // Update active step
            document.querySelectorAll('.step').forEach((step, index) => {
                if (index + 1 < stepData.step) {
                    step.classList.remove('active');
                    step.classList.add('completed');
                } else if (index + 1 === stepData.step) {
                    step.classList.add('active');
                } else {
                    step.classList.remove('active', 'completed');
                }
            });

            // Update progress text
            const progressText = document.getElementById('progress-text');
            if (progressText) progressText.textContent = stepData.text;

            // Update progress bar
            const progressFill = document.getElementById('progress-fill');
            if (progressFill) progressFill.style.width = stepData.progress + '%';

            // Wait for step duration
            setTimeout(resolve, stepData.duration);
        });
    }

    showResults() {
        // Hide progress card, show results card
        const progressCard = document.getElementById('progress-card');
        const resultsCard = document.getElementById('results-card');

        if (progressCard) progressCard.classList.add('hidden');
        if (resultsCard) resultsCard.classList.remove('hidden');

        // Display results (already set from API call)
        this.displayResults();
    }

    async downloadReport() {
        if (!this.analysisResults) {
            alert("No analysis exists to download.");
            return;
        }

        if (!window.jspdf) {
            alert("PDF Generator library not found. Please refresh the page.");
            console.error("jsPDF not loaded");
            return;
        }

        try {
            console.log("Starting PDF generation...");
            const { jsPDF } = window.jspdf;
            const doc = new jsPDF();
            const r = this.analysisResults;
            const date = new Date().toLocaleString();

            // Colors (Arsenal Theme)
            const red = '#EF0107';
            const dark = '#001321';
            const gray = '#666666';

            // Header
            doc.setFillColor(dark);
            doc.rect(0, 0, 210, 40, 'F');

            doc.setFontSize(22);
            doc.setTextColor('#FFFFFF');
            doc.text("PLAUGE Analysis Report", 20, 20);

            doc.setFontSize(10);
            doc.setTextColor('#CCCCCC');
            doc.text("Unified Plagiarism & AI Detection", 20, 30);
            doc.text(date, 150, 30);

            // File Info
            doc.setTextColor(dark);
            doc.setFontSize(12);
            doc.text("File Analyzed:", 20, 55);
            doc.setFont("helvetica", "bold");
            doc.text(this.currentFile ? this.currentFile.name : 'Document', 60, 55);

            doc.setFont("helvetica", "normal");
            doc.text("Total Documents Compared:", 20, 65);
            doc.setFont("helvetica", "bold");
            doc.text(r.documentsCompared.toString(), 80, 65);

            // Scores Box
            doc.setDrawColor(red);
            doc.setLineWidth(1);
            doc.rect(20, 75, 170, 45);

            // Plagiarism Score
            doc.setTextColor(red);
            doc.setFontSize(30);
            doc.text(`${r.overallScore}%`, 35, 95);

            doc.setTextColor(dark);
            doc.setFontSize(10);
            doc.text("Plagiarism Score", 35, 105);

            doc.line(80, 75, 80, 120); // Divider

            // AI Score
            let aiScore = "N/A";
            let aiLevel = "Unknown";
            if (r.aiDetection) {
                aiScore = `${r.aiDetection.score}%`;
                aiLevel = r.aiDetection.level;
            }

            doc.setTextColor(red);
            doc.setFontSize(20);
            doc.text(aiScore, 95, 95);

            doc.setTextColor(dark);
            doc.setFontSize(10);
            doc.text("AI Probability", 95, 105);
            doc.setFontSize(8);
            doc.text(`(${aiLevel} Risk)`, 95, 110);

            doc.line(135, 75, 135, 120); // Divider

            // Status
            doc.setFontSize(14);
            doc.setTextColor(dark);
            doc.text("Status:", 145, 95);
            doc.setFont("helvetica", "bold");
            doc.setTextColor(red);
            doc.text(this.getRiskStatus(r.overallScore), 145, 105);

            // Matches Section
            let y = 140;
            doc.setFontSize(14);
            doc.setTextColor(dark);
            doc.setFont("helvetica", "bold");
            doc.text("Top Similarity Matches", 20, y);
            y += 10;

            doc.setLineWidth(0.5);
            doc.line(20, y, 190, y);
            y += 10;

            doc.setFontSize(10);
            r.matches.forEach((m, i) => {
                if (y > 270) {
                    doc.addPage();
                    y = 20;
                }

                doc.setFont("helvetica", "bold");
                doc.setTextColor(red);
                doc.text(`${i + 1}. ${m.score}% Match`, 20, y);

                doc.setFont("helvetica", "bold");
                doc.setTextColor(dark);
                const title = m.title.length > 50 ? m.title.substring(0, 50) + "..." : m.title;
                doc.text(title, 60, y);

                y += 6;
                doc.setFont("helvetica", "normal");
                doc.setTextColor(gray);
                doc.text(`Source: ${m.category} | Authors: ${m.authors || 'N/A'}`, 60, y);

                if (m.url) {
                    y += 5;
                    doc.setTextColor('#023474'); // Link color
                    doc.textWithLink("View Source", 60, y, { url: m.url });
                }

                y += 12;
            });

            // Footer
            const pageCount = doc.internal.getNumberOfPages();
            for (let i = 1; i <= pageCount; i++) {
                doc.setPage(i);
                doc.setFontSize(8);
                doc.setTextColor(gray);
                doc.text(`Generated by PLAUGE System - Page ${i} of ${pageCount}`, 105, 290, { align: "center" });
            }

            const filename = `PLAUGE_Report_${Date.now()}.pdf`;

            // Force download using Blob (Fix for file:// protocol issues)
            const pdfBlob = doc.output('blob');
            const url = URL.createObjectURL(pdfBlob);
            const link = document.createElement('a');
            link.href = url;
            link.download = filename;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(url);

            console.log(`PDF Saved via forced link: ${filename}`);

        } catch (e) {
            console.error("PDF Generation Error:", e);
            alert("Error generating PDF. Please ensure your browser supports safe file downloads.");
        }
    }

    shareResults() {
        if (!this.analysisResults) return;

        const text = `I just analyzed a document with PLAUGE!\nSimilarity: ${this.analysisResults.overallScore}%\nHighest Match: ${this.analysisResults.highestMatch}%`;

        // Visual feedback
        const btn = document.getElementById('share-results-btn');
        if (btn) {
            const originalText = btn.innerHTML;
            btn.innerHTML = `<span style="color: #10b981">✓ Copied!</span>`;
            setTimeout(() => btn.innerHTML = originalText, 2000);
        }

        if (navigator.share) {
            navigator.share({
                title: 'PLAUGE Analysis Result',
                text: text,
                url: window.location.href
            }).catch(console.error);
        } else {
            // Fallback to clipboard
            navigator.clipboard.writeText(text).then(() => {
                // Feedback shown via button text
            }).catch(err => {
                alert('Could not copy results.');
            });
        }
    }

    getRiskStatus(score) {
        if (score >= 80) return 'High Risk';
        if (score >= 50) return 'Medium Risk';
        return 'Low Risk';
    }

    displayResults() {
        const results = this.analysisResults;

        // Update score circle
        this.updateScoreCircle(results.overallScore);

        // Update details
        const docsCompared = document.getElementById('docs-compared');
        const highestMatch = document.getElementById('highest-match');
        const avgSimilarity = document.getElementById('avg-similarity');
        const analysisTime = document.getElementById('analysis-time');

        if (docsCompared) docsCompared.textContent = results.documentsCompared || '603';
        if (highestMatch) highestMatch.textContent = results.highestMatch + '%';
        if (avgSimilarity) avgSimilarity.textContent = results.avgSimilarity + '%';
        if (analysisTime) analysisTime.textContent = results.analysisTime;

        // Show AI Detection if available
        const aiCard = document.getElementById('ai-card');
        if (results.aiDetection) {
            if (aiCard) aiCard.classList.remove('hidden');
            const ai = results.aiDetection;

            // Animate AI Score
            setTimeout(() => {
                const aiFill = document.getElementById('ai-fill');
                if (aiFill) {
                    aiFill.style.width = ai.score + '%';
                    if (ai.score > 70) aiFill.style.background = 'var(--gradient-danger)';
                    else if (ai.score > 40) aiFill.style.background = 'var(--gradient-warning)';
                    else aiFill.style.background = 'var(--gradient-success)';
                }
            }, 300);

            const aiScore = document.getElementById('ai-score');
            if (aiScore) this.animateValue(aiScore, 0, ai.score, 1000, '%');

            const aiStatus = document.getElementById('ai-status');
            if (aiStatus) aiStatus.textContent = `${ai.level} Probability of AI Content`;

            if (ai.details) {
                const metricVariance = document.getElementById('metric-variance');
                const metricVocab = document.getElementById('metric-vocab');
                if (metricVariance) metricVariance.textContent = ai.details.std_dev || '-';
                if (metricVocab) metricVocab.textContent = ai.details.vocabulary_richness || '-';
            }
        } else {
            if (aiCard) aiCard.classList.add('hidden');
        }

        // Display matches
        this.displayMatches(results.matches);
    }

    updateScoreCircle(score) {
        const scoreValue = document.getElementById('score-value');
        const scoreLabel = document.getElementById('score-label');
        const scoreStatus = document.getElementById('score-status');
        const scoreCircle = document.getElementById('score-circle-progress');

        if (!scoreValue || !scoreCircle) return;

        const scoreGradient = scoreCircle.parentElement.querySelector('linearGradient');

        // Animate score counting
        this.animateValue(scoreValue, 0, score, 1000, '%');

        // Calculate circle progress (534 is circumference for r=85)
        const circumference = 534;
        const offset = circumference - (score / 100) * circumference;

        setTimeout(() => {
            scoreCircle.style.strokeDashoffset = offset;
        }, 100);

        // Update color and status based on score
        let status, statusText, color1, color2;

        if (score >= 80) {
            status = 'High Risk';
            statusText = 'High Plagiarism Detected';
            color1 = '#ef4444';
            color2 = '#dc2626';
        } else if (score >= 50) {
            status = 'Medium Risk';
            statusText = 'Moderate Similarity';
            color1 = '#f59e0b';
            color2 = '#d97706';
        } else {
            status = 'Low Risk';
            statusText = 'Original Content';
            color1 = '#10b981';
            color2 = '#059669';
        }

        if (scoreStatus) scoreStatus.textContent = status;
        if (scoreLabel) scoreLabel.textContent = statusText;

        // Update gradient colors
        if (scoreGradient && scoreGradient.children.length >= 2) {
            scoreGradient.children[0].setAttribute('stop-color', color1);
            scoreGradient.children[1].setAttribute('stop-color', color2);
        }
    }

    displayMatches(matches) {
        const matchesList = document.getElementById('matches-list');
        if (!matchesList) return;
        matchesList.innerHTML = '';

        matches.forEach((match, index) => {
            const matchItem = document.createElement('div');
            matchItem.className = 'match-item';
            matchItem.style.animation = `fadeInUp 0.5s ease-out ${index * 0.1}s both`;

            const riskLevel = match.score >= 80 ? 'high' : match.score >= 50 ? 'medium' : 'low';

            // Handle Web Search Links
            let titleHtml = match.title;
            if (match.url) {
                titleHtml = `<a href="${match.url}" target="_blank" class="match-link">${match.title} <span class="external-icon">↗</span></a>`;
            }

            matchItem.innerHTML = `
                <div class="match-header">
                    <h4 class="match-title">${titleHtml}</h4>
                    <span class="match-score">${match.score}%</span>
                </div>
                <p class="match-category">${match.category} ${match.authors ? '• ' + match.authors : ''}</p>
                <div class="match-snippet">
                    <span class="snippet-label">Matched Text:</span>
                    <p>"${match.snippet || 'Similar concepts or formatting detected.'}"</p>
                </div>
                <div class="match-bar">
                    <div class="match-bar-fill ${riskLevel}" style="width: 0%"></div>
                </div>
            `;

            matchesList.appendChild(matchItem);

            // Animate bar fill
            setTimeout(() => {
                const fill = matchItem.querySelector('.match-bar-fill');
                if (fill) fill.style.width = match.score + '%';
            }, 200 + (index * 100));
        });
    }

    animateValue(element, start, end, duration, suffix = '') {
        if (!element) return;
        const range = end - start;
        const increment = range / (duration / 16); // 60fps
        let current = start;

        const timer = setInterval(() => {
            current += increment;
            if (current >= end) {
                current = end;
                clearInterval(timer);
            }
            element.textContent = Math.floor(current) + suffix;
        }, 16);
    }

    resetToUpload() {
        // Hide analysis section, show hero section
        const analysisSection = document.getElementById('analysis-section');
        const heroSection = document.getElementById('hero-section');

        if (analysisSection) analysisSection.classList.add('hidden');
        if (heroSection) heroSection.classList.remove('hidden');

        // Reset file
        this.removeFile();
        this.analysisResults = null;
    }

    showModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove('hidden');
            // Prevent body scroll
            document.body.style.overflow = 'hidden';
        }
    }

    hideModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('hidden');
            // Restore body scroll
            document.body.style.overflow = '';
        }
    }

    async loadHistory() {
        const list = document.getElementById('history-list');
        if (!list) return;

        list.innerHTML = '<p class="no-history">Loading history...</p>';

        try {
            const response = await fetch(`${this.apiBaseUrl}/api/history`);
            const history = await response.json();

            if (!history || history.length === 0) {
                list.innerHTML = '<p class="no-history">No history available yet.</p>';
                return;
            }

            list.innerHTML = '';
            history.forEach(item => {
                const el = document.createElement('div');
                el.className = 'history-item';

                const scoreClass = item.overallScore >= 80 ? 'high' : item.overallScore >= 50 ? 'medium' : 'low';
                const riskLabel = item.overallScore >= 80 ? 'High Risk' : item.overallScore >= 50 ? 'Medium Risk' : 'Low Risk';

                el.innerHTML = `
                    <div class="history-main">
                        <div class="history-file">${item.fileName}</div>
                        <div class="history-date">${item.timestamp}</div>
                    </div>
                    <div class="history-meta">
                        <span class="history-badge ${scoreClass}">${riskLabel}</span>
                        <div class="history-score" style="color: var(--${scoreClass === 'high' ? 'danger' : scoreClass === 'medium' ? 'warning' : 'success'})">
                            ${item.overallScore}%
                        </div>
                    </div>
                `;
                list.appendChild(el);
            });

        } catch (e) {
            console.error('History Error:', e);
            list.innerHTML = '<p class="no-history">Failed to load history.</p>';
        }
    }

    async clearHistory() {
        if (!confirm('Are you sure you want to clear your analysis history?')) return;

        try {
            await fetch(`${this.apiBaseUrl}/api/history`, { method: 'DELETE' });
            this.loadHistory(); // Refresh list
        } catch (e) {
            console.error('Clear History Error:', e);
            alert('Failed to clear history');
        }
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.detectorInstance = new PlagiarismDetector();
});

// Add some extra interactivity
document.addEventListener('DOMContentLoaded', () => {
    // Smooth scroll for links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#') return;
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Add parallax effect to gradient orbs
    document.addEventListener('mousemove', (e) => {
        const orbs = document.querySelectorAll('.gradient-orb');
        const mouseX = e.clientX / window.innerWidth;
        const mouseY = e.clientY / window.innerHeight;

        orbs.forEach((orb, index) => {
            const speed = (index + 1) * 20;
            const x = (mouseX - 0.5) * speed;
            const y = (mouseY - 0.5) * speed;
            orb.style.transform = `translate(${x}px, ${y}px)`;
        });
    });

    // Typing effect removed to preserve HTML formatting and spacing
    const heroDesc = document.querySelector('.hero-description');
    if (heroDesc) {
        heroDesc.style.opacity = '1'; // Ensure it's visible
    }
});
