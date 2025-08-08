"""
Delta Flight Search Automation Script
=====================================
This script automates flight search on Delta's website using Selenium WebDriver.
"""

import time
import os
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains


class DeltaFlightAutomation:
    def __init__(self, headless=False, timeout=30):
        """
        Initialize the Delta Flight Automation
        
        Args:
            headless (bool): Run browser in headless mode
            timeout (int): Default timeout for WebDriverWait
        """
        self.timeout = timeout
        self.driver = None
        self.wait = None
        self.setup_driver(headless)
        
    def setup_driver(self, headless=False):
        """Setup Chrome WebDriver with optimal configurations"""
        try:
            chrome_options = Options()
            
            # Basic options for stability
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Window size and user agent
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            if headless:
                chrome_options.add_argument("--headless")
            
            # Initialize driver
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.wait = WebDriverWait(self.driver, self.timeout)
            
            print("✅ Chrome WebDriver initialized successfully")
            
        except Exception as e:
            print(f"❌ Error setting up WebDriver: {e}")
            raise
    
    def safe_click(self, element_locator, timeout=None):
        """
        Safely click an element with multiple retry strategies
        
        Args:
            element_locator: Tuple of (By, locator_string)
            timeout: Custom timeout for this element
        """
        timeout = timeout or self.timeout
        
        strategies = [
            self._click_when_clickable,
            self._click_with_js,
            self._click_with_actions
        ]
        
        for i, strategy in enumerate(strategies, 1):
            try:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located(element_locator)
                )
                strategy(element)
                print(f"✅ Successfully clicked element using strategy {i}")
                return True
            except Exception as e:
                print(f"⚠️ Strategy {i} failed: {e}")
                if i == len(strategies):
                    print(f"❌ All click strategies failed for {element_locator}")
                    return False
                continue
        return False
    
    def _click_when_clickable(self, element):
        """Strategy 1: Wait for element to be clickable"""
        clickable_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(element)
        )
        clickable_element.click()
    
    def _click_with_js(self, element):
        """Strategy 2: Click using JavaScript"""
        self.driver.execute_script("arguments[0].click();", element)
    
    def _click_with_actions(self, element):
        """Strategy 3: Click using ActionChains"""
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click().perform()
    
    def safe_send_keys(self, element_locator, text, clear_first=True, timeout=None):
        """
        Safely send keys to an element
        
        Args:
            element_locator: Tuple of (By, locator_string)
            text: Text to send
            clear_first: Clear field before typing
            timeout: Custom timeout
        """
        timeout = timeout or self.timeout
        
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(element_locator)
            )
            
            if clear_first:
                element.clear()
            
            element.send_keys(text)
            print(f"✅ Successfully sent '{text}' to element")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send keys to {element_locator}: {e}")
            return False
    
    def wait_for_element(self, element_locator, timeout=None, condition="presence"):
        """
        Wait for element with different conditions
        
        Args:
            element_locator: Tuple of (By, locator_string)
            timeout: Custom timeout
            condition: Type of condition ('presence', 'visible', 'clickable')
        """
        timeout = timeout or self.timeout
        
        conditions = {
            "presence": EC.presence_of_element_located,
            "visible": EC.visibility_of_element_located,
            "clickable": EC.element_to_be_clickable
        }
        
        try:
            element = WebDriverWait(self.driver, timeout).until(
                conditions[condition](element_locator)
            )
            print(f"✅ Element found with {condition} condition")
            return element
        except TimeoutException:
            print(f"❌ Timeout waiting for element {element_locator} with {condition} condition")
            return None
    
    def navigate_to_delta(self):
        """Navigate to Delta flight search page"""
        try:
            print("🔄 Navigating to Delta flight search...")
            self.driver.get("https://www.delta.com/flightsearch/book-a-flight")
            
            # Wait for page to load
            self.wait_for_element((By.TAG_NAME, "body"), timeout=20)
            time.sleep(2)  # Additional wait for dynamic content
            self.driver.get("https://www.delta.com/flightsearch/book-a-flight")
            self.wait_for_element((By.TAG_NAME, "body"), timeout=20)
            time.sleep(3)  # Additional wait for dynamic content
            
            print("✅ Successfully navigated to Delta website")
            return True
            
        except Exception as e:
            print(f"❌ Failed to navigate to Delta website: {e}")
            return False
    
    def select_from_airport(self, airport_code):
        """
        Select departure airport
        
        Args:
            airport_code (str): 3-letter airport code (e.g., 'DEL')
        """
        try:
            print(f"🔄 Selecting departure airport: {airport_code}")
            
            # Click on 'From' field
            from_xpath = "//div[contains(@class, 'departure-airport')]//a[1] | //a[contains(@aria-label, 'From')]"
            if not self.safe_click((By.XPATH, from_xpath)):
                # Fallback xpath
                from_xpath = "/html/body/idp-root/div/div[2]/idp-advance-search/div/div[1]/div[2]/idp-book-widget/div/ngc-book/div[1]/div/form/div[1]/div/div[1]/div[1]/div[1]/div[1]/a[1]"
                self.safe_click((By.XPATH, from_xpath))
            
            time.sleep(2)
            
            # Enter airport code
            input_xpath = "//input[contains(@placeholder, 'airport') or contains(@class, 'airport')] | //input[@type='text']"
            if not self.safe_send_keys((By.XPATH, input_xpath), airport_code):
                # Fallback xpath
                input_xpath = "/html/body/idp-root/div/div[1]/ngc-global-nav/header/modal-container/div/div/ngc-airport-lookup-modal/div/div[2]/tabset/div/tab/div/div/div[1]/input"
                self.safe_send_keys((By.XPATH, input_xpath), airport_code)
            
            time.sleep(2)
            
            # Click first suggestion
            suggestion_xpath = "//li[1] | //div[contains(@class, 'airport-option')][1]"
            if not self.safe_click((By.XPATH, suggestion_xpath)):
                # Fallback xpath
                suggestion_xpath = "/html/body/idp-root/div/div[1]/ngc-global-nav/header/modal-container/div/div/ngc-airport-lookup-modal/div/div[2]/tabset/div/tab/div/div/div[2]/div/ul/li[1]"
                self.safe_click((By.XPATH, suggestion_xpath))
            
            print(f"✅ Successfully selected departure airport: {airport_code}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to select departure airport {airport_code}: {e}")
            return False
    
    def select_to_airport(self, airport_code):
        """
        Select destination airport
        
        Args:
            airport_code (str): 3-letter airport code (e.g., 'BCN')
        """
        try:
            print(f"🔄 Selecting destination airport: {airport_code}")
            
            # Click on 'To' field
            to_xpath = "//div[contains(@class, 'arrival-airport')]//a[1] | //a[contains(@aria-label, 'To')]"
            if not self.safe_click((By.XPATH, to_xpath)):
                # Fallback xpath
                to_xpath = "/html/body/idp-root/div/div[2]/idp-advance-search/div/div[1]/div[2]/idp-book-widget/div/ngc-book/div[1]/div/form/div[1]/div/div[1]/div[1]/div[1]/div[1]/a[2]"
                self.safe_click((By.XPATH, to_xpath))
            
            time.sleep(2)
            
            # Enter airport code
            input_xpath = "//input[contains(@placeholder, 'airport') or contains(@class, 'airport')] | //input[@type='text']"
            if not self.safe_send_keys((By.XPATH, input_xpath), airport_code):
                # Fallback xpath
                input_xpath = "/html/body/idp-root/div/div[1]/ngc-global-nav/header/modal-container/div/div/ngc-airport-lookup-modal/div/div[2]/tabset/div/tab/div/div/div[1]/input"
                self.safe_send_keys((By.XPATH, input_xpath), airport_code)
            
            time.sleep(2)
            
            # Click first suggestion
            suggestion_xpath = "//li[1] | //div[contains(@class, 'airport-option')][1]"
            if not self.safe_click((By.XPATH, suggestion_xpath)):
                # Fallback xpath
                suggestion_xpath = "/html/body/idp-root/div/div[1]/ngc-global-nav/header/modal-container/div/div/ngc-airport-lookup-modal/div/div[2]/tabset/div/tab/div/div/div[2]/div"
                self.safe_click((By.XPATH, suggestion_xpath))
            
            print(f"✅ Successfully selected destination airport: {airport_code}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to select destination airport {airport_code}: {e}")
            return False
    
    def select_trip_type(self, trip_type="one_way"):
        """
        Select trip type
        
        Args:
            trip_type (str): 'round_trip', 'one_way', or 'multi_city'
        """
        try:
            print(f"🔄 Selecting trip type: {trip_type}")
            
            # Click trip type dropdown
            dropdown_xpath = "//span[contains(@class, 'trip-type')] | //div[contains(@class, 'trip-type')]"
            if not self.safe_click((By.XPATH, dropdown_xpath)):
                # Fallback xpath
                dropdown_xpath = "/html/body/idp-root/div/div[2]/idp-advance-search/div/div[1]/div[2]/idp-book-widget/div/ngc-book/div[1]/div/form/div[1]/div/div[1]/div[1]/div[2]/span/span[1]"
                self.safe_click((By.XPATH, dropdown_xpath))
            
            time.sleep(1)
            
            # Select option based on trip type
            trip_options = {
                "round_trip": "//li[1] | //span[contains(text(), 'Round')]",
                "one_way": "//li[2] | //span[contains(text(), 'One')]",
                "multi_city": "//li[3] | //span[contains(text(), 'Multi')]"
            }
            
            if trip_type in trip_options:
                option_xpath = trip_options[trip_type]
                if not self.safe_click((By.XPATH, option_xpath)):
                    # Fallback xpath based on trip type
                    fallback_xpaths = {
                        "round_trip": "/html/body/idp-root/div/div[2]/idp-advance-search/div/div[1]/div[2]/idp-book-widget/div/ngc-book/div[1]/div/form/div[1]/div/div[1]/div[1]/div[2]/span/span[2]/ul/li[1]",
                        "one_way": "/html/body/idp-root/div/div[2]/idp-advance-search/div/div[1]/div[2]/idp-book-widget/div/ngc-book/div[1]/div/form/div[1]/div/div[1]/div[1]/div[2]/span/span[2]/ul/li[2]",
                        "multi_city": "/html/body/idp-root/div/div[2]/idp-advance-search/div/div[1]/div[2]/idp-book-widget/div/ngc-book/div[1]/div/form/div[1]/div/div[1]/div[1]/div[2]/span/span[2]/ul/li[3]"
                    }
                    self.safe_click((By.XPATH, fallback_xpaths[trip_type]))
            
            print(f"✅ Successfully selected trip type: {trip_type}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to select trip type {trip_type}: {e}")
            return False
    
    def select_departure_date(self, date_str="09/24/25"):
        """
        Select departure date
        
        Args:
            date_str (str): Date in MM/DD/YY format
        """
        try:
            print(f"🔄 Selecting departure date: {date_str}")
            
            # Parse the date
            date_obj = datetime.strptime(date_str, "%m/%d/%y")
            target_day = date_obj.day
            target_month = date_obj.month
            target_year = date_obj.year
            
            # Click departure date field
            date_xpath = "//div[contains(@class, 'depart')] | //input[contains(@placeholder, 'Depart')]"
            if not self.safe_click((By.XPATH, date_xpath)):
                # Fallback xpath
                date_xpath = "/html/body/idp-root/div/div[2]/idp-advance-search/div/div[1]/div[2]/idp-book-widget/div/ngc-book/div[1]/div/form/div[1]/div/div[1]/div[1]/div[3]/date-selection-view/div/div/div/div/div[2]"
                self.safe_click((By.XPATH, date_xpath))
            
            time.sleep(2)
            
            # Navigate to correct month if needed
            current_date = datetime.now()
            months_diff = (target_year - current_date.year) * 12 + (target_month - current_date.month)
            
            if months_diff > 0:
                next_button_xpath = "//button[contains(@class, 'next')] | //button[contains(@aria-label, 'next')]"
                for _ in range(months_diff):
                    self.safe_click((By.XPATH, next_button_xpath))
                    time.sleep(1)
            elif months_diff < 0:
                prev_button_xpath = "//button[contains(@class, 'prev')] | //button[contains(@aria-label, 'prev')]"
                for _ in range(abs(months_diff)):
                    self.safe_click((By.XPATH, prev_button_xpath))
                    time.sleep(1)
            
            # Select the specific date
            day_xpath = f"//td[@aria-label='{target_day}' or contains(@aria-label, '{target_day}')]//button | //button[text()='{target_day}'] | //td[text()='{target_day}']"
            if not self.safe_click((By.XPATH, day_xpath)):
                # Try alternative selectors
                day_xpath = f"//td[contains(@class, 'available') and contains(text(), '{target_day}')]"
                self.safe_click((By.XPATH, day_xpath))
            
            time.sleep(1)
            
            # Click Done button
            done_xpath = "//button[contains(text(), 'Done') or contains(@class, 'done')]"
            if not self.safe_click((By.XPATH, done_xpath)):
                # Fallback xpath
                done_xpath = "/html/body/idp-root/div/div[2]/idp-advance-search/div/div[1]/div[2]/idp-book-widget/div/ngc-book/div[1]/div/form/div[1]/div/div[1]/div[1]/div[3]/date-selection-view/div/div/div/div/div[4]/div/div[3]/button[2]"
                self.safe_click((By.XPATH, done_xpath))
            
            print(f"✅ Successfully selected departure date: {date_str}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to select departure date {date_str}: {e}")
            return False
    
    def search_flights(self):
        """Click search button to find flights"""
        try:
            print("🔄 Searching for flights...")
            
            # Click search button
            search_xpath = "//button[contains(text(), 'Search') or contains(@class, 'search')]"
            if not self.safe_click((By.XPATH, search_xpath)):
                # Fallback xpath
                search_xpath = "/html/body/idp-root/div/div[2]/idp-advance-search/div/div[1]/div[2]/idp-book-widget/div/ngc-book/div[1]/div/form/div[2]/div/div[2]/div[2]/button"
                self.safe_click((By.XPATH, search_xpath))
            
            print("✅ Search initiated successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to initiate search: {e}")
            return False
    
    def wait_for_results(self, timeout=60):
        """Wait for flight results to load"""
        try:
            print("🔄 Waiting for flight results...")
            
            # Wait for results container
            results_selector = (By.CSS_SELECTOR, "div.flight-results-grid.mach-flight-results-grid.ng-star-inserted")
            results_element = self.wait_for_element(results_selector, timeout=timeout)
            
            if results_element:
                # Additional wait for results to fully populate
                time.sleep(5)
                print("✅ Flight results loaded successfully")
                return True
            else:
                print("❌ Flight results did not load within timeout")
                return False
                
        except Exception as e:
            print(f"❌ Error waiting for results: {e}")
            return False
    
    def dump_html(self, filename="flight_results.html"):
        """
        Save current page HTML to file
        
        Args:
            filename (str): Name of output file
        """
        try:
            # Create dumps directory if it doesn't exist
            dumps_dir = "html_dumps"
            if not os.path.exists(dumps_dir):
                os.makedirs(dumps_dir)
            
            filepath = os.path.join(dumps_dir, filename)
            
            # Get page source and save
            html_content = self.driver.page_source
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"✅ HTML dumped successfully to: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ Failed to dump HTML: {e}")
            return None
    
    def click_price_tab(self):
        """Click on the price tab to see different pricing options"""
        try:
            print("🔄 Clicking price tab...")
            
            # Click on price/tabs button
            price_tab_xpath = "//button[contains(@class, 'tab')] | //button[2]"
            if not self.safe_click((By.XPATH, price_tab_xpath)):
                # Fallback xpath
                price_tab_xpath = "/html/body/idp-root/div/div[2]/idp-search-results/div/div[2]/idp-search-results-head/div/div[1]/div[2]/idp-shopping-price-in-tabs/div/idp-show-price-in-tabs/mach-global-tabs/div/div[2]/button[2]"
                self.safe_click((By.XPATH, price_tab_xpath))
            
            # Wait for new results to load
            time.sleep(5)
            
            print("✅ Successfully clicked price tab")
            return True
            
        except Exception as e:
            print(f"❌ Failed to click price tab: {e}")
            return False
    
    def run_automation(self, from_airport="DEL", to_airport="BCN", trip_type="one_way", date="09/24/25"):
        """
        Run the complete automation process
        
        Args:
            from_airport (str): Departure airport code
            to_airport (str): Destination airport code
            trip_type (str): Type of trip
            date (str): Departure date
        """
        try:
            print("🚀 Starting Delta Flight Automation")
            print(f"📋 Search Parameters:")
            print(f"   From: {from_airport}")
            print(f"   To: {to_airport}")
            print(f"   Trip Type: {trip_type}")
            print(f"   Date: {date}")
            print("-" * 50)
            
            # Step 1: Navigate to Delta
            if not self.navigate_to_delta():
                return False
            
            # Step 2: Select from airport
            if not self.select_from_airport(from_airport):
                return False
            
            # Step 3: Select to airport
            if not self.select_to_airport(to_airport):
                return False
            
            # Step 4: Select trip type
            if not self.select_trip_type(trip_type):
                return False
            
            # Step 5: Select departure date
            if not self.select_departure_date(date):
                return False
            
            # Step 6: Search flights
            if not self.search_flights():
                return False
            
            # Step 7: Wait for results
            if not self.wait_for_results():
                return False
            
            # Step 8: Dump first results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            first_dump = f"flight_results_initial_{timestamp}.html"
            self.dump_html(first_dump)
            
            # Step 9: Click price tab
            if self.click_price_tab():
                # Step 10: Dump second results
                second_dump = f"flight_results_price_tab_{timestamp}.html"
                self.dump_html(second_dump)
            
            print("🎉 Automation completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Automation failed: {e}")
            return False
    
    def close(self):
        """Close the browser and cleanup"""
        try:
            if self.driver:
                self.driver.quit()
                print("✅ Browser closed successfully")
        except Exception as e:
            print(f"⚠️ Error closing browser: {e}")


def main():
    """Main function to run the automation"""
    # Configuration
    config = {
        "from_airport": "DEL",  # Delhi
        "to_airport": "BCN",    # Barcelona  
        "trip_type": "one_way", # one_way, round_trip, multi_city
        "date": "09/24/25",     # MM/DD/YY format
        "headless": False       # Set to True for headless mode
    }
    
    automation = None
    
    try:
        # Initialize automation
        automation = DeltaFlightAutomation(headless=config["headless"])
        
        # Run automation
        success = automation.run_automation(
            from_airport=config["from_airport"],
            to_airport=config["to_airport"],
            trip_type=config["trip_type"],
            date=config["date"]
        )
        
        if success:
            print("\n🎯 All tasks completed successfully!")
            print("📁 Check the 'html_dumps' folder for saved HTML files")
        else:
            print("\n❌ Automation completed with errors")
            
    except KeyboardInterrupt:
        print("\n⏹️ Automation stopped by user")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
    finally:
        # Always cleanup
        if automation:
            automation.close()


if __name__ == "__main__":
    main()
