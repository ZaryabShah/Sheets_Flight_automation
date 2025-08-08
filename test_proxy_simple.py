"""
Simple Proxy Test - Working Configuration
========================================
Test the confirmed working proxy setup
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


def test_working_proxy():
    """Test the confirmed working proxy configuration"""
    print("🔄 Testing confirmed working proxy setup...")
    
    driver = None
    try:
        # Chrome options
        chrome_options = Options()
        
        # Basic options
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Proxy configuration that works
        proxy_host = "pr.oxylabs.io"
        proxy_port = "10000"
        proxy_url = f"{proxy_host}:{proxy_port}"
        
        # Add proxy to Chrome options
        chrome_options.add_argument(f'--proxy-server=https://{proxy_url}')
        
        # Window size and user agent
        chrome_options.add_argument("--window-size=1280,720")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        # Initialize driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("✅ Chrome driver initialized with proxy")
        
        # Test 1: Check IP
        print("🔄 Test 1: Checking IP address...")
        driver.get("http://httpbin.org/ip")
        time.sleep(3)
        
        page_text = driver.find_element("tag name", "body").text
        print(f"✅ IP Response: {page_text}")
        
        # Test 2: Check simple website
        print("🔄 Test 2: Testing Google...")
        driver.get("https://www.google.com")
        time.sleep(3)
        
        title = driver.title
        print(f"✅ Google loaded: {title}")
        
        print("🎉 Proxy configuration confirmed working!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    finally:
        if driver:
            try:
                driver.quit()
                print("🔄 Browser closed")
            except:
                pass  # Ignore cleanup errors


if __name__ == "__main__":
    test_working_proxy()
