"""
Enhanced Delta Flight Automation with WebDriver Manager
======================================================
This version automatically manages ChromeDriver installation
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
from webdriver_manager.chrome import ChromeDriverManager


class DeltaFlightAutomationAdvanced:
    def __init__(self, headless=False, timeout=30):
        """
        Initialize the Delta Flight Automation with WebDriver Manager
        
        Args:
            headless (bool): Run browser in headless mode
            timeout (int): Default timeout for WebDriverWait
        """
        self.timeout = timeout
        self.driver = None
        self.wait = None
        self.setup_driver(headless)
        
    def setup_driver(self, headless=False):
        """Setup Chrome WebDriver with automatic driver management"""
        try:
            print("🔄 Setting up ChromeDriver...")
            
            chrome_options = Options()
            
            # Basic options for stability
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Performance optimizations
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins")
            chrome_options.add_argument("--disable-images")  # Faster loading
            chrome_options.add_argument("--disable-javascript")  # Remove if JS is needed for clicks
            
            # Window size and user agent
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            if headless:
                chrome_options.add_argument("--headless")
            
            # Use WebDriver Manager to automatically download and manage ChromeDriver
            service = Service(ChromeDriverManager().install())
            
            # Initialize driver
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.wait = WebDriverWait(self.driver, self.timeout)
            
            print("✅ Chrome WebDriver initialized successfully with WebDriver Manager")
            
        except Exception as e:
            print(f"❌ Error setting up WebDriver: {e}")
            print("💡 Make sure Chrome browser is installed on your system")
            raise
    
    def smart_wait_and_click(self, selectors, timeout=None, description="element"):
        """
        Smart function to try multiple selectors and click strategies
        
        Args:
            selectors (list): List of tuples (By, selector_string)
            timeout: Custom timeout
            description: Description for logging
        """
        timeout = timeout or self.timeout
        
        for i, (by, selector) in enumerate(selectors, 1):
            try:
                print(f"🔍 Trying selector {i}/{len(selectors)} for {description}")
                
                # Wait for element to be present
                element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((by, selector))
                )
                
                # Try different click strategies
                click_methods = [
                    lambda el: WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(el)).click(),
                    lambda el: self.driver.execute_script("arguments[0].click();", el),
                    lambda el: ActionChains(self.driver).move_to_element(el).click().perform(),
                    lambda el: el.click()
                ]
                
                for j, click_method in enumerate(click_methods, 1):
                    try:
                        click_method(element)
                        print(f"✅ Successfully clicked {description} using selector {i}, method {j}")
                        return True
                    except Exception as click_error:
                        print(f"⚠️ Click method {j} failed: {click_error}")
                        continue
                        
            except Exception as e:
                print(f"⚠️ Selector {i} failed for {description}: {e}")
                continue
        
        print(f"❌ All selectors failed for {description}")
        return False
    
    def smart_send_keys(self, selectors, text, description="field"):
        """
        Smart function to send keys to elements with multiple selector fallbacks
        """
        for i, (by, selector) in enumerate(selectors, 1):
            try:
                element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((by, selector))
                )
                
                element.clear()
                element.send_keys(text)
                print(f"✅ Successfully sent '{text}' to {description} using selector {i}")
                return True
                
            except Exception as e:
                print(f"⚠️ Selector {i} failed for {description}: {e}")
                continue
        
        print(f"❌ All selectors failed for {description}")
        return False
    
    def navigate_to_delta(self):
        """Navigate to Delta flight search page"""
        try:
            print("🔄 Navigating to Delta flight search...")
            self.driver.get("https://www.delta.com/flightsearch/book-a-flight")
            
            # Wait for page to load completely
            WebDriverWait(self.driver, 30).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            time.sleep(3)  # Additional wait for dynamic content
            self.driver.get("https://www.delta.com/flightsearch/book-a-flight")
            
            # Wait for page to load completely
            WebDriverWait(self.driver, 30).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            time.sleep(5)  # Additional wait for dynamic content
            print("✅ Successfully navigated to Delta website")
            return True
            
        except Exception as e:
            print(f"❌ Failed to navigate to Delta website: {e}")
            return False
    
    def select_from_airport(self, airport_code):
        """Select departure airport with multiple selector strategies"""
        try:
            print(f"🔄 Selecting departure airport: {airport_code}")
            
            # Multiple selectors for 'From' field
            from_selectors = [
                # (By.XPATH, "//a[contains(@aria-label, 'From')]"),
                # (By.XPATH, "//div[contains(@class, 'departure')]//a"),
                (By.XPATH, "/html/body/idp-root/div/div[2]/idp-advance-search/div/div[1]/div[2]/idp-book-widget/div/ngc-book/div[1]/div/form/div[1]/div/div[1]/div[1]/div[1]/div[1]/a[1]"),
                # (By.CSS_SELECTOR, "a[aria-label*='From']"),
                # (By.XPATH, "//a[1][contains(@class, 'airport')]")
            ]
            
            if not self.smart_wait_and_click(from_selectors, description="From airport field"):
                return False
            
            time.sleep(2)
            
            # Multiple selectors for input field
            input_selectors = [
                # (By.XPATH, "//input[@type='text']"),
                # (By.XPATH, "//input[contains(@placeholder, 'airport')]"),
                (By.XPATH, "/html/body/idp-root/div/div[1]/ngc-global-nav/header/modal-container/div/div/ngc-airport-lookup-modal/div/div[2]/tabset/div/tab/div/div/div[1]/input"),
                # (By.CSS_SELECTOR, "input[type='text']"),
                # (By.XPATH, "//input[contains(@class, 'airport')]")
            ]
            
            if not self.smart_send_keys(input_selectors, airport_code, "airport input"):
                return False
            
            time.sleep(2)
            
            # Multiple selectors for first suggestion
            suggestion_selectors = [
                # (By.XPATH, "//li[1]"),
                # (By.XPATH, "//ul/li[1]"),
                (By.XPATH, "/html/body/idp-root/div/div[1]/ngc-global-nav/header/modal-container/div/div/ngc-airport-lookup-modal/div/div[2]/tabset/div/tab/div/div/div[2]/div/ul/li[1]"),
                # (By.CSS_SELECTOR, "li:first-child"),
                # (By.XPATH, "//div[contains(@class, 'airport-option')][1]")
            ]
            
            if not self.smart_wait_and_click(suggestion_selectors, description="first airport suggestion"):
                return False
            
            print(f"✅ Successfully selected departure airport: {airport_code}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to select departure airport {airport_code}: {e}")
            return False
    
    def select_to_airport(self, airport_code):
        """Select destination airport with multiple selector strategies"""
        try:
            print(f"🔄 Selecting destination airport: {airport_code}")
            
            # Multiple selectors for 'To' field
            to_selectors = [
                # (By.XPATH, "//a[contains(@aria-label, 'To')]"),
                # (By.XPATH, "//div[contains(@class, 'arrival')]//a"),
                (By.XPATH, "/html/body/idp-root/div/div[2]/idp-advance-search/div/div[1]/div[2]/idp-book-widget/div/ngc-book/div[1]/div/form/div[1]/div/div[1]/div[1]/div[1]/div[1]/a[2]"),
                (By.CSS_SELECTOR, "a[aria-label*='To']"),
                (By.XPATH, "//a[2][contains(@class, 'airport')]")
            ]
            
            if not self.smart_wait_and_click(to_selectors, description="To airport field"):
                return False
            
            time.sleep(2)
            
            # Reuse input selectors
            input_selectors = [
                # (By.XPATH, "//input[@type='text']"),
                # (By.XPATH, "//input[contains(@placeholder, 'airport')]"),
                (By.XPATH, "/html/body/idp-root/div/div[1]/ngc-global-nav/header/modal-container/div/div/ngc-airport-lookup-modal/div/div[2]/tabset/div/tab/div/div/div[1]/input"),
                (By.CSS_SELECTOR, "input[type='text']")
            ]
            
            if not self.smart_send_keys(input_selectors, airport_code, "airport input"):
                return False
            
            time.sleep(2)
            
            # Multiple selectors for suggestion click
            suggestion_selectors = [
                # (By.XPATH, "//li[1]"),
                # (By.XPATH, "//ul/li[1]"),
                (By.XPATH, "/html/body/idp-root/div/div[1]/ngc-global-nav/header/modal-container/div/div/ngc-airport-lookup-modal/div/div[2]/tabset/div/tab/div/div/div[2]/div"),
                (By.CSS_SELECTOR, "li:first-child")
            ]
            
            if not self.smart_wait_and_click(suggestion_selectors, description="first airport suggestion"):
                return False
            
            print(f"✅ Successfully selected destination airport: {airport_code}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to select destination airport {airport_code}: {e}")
            return False
    
    def select_trip_type(self, trip_type="one_way"):
        """Select trip type with robust error handling"""
        try:
            print(f"🔄 Selecting trip type: {trip_type}")
            
            # Trip type dropdown selectors
            dropdown_selectors = [
                # (By.XPATH, "//span[contains(@class, 'trip-type')]"),
                (By.XPATH, "/html/body/idp-root/div/div[2]/idp-advance-search/div/div[1]/div[2]/idp-book-widget/div/ngc-book/div[1]/div/form/div[1]/div/div[1]/div[1]/div[2]/span/span[1]"),
                (By.CSS_SELECTOR, "span[class*='trip-type']"),
                (By.XPATH, "//div[contains(@class, 'trip-type')]")
            ]
            
            if not self.smart_wait_and_click(dropdown_selectors, description="trip type dropdown"):
                return False
            
            time.sleep(1)
            
            # Trip type option selectors
            trip_options = {
                "round_trip": [
                    # (By.XPATH, "//li[1]"),
                    # (By.XPATH, "//span[contains(text(), 'Round')]"),
                    (By.XPATH, "/html/body/idp-root/div/div[2]/idp-advance-search/div/div[1]/div[2]/idp-book-widget/div/ngc-book/div[1]/div/form/div[1]/div/div[1]/div[1]/div[2]/span/span[2]/ul/li[1]")
                ],
                "one_way": [
                    # (By.XPATH, "//li[2]"),
                    # (By.XPATH, "//span[contains(text(), 'One')]"),
                    (By.XPATH, "/html/body/idp-root/div/div[2]/idp-advance-search/div/div[1]/div[2]/idp-book-widget/div/ngc-book/div[1]/div/form/div[1]/div/div[1]/div[1]/div[2]/span/span[2]/ul/li[2]")
                ],
                "multi_city": [
                    # (By.XPATH, "//li[3]"),
                    # (By.XPATH, "//span[contains(text(), 'Multi')]"),
                    (By.XPATH, "/html/body/idp-root/div/div[2]/idp-advance-search/div/div[1]/div[2]/idp-book-widget/div/ngc-book/div[1]/div/form/div[1]/div/div[1]/div[1]/div[2]/span/span[2]/ul/li[3]")
                ]
            }
            
            if trip_type in trip_options:
                if not self.smart_wait_and_click(trip_options[trip_type], description=f"{trip_type} option"):
                    return False
            
            print(f"✅ Successfully selected trip type: {trip_type}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to select trip type {trip_type}: {e}")
            return False
    
    def select_departure_date(self, date_str="09/24/25"):
        """Select departure date with intelligent date navigation"""
        try:
            print(f"🔄 Selecting departure date: {date_str}")
            
            # Parse the date
            date_obj = datetime.strptime(date_str, "%m/%d/%y")
            target_day = date_obj.day
            
            # Date field selectors
            date_selectors = [
                # (By.XPATH, "//div[contains(@class, 'depart')]"),
                (By.XPATH, "/html/body/idp-root/div/div[2]/idp-advance-search/div/div[1]/div[2]/idp-book-widget/div/ngc-book/div[1]/div/form/div[1]/div/div[1]/div[1]/div[3]/date-selection-view/div/div/div/div/div[2]"),
                (By.CSS_SELECTOR, "div[class*='depart']"),
                (By.XPATH, "//input[contains(@placeholder, 'Depart')]")
            ]
            
            if not self.smart_wait_and_click(date_selectors, description="departure date field"):
                return False
            
            time.sleep(3)
            
            # Try to find and click the target day
            day_selectors = [
                (By.XPATH, f"//button[text()='{target_day}']"),
                (By.XPATH, f"//td[text()='{target_day}']"),
                (By.XPATH, f"//td[@aria-label='{target_day}']//button"),
                (By.XPATH, f"//td[contains(@aria-label, '{target_day}')]"),
                (By.CSS_SELECTOR, f"td[aria-label*='{target_day}']"),
                (By.XPATH, f"//button[contains(@aria-label, '{target_day}')]")
            ]
            
            if not self.smart_wait_and_click(day_selectors, description=f"day {target_day}"):
                print(f"⚠️ Could not find day {target_day}, trying alternative approach")
                # If specific day not found, try clicking any available date
                any_day_selectors = [
                    (By.XPATH, "//td[contains(@class, 'available')]//button"),
                    (By.XPATH, "//button[contains(@class, 'day')]"),
                    (By.CSS_SELECTOR, "td.available button")
                ]
                self.smart_wait_and_click(any_day_selectors, description="any available day")
            
            time.sleep(1)
            
            # Done button selectors
            done_selectors = [
                (By.XPATH, "//button[contains(text(), 'Done')]"),
                (By.XPATH, "/html/body/idp-root/div/div[2]/idp-advance-search/div/div[1]/div[2]/idp-book-widget/div/ngc-book/div[1]/div/form/div[1]/div/div[1]/div[1]/div[3]/date-selection-view/div/div/div/div/div[4]/div/div[3]/button[2]"),
                (By.CSS_SELECTOR, "button[class*='done']"),
                (By.XPATH, "//button[contains(@class, 'done')]")
            ]
            
            if not self.smart_wait_and_click(done_selectors, description="Done button"):
                return False
            
            print(f"✅ Successfully selected departure date: {date_str}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to select departure date {date_str}: {e}")
            return False
    
    def search_flights(self):
        """Click search button to find flights"""
        try:
            print("🔄 Searching for flights...")
            
            # Search button selectors
            search_selectors = [
                (By.XPATH, "//button[contains(text(), 'Search')]"),
                (By.XPATH, "/html/body/idp-root/div/div[2]/idp-advance-search/div/div[1]/div[2]/idp-book-widget/div/ngc-book/div[1]/div/form/div[2]/div/div[2]/div[2]/button"),
                (By.CSS_SELECTOR, "button[class*='search']"),
                (By.XPATH, "//button[contains(@class, 'search')]"),
                (By.XPATH, "//input[@type='submit']")
            ]
            
            if not self.smart_wait_and_click(search_selectors, description="search button"):
                return False
            
            print("✅ Search initiated successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to initiate search: {e}")
            return False
    
    def wait_for_results(self, timeout=120):
        """Wait for flight results to load with multiple indicators"""
        try:
            print("🔄 Waiting for flight results...")
            
            # Multiple selectors to detect results
            result_selectors = [
                "div.flight-results-grid",
                "div[id*='flight-results']",
                "[class*='flight-card']",
                "[class*='flight-results']",
                "div[class*='mach-flight-results-grid']"
            ]
            
            for selector in result_selectors:
                try:
                    element = WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    if element:
                        print(f"✅ Found results using selector: {selector}")
                        time.sleep(5)  # Wait for full load
                        return True
                except TimeoutException:
                    continue
            
            print("❌ No flight results found within timeout")
            return False
                
        except Exception as e:
            print(f"❌ Error waiting for results: {e}")
            return False
    
    def dump_html(self, filename="flight_results.html"):
        """Save current page HTML to file with error handling"""
        try:
            # Create dumps directory
            dumps_dir = "html_dumps"
            os.makedirs(dumps_dir, exist_ok=True)
            
            filepath = os.path.join(dumps_dir, filename)
            
            # Get page source
            html_content = self.driver.page_source
            
            # Save with UTF-8 encoding
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            file_size = os.path.getsize(filepath) / 1024  # Size in KB
            print(f"✅ HTML dumped successfully to: {filepath} ({file_size:.1f} KB)")
            return filepath
            
        except Exception as e:
            print(f"❌ Failed to dump HTML: {e}")
            return None
    
    def click_price_tab(self):
        """Click on price tab with multiple strategies"""
        try:
            print("🔄 Clicking price tab...")
            
            # Price tab selectors
            price_tab_selectors = [
                (By.XPATH, "//button[2]"),
                (By.XPATH, "/html/body/idp-root/div/div[2]/idp-search-results/div/div[2]/idp-search-results-head/div/div[1]/div[2]/idp-shopping-price-in-tabs/div/idp-show-price-in-tabs/mach-global-tabs/div/div[2]/button[2]"),
                (By.CSS_SELECTOR, "button:nth-child(2)"),
                (By.XPATH, "//button[contains(@class, 'tab')]"),
                (By.XPATH, "//div[contains(@class, 'tabs')]//button[2]")
            ]
            
            if not self.smart_wait_and_click(price_tab_selectors, description="price tab"):
                return False
            
            # Wait for new content to load
            time.sleep(5)
            
            print("✅ Successfully clicked price tab")
            return True
            
        except Exception as e:
            print(f"❌ Failed to click price tab: {e}")
            return False
    
    def run_automation(self, from_airport="DEL", to_airport="BCN", trip_type="one_way", date="09/24/25"):
        """Run the complete automation with comprehensive error handling"""
        try:
            print("🚀 Starting Enhanced Delta Flight Automation")
            print("=" * 60)
            print(f"📋 Search Parameters:")
            print(f"   From: {from_airport}")
            print(f"   To: {to_airport}")
            print(f"   Trip Type: {trip_type}")
            print(f"   Date: {date}")
            print("=" * 60)
            
            steps = [
                ("Navigate to Delta", lambda: self.navigate_to_delta()),
                ("Select From Airport", lambda: self.select_from_airport(from_airport)),
                ("Select To Airport", lambda: self.select_to_airport(to_airport)),
                ("Select Trip Type", lambda: self.select_trip_type(trip_type)),
                ("Select Departure Date", lambda: self.select_departure_date(date)),
                ("Search Flights", lambda: self.search_flights()),
                ("Wait for Results", lambda: self.wait_for_results())
            ]
            
            # Execute each step
            for step_name, step_func in steps:
                print(f"\n🔄 Step: {step_name}")
                if not step_func():
                    print(f"❌ Failed at step: {step_name}")
                    return False
                print(f"✅ Completed: {step_name}")
            
            # Generate timestamp for file names
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Dump initial results
            first_dump = f"flight_results_initial_{from_airport}_{to_airport}_{timestamp}.html"
            self.dump_html(first_dump)
            
            # Try to click price tab and dump again
            if self.click_price_tab():
                second_dump = f"flight_results_price_tab_{from_airport}_{to_airport}_{timestamp}.html"
                self.dump_html(second_dump)
            
            print("\n" + "=" * 60)
            print("🎉 AUTOMATION COMPLETED SUCCESSFULLY!")
            print("📁 Check the 'html_dumps' folder for saved HTML files")
            print("=" * 60)
            return True
            
        except Exception as e:
            print(f"\n❌ Automation failed with error: {e}")
            return False
    
    def close(self):
        """Close browser with cleanup"""
        try:
            if self.driver:
                self.driver.quit()
                print("✅ Browser closed successfully")
        except Exception as e:
            print(f"⚠️ Error closing browser: {e}")


def main():
    """Main function with user-friendly configuration"""
    print("🛫 Delta Flight Search Automation")
    print("=" * 50)
    
    # Default configuration - modify as needed
    config = {
        "from_airport": "DEL",      # Delhi
        "to_airport": "BCN",        # Barcelona  
        "trip_type": "one_way",     # one_way, round_trip, multi_city
        "date": "09/24/25",         # MM/DD/YY format
        "headless": False           # Set to True for headless mode
    }
    
    print(f"Configuration:")
    for key, value in config.items():
        print(f"  {key}: {value}")
    print("=" * 50)
    
    automation = None
    
    try:
        # Initialize automation
        automation = DeltaFlightAutomationAdvanced(headless=config["headless"])
        
        # Run automation
        success = automation.run_automation(
            from_airport=config["from_airport"],
            to_airport=config["to_airport"],
            trip_type=config["trip_type"],
            date=config["date"]
        )
        
        if success:
            print("\n🎯 SUCCESS: All automation tasks completed!")
        else:
            print("\n❌ FAILURE: Automation completed with errors")
            
        # Keep browser open for a moment to see results
        input("\n🔍 Press Enter to close the browser and exit...")
            
    except KeyboardInterrupt:
        print("\n⏹️ Automation stopped by user (Ctrl+C)")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Always cleanup
        if automation:
            automation.close()


if __name__ == "__main__":
    main()
