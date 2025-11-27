# Google Reviews Sentiment Analysis System

## Quick Setup Guide

### 1. Prerequisites
- Python 3.8+
- Google Chrome
- Google Business Profile access

### 2. Installation
```bash
# Clone repository
git clone https://github.com/yourusername/google-reviews-sentiment-analysis.git
cd google-reviews-sentiment-analysis

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('vader_lexicon')"
```

### 3. Configuration
Edit `src/config.py` to customize settings:
- Chrome debugging port
- Sentiment thresholds
- Database credentials (optional)
- File paths

### 4. Run the System

**Option A: Full Automated Pipeline**
```bash
python scripts/run_full_pipeline.py
```

**Option B: Step by Step**

1. Start Chrome with debugging:
```powershell
.\scripts\start_chrome.ps1
```

2. Scrape reviews:
```bash
python src/scraper.py
```

3. Analyze sentiment (use Jupyter notebook):
```bash
jupyter notebook notebooks/sentiment_analysis.ipynb
```

### 5. Output
- Scraped reviews: `output/reviews/`
- Analysis reports: `output/reports/`

## Project Structure
```
├── src/              # Source code
├── scripts/          # Automation scripts
├── notebooks/        # Jupyter notebooks
├── data/             # Data files
├── assets/           # Brand assets
└── output/           # Generated files
```

## Need Help?
- Check the [full README](README.md)
- Open an [issue](https://github.com/yourusername/google-reviews-sentiment-analysis/issues)
- Read [Contributing Guide](CONTRIBUTING.md)
