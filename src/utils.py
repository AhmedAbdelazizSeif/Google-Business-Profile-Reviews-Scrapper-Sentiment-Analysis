"""
Utility functions for the sentiment analysis system.
"""

import re
from datetime import datetime, timedelta
from typing import Optional, List


def parse_relative_date(date_text: str) -> Optional[datetime]:
    """
    Parse relative date strings (e.g., '2 days ago') to datetime objects.
    
    Args:
        date_text: Relative date string
        
    Returns:
        Datetime object or None if parsing fails
    """
    now = datetime.now()
    date_text_lower = date_text.lower()
    
    # Handle various date formats
    if "min" in date_text_lower or "minute" in date_text_lower:
        match = re.search(r'\d+', date_text)
        minutes = int(match.group()) if match else 1
        return now - timedelta(minutes=minutes)
    
    elif "hour" in date_text_lower:
        match = re.search(r'\d+', date_text)
        hours = int(match.group()) if match else 1
        return now - timedelta(hours=hours)
    
    elif "yesterday" in date_text_lower:
        return now - timedelta(days=1)
    
    elif "day" in date_text_lower:
        match = re.search(r'\d+', date_text)
        days = int(match.group()) if match else 1
        return now - timedelta(days=days)
    
    elif "week" in date_text_lower:
        match = re.search(r'\d+', date_text)
        weeks = int(match.group()) if match else 1
        return now - timedelta(weeks=weeks)
    
    elif "month" in date_text_lower:
        match = re.search(r'\d+', date_text)
        months = int(match.group()) if match else 1
        return now - timedelta(days=months * 30)
    
    return None


def clean_review_text(text: str) -> str:
    """
    Clean and normalize review text.
    
    Args:
        text: Raw review text
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters (keep basic punctuation)
    text = re.sub(r'[^\w\s.,!?;:()\-]', '', text)
    
    return text.strip()


def extract_store_code(text: str) -> Optional[str]:
    """
    Extract store code from text using pattern matching.
    
    Args:
        text: Text containing store code
        
    Returns:
        Store code or None if not found
    """
    # Look for alphanumeric codes (4+ characters)
    matches = re.findall(r'\b[A-Z0-9]{4,}\b', text)
    return matches[0] if matches else None


def split_arabic_english_review(review_text: str) -> tuple:
    """
    Split review into Arabic original and English translation.
    
    Args:
        review_text: Full review text with translations
        
    Returns:
        Tuple of (arabic_text, english_text)
    """
    if '(Translated by Google)' in review_text:
        parts = review_text.split('(Translated by Google)')
        
        arabic_part = parts[0].replace('(Original)', '').strip() if len(parts) > 0 else ""
        english_part = parts[2].strip() if len(parts) > 2 else ""
        
        return arabic_part, english_part
    
    return review_text, ""


def validate_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email: Email string to validate
        
    Returns:
        True if valid email format
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def format_number(num: float, decimals: int = 2) -> str:
    """
    Format number with specified decimal places.
    
    Args:
        num: Number to format
        decimals: Number of decimal places
        
    Returns:
        Formatted number string
    """
    return f"{num:.{decimals}f}"


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


# Example usage
if __name__ == "__main__":
    # Test date parsing
    print("Date Parsing Tests:")
    test_dates = ["2 days ago", "1 week ago", "yesterday", "3 months ago"]
    for date_str in test_dates:
        parsed = parse_relative_date(date_str)
        print(f"  {date_str} -> {parsed}")
    
    # Test review splitting
    print("\nReview Splitting Test:")
    sample_review = "(Original) الخدمة ممتازة (Translated by Google) The service is excellent"
    arabic, english = split_arabic_english_review(sample_review)
    print(f"  Arabic: {arabic}")
    print(f"  English: {english}")
