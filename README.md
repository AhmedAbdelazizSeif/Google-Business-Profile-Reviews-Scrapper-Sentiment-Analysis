# Google Reviews Sentiment Analysis System 🎯

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Selenium](https://img.shields.io/badge/selenium-4.15+-green.svg)](https://www.selenium.dev/)
[![Pandas](https://img.shields.io/badge/pandas-2.0+-orange.svg)](https://pandas.pydata.org/)

A comprehensive automated system for scraping Google Business reviews, performing sentiment analysis, and generating beautifully styled Excel reports with bilingual (Arabic/English) support.

## 📋 Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
  - [1. Scraping Reviews](#1-scraping-reviews)
  - [2. Sentiment Analysis](#2-sentiment-analysis)
  - [3. Report Generation](#3-report-generation)
- [Configuration](#-configuration)
- [Output Examples](#-output-examples)
- [Advanced Features](#-advanced-features)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

## ✨ Features

### 🔍 Web Scraping
- **Automated Google Business Profile scraping** using Selenium
- **Connection to existing Chrome sessions** for authenticated access
- **Intelligent pagination** with automatic page navigation
- **Time-based filtering** (scrape reviews from last N weeks)
- **Duplicate detection** to avoid redundant data
- **Robust error handling** and retry mechanisms

### 📊 Sentiment Analysis
- **Context-aware sentiment analysis** using VADER (Valence Aware Dictionary and sEntiment Reasoner)
- **Dual-context analysis**:
  - **Salesman-specific sentiment** (staff, service, friendliness)
  - **Store-specific sentiment** (location, cleanliness, products)
- **Star rating integration** for enhanced accuracy
- **Bilingual support** (Arabic and English reviews)
- **Salesman name extraction** from reviews

### 📈 Report Generation
- **Beautiful Excel reports** with professional styling
- **Brand color extraction** from logo images using PIL
- **Multi-sheet workbooks** with different analyses:
  - Salesman performance summary
  - Store/branch performance summary
  - Cross-analysis (Store × Salesman)
  - Detailed reviews with full context
- **Arabic and English column headers**
- **Modern UI elements**:
  - Logo integration in headers
  - Alternating row colors for readability
  - Frozen header rows
  - Auto-adjusted column widths
  - Custom color schemes

### 🎨 Design & UX
- **Automatic color palette extraction** from brand logos
- **Eye-comfortable color schemes** (green/blue palettes)
- **Professional formatting** with borders and alignment
- **Responsive column sizing**
- **Arabic date formats** in sheet names

## 📁 Project Structure

```
google-reviews-sentiment-analysis/
├── src/
│   ├── scraper.py              # Google Business reviews scraper
│   ├── sentiment_analyzer.py   # Sentiment analysis module (extracted from notebook)
│   └── report_generator.py     # Excel report generation module
├── scripts/
│   ├── start_chrome.bat        # Windows batch script to start Chrome
│   ├── start_chrome.ps1        # PowerShell script to start Chrome
│   └── run_full_pipeline.py    # Complete automation pipeline
├── notebooks/
│   └── sentiment_analysis.ipynb # Jupyter notebook for analysis
├── data/
│   ├── arabic_names.csv        # Database of Arabic names for extraction
│   └── .gitkeep
├── assets/
│   ├── logo.png                # Brand logo for reports
│   └── screenshots/            # Documentation screenshots
├── output/
│   ├── reviews/                # Scraped reviews (Excel files)
│   ├── reports/                # Generated sentiment reports
│   └── .gitkeep
├── .github/
│   └── workflows/
│       └── python-app.yml      # GitHub Actions CI/CD
├── .gitignore
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── LICENSE                     # MIT License
└── CHANGELOG.md               # Version history

```

## 🚀 Installation

### Prerequisites

- **Python 3.8 or higher**
- **Google Chrome browser**
- **Google Business Profile** with access to reviews
- **PostgreSQL** (optional, for branch data integration)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/google-reviews-sentiment-analysis.git
cd google-reviews-sentiment-analysis
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Download NLTK Data (Required for Sentiment Analysis)

```python
python -c "import nltk; nltk.download('punkt'); nltk.download('vader_lexicon')"
```

## 🎯 Quick Start

### 1. Start Chrome with Remote Debugging

**Windows (PowerShell):**
```powershell
.\scripts\start_chrome.ps1
```

**Windows (Batch):**
```cmd
.\scripts\start_chrome.bat
```

### 2. Log into Google Business

1. Chrome will open automatically
2. Navigate to your Google Business Profile
3. Log in and navigate to the reviews page

### 3. Run the Scraper

```bash
python src/scraper.py
```

### 4. Analyze Sentiment

```bash
# Open Jupyter notebook
jupyter notebook notebooks/sentiment_analysis.ipynb

# Or run the full pipeline
python scripts/run_full_pipeline.py
```

## 📖 Usage

### 1. Scraping Reviews

The scraper connects to an existing Chrome session to bypass authentication:

```python
from src.scraper import GoogleReviewsScraper

# Initialize scraper
scraper = GoogleReviewsScraper(debugger_address="localhost:9222")

# Scrape reviews from the last 4 weeks
scraper.scrape_reviews(
    url="https://business.google.com/groups/YOUR_GROUP_ID/reviews",
    weeks=4,
    max_pages=50
)

# Save to Excel
scraper.save_to_excel()
```

**Key Parameters:**
- `weeks`: How many weeks back to scrape (default: 4)
- `max_pages`: Safety limit for pagination (default: 50)
- `debugger_address`: Chrome remote debugging address (default: localhost:9222)

### 2. Sentiment Analysis

The system performs dual-context sentiment analysis:

```python
# Salesman-related keywords
salesman_keywords = [
    'salesman', 'sales', 'staff', 'employee', 'service',
    'representative', 'helped', 'assist', 'friendly',
    'professional', 'rude', 'polite', 'customer service'
]

# Store-related keywords
store_keywords = [
    'store', 'shop', 'location', 'place', 'branch',
    'showroom', 'clean', 'organized', 'parking',
    'atmosphere', 'environment', 'products', 'quality'
]
```

**Sentiment Labels:**
- **Positive**: Compound score ≥ 0.05 (adjusted with star rating)
- **Negative**: Compound score ≤ -0.05 (adjusted with star rating)
- **Neutral**: Compound score between -0.05 and 0.05
- **No Context**: No relevant keywords found

### 3. Report Generation

Generate professional Excel reports with automatic color extraction:

```python
from src.report_generator import create_styled_workbook

# Prepare your data
workbook_data = {
    'شيت المدح والذم - 2025-11-27': (salesman_sentiment_df, 'primary'),
    '📊 أداء البائعين': (salesman_performance_df, 'primary'),
    '🏪 أداء الفروع': (store_performance_df, 'secondary'),
    '📝 جميع المراجعات': (all_reviews_df, 'primary'),
}

# Create report
create_styled_workbook(
    dataframes_dict=workbook_data,
    filename='تقرير_تحليل_المشاعر_2025-11-27.xlsx',
    logo_path='assets/logo.png'
)
```

## ⚙️ Configuration

### Chrome Remote Debugging Setup

The scraper uses Chrome's remote debugging protocol. Configure it in `start_chrome.ps1`:

```powershell
$profileDir = "C:\selenium\ChromeProfile"
$debugPort = 9222
```

### Database Connection (Optional)

For branch data integration, configure PostgreSQL connection:

```python
db_config = {
    "db_name": "your_database",
    "user": "postgres",
    "password": "your_password",
    "host": "192.168.1.143",
    "port": 5432
}
```

### Sentiment Analysis Tuning

Adjust sentiment thresholds in the analysis module:

```python
SENTIMENT_THRESHOLDS = {
    'positive': 0.05,
    'negative': -0.05,
    'star_weight': 0.1  # Weight for star rating adjustment
}
```

## 📊 Output Examples

### Excel Report Structure

**Sheet 1: شيت المدح والذم (Praise & Criticism)**
| اسم البائع | Positive | Negative | Neutral | No Context |
|------------|----------|----------|---------|------------|
| Ahmed      | 45       | 3        | 12      | 5          |
| Mohamed    | 38       | 5        | 8       | 3          |

**Sheet 2: 📊 أداء البائعين (Salesman Performance)**
- Detailed sentiment breakdown per salesman
- Star rating averages
- Review counts

**Sheet 3: 🏪 أداء الفروع (Store Performance)**
- Sentiment analysis per branch
- Location-based insights
- Cross-reference with salesmen

**Sheet 4: 📝 جميع المراجعات (All Reviews)**
- Full review text (Arabic & English)
- Sentiment scores
- Context extractions
- Timestamps and ratings

### Color Palette Extraction

The system automatically extracts colors from your logo:

```
✓ Extracted 8 colors from logo:
  Color 1: #2E9849 (Primary Green)
  Color 2: #279443 (Secondary Green)
  Color 3: #2D9B4A (Accent 1)
  Color 4: #289544 (Accent 2)
```

## 🔧 Advanced Features

### Custom Date Parsing

The scraper intelligently parses various date formats:

- "2 days ago"
- "1 week ago"
- "3 months ago"
- "Yesterday"
- Relative timestamps

### Salesman Name Extraction

Automatically identifies salesman names from reviews using fuzzy matching:

```python
def contains_arabic_name(review):
    for name in arabic_names_list:
        if name in review:
            return name
    return ''
```

### Multi-Language Support

- **Review Translation Detection**: Separates original Arabic text from Google-translated English
- **Bilingual Reports**: Column headers in both Arabic and English
- **RTL Support**: Proper rendering of Arabic text in Excel

## 🐛 Troubleshooting

### Chrome Connection Issues

**Problem**: Cannot connect to Chrome remote debugging

**Solution**:
```bash
# Kill all Chrome processes
taskkill /F /IM chrome.exe

# Restart Chrome with debugging
.\scripts\start_chrome.ps1
```

### Sentiment Analysis Errors

**Problem**: NLTK data not found

**Solution**:
```python
import nltk
nltk.download('vader_lexicon')
nltk.download('punkt')
```

### Excel Export Issues

**Problem**: Unicode errors in Arabic text

**Solution**:
- Ensure `openpyxl >= 3.1.0` is installed
- Use UTF-8 encoding when reading/writing files

### Database Connection Timeout

**Problem**: Cannot connect to PostgreSQL

**Solution**:
- Check firewall settings
- Verify PostgreSQL is running
- Test connection with: `psql -h 192.168.1.143 -U postgres`

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Coding Standards

- Follow PEP 8 style guide
- Add docstrings to all functions
- Include type hints where applicable
- Write unit tests for new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **VADER Sentiment Analysis**: [vaderSentiment](https://github.com/cjhutto/vaderSentiment)
- **Selenium WebDriver**: [selenium.dev](https://www.selenium.dev/)
- **OpenPyXL**: [openpyxl.readthedocs.io](https://openpyxl.readthedocs.io/)
- **Pillow (PIL)**: [pillow.readthedocs.io](https://pillow.readthedocs.io/)

## 📞 Support

For questions or support:
- Create an [Issue](https://github.com/yourusername/google-reviews-sentiment-analysis/issues)
- Email: your.email@example.com

## 🗺️ Roadmap

- [ ] **Dashboard**: Web-based visualization dashboard
- [ ] **Real-time Alerts**: Notification system for negative reviews
- [ ] **AI Integration**: GPT-4 for advanced sentiment analysis
- [ ] **Multi-platform**: Support for other review platforms (Yelp, TripAdvisor)
- [ ] **API**: RESTful API for integration with other systems
- [ ] **Docker**: Containerization for easy deployment

---

**Made with ❤️ for data-driven business insights**

**Star ⭐ this repository if you find it helpful!**
