"""
Configuration settings for the sentiment analysis system.

This module provides configuration using environment variables for security.
Use .env file to set sensitive values - never commit credentials to version control!
"""

import os
from pathlib import Path

# Try to load environment variables from .env file
try:
    from .env_manager import get_env_manager
    _env = get_env_manager()
except ImportError:
    # Fallback if env_manager not available
    _env = None
    import warnings
    warnings.warn("Environment manager not available, using defaults", UserWarning)


def get_env(key: str, default=None):
    """Get environment variable with fallback."""
    if _env:
        return _env.get(key, default)
    return os.getenv(key, default)


def get_env_int(key: str, default: int = 0) -> int:
    """Get environment variable as integer."""
    if _env:
        return _env.get_int(key, default)
    try:
        return int(os.getenv(key, default))
    except (ValueError, TypeError):
        return default


# Scraper Configuration
SCRAPER_CONFIG = {
    'debugger_address': get_env('CHROME_DEBUG_ADDRESS', 'localhost:9222'),
    'default_weeks': get_env_int('SCRAPING_WEEKS', 4),
    'max_pages': get_env_int('SCRAPING_MAX_PAGES', 50),
    'page_load_delay': get_env_int('SCRAPING_PAGE_DELAY', 3),
    'next_page_delay': get_env_int('SCRAPING_NEXT_PAGE_DELAY', 4),
}

# Chrome Configuration
CHROME_CONFIG = {
    'profile_dir': get_env('CHROME_PROFILE_DIR', r'C:\selenium\ChromeProfile'),
    'debug_port': get_env_int('CHROME_DEBUG_PORT', 9222),
    'chrome_paths': [
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
        os.path.join(os.getenv('LOCALAPPDATA', ''), 'Google\Chrome\Application\chrome.exe')
    ]
}

# Sentiment Analysis Configuration
SENTIMENT_CONFIG = {
    'positive_threshold': 0.05,
    'negative_threshold': -0.05,
    'star_weight': 0.1,
    'salesman_keywords': [
        'salesman', 'sales', 'staff', 'employee', 'service', 'representative',
        'helped', 'assist', 'friendly', 'professional', 'rude', 'polite',
        'customer service', 'agent', 'worker', 'team member', 'seller'
    ],
    'store_keywords': [
        'store', 'shop', 'location', 'place', 'branch', 'showroom', 'facility',
        'clean', 'organized', 'parking', 'atmosphere', 'environment', 'products',
        'inventory', 'selection', 'variety', 'quality', 'price', 'pricing',
        'building', 'area', 'space', 'display'
    ]
}

# Database Configuration (Optional)
# IMPORTANT: Set these in .env file, not here!
DB_CONFIG = {
    'db_name': get_env('DB_NAME', 'your_database'),
    'user': get_env('DB_USER', 'postgres'),
    'password': get_env('DB_PASSWORD', ''),  # NEVER hardcode passwords!
    'host': get_env('DB_HOST', 'localhost'),
    'port': get_env_int('DB_PORT', 5432)
}

# Report Configuration
REPORT_CONFIG = {
    'default_colors': {
        'primary': 'FF6B35',
        'secondary': '004E89',
        'accent1': 'F7B801',
        'accent2': '1B998B',
        'light_gray': 'F4F4F4',
        'medium_gray': 'E0E0E0',
        'dark_gray': '666666',
        'white': 'FFFFFF',
        'text_dark': '2C2C2C',
    },
    'logo_height': 60,  # pixels
    'title_row_height': 35,  # pixels
    'max_column_width': 50,
    'font_name': 'Segoe UI'
}

# File Paths
PATHS = {
    'data_dir': 'data',
    'output_dir': 'output',
    'assets_dir': 'assets',
    'reviews_dir': os.path.join('output', 'reviews'),
    'reports_dir': os.path.join('output', 'reports'),
    'arabic_names_file': os.path.join('data', 'arabic_names.csv'),
    'logo_file': os.path.join('assets', 'logo.png')
}
