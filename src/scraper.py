"""
Google Business Reviews Scraper
Connects to an existing Chrome session to scrape reviews from Google Business Profile
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import csv
from datetime import datetime, timedelta
import re
import pandas as pd


class GoogleReviewsScraper:
    def __init__(self, debugger_address="localhost:9222"):
        """
        Initialize the scraper with connection to existing Chrome session
        
        Args:
            debugger_address: Chrome debugger address (default: localhost:9222)
        """
        self.debugger_address = debugger_address
        self.driver = None
        self.reviews = []
        
    def connect_to_chrome(self):
        """Connect to existing Chrome session"""
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", self.debugger_address)
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            print(f"✓ Connected to Chrome session at {self.debugger_address}")
            return True
        except Exception as e:
            print(f"✗ Failed to connect to Chrome: {e}")
            print("\nMake sure Chrome is running with remote debugging enabled:")
            print('  chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\selenium\\ChromeProfile"')
            return False
    
    def navigate_to_reviews(self, url):
        """Navigate to the reviews page"""
        try:
            self.driver.get(url)
            print(f"✓ Navigated to: {url}")
            time.sleep(3)  # Wait for page to load
            return True
        except Exception as e:
            print(f"✗ Failed to navigate: {e}")
            return False
    
    def parse_review_date(self, date_text):
        """
        Parse review date text and return datetime object
        
        Args:
            date_text: Date string from review (e.g., "2 days ago", "1 week ago")
        """
        now = datetime.now()
        date_text_lower = date_text.lower()
        
        # Handle various date formats
        if "min" in date_text_lower or "minute" in date_text_lower:
            match = re.search(r'\d+', date_text)
            if match:
                minutes = int(match.group())
                return now - timedelta(minutes=minutes)
            else:
                # "a minute ago" or similar
                return now - timedelta(minutes=1)
        elif "hour" in date_text_lower:
            match = re.search(r'\d+', date_text)
            if match:
                hours = int(match.group())
                return now - timedelta(hours=hours)
            else:
                # "an hour ago" or similar
                return now - timedelta(hours=1)
        elif "yesterday" in date_text_lower:
            return now - timedelta(days=1)
        elif "day" in date_text_lower:
            match = re.search(r'\d+', date_text)
            if match:
                days = int(match.group())
                return now - timedelta(days=days)
            else:
                # "a day ago" or similar
                return now - timedelta(days=1)
        elif "week" in date_text_lower:
            match = re.search(r'\d+', date_text)
            if match:
                weeks = int(match.group())
                return now - timedelta(weeks=weeks)
            else:
                # "a week ago" or similar
                return now - timedelta(weeks=1)
        elif "month" in date_text_lower:
            match = re.search(r'\d+', date_text)
            if match:
                months = int(match.group())
                return now - timedelta(days=months * 30)
            else:
                # "a month ago" or similar
                return now - timedelta(days=30)
        
        # If we can't parse the date, return None instead of now
        return None
    
    def is_within_timeframe(self, date_text, weeks=4):
        """Check if review date is within specified weeks"""
        review_date = self.parse_review_date(date_text)
        if review_date is None:
            # If we can't parse the date, assume it's too old to be safe
            return False
        cutoff_date = datetime.now() - timedelta(weeks=weeks)
        return review_date >= cutoff_date
    
    def is_older_than_timeframe(self, date_text, weeks=4):
        """Check if review date is older than specified weeks"""
        review_date = self.parse_review_date(date_text)
        if review_date is None:
            # If we can't parse the date, assume it's old
            return True
        cutoff_date = datetime.now() - timedelta(weeks=weeks)
        return review_date < cutoff_date
    
    def extract_review_data(self, review_container):
        """Extract all data from a single review container"""
        try:
            # Extract full review text (class: oiQd1c)
            review_text = "N/A"
            try:
                # Find all review text elements (there might be multiple)
                review_text_elements = review_container.find_elements(By.CLASS_NAME, "oiQd1c")
                
                if review_text_elements:
                    # Try to get text using JavaScript to capture hidden content
                    review_text = self.driver.execute_script(
                        "return arguments[0].textContent;", 
                        review_text_elements[0]
                    )
                    # Fallback to .text if textContent is empty
                    if not review_text or review_text.strip() == "":
                        review_text = review_text_elements[0].text
                
                # If still no text found, try alternate approach
                if not review_text or review_text.strip() == "":
                    review_text = "N/A"
            except NoSuchElementException:
                pass
            
            # Extract store code (class: mjZtse wjs4p)
            store_code = "N/A"
            try:
                store_code_element = review_container.find_element(By.CSS_SELECTOR, ".mjZtse.wjs4p")
                store_code = store_code_element.text
            except NoSuchElementException:
                pass
            
            # Extract review date (class: Wxf3Bf wUfJz)
            review_date = "Unknown"
            try:
                date_element = review_container.find_element(By.CSS_SELECTOR, ".Wxf3Bf.wUfJz")
                review_date = date_element.text
            except NoSuchElementException:
                pass
            
            # Extract star rating (parent: YMWsEc dv8URd, children: DPvwYc L12a3c z3FsAc)
            stars = 0
            try:
                star_container = review_container.find_element(By.CSS_SELECTOR, ".YMWsEc.dv8URd")
                filled_stars = star_container.find_elements(By.CSS_SELECTOR, ".DPvwYc.L12a3c.z3FsAc")
                stars = len(filled_stars)
            except NoSuchElementException:
                pass
            
            # Extract reviewer name (class: z2S9Hc)
            reviewer_name = "N/A"
            try:
                reviewer_element = review_container.find_element(By.CLASS_NAME, "z2S9Hc")
                reviewer_name = reviewer_element.text
            except NoSuchElementException:
                pass
            
            store_code = re.findall(r'\b[A-Z0-9]{4,}\b', store_code)[0] if re.findall(r'\b[A-Z0-9]{4,}\b', store_code) else "N/A"
            return {
                "review_text": review_text,
                "store_code": store_code,
                "review_date": review_date,
                "stars": stars,
                "reviewer_name": reviewer_name,
                "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            print(f"  Warning: Could not extract data from review container: {e}")
            return None
    
    def scrape_reviews(self, url, weeks=4, max_pages=50):
        """
        Scrape reviews from Google Business Profile
        
        Args:
            url: Google Business reviews URL
            weeks: Number of weeks to go back (default: 4)
            max_pages: Maximum number of pages to scrape (safety limit)
        """
        if not self.connect_to_chrome():
            return False
        
        if not self.navigate_to_reviews(url):
            return False
        
        page_count = 0
        total_reviews = 0
        reviews_in_timeframe = 0
        
        print(f"\n⚙ Starting to scrape reviews (looking back {weeks} weeks)...\n")
        
        while page_count < max_pages:
            page_count += 1
            print(f"📄 Processing page {page_count}...")
            
            # Wait for reviews to load
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "DsOcnf"))
                )
            except TimeoutException:
                print("  ⚠ No reviews found on this page")
                break
            
            # Find ALL review containers on the current page (class: DsOcnf)
            review_containers = self.driver.find_elements(By.CLASS_NAME, "DsOcnf")
            
            if not review_containers:
                print("  ⚠ No review containers found on this page")
                break
            
            print(f"  Found {len(review_containers)} review containers")
            
            page_reviews = 0
            stop_scraping = False
            old_reviews_count = 0
            
            # Process each review container
            for review_container in review_containers:
                review_data = self.extract_review_data(review_container)
                
                if review_data:
                    total_reviews += 1
                    
                    # Check if review is older than timeframe
                    if self.is_older_than_timeframe(review_data["review_date"], weeks):
                        old_reviews_count += 1
                        print(f"  ⏸ Found review from '{review_data['review_date']}' - older than {weeks} weeks")
                        # If we find 3 consecutive old reviews, stop scraping
                        if old_reviews_count >= 3:
                            print(f"  ⏸ Found {old_reviews_count} consecutive reviews older than {weeks} weeks, stopping...")
                            stop_scraping = True
                            break
                    # Check if review is within timeframe
                    elif self.is_within_timeframe(review_data["review_date"], weeks):
                        self.reviews.append(review_data)
                        reviews_in_timeframe += 1
                        page_reviews += 1
                        old_reviews_count = 0  # Reset counter if we find a recent review
            
            print(f"  ✓ Extracted {page_reviews} reviews from this page (Total in timeframe: {reviews_in_timeframe})")
            
            if stop_scraping:
                break
            
            # Try to click next page button
            try:
                next_button = self.driver.find_element(By.CLASS_NAME, 
                    "VfPpkd-Bz112c-LgbsSe.yHy1rc.eT1oJ.QDwDD.mN1ivc.vX5N7b")
                
                if next_button.is_enabled() and next_button.is_displayed():
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                    time.sleep(1)
                    next_button.click()
                    print("  → Moving to next page...")
                    time.sleep(4)  # Wait 4 seconds for next page to load
                else:
                    print("  ℹ No more pages available")
                    break
            except NoSuchElementException:
                print("  ℹ Pagination button not found, reached last page")
                break
            except Exception as e:
                print(f"  ⚠ Could not navigate to next page: {e}")
                break
        
        print(f"\n✓ Scraping completed!")
        print(f"  - Total reviews found: {total_reviews}")
        print(f"  - Reviews within {weeks} weeks: {reviews_in_timeframe}")
        print(f"  - Pages processed: {page_count}")
        
        return True
    
    def save_to_excel(self, filename=None):
        """Save scraped reviews to Excel file with timestamp"""
        if not self.reviews:
            print("No reviews to save")
            return False
        
        try:
            # Generate filename with timestamp if not provided
            if filename is None:
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = fr"C:\Users\aseif\Jupyter\scraps\google_reviews\google_reviews_{timestamp}.xlsx"
            
            # Convert reviews to DataFrame
            df = pd.DataFrame(self.reviews)
            
            # Reorder columns
            column_order = ['review_date', 'stars', 'store_code', 'reviewer_name', 'review_text']
            df = df[column_order]

            # Split review_text into English and Arabic, handling cases where '(Original)' is not present
            df["English Review"] = df["review_text"].str.split('(Translated by Google)').str[2].str.strip()
            df["Arabic Review"] = df["review_text"].str.split('(Translated by Google)').str[0].str.replace('(Original)', '').str.strip()
            df.drop_duplicates(subset=["review_text", "reviewer_name", "review_date"], inplace=True)
            # Save to Excel
            df.to_excel(filename, index=False, engine='openpyxl')
            
            print(f"\n✓ Reviews saved to: {filename}")
            return True
        except Exception as e:
            print(f"✗ Failed to save Excel: {e}")
            return False
    
    def close(self):
        """Close the browser connection (optional - keeps Chrome open)"""
        if self.driver:
            # Don't close the browser, just disconnect
            self.driver.quit()
            print("\n✓ Disconnected from Chrome session")


def main():
    try:
        # Configuration
        REVIEWS_URL = "https://business.google.com/groups/112241629083201481462/reviews"
        WEEKS_TO_SCRAPE = 1 # Look back 1 year (approximately 52 weeks)
        
        # Initialize scraper
        scraper = GoogleReviewsScraper()
        
        # Scrape reviews
        success = scraper.scrape_reviews(REVIEWS_URL, weeks=WEEKS_TO_SCRAPE)

        
        if success and scraper.reviews:

            
            # Save to Excel with timestamp filename
            scraper.save_to_excel()
            
            # Print sample of reviews
            print("\n" + "="*80)
            print("SAMPLE REVIEWS:")
            print("="*80)
            for i, review in enumerate(scraper.reviews[:3], 1):
                print(f"\n#{i}")
                print(f"Store: {review['store_code']}")
                print(f"Date: {review['review_date']}")
                print(f"Stars: {review['stars']}/5")
                print(f"Reviewer: {review['reviewer_name']}")
                print(f"Review: {review['review_text'][:200]}...")
    except KeyboardInterrupt:
        scraper.save_to_excel()
        
        # Optional: Uncomment to disconnect from Chrome
        # scraper.close()


if __name__ == "__main__":
    main()
