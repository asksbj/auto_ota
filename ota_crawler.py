"""
OTA Web Crawler using Selenium
This crawler visits OTA websites and searches for available rooms based on given dates.
"""

import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
import json


class OTACrawler:
    """
    A flexible web crawler for Online Travel Agency (OTA) websites.
    Supports searching for hotel rooms with customizable parameters.
    """
    
    def __init__(self, headless=False, timeout=10):
        """
        Initialize the crawler with browser settings.
        
        Args:
            headless (bool): Run browser in headless mode (no GUI)
            timeout (int): Default timeout for element waits in seconds
        """
        self.timeout = timeout
        self.driver = self._setup_driver(headless)
        self.wait = WebDriverWait(self.driver, timeout)
        
    def _setup_driver(self, headless):
        """Configure Chrome WebDriver."""
        chrome_options = Options()
        
        if headless:
            chrome_options.add_argument('--headless')
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36')
        
        # ✨ 让 Selenium 自动处理 ChromeDriver（Selenium 4.6+）
        print("Setting up ChromeDriver...")
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()
        print("✓ ChromeDriver ready!")
        return driver
    
    def search_booking_com(self, destination, check_in, check_out, adults=2, rooms=1):
        """
        Search for available rooms on Booking.com
        
        Args:
            destination (str): City or hotel name to search
            check_in (str): Check-in date in format 'YYYY-MM-DD'
            check_out (str): Check-out date in format 'YYYY-MM-DD'
            adults (int): Number of adults
            rooms (int): Number of rooms
            
        Returns:
            list: List of available rooms with details
        """
        print(f"Searching Booking.com for {destination}")
        print(f"Check-in: {check_in}, Check-out: {check_out}")
        
        try:
            # Navigate to Booking.com
            self.driver.get("https://www.booking.com")
            time.sleep(2)
            
            # Close any popup/cookie banner
            self._handle_popups()
            
            # Enter destination
            destination_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "ss"))
            )
            destination_input.clear()
            destination_input.send_keys(destination)
            time.sleep(1)
            
            # Click first autocomplete suggestion
            try:
                first_result = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "li[data-i='0']"))
                )
                first_result.click()
            except:
                destination_input.send_keys(Keys.ENTER)
            
            time.sleep(1)
            
            # Select dates
            self._select_dates_booking(check_in, check_out)
            
            # Configure guests and rooms
            self._configure_occupancy_booking(adults, rooms)
            
            # Click search button
            search_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
            )
            search_button.click()
            
            print("Waiting for search results...")
            time.sleep(5)
            
            # Extract room results
            results = self._extract_results_booking()
            
            return results
            
        except Exception as e:
            print(f"Error during search: {str(e)}")
            self._take_screenshot("error_screenshot")
            return []
    
    def search_generic_ota(self, url, selectors, destination, check_in, check_out):
        """
        Generic search function for other OTA websites.
        
        Args:
            url (str): OTA website URL
            selectors (dict): CSS selectors for different elements
            destination (str): Search destination
            check_in (str): Check-in date
            check_out (str): Check-out date
            
        Returns:
            list: Search results
        """
        print(f"Searching {url} for {destination}")
        
        try:
            self.driver.get(url)
            time.sleep(2)
            
            self._handle_popups()
            
            # Enter destination
            if 'destination' in selectors:
                dest_input = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selectors['destination']))
                )
                dest_input.clear()
                dest_input.send_keys(destination)
                time.sleep(1)
            
            # Handle dates (implementation depends on site structure)
            # This is a template - customize based on specific OTA
            
            # Click search
            if 'search_button' in selectors:
                search_btn = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selectors['search_button']))
                )
                search_btn.click()
            
            time.sleep(5)
            
            # Extract results based on provided selectors
            return self._extract_generic_results(selectors)
            
        except Exception as e:
            print(f"Error: {str(e)}")
            return []
    
    def _select_dates_booking(self, check_in, check_out):
        """Select check-in and check-out dates on Booking.com"""
        try:
            # Click on date input to open calendar
            date_button = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='date-display-field-start']")
            date_button.click()
            time.sleep(1)
            
            # Parse dates
            checkin_date = datetime.strptime(check_in, '%Y-%m-%d')
            checkout_date = datetime.strptime(check_out, '%Y-%m-%d')
            
            # Select check-in date
            checkin_selector = f"span[data-date='{check_in}']"
            checkin_element = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, checkin_selector))
            )
            checkin_element.click()
            time.sleep(0.5)
            
            # Select check-out date
            checkout_selector = f"span[data-date='{check_out}']"
            checkout_element = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, checkout_selector))
            )
            checkout_element.click()
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error selecting dates: {str(e)}")
    
    def _configure_occupancy_booking(self, adults, rooms):
        """Configure number of adults and rooms on Booking.com"""
        try:
            # Click occupancy selector
            occupancy_button = self.driver.find_element(
                By.CSS_SELECTOR, "[data-testid='occupancy-config']"
            )
            occupancy_button.click()
            time.sleep(1)
            
            # This is a simplified version - actual implementation may need
            # to handle adding/removing adults and rooms with +/- buttons
            
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error configuring occupancy: {str(e)}")
    
    def _extract_results_booking(self):
        """Extract hotel results from Booking.com search results page"""
        results = []
        
        try:
            # Wait for results to load
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='property-card']"))
            )
            
            # Find all property cards
            property_cards = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='property-card']")
            
            print(f"Found {len(property_cards)} properties")
            
            for idx, card in enumerate(property_cards[:10]):  # Limit to first 10
                try:
                    result = {}
                    
                    # Extract hotel name
                    try:
                        name_element = card.find_element(By.CSS_SELECTOR, "[data-testid='title']")
                        result['name'] = name_element.text
                    except:
                        result['name'] = "N/A"
                    
                    # Extract price
                    try:
                        price_element = card.find_element(By.CSS_SELECTOR, "[data-testid='price-and-discounted-price']")
                        result['price'] = price_element.text
                    except:
                        result['price'] = "N/A"
                    
                    # Extract rating
                    try:
                        rating_element = card.find_element(By.CSS_SELECTOR, "[data-testid='review-score']")
                        result['rating'] = rating_element.text
                    except:
                        result['rating'] = "N/A"
                    
                    # Extract location
                    try:
                        location_element = card.find_element(By.CSS_SELECTOR, "[data-testid='address']")
                        result['location'] = location_element.text
                    except:
                        result['location'] = "N/A"
                    
                    results.append(result)
                    
                except Exception as e:
                    print(f"Error extracting data from card {idx}: {str(e)}")
                    continue
            
        except TimeoutException:
            print("Timeout waiting for results to load")
        except Exception as e:
            print(f"Error extracting results: {str(e)}")
        
        return results
    
    def _extract_generic_results(self, selectors):
        """Extract results using custom selectors"""
        results = []
        
        try:
            if 'result_card' in selectors:
                cards = self.driver.find_elements(By.CSS_SELECTOR, selectors['result_card'])
                
                for card in cards[:10]:
                    result = {}
                    
                    for key, selector in selectors.items():
                        if key != 'result_card':
                            try:
                                element = card.find_element(By.CSS_SELECTOR, selector)
                                result[key] = element.text
                            except:
                                result[key] = "N/A"
                    
                    results.append(result)
        
        except Exception as e:
            print(f"Error extracting generic results: {str(e)}")
        
        return results
    
    def _handle_popups(self):
        """Close common popups like cookie banners"""
        popup_selectors = [
            "button[aria-label='Dismiss sign-in info.']",
            "button.fc-button.fc-cta-consent",
            "button#onetrust-accept-btn-handler",
            "[aria-label='Close']",
            ".modal-close"
        ]
        
        for selector in popup_selectors:
            try:
                popup = self.driver.find_element(By.CSS_SELECTOR, selector)
                popup.click()
                time.sleep(0.5)
                print(f"Closed popup: {selector}")
            except:
                continue
    
    def _take_screenshot(self, filename):
        """Take a screenshot for debugging"""
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            filepath = os.path.join(base_dir, f"{filename}.png")
            self.driver.save_screenshot(filepath)
            print(f"Screenshot saved: {filepath}")
        except Exception as e:
            print(f"Failed to take screenshot: {str(e)}")
    
    def save_results(self, results, filename="results.json"):
        """Save results to JSON file in project directory"""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(base_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"Results saved to {filepath}")
        return filepath
    
    def close(self):
        """Close the browser and clean up"""
        if self.driver:
            self.driver.quit()
            print("Browser closed")


def main():
    """Example usage of the OTA crawler"""
    
    # Initialize crawler
    crawler = OTACrawler(headless=False, timeout=15)
    
    try:
        # Example 1: Search Booking.com
        destination = "New York"
        check_in = "2025-12-01"
        check_out = "2025-12-05"
        
        results = crawler.search_booking_com(
            destination=destination,
            check_in=check_in,
            check_out=check_out,
            adults=2,
            rooms=1
        )
        
        # Display results
        print("\n" + "="*60)
        print(f"SEARCH RESULTS FOR {destination.upper()}")
        print("="*60)
        
        for idx, hotel in enumerate(results, 1):
            print(f"\n{idx}. {hotel.get('name', 'N/A')}")
            print(f"   Price: {hotel.get('price', 'N/A')}")
            print(f"   Rating: {hotel.get('rating', 'N/A')}")
            print(f"   Location: {hotel.get('location', 'N/A')}")
        
        # Save results
        if results:
            crawler.save_results(results, "booking_results.json")
        
    except Exception as e:
        print(f"Error in main: {str(e)}")
    
    finally:
        # Clean up
        crawler.close()


if __name__ == "__main__":
    main()
