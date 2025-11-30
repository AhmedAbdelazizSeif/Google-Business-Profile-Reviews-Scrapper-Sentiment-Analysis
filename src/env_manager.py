"""
Environment Configuration Manager

This module handles loading and validation of environment variables
from .env file with secure defaults and error handling.
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
import warnings


class EnvManager:
    """
    Manages environment variables with validation and secure defaults.
    
    Loads configuration from .env file and provides safe access to
    sensitive credentials and configuration values.
    """
    
    def __init__(self, env_file: str = '.env'):
        """
        Initialize environment manager.
        
        Args:
            env_file: Path to .env file (default: '.env')
        """
        self.env_file = env_file
        self.config = {}
        self._load_env()
        self._validate_required_vars()
    
    def _load_env(self):
        """Load environment variables from .env file."""
        env_path = Path(self.env_file)
        
        if not env_path.exists():
            warnings.warn(
                f"⚠️  .env file not found at {env_path}. "
                f"Copy .env.example to .env and configure your settings.",
                UserWarning
            )
            return
        
        # Parse .env file
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                
                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue
                
                # Parse KEY=VALUE
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Remove quotes if present
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    
                    # Set environment variable and store in config
                    os.environ[key] = value
                    self.config[key] = value
    
    def _validate_required_vars(self):
        """Validate that required environment variables are set."""
        required_vars = [
            'GOOGLE_BUSINESS_GROUP_ID',
        ]
        
        missing_vars = []
        for var in required_vars:
            if not self.get(var) or self.get(var) == f'YOUR_{var}' or 'YOUR_' in self.get(var, ''):
                missing_vars.append(var)
        
        if missing_vars:
            warnings.warn(
                f"⚠️  Missing or unconfigured environment variables: {', '.join(missing_vars)}\n"
                f"Please update your .env file with actual values.",
                UserWarning
            )
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get environment variable value.
        
        Args:
            key: Environment variable name
            default: Default value if not found
            
        Returns:
            Environment variable value or default
        """
        return os.environ.get(key, self.config.get(key, default))
    
    def get_int(self, key: str, default: int = 0) -> int:
        """Get environment variable as integer."""
        value = self.get(key, default)
        try:
            return int(value)
        except (ValueError, TypeError):
            return default
    
    def get_float(self, key: str, default: float = 0.0) -> float:
        """Get environment variable as float."""
        value = self.get(key, default)
        try:
            return float(value)
        except (ValueError, TypeError):
            return default
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get environment variable as boolean."""
        value = self.get(key, str(default)).lower()
        return value in ('true', '1', 'yes', 'on')
    
    def get_list(self, key: str, separator: str = ',', default: list = None) -> list:
        """Get environment variable as list."""
        if default is None:
            default = []
        
        value = self.get(key)
        if not value:
            return default
        
        return [item.strip() for item in value.split(separator)]
    
    def get_reviews_url(self) -> str:
        """
        Get Google Business reviews URL.
        
        Returns:
            Complete reviews URL
        """
        # Check if full URL is provided
        full_url = self.get('GOOGLE_REVIEWS_URL')
        if full_url:
            return full_url
        
        # Build URL from group ID
        group_id = self.get('GOOGLE_BUSINESS_GROUP_ID')
        if not group_id or 'YOUR_' in group_id:
            raise ValueError(
                "GOOGLE_BUSINESS_GROUP_ID not configured in .env file. "
                "Please set your actual Group ID."
            )
        
        return f"https://business.google.com/groups/{group_id}/reviews"
    
    def get_db_config(self) -> Dict[str, Any]:
        """
        Get database configuration.
        
        Returns:
            Dictionary with database settings
        """
        # Check for full DATABASE_URL first
        db_url = self.get('DATABASE_URL')
        if db_url:
            return {'database_url': db_url}
        
        # Build from individual settings
        return {
            'db_name': self.get('DB_NAME', 'postgres'),
            'user': self.get('DB_USER', 'postgres'),
            'password': self.get('DB_PASSWORD', ''),
            'host': self.get('DB_HOST', 'localhost'),
            'port': self.get_int('DB_PORT', 5432),
        }
    
    def get_chrome_config(self) -> Dict[str, Any]:
        """
        Get Chrome debugging configuration.
        
        Returns:
            Dictionary with Chrome settings
        """
        return {
            'debug_address': self.get('CHROME_DEBUG_ADDRESS', 'localhost:9222'),
            'profile_dir': self.get('CHROME_PROFILE_DIR', r'C:\selenium\ChromeProfile'),
            'debug_port': self.get_int('CHROME_DEBUG_PORT', 9222),
        }
    
    def get_scraping_config(self) -> Dict[str, Any]:
        """
        Get scraping configuration.
        
        Returns:
            Dictionary with scraping settings
        """
        return {
            'weeks': self.get_int('SCRAPING_WEEKS', 4),
            'max_pages': self.get_int('SCRAPING_MAX_PAGES', 50),
            'page_delay': self.get_int('SCRAPING_PAGE_DELAY', 3),
            'next_page_delay': self.get_int('SCRAPING_NEXT_PAGE_DELAY', 4),
        }
    
    def get_sentiment_config(self) -> Dict[str, Any]:
        """
        Get sentiment analysis configuration.
        
        Returns:
            Dictionary with sentiment settings
        """
        return {
            'positive_threshold': self.get_float('SENTIMENT_POSITIVE_THRESHOLD', 0.05),
            'negative_threshold': self.get_float('SENTIMENT_NEGATIVE_THRESHOLD', -0.05),
            'star_weight': self.get_float('SENTIMENT_STAR_WEIGHT', 0.1),
        }
    
    def is_feature_enabled(self, feature: str) -> bool:
        """
        Check if a feature is enabled.
        
        Args:
            feature: Feature name (e.g., 'DATABASE', 'EMAIL_NOTIFICATIONS')
            
        Returns:
            True if feature is enabled
        """
        return self.get_bool(f'ENABLE_{feature}', False)
    
    def mask_sensitive_value(self, value: str, show_chars: int = 4) -> str:
        """
        Mask sensitive value for logging.
        
        Args:
            value: Sensitive value to mask
            show_chars: Number of characters to show at end
            
        Returns:
            Masked value
        """
        if not value or len(value) <= show_chars:
            return '***'
        
        return '*' * (len(value) - show_chars) + value[-show_chars:]
    
    def print_config_summary(self, show_sensitive: bool = False):
        """
        Print configuration summary.
        
        Args:
            show_sensitive: Whether to show sensitive values (default: False)
        """
        print("=" * 80)
        print("CONFIGURATION SUMMARY")
        print("=" * 80)
        
        # Google Business
        print("\n[Google Business Profile]")
        group_id = self.get('GOOGLE_BUSINESS_GROUP_ID', 'NOT SET')
        print(f"  Group ID: {self.mask_sensitive_value(group_id) if not show_sensitive else group_id}")
        
        # Chrome
        print("\n[Chrome Debugging]")
        chrome_config = self.get_chrome_config()
        print(f"  Debug Address: {chrome_config['debug_address']}")
        print(f"  Profile Dir: {chrome_config['profile_dir']}")
        
        # Scraping
        print("\n[Scraping Settings]")
        scraping_config = self.get_scraping_config()
        print(f"  Weeks to scrape: {scraping_config['weeks']}")
        print(f"  Max pages: {scraping_config['max_pages']}")
        
        # Database
        if self.is_feature_enabled('DATABASE'):
            print("\n[Database]")
            db_config = self.get_db_config()
            if 'database_url' in db_config:
                print(f"  URL: {self.mask_sensitive_value(db_config['database_url'])}")
            else:
                print(f"  Host: {db_config['host']}:{db_config['port']}")
                print(f"  Database: {db_config['db_name']}")
                print(f"  User: {db_config['user']}")
        
        # Features
        print("\n[Enabled Features]")
        features = ['DATABASE', 'EMAIL_NOTIFICATIONS', 'AUTO_BACKUP']
        for feature in features:
            status = '✓' if self.is_feature_enabled(feature) else '✗'
            print(f"  {status} {feature}")
        
        print("\n" + "=" * 80)


# Global instance
_env_manager = None


def get_env_manager() -> EnvManager:
    """
    Get global EnvManager instance (singleton pattern).
    
    Returns:
        EnvManager instance
    """
    global _env_manager
    if _env_manager is None:
        _env_manager = EnvManager()
    return _env_manager


# Convenience functions
def get_env(key: str, default: Any = None) -> Any:
    """Get environment variable."""
    return get_env_manager().get(key, default)


def get_reviews_url() -> str:
    """Get Google Business reviews URL."""
    return get_env_manager().get_reviews_url()


def get_db_config() -> Dict[str, Any]:
    """Get database configuration."""
    return get_env_manager().get_db_config()


# Example usage
if __name__ == "__main__":
    # Initialize environment manager
    env = EnvManager()
    
    # Print configuration summary
    env.print_config_summary(show_sensitive=False)
    
    # Example: Get specific values
    print("\n" + "=" * 80)
    print("EXAMPLE VALUE ACCESS")
    print("=" * 80)
    
    try:
        reviews_url = env.get_reviews_url()
        print(f"\nReviews URL: {reviews_url}")
    except ValueError as e:
        print(f"\n⚠️  {e}")
    
    print(f"\nScraping weeks: {env.get_int('SCRAPING_WEEKS', 4)}")
    print(f"Max pages: {env.get_int('SCRAPING_MAX_PAGES', 50)}")
    print(f"Database enabled: {env.is_feature_enabled('DATABASE')}")
