"""
Sentiment Analysis Module

This module provides sentiment analysis functionality for Google Business reviews,
including context-aware analysis for both salesman and store-related sentiments.
"""

import pandas as pd
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from typing import Dict, List, Optional


class SentimentAnalyzer:
    """
    Analyzes sentiment in customer reviews using VADER sentiment analysis.
    
    Provides dual-context analysis:
    - Salesman-specific sentiment (staff, service quality)
    - Store-specific sentiment (location, cleanliness, products)
    """
    
    # Keywords to identify salesman-related context
    SALESMAN_KEYWORDS = [
        'salesman', 'sales', 'staff', 'employee', 'service', 'representative',
        'helped', 'assist', 'friendly', 'professional', 'rude', 'polite',
        'customer service', 'agent', 'worker', 'team member', 'seller'
    ]
    
    # Keywords to identify store-related context
    STORE_KEYWORDS = [
        'store', 'shop', 'location', 'place', 'branch', 'showroom', 'facility',
        'clean', 'organized', 'parking', 'atmosphere', 'environment', 'products',
        'inventory', 'selection', 'variety', 'quality', 'price', 'pricing',
        'building', 'area', 'space', 'display'
    ]
    
    # Sentiment thresholds
    POSITIVE_THRESHOLD = 0.05
    NEGATIVE_THRESHOLD = -0.05
    STAR_WEIGHT = 0.1  # Weight for star rating adjustment
    
    def __init__(self):
        """Initialize the sentiment analyzer with VADER."""
        self.vader = SentimentIntensityAnalyzer()
    
    def extract_context_sentences(self, text: str, keywords: List[str]) -> str:
        """
        Extract sentences containing specific keywords from review text.
        
        Args:
            text: The review text to analyze
            keywords: List of keywords to search for
            
        Returns:
            String containing all sentences with matching keywords
        """
        if pd.isna(text) or text == '':
            return ''
        
        sentences = re.split(r'[.!?]+', str(text))
        context_sentences = []
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(keyword in sentence_lower for keyword in keywords):
                context_sentences.append(sentence.strip())
        
        return ' '.join(context_sentences)
    
    def get_sentiment_score(self, text: str) -> float:
        """
        Calculate sentiment score using VADER.
        
        Args:
            text: Text to analyze
            
        Returns:
            Compound sentiment score between -1 and 1
        """
        if not text or text == '':
            return 0
        
        scores = self.vader.polarity_scores(text)
        return scores['compound']
    
    def label_sentiment(self, score: float) -> str:
        """
        Convert sentiment score to categorical label.
        
        Args:
            score: Sentiment score (or empty string for no context)
            
        Returns:
            Sentiment label: 'positive', 'negative', 'neutral', or 'No Context'
        """
        if score == '' or score == 0:
            return 'No Context'
        
        if score >= self.POSITIVE_THRESHOLD:
            return 'positive'
        elif score <= self.NEGATIVE_THRESHOLD:
            return 'negative'
        else:
            return 'neutral'
    
    def analyze_review(
        self, 
        review_text: str, 
        stars: Optional[int] = None
    ) -> Dict[str, any]:
        """
        Perform comprehensive sentiment analysis on a review.
        
        Args:
            review_text: The review text to analyze
            stars: Star rating (1-5), used to adjust sentiment scores
            
        Returns:
            Dictionary containing:
                - salesman_context: Extracted salesman-related text
                - salesman_score: Salesman sentiment score
                - salesman_sentiment: Salesman sentiment label
                - store_context: Extracted store-related text
                - store_score: Store sentiment score
                - store_sentiment: Store sentiment label
        """
        # Extract contexts
        salesman_context = self.extract_context_sentences(
            review_text, self.SALESMAN_KEYWORDS
        )
        store_context = self.extract_context_sentences(
            review_text, self.STORE_KEYWORDS
        )
        
        # Calculate base sentiment scores
        salesman_score = self.get_sentiment_score(salesman_context)
        store_score = self.get_sentiment_score(store_context)
        
        # Adjust scores based on star rating if provided
        if stars is not None:
            star_adjustment = (stars - 3) * self.STAR_WEIGHT
            salesman_score += star_adjustment
            store_score += star_adjustment
        
        # Label sentiments
        salesman_sentiment = self.label_sentiment(salesman_score)
        store_sentiment = self.label_sentiment(store_score)
        
        return {
            'salesman_context': salesman_context,
            'salesman_score': salesman_score,
            'salesman_sentiment': salesman_sentiment,
            'store_context': store_context,
            'store_score': store_score,
            'store_sentiment': store_sentiment
        }
    
    def analyze_dataframe(
        self, 
        df: pd.DataFrame, 
        text_column: str = 'English Review',
        stars_column: str = 'stars'
    ) -> pd.DataFrame:
        """
        Analyze sentiment for all reviews in a DataFrame.
        
        Args:
            df: DataFrame containing reviews
            text_column: Name of column containing review text
            stars_column: Name of column containing star ratings
            
        Returns:
            DataFrame with added sentiment analysis columns
        """
        results = []
        
        for idx, row in df.iterrows():
            review_text = row[text_column] if text_column in row else ''
            stars = row[stars_column] if stars_column in row else None
            
            analysis = self.analyze_review(review_text, stars)
            results.append(analysis)
        
        # Add results to DataFrame
        result_df = pd.DataFrame(results)
        return pd.concat([df, result_df], axis=1)
    
    def get_summary_statistics(self, df: pd.DataFrame) -> Dict[str, any]:
        """
        Generate summary statistics for sentiment analysis results.
        
        Args:
            df: DataFrame with sentiment analysis results
            
        Returns:
            Dictionary containing summary statistics
        """
        return {
            'salesman_sentiment_distribution': 
                df['salesman_sentiment'].value_counts().to_dict(),
            'store_sentiment_distribution': 
                df['store_sentiment'].value_counts().to_dict(),
            'average_salesman_score': 
                df['salesman_score'].mean(),
            'average_store_score': 
                df['store_score'].mean(),
            'total_reviews': len(df)
        }


def extract_salesman_name(review_text: str, names_list: List[str]) -> str:
    """
    Extract salesman name from review text using name matching.
    
    Args:
        review_text: The review text to search
        names_list: List of known salesman names
        
    Returns:
        Matched name or empty string if none found
    """
    for name in names_list:
        if name.lower() in review_text.lower():
            return name
    return ''


# Example usage
if __name__ == "__main__":
    # Initialize analyzer
    analyzer = SentimentAnalyzer()
    
    # Example review
    sample_review = """
    The store was very clean and well-organized. The salesman Ahmed was 
    extremely helpful and professional. Great experience overall!
    """
    
    # Analyze single review
    result = analyzer.analyze_review(sample_review, stars=5)
    
    print("Sentiment Analysis Results:")
    print(f"Salesman Sentiment: {result['salesman_sentiment']}")
    print(f"Store Sentiment: {result['store_sentiment']}")
    print(f"\nSalesman Context: {result['salesman_context']}")
    print(f"Store Context: {result['store_context']}")
