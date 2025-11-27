"""
Full Pipeline Automation Script

This script runs the complete pipeline:
1. Scrape reviews from Google Business
2. Analyze sentiment
3. Generate Excel reports
"""

import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.scraper import GoogleReviewsScraper
from src.sentiment_analyzer import SentimentAnalyzer, extract_salesman_name
from src.report_generator import ReportGenerator
import pandas as pd


def main():
    """Run the complete analysis pipeline."""
    
    print("="*80)
    print("GOOGLE REVIEWS SENTIMENT ANALYSIS PIPELINE")
    print("="*80)
    
    # Configuration
    REVIEWS_URL = "https://business.google.com/groups/YOUR_GROUP_ID/reviews"
    WEEKS_TO_SCRAPE = 4
    LOGO_PATH = os.path.join('assets', 'logo.png')
    NAMES_FILE = os.path.join('data', 'arabic_names.csv')
    
    # Step 1: Scrape Reviews
    print("\n[1/3] Scraping reviews...")
    scraper = GoogleReviewsScraper()
    
    success = scraper.scrape_reviews(REVIEWS_URL, weeks=WEEKS_TO_SCRAPE)
    
    if not success or not scraper.reviews:
        print("✗ Scraping failed or no reviews found")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(scraper.reviews)
    print(f"✓ Scraped {len(df)} reviews")
    
    # Step 2: Sentiment Analysis
    print("\n[2/3] Analyzing sentiment...")
    analyzer = SentimentAnalyzer()
    
    # Analyze sentiments
    df = analyzer.analyze_dataframe(df, text_column='review_text')
    
    # Extract salesman names if file exists
    if os.path.exists(NAMES_FILE):
        names_df = pd.read_csv(NAMES_FILE)
        names_list = names_df['english_name'].tolist()
        df['salesman_name'] = df['review_text'].apply(
            lambda x: extract_salesman_name(x, names_list)
        )
    
    # Print summary
    summary = analyzer.get_summary_statistics(df)
    print(f"✓ Sentiment Analysis Complete")
    print(f"  - Salesman Sentiment: {summary['salesman_sentiment_distribution']}")
    print(f"  - Store Sentiment: {summary['store_sentiment_distribution']}")
    
    # Step 3: Generate Reports
    print("\n[3/3] Generating Excel reports...")
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Prepare data for reports
    if 'salesman_name' in df.columns:
        salesman_summary = df.groupby('salesman_name')['salesman_sentiment'].value_counts().unstack(fill_value=0).reset_index()
    else:
        salesman_summary = pd.DataFrame()
    
    # Create report
    generator = ReportGenerator(logo_path=LOGO_PATH if os.path.exists(LOGO_PATH) else None)
    
    workbook_data = {
        f'شيت المدح والذم - {today}': (salesman_summary, 'primary') if not salesman_summary.empty else (df, 'primary'),
        '📝 All Reviews': (df[['review_date', 'stars', 'review_text', 'salesman_sentiment', 'store_sentiment']], 'secondary')
    }
    
    output_file = os.path.join('output', 'reports', f'sentiment_report_{today}.xlsx')
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    generator.create_workbook(workbook_data, output_file)
    
    print("\n" + "="*80)
    print("✓ PIPELINE COMPLETE")
    print(f"  - Reviews analyzed: {len(df)}")
    print(f"  - Report saved: {output_file}")
    print("="*80)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Pipeline interrupted by user")
    except Exception as e:
        print(f"\n✗ Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
