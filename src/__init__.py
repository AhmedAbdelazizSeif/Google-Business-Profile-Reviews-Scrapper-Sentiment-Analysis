"""
Google Reviews Sentiment Analysis System

A comprehensive system for scraping, analyzing, and reporting on
Google Business reviews with bilingual support.
"""

__version__ = "2.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .scraper import GoogleReviewsScraper
from .sentiment_analyzer import SentimentAnalyzer
from .report_generator import ReportGenerator

__all__ = [
    'GoogleReviewsScraper',
    'SentimentAnalyzer',
    'ReportGenerator',
]
