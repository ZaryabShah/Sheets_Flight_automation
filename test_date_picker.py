"""
Test script for Delta Date Picker functionality
==============================================
This script tests only the date selection part to help debug date picker issues.
"""

import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager


class DatePickerTester:
    def __init__(self):
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        """Setup Chrome WebDriver"""
        try:
            print("🔄 Setting up ChromeDriver for date picker test...")
            
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--window-size=1920,1080")
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            print("✅ Chrome WebDriver initialized successfully")
            
        except Exception as e:
            print(f"❌ Error setting up WebDriver: {e}")
            raise
    
    def navigate_to_delta(self):
        """Navigate to Delta and open date picker"""
        try:
            print("🔄 Navigating to Delta...")
            self.driver.get("https://www.delta.com/flightsearch/book-a-flight")
            
            # Wait for page load
            WebDriverWait(self.driver, 30).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            time.sleep(5)
            
            print("✅ Page loaded successfully")
            return True
            
        except Exception as e:
            print(f"❌ Navigation failed: {e}")
            return False
    
    def open_date_picker(self):
        """Open the departure date picker"""
        try:
            print("🔄 Opening date picker...")
            
            # Try to click departure date field
            date_selectors = [
                "/html/body/idp-root/div/div[2]/idp-advance-search/div/div[1]/div[2]/idp-book-widget/div/ngc-book/div[1]/div/form/div[1]/div/div[1]/div[1]/div[3]/date-selection-view/div/div/div/div/div[2]",
                "//div[contains(@class, 'depart')]",
                "//input[contains(@placeholder, 'Depart')]"
            ]
            
            for selector in date_selectors:
                try:
                    element = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    element.click()
                    print(f"✅ Opened date picker using selector: {selector}")
                    time.sleep(3)
                    return True
                except TimeoutException:
                    continue
            
            return False
            
        except Exception as e:
            print(f"❌ Failed to open date picker: {e}")
            return False
    
    def analyze_calendar(self):
        """Analyze the calendar structure"""
        try:
            print("🔍 Analyzing calendar structure...")
            
            # Get page source to see current DOM
            page_source = self.driver.page_source
            
            # Look for common calendar elements
            calendar_indicators = [
                "datepicker",
                "calendar",
                "date-picker",
                "month",
                "available",
                "disabled"
            ]
            
            found_indicators = []
            for indicator in calendar_indicators:
                if indicator.lower() in page_source.lower():
                    found_indicators.append(indicator)
            
            print(f"📋 Found calendar indicators: {found_indicators}")
            
            # Try to find available dates with different approaches
            self._find_available_dates_approach_1()
            self._find_available_dates_approach_2()
            self._find_available_dates_approach_3()
            
        except Exception as e:
            print(f"❌ Calendar analysis failed: {e}")
    
    def _find_available_dates_approach_1(self):
        """Approach 1: Look for Delta-specific date picker classes"""
        try:
            print("\n🔍 Approach 1: Delta-specific classes")
            
            selectors = [
                "td.dl-datepicker-available-day",
                "td.dl-datepicker-available-day a",
                ".dl-datepicker-available-day",
                "[class*='dl-datepicker']",
                "[class*='available-day']"
            ]
            
            for selector in selectors:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"✅ Found {len(elements)} elements with selector: {selector}")
                    for i, elem in enumerate(elements[:3]):  # Show first 3
                        try:
                            text = elem.text
                            aria_label = elem.get_attribute("aria-label")
                            data_date = elem.get_attribute("data-date")
                            print(f"   Element {i}: text='{text}', aria-label='{aria_label}', data-date='{data_date}'")
                        except:
                            pass
                else:
                    print(f"❌ No elements found for: {selector}")
                    
        except Exception as e:
            print(f"⚠️ Approach 1 failed: {e}")
    
    def _find_available_dates_approach_2(self):
        """Approach 2: Look for generic calendar elements"""
        try:
            print("\n🔍 Approach 2: Generic calendar elements")
            
            selectors = [
                "td[class*='available']",
                "button[class*='available']", 
                "a[class*='available']",
                "td:not([class*='disabled'])",
                "[aria-label*='2025']",
                "td[data-date]",
                "button[data-date]",
                "a[data-date]"
            ]
            
            for selector in selectors:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"✅ Found {len(elements)} elements with selector: {selector}")
                    for i, elem in enumerate(elements[:3]):  # Show first 3
                        try:
                            text = elem.text
                            classes = elem.get_attribute("class")
                            aria_label = elem.get_attribute("aria-label")
                            print(f"   Element {i}: text='{text}', class='{classes}', aria-label='{aria_label}'")
                        except:
                            pass
                else:
                    print(f"❌ No elements found for: {selector}")
                    
        except Exception as e:
            print(f"⚠️ Approach 2 failed: {e}")
    
    def _find_available_dates_approach_3(self):
        """Approach 3: Look for clickable date elements"""
        try:
            print("\n🔍 Approach 3: Clickable date elements")
            
            xpath_selectors = [
                "//td//a[string-length(text()) <= 2 and text() > 0]",
                "//td//button[string-length(text()) <= 2 and text() > 0]",
                "//a[contains(@aria-label, 'August') or contains(@aria-label, 'September')]",
                "//button[contains(@aria-label, 'August') or contains(@aria-label, 'September')]",
                "//td[contains(@class, 'day')]//a",
                "//td[contains(@class, 'day')]//button"
            ]
            
            for xpath in xpath_selectors:
                elements = self.driver.find_elements(By.XPATH, xpath)
                if elements:
                    print(f"✅ Found {len(elements)} elements with XPath: {xpath}")
                    for i, elem in enumerate(elements[:3]):  # Show first 3
                        try:
                            text = elem.text
                            aria_label = elem.get_attribute("aria-label")
                            onclick = elem.get_attribute("onclick")
                            print(f"   Element {i}: text='{text}', aria-label='{aria_label}', onclick='{onclick}'")
                        except:
                            pass
                else:
                    print(f"❌ No elements found for XPath: {xpath}")
                    
        except Exception as e:
            print(f"⚠️ Approach 3 failed: {e}")
    
    def test_date_selection(self, target_day=22):
        """Test selecting a specific date"""
        try:
            print(f"\n🎯 Testing date selection for day: {target_day}")
            
            # Try different approaches to click the date
            approaches = [
                ("Data attribute", f"a[data-date*='{target_day:02d}']"),
                ("Text match", f"//a[text()='{target_day}']"),
                ("Button text", f"//button[text()='{target_day}']"),
                ("Aria label", f"//*[contains(@aria-label, '{target_day}')]")
            ]
            
            for approach_name, selector in approaches:
                try:
                    if selector.startswith("//"):
                        element = WebDriverWait(self.driver, 2).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                    else:
                        element = WebDriverWait(self.driver, 2).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    
                    print(f"✅ Found clickable element using {approach_name}")
                    
                    # Try to click it
                    element.click()
                    print(f"🎉 Successfully clicked date using {approach_name}")
                    return True
                    
                except TimeoutException:
                    print(f"❌ {approach_name} approach failed - element not found")
                except Exception as e:
                    print(f"❌ {approach_name} approach failed - {e}")
            
            return False
            
        except Exception as e:
            print(f"❌ Date selection test failed: {e}")
            return False
    
    def close(self):
        """Close the browser"""
        try:
            if self.driver:
                input("\n🔍 Press Enter to close browser...")
                self.driver.quit()
                print("✅ Browser closed")
        except Exception as e:
            print(f"⚠️ Error closing browser: {e}")


def main():
    """Main test function"""
    print("🧪 Delta Date Picker Test")
    print("=" * 40)
    
    tester = None
    
    try:
        tester = DatePickerTester()
        
        # Step 1: Navigate to Delta
        if not tester.navigate_to_delta():
            return
        
        # Step 2: Open date picker
        if not tester.open_date_picker():
            print("❌ Could not open date picker, analyzing current page...")
            tester.analyze_calendar()
            return
        
        # Step 3: Analyze calendar structure
        tester.analyze_calendar()
        
        # Step 4: Test date selection
        tester.test_date_selection(22)  # Try to select day 22
        
        print("\n" + "=" * 40)
        print("🎯 Test completed! Check the output above for working selectors.")
        
    except Exception as e:
        print(f"💥 Test failed with error: {e}")
    finally:
        if tester:
            tester.close()


if __name__ == "__main__":
    main()
