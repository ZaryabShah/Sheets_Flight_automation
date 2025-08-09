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
    def __init__(self, headless=True, timeout=30, use_proxy=True):
        """
        Initialize the Delta Flight Automation with WebDriver Manager
        
        Args:
            headless (bool): Run browser in headless mode
            timeout (int): Default timeout for WebDriverWait
            use_proxy (bool): Use proxy server for requests
        """
        self.timeout = timeout
        self.driver = None
        self.wait = None
        self.use_proxy = True
        self.setup_driver(headless)
        
    def setup_driver(self, headless=False):
        """Setup Chrome WebDriver with automatic driver management and optional proxy"""
        try:
            print("🔄 Setting up ChromeDriver...")
            
            chrome_options = Options()
            
            # Proxy configuration if enabled
            if self.use_proxy:
                proxy_server = "https://pr.oxylabs.io:10000"
                print(f"🌐 Using proxy: {proxy_server}")
                chrome_options.add_argument(f'--proxy-server={proxy_server}')
            
            # Basic options for stability
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Performance optimizations
            # chrome_options.add_argument("--disable-extensions")
            # chrome_options.add_argument("--disable-plugins")
            # chrome_options.add_argument("--disable-images")  # Faster loading
            # Note: JavaScript is needed for Delta's calendar functionality
            
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
            
            proxy_status = "with proxy" if self.use_proxy else "without proxy"
            print(f"✅ Chrome WebDriver initialized successfully {proxy_status}")
            
        except Exception as e:
            print(f"❌ Error setting up WebDriver: {e}")
            print("💡 Make sure Chrome browser is installed on your system")
            if self.use_proxy:
                print("💡 Check your proxy connection")
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
            self.driver.get("https://www.delta.com/")
            
            # Wait for page to load completely
            WebDriverWait(self.driver, 30).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            # time.sleep(3)  # Additional wait for dynamic content
            # self.driver.get("https://www.delta.com/")
            
            # # Wait for page to load completely
            # WebDriverWait(self.driver, 30).until(
            #     lambda driver: driver.execute_script("return document.readyState") == "complete"
            # )
            # time.sleep(3)  # Additional wait for dynamic content
            # self.driver.get("https://www.delta.com/flightsearch/book-a-flight")
            
            # # Wait for page to load completely
            # WebDriverWait(self.driver, 30).until(
            #     lambda driver: driver.execute_script("return document.readyState") == "complete"
            # )
            
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
                (By.XPATH, "/html/body/idp-root/ngc-global-nav/header/div/div[1]/ngc-book/div[1]/div/form/div[1]/div/div[1]/div[1]/div[1]/div[1]/a[1]"),
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
                (By.XPATH, "/html/body/modal-container/div/div/ngc-airport-lookup-modal/div/div[2]/tabset/div/tab[1]/div/div/div[1]/input"),
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
                (By.XPATH, "/html/body/modal-container/div/div/ngc-airport-lookup-modal/div/div[2]/tabset/div/tab[1]/div/div/div[2]/div"),
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
                (By.XPATH, "/html/body/idp-root/ngc-global-nav/header/div/div[1]/ngc-book/div[1]/div/form/div[1]/div/div[1]/div[1]/div[1]/div[1]/a[2]"),
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
                (By.XPATH, "/html/body/modal-container/div/div/ngc-airport-lookup-modal/div/div[2]/tabset/div/tab[1]/div/div/div[1]/input"),
                (By.CSS_SELECTOR, "input[type='text']")
            ]
            
            if not self.smart_send_keys(input_selectors, airport_code, "airport input"):
                return False
            
            time.sleep(2)
            
            # Multiple selectors for suggestion click
            suggestion_selectors = [
                # (By.XPATH, "//li[1]"),
                # (By.XPATH, "//ul/li[1]"),
                (By.XPATH, "/html/body/modal-container/div/div/ngc-airport-lookup-modal/div/div[2]/tabset/div/tab[1]/div/div/div[2]/div/ul/li[1]"),
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
                (By.XPATH, "/html/body/idp-root/ngc-global-nav/header/div/div[1]/ngc-book/div[1]/div/form/div[1]/div/div[1]/div[1]/div[2]/select"),
                (By.CSS_SELECTOR, "span[class*='trip-type']"),
                (By.XPATH, "/html/body/idp-root/ngc-global-nav/header/div/div[1]/ngc-book/div[1]/div/form/div[1]/div/div[1]/div[1]/div[2]")
            ]
            
            if not self.smart_wait_and_click(dropdown_selectors, description="trip type dropdown"):
                return False
            
            time.sleep(1)
            
            # Trip type option selectors
            trip_options = {
                "round_trip": [
                    # (By.XPATH, "//li[1]"),
                    # (By.XPATH, "//span[contains(text(), 'Round')]"),
                    (By.XPATH, "/html/body/idp-root/ngc-global-nav/header/div/div[1]/ngc-book/div[1]/div/form/div[1]/div/div[1]/div[1]/div[2]/span/span[2]/ul/li[1]")
                ],
                "one_way": [
                    # (By.XPATH, "//li[2]"),
                    # (By.XPATH, "//span[contains(text(), 'One')]"),
                    (By.XPATH, "/html/body/idp-root/ngc-global-nav/header/div/div[1]/ngc-book/div[1]/div/form/div[1]/div/div[1]/div[1]/div[2]/span/span[2]/ul/li[2]")
                ],
                "multi_city": [
                    # (By.XPATH, "//li[3]"),
                    # (By.XPATH, "//span[contains(text(), 'Multi')]"),
                    (By.XPATH, "/html/body/idp-root/ngc-global-nav/header/div/div[1]/ngc-book/div[1]/div/form/div[1]/div/div[1]/div[1]/div[2]/span/span[2]/ul/li[3]")
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
        """Select departure date with advanced calendar navigation"""
        try:
            print(f"🔄 Selecting departure date: {date_str}")
            
            # Parse the date
            date_obj = datetime.strptime(date_str, "%m/%d/%y")
            target_day = date_obj.day
            target_month = date_obj.month
            target_year = date_obj.year
            target_date_formatted = date_obj.strftime("%m/%d/%Y")
            
            print(f"📅 Target date: Day={target_day}, Month={target_month}, Year={target_year}")
            
            # Date field selectors
            date_selectors = [
                (By.XPATH, "/html/body/idp-root/ngc-global-nav/header/div/div[1]/ngc-book/div[1]/div/form/div[1]/div/div[1]/div[1]/div[3]/date-selection-view"),
                (By.CSS_SELECTOR, "div[class*='depart']"),
                (By.XPATH, "/html/body/idp-root/ngc-global-nav/header/div/div[1]/ngc-book/div[1]/div/form/div[1]/div/div[1]/div[1]/div[3]"),
                (By.XPATH, "//input[contains(@placeholder, 'Depart')]")
            ]
            
            if not self.smart_wait_and_click(date_selectors, description="departure date field"):
                return False
            
            time.sleep(3)
            
            # Try multiple approaches to select the date
            success = False
            
            # Approach 1: Try Delta-specific date picker with data-date attribute
            # print("🔍 Approach 1: Trying Delta date picker with data-date...")
            # if self._select_date_by_data_attribute(target_date_formatted, target_day):
            #     success = True
            
            # Approach 2: Try generic calendar navigation
            if not success:
                print("🔍 Approach 2: Trying calendar navigation...")
                if self._select_date_by_navigation(target_day, target_month, target_year):
                    success = True
            
            # Approach 3: Try clicking any available date if specific date fails
            # if not success:
            #     print("🔍 Approach 3: Trying to click any available date...")
            #     if self._select_any_available_date():
            #         success = True
            
            if not success:
                print("❌ All date selection approaches failed")
                return False
            
            time.sleep(1)
            
            # Click Done button
            done_selectors = [
                # (By.XPATH, "//button[contains(text(), 'Done')]"),
                (By.XPATH, "/html/body/idp-root/ngc-global-nav/header/div/div[1]/ngc-book/div[1]/div/form/div[1]/div/div[1]/div[1]/div[3]/date-selection-view/div/div/div/div/div[4]/div/div[3]/button[2]"),
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
    
    def _select_date_by_data_attribute(self, target_date_formatted, target_day):
        """Try to select date using data-date attribute (Delta-specific approach)"""
        try:
            # Try Delta's date picker format with data-date
            selectors = [
                f"td.dl-datepicker-available-day a[data-date='{target_date_formatted}']",
                f"a[data-date='{target_date_formatted}']",
                f"td[data-date='{target_date_formatted}']",
                f"button[data-date='{target_date_formatted}']"
            ]
            
            for selector in selectors:
                try:
                    element = WebDriverWait(self.driver, 2).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    element.click()
                    print(f"✅ Selected date using data-attribute: {selector}")
                    return True
                except TimeoutException:
                    continue
            
            # If exact date not found, try navigating months and then clicking
            return self._navigate_and_select_by_data_attribute(target_date_formatted, target_day)
            
        except Exception as e:
            print(f"⚠️ Data attribute approach failed: {e}")
            return False
    
    def _navigate_and_select_by_data_attribute(self, target_date_formatted, target_day, max_attempts=12):
        """Navigate through months to find the target date"""
        try:
            for attempt in range(max_attempts):
                # Try to find the date in current month view
                selectors = [
                    f"td.dl-datepicker-available-day a[data-date='{target_date_formatted}']",
                    f"a[data-date='{target_date_formatted}']"
                ]
                
                for selector in selectors:
                    try:
                        element = WebDriverWait(self.driver, 1).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                        element.click()
                        print(f"✅ Found and clicked date after {attempt} navigation attempts")
                        return True
                    except TimeoutException:
                        continue
                
                # If not found, try to navigate to next month
                next_selectors = [
                    "button[aria-label*='next' i]",
                    "button[aria-label*='Next' i]",
                    ".dl-datepicker-next",
                    "button[class*='next']",
                    "button:contains('Next')"
                ]
                
                navigated = False
                for next_selector in next_selectors:
                    try:
                        next_button = WebDriverWait(self.driver, 1).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, next_selector))
                        )
                        next_button.click()
                        time.sleep(0.5)
                        navigated = True
                        break
                    except TimeoutException:
                        continue
                
                if not navigated:
                    print("⚠️ Could not navigate to next month")
                    break
            
            return False
            
        except Exception as e:
            print(f"⚠️ Navigation approach failed: {e}")
            return False
    
    def _select_date_by_navigation(self, target_day, target_month, target_year):
        """Try generic calendar navigation approach"""
        try:
            # Get current month/year from calendar
            month_year_selectors = [
                ".dl-datepicker-title",
                ".calendar-title",
                "[class*='month-year']",
                "[class*='calendar-header']"
            ]
            
            current_month_element = None
            for selector in month_year_selectors:
                try:
                    current_month_element = WebDriverWait(self.driver, 2).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    break
                except TimeoutException:
                    continue
            
            if not current_month_element:
                print("⚠️ Could not find calendar header")
                return False
            
            # Navigate to correct month/year (simplified - just try clicking next a few times)
            for _ in range(6):  # Try up to 6 months ahead
                # Try to click the target day
                day_selectors = [
                    f"td.dl-datepicker-available-day a:contains('{target_day}')",
                    f"td[class*='available'] a[text()='{target_day}']",
                    f"button[text()='{target_day}']",
                    f"a[text()='{target_day}']",
                    f"td:contains('{target_day}'):not([class*='disabled'])"
                ]
                
                for selector in day_selectors:
                    try:
                        # Convert CSS selector to XPath for text matching
                        xpath_selector = f"//td[contains(@class, 'available')]//a[text()='{target_day}'] | //button[text()='{target_day}'] | //a[text()='{target_day}']"
                        element = WebDriverWait(self.driver, 1).until(
                            EC.element_to_be_clickable((By.XPATH, xpath_selector))
                        )
                        element.click()
                        print(f"✅ Selected day {target_day} using navigation")
                        return True
                    except TimeoutException:
                        continue
                
                # Navigate to next month
                next_selectors = [
                    "button[aria-label*='next' i]",
                    ".dl-datepicker-next",
                    "button[class*='next']"
                ]
                
                navigated = False
                for next_selector in next_selectors:
                    try:
                        next_button = WebDriverWait(self.driver, 1).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, next_selector))
                        )
                        next_button.click()
                        time.sleep(0.5)
                        navigated = True
                        break
                    except TimeoutException:
                        continue
                
                if not navigated:
                    break
            
            return False
            
        except Exception as e:
            print(f"⚠️ Calendar navigation failed: {e}")
            return False
    
    def _select_any_available_date(self):
        """Fallback: select any available date"""
        try:
            print("🔍 Looking for any available date...")
            
            # Try various selectors for available dates
            available_date_selectors = [
                "td.dl-datepicker-available-day a",
                "td[class*='available'] a",
                "td[class*='available'] button",
                "button[class*='available']",
                "a[class*='available']",
                "td:not([class*='disabled']) a",
                "td:not([class*='disabled']) button"
            ]
            
            for selector in available_date_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        # Click the first available date
                        elements[0].click()
                        selected_text = elements[0].text if elements[0].text else "unknown"
                        print(f"✅ Selected first available date: {selected_text}")
                        return True
                except Exception as e:
                    print(f"⚠️ Selector {selector} failed: {e}")
                    continue
            
            # Try XPath approach for available dates
            xpath_selectors = [
                "//td[contains(@class, 'available')]//a",
                "//td[not(contains(@class, 'disabled'))]//a",
                "//td[not(contains(@class, 'disabled'))]//button",
                "//a[contains(@aria-label, '2025')]",
                "//button[contains(@aria-label, '2025')]"
            ]
            
            for xpath in xpath_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, xpath)
                    if elements:
                        elements[0].click()
                        print(f"✅ Selected available date using XPath")
                        return True
                except Exception as e:
                    continue
            
            return False
            
        except Exception as e:
            print(f"⚠️ Fallback date selection failed: {e}")
            return False
    
    def select_next_available_date(self):
        """Select the next available date from today onwards"""
        try:
            print("🔄 Selecting next available date...")
            
            # Date field selectors
            date_selectors = [
                (By.XPATH, "/html/body/idp-root/div/div[2]/idp-advance-search/div/div[1]/div[2]/idp-book-widget/div/ngc-book/div[1]/div/form/div[1]/div/div[1]/div[1]/div[3]/date-selection-view/div/div/div/div/div[2]"),
                (By.CSS_SELECTOR, "div[class*='depart']"),
                (By.XPATH, "//div[contains(@class, 'depart')]")
            ]
            
            if not self.smart_wait_and_click(date_selectors, description="departure date field"):
                return False
            
            time.sleep(3)
            
            # Find the first available date and click it
            today = datetime.now()
            
            # Try different strategies to find available dates
            strategies = [
                self._find_next_available_delta_format,
                self._find_next_available_generic,
                self._find_next_available_by_text
            ]
            
            for i, strategy in enumerate(strategies, 1):
                print(f"🔍 Trying strategy {i} to find next available date...")
                if strategy():
                    break
            else:
                print("❌ All strategies failed to find available date")
                return False
            
            time.sleep(1)
            
            # Click Done button
            done_selectors = [
                (By.XPATH, "//button[contains(text(), 'Done')]"),
                (By.XPATH, "/html/body/idp-root/div/div[2]/idp-advance-search/div/div[1]/div[2]/idp-book-widget/div/ngc-book/div[1]/div/form/div[1]/div/div[1]/div[1]/div[3]/date-selection-view/div/div/div/div/div[4]/div/div[3]/button[2]"),
                (By.CSS_SELECTOR, "button[class*='done']")
            ]
            
            if not self.smart_wait_and_click(done_selectors, description="Done button"):
                return False
            
            print("✅ Successfully selected next available date")
            return True
            
        except Exception as e:
            print(f"❌ Failed to select next available date: {e}")
            return False
    
    def _find_next_available_delta_format(self):
        """Strategy 1: Look for Delta-specific available date format"""
        try:
            selectors = [
                "td.dl-datepicker-available-day a",
                "td[class*='available'] a",
                "a[data-date]",
                "button[data-date]"
            ]
            
            for selector in selectors:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    # Find the first date that's today or later
                    for element in elements:
                        try:
                            data_date = element.get_attribute("data-date")
                            if data_date:
                                # Parse the date and check if it's today or later
                                element_date = datetime.strptime(data_date, "%m/%d/%Y")
                                if element_date.date() >= datetime.now().date():
                                    element.click()
                                    print(f"✅ Selected date: {data_date}")
                                    return True
                            else:
                                # If no data-date, just click the first available
                                element.click()
                                text = element.text or "unknown"
                                print(f"✅ Selected available date: {text}")
                                return True
                        except Exception:
                            continue
            return False
        except Exception as e:
            print(f"⚠️ Delta format strategy failed: {e}")
            return False
    
    def _find_next_available_generic(self):
        """Strategy 2: Generic approach to find available dates"""
        try:
            # Look for clickable elements that could be dates
            selectors = [
                "td:not([class*='disabled']) a",
                "td:not([class*='disabled']) button",
                "button[class*='available']",
                "a[class*='available']",
                "[aria-label*='2025']:not([class*='disabled'])"
            ]
            
            for selector in selectors:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    for element in elements:
                        try:
                            # Check if it looks like a date (1-31)
                            text = element.text.strip()
                            if text.isdigit() and 1 <= int(text) <= 31:
                                element.click()
                                print(f"✅ Selected date: {text}")
                                return True
                        except Exception:
                            continue
            return False
        except Exception as e:
            print(f"⚠️ Generic strategy failed: {e}")
            return False
    
    def _find_next_available_by_text(self):
        """Strategy 3: Find by text content"""
        try:
            # Look for elements with day numbers
            for day in range(1, 32):
                xpath_selectors = [
                    f"//a[text()='{day}' and not(ancestor::*[contains(@class, 'disabled')])]",
                    f"//button[text()='{day}' and not(ancestor::*[contains(@class, 'disabled')])]",
                    f"//td[not(contains(@class, 'disabled'))]//a[text()='{day}']",
                    f"//td[not(contains(@class, 'disabled'))]//button[text()='{day}']"
                ]
                
                for xpath in xpath_selectors:
                    try:
                        element = WebDriverWait(self.driver, 0.5).until(
                            EC.element_to_be_clickable((By.XPATH, xpath))
                        )
                        element.click()
                        print(f"✅ Selected date: {day}")
                        return True
                    except TimeoutException:
                        continue
            return False
        except Exception as e:
            print(f"⚠️ Text-based strategy failed: {e}")
            return False
    
    def search_flights(self):
        """Click search button to find flights"""
        try:
            print("🔄 Searching for flights...")
            
            # Search button selectors
            search_selectors = [
                # (By.XPATH, "//button[contains(text(), 'Search')]"),
                (By.XPATH, "/html/body/idp-root/ngc-global-nav/header/div/div[1]/ngc-book/div[1]/div/form/div[1]/div/div[2]/button"),
                # (By.CSS_SELECTOR, "button[class*='search']"),
                # (By.XPATH, "//button[contains(@class, 'search')]"),
                # (By.XPATH, "//input[@type='submit']")
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
    
    def run_automation(self, from_airport="DEL", to_airport="BCN", trip_type="one_way", date="09/24/25", use_next_available=True):
        """Run the complete automation with comprehensive error handling"""
        try:
            print("🚀 Starting Enhanced Delta Flight Automation")
            print("=" * 60)
            print(f"📋 Search Parameters:")
            print(f"   From: {from_airport}")
            print(f"   To: {to_airport}")
            print(f"   Trip Type: {trip_type}")
            print(f"   Date: {date}")
            print(f"   Use Next Available: {use_next_available}")
            print("=" * 60)
            
            steps = [
                ("Navigate to Delta", lambda: self.navigate_to_delta()),
                ("Select From Airport", lambda: self.select_from_airport(from_airport)),
                ("Select To Airport", lambda: self.select_to_airport(to_airport)),
                ("Select Trip Type", lambda: self.select_trip_type(trip_type)),
                ("Select Departure Date", lambda: self._select_date_with_fallback(date, use_next_available)),
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
    
    def _select_date_with_fallback(self, date, use_next_available):
        """Select date with fallback to next available date"""
        try:
            # First try to select the specific date
            if self.select_departure_date(date):
                return True
            
            # If specific date failed and fallback is enabled, try next available
            if use_next_available:
                print("🔄 Specific date failed, trying next available date...")
                return self.select_next_available_date()
            
            return False
            
        except Exception as e:
            print(f"❌ Date selection with fallback failed: {e}")
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
        "from_airport": "MCO",          # Orlando
        "to_airport": "BCN",            # Barcelona
        "trip_type": "one_way",         # one_way, round_trip, multi_city
        "date": "09/24/25",             # MM/DD/YY format
        "use_next_available": True,     # If specific date fails, use next available
        "headless": False,              # Set to True for headless mode
        "use_proxy": False              # Set to True to use Oxylabs proxy
    }
    
    print(f"Configuration:")
    for key, value in config.items():
        print(f"  {key}: {value}")
    if config["use_proxy"]:
        print("  proxy_server: https://pr.oxylabs.io:10000")
    print("=" * 50)
    
    automation = None
    
    try:
        # Initialize automation
        automation = DeltaFlightAutomationAdvanced(
            headless=config["headless"],
            use_proxy=config["use_proxy"]
        )
        
        # Run automation
        success = automation.run_automation(
            from_airport=config["from_airport"],
            to_airport=config["to_airport"],
            trip_type=config["trip_type"],
            date=config["date"],
            use_next_available=config["use_next_available"]
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
