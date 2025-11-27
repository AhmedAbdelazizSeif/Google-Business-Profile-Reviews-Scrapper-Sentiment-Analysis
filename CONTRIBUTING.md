# Contributing to Google Reviews Sentiment Analysis System

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project adheres to a code of conduct that all contributors are expected to follow. Please be respectful and constructive in all interactions.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/google-reviews-sentiment-analysis.git
   cd google-reviews-sentiment-analysis
   ```
3. **Add the upstream repository**:
   ```bash
   git remote add upstream https://github.com/ORIGINAL_OWNER/google-reviews-sentiment-analysis.git
   ```

## Development Setup

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install development dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If available
   ```

3. **Install pre-commit hooks** (if available):
   ```bash
   pre-commit install
   ```

## How to Contribute

### Reporting Bugs

Before creating a bug report:
- **Check existing issues** to avoid duplicates
- **Collect relevant information**:
  - OS version
  - Python version
  - Package versions
  - Error messages and stack traces
  - Steps to reproduce

Create a bug report with:
- **Clear title** describing the issue
- **Detailed description** of the problem
- **Steps to reproduce** the bug
- **Expected vs. actual behavior**
- **Screenshots** if applicable
- **Environment details**

### Suggesting Enhancements

Enhancement suggestions are welcome! Please include:
- **Clear use case** for the enhancement
- **Detailed description** of the proposed feature
- **Potential implementation approach**
- **Benefits** to users or developers

### Contributing Code

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following our coding standards

3. **Test your changes** thoroughly

4. **Commit your changes** with clear messages

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request** on GitHub

## Coding Standards

### Python Style Guide

Follow [PEP 8](https://pep8.org/) style guide:

```python
# Good
def extract_sentiment(review_text: str, keywords: list) -> dict:
    """
    Extract sentiment from review text based on keywords.
    
    Args:
        review_text: The text to analyze
        keywords: List of keywords to look for
        
    Returns:
        Dictionary containing sentiment score and label
    """
    # Implementation here
    pass

# Bad
def ext_sent(txt,kw):
    pass
```

### Key Principles

1. **Use descriptive variable names**:
   ```python
   # Good
   total_positive_reviews = 45
   
   # Bad
   tpr = 45
   ```

2. **Add docstrings** to all functions and classes:
   ```python
   def scrape_reviews(url: str, weeks: int = 4) -> List[dict]:
       """
       Scrape reviews from Google Business Profile.
       
       Args:
           url: Google Business reviews URL
           weeks: Number of weeks to look back (default: 4)
           
       Returns:
           List of dictionaries containing review data
           
       Raises:
           ConnectionError: If cannot connect to Chrome
           ValueError: If URL is invalid
       """
       pass
   ```

3. **Use type hints**:
   ```python
   from typing import List, Dict, Optional
   
   def process_reviews(
       reviews: List[Dict[str, any]], 
       sentiment_threshold: float = 0.5
   ) -> pd.DataFrame:
       pass
   ```

4. **Keep functions small and focused**:
   - Each function should do one thing well
   - Aim for functions under 50 lines
   - Extract complex logic into separate functions

5. **Handle errors gracefully**:
   ```python
   try:
       result = scrape_reviews(url)
   except ConnectionError as e:
       logger.error(f"Failed to connect: {e}")
       return None
   except Exception as e:
       logger.exception(f"Unexpected error: {e}")
       raise
   ```

### File Organization

```python
# Standard library imports
import os
import re
from datetime import datetime
from typing import List, Dict

# Third-party imports
import pandas as pd
from selenium import webdriver

# Local imports
from src.utils import parse_date
from src.config import SCRAPER_CONFIG
```

## Testing Guidelines

### Writing Tests

1. **Create test files** in the `tests/` directory:
   ```
   tests/
   ├── test_scraper.py
   ├── test_sentiment_analyzer.py
   └── test_report_generator.py
   ```

2. **Use pytest** for testing:
   ```python
   import pytest
   from src.scraper import GoogleReviewsScraper
   
   def test_date_parsing():
       scraper = GoogleReviewsScraper()
       result = scraper.parse_review_date("2 days ago")
       assert result is not None
       assert isinstance(result, datetime)
   
   def test_sentiment_analysis():
       from src.sentiment_analyzer import analyze_sentiment
       
       positive_review = "Excellent service! Very friendly staff."
       result = analyze_sentiment(positive_review)
       assert result['label'] == 'positive'
       assert result['score'] > 0.5
   ```

3. **Run tests**:
   ```bash
   pytest tests/
   pytest tests/ -v  # Verbose output
   pytest tests/test_scraper.py  # Specific file
   ```

### Test Coverage

Aim for high test coverage:
```bash
pytest --cov=src tests/
```

## Documentation

### Code Documentation

- **Add docstrings** to all public functions and classes
- **Use Google-style docstrings**:
  ```python
  def calculate_sentiment_score(text: str, keywords: List[str]) -> float:
      """
      Calculate sentiment score for given text.
      
      This function uses VADER sentiment analysis combined with
      keyword matching to determine the sentiment score.
      
      Args:
          text: Review text to analyze
          keywords: List of keywords to look for
          
      Returns:
          Float between -1 and 1 representing sentiment score
          
      Raises:
          ValueError: If text is empty or None
          
      Examples:
          >>> calculate_sentiment_score("Great service!", ["service"])
          0.85
      """
      pass
  ```

### README Updates

When adding new features:
- Update the README.md with usage examples
- Add to the features list
- Update the configuration section if needed

## Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples**:
```
feat(scraper): add support for multi-page scraping

- Implement automatic pagination
- Add configurable max_pages parameter
- Handle timeout errors gracefully

Closes #123
```

```
fix(sentiment): correct VADER threshold values

Previously, neutral sentiment was incorrectly classified
as positive. Updated thresholds to match documentation.

Fixes #456
```

### Commit Best Practices

- Write clear, concise commit messages
- Use present tense ("add feature" not "added feature")
- Limit first line to 72 characters
- Reference issues and PRs when applicable
- Make atomic commits (one logical change per commit)

## Pull Request Process

### Before Submitting

1. **Update your fork**:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run tests** and ensure they pass:
   ```bash
   pytest tests/
   ```

3. **Check code style**:
   ```bash
   flake8 src/
   black src/ --check
   ```

4. **Update documentation** if needed

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] All tests pass
- [ ] Added new tests for new features
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-reviewed code
- [ ] Commented complex code
- [ ] Updated documentation
- [ ] No new warnings
- [ ] Added tests
- [ ] All tests pass
```

### Review Process

1. **Automated checks** run on PR submission
2. **Code review** by maintainers
3. **Address feedback** and make requested changes
4. **Approval** and merge by maintainer

## Questions?

If you have questions:
- Check existing [Issues](https://github.com/yourusername/google-reviews-sentiment-analysis/issues)
- Create a new issue with the "question" label
- Reach out to maintainers

Thank you for contributing! 🎉
