"""
Configuration settings for the sentiment analysis system.
"""

import os

# Scraper Configuration
SCRAPER_CONFIG = {
    'debugger_address': 'localhost:9222',
    'default_weeks': 4,
    'max_pages': 50,
    'page_load_delay': 3,  # seconds
    'next_page_delay': 4,  # seconds
}

# Chrome Configuration
CHROME_CONFIG = {
    'profile_dir': r'C:\selenium\ChromeProfile',
    'debug_port': 9222,
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
DB_CONFIG = {
    'db_name': 'your_database',
    'user': 'postgres',
    'password': 'your_password',  # Change in production!
    'host': '192.168.1.143',
    'port': 5432
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
