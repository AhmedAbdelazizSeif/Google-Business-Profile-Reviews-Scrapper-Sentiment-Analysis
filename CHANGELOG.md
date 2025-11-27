# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Web-based dashboard for real-time monitoring
- API endpoints for integration with other systems
- Docker containerization
- Multi-platform support (Yelp, TripAdvisor)
- Automated email reports

## [2.0.0] - 2025-11-27

### Added
- **Automatic Color Palette Extraction** from brand logos using PIL
- **Multi-sheet Excel Reports** with professional styling
- **Arabic Language Support** for sheet names and column headers
- **Brand Color Integration** in report headers and tables
- **Frozen Panes** for better Excel navigation
- **Auto-adjusted Column Widths** for optimal readability
- **Alternating Row Colors** for improved visual comfort

### Changed
- Enhanced sentiment analysis with star rating integration
- Improved date parsing for various relative date formats
- Optimized Excel report generation performance
- Updated VADER sentiment thresholds for better accuracy

### Fixed
- Unicode encoding issues with Arabic text in Excel
- Date parsing errors for edge cases
- Pagination issues when reaching last page

## [1.5.0] - 2025-11-24

### Added
- **Dual-Context Sentiment Analysis**
  - Salesman-specific sentiment detection
  - Store-specific sentiment detection
- **Salesman Name Extraction** from review text using fuzzy matching
- **Database Integration** with PostgreSQL for branch data
- **Cross-Analysis Reports** (Store × Salesman, Salesman × Store)

### Changed
- Migrated from basic sentiment to VADER for improved accuracy
- Enhanced keyword detection for context extraction
- Improved review deduplication logic

## [1.0.0] - 2025-10-27

### Added
- **Google Business Reviews Scraper** using Selenium
- **Chrome Remote Debugging Connection** for authenticated sessions
- **Intelligent Pagination** with automatic page navigation
- **Time-based Filtering** (scrape reviews from last N weeks)
- **Excel Export** with timestamp-based filenames
- **Duplicate Detection** to avoid redundant data
- **Robust Error Handling** and retry mechanisms
- **PowerShell and Batch Scripts** for Chrome startup
- **Basic Sentiment Analysis** using TextBlob
- **Review Translation Detection** (Arabic ↔ English)

### Technical Details
- Initial release with core scraping functionality
- Support for Windows platform
- Command-line interface
- Excel output with basic formatting

## [0.1.0] - 2025-10-05

### Added
- Project initialization
- Basic project structure
- Initial requirements specification
- Proof of concept for web scraping

---

## Release Notes Template

### [Version] - YYYY-MM-DD

#### Added
- New features

#### Changed
- Changes in existing functionality

#### Deprecated
- Soon-to-be removed features

#### Removed
- Removed features

#### Fixed
- Bug fixes

#### Security
- Security updates
