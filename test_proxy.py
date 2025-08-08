"""
Proxy Test Script for Selenium
=============================
Test the Oxylabs proxy before integrating into the main automation
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests


def test_proxy_connection():
    """Test if the proxy is working with basic requests"""
    print("🔄 Testing proxy connection with requests...")
    
    proxy_url = "https://pr.oxylabs.io:10000"
    
    # Parse proxy URL
    proxy_host = "pr.oxylabs.io"
    proxy_port = "10000"
    
    proxies = {
        'http': f'http://{proxy_host}:{proxy_port}',
        'https': f'https://{proxy_host}:{proxy_port}'
    }
    
    try:
        # Test with a simple request
        response = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=10)
        print(f"✅ Proxy test successful! Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Proxy test failed: {e}")
        return False


def test_selenium_with_proxy():
    """Test Selenium with the proxy configuration"""
    print("🔄 Testing Selenium with proxy...")
    
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
        
        # Proxy configuration
        proxy_host = "pr.oxylabs.io"
        proxy_port = "10000"
        proxy_url = f"{proxy_host}:{proxy_port}"
        
        # Add proxy to Chrome options
        chrome_options.add_argument(f'--proxy-server=https://{proxy_url}')
        
        # Optional: If proxy requires authentication, you might need these
        # chrome_options.add_argument('--proxy-auth=username:password')
        
        # Window size and user agent
        chrome_options.add_argument("--window-size=1280,720")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        # Initialize driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("✅ Chrome driver initialized with proxy")
        
        # Test navigation to check IP
        print("🔄 Testing navigation to check IP...")
        driver.get("http://httpbin.org/ip")
        
        # Wait for page to load
        time.sleep(3)
        
        # Get page content
        page_source = driver.page_source
        print(f"📄 Page content: {page_source[:500]}...")
        
        # Test navigation to Delta (the actual target)
        print("🔄 Testing navigation to Delta website...")
        driver.get("https://www.delta.com")
        
        # Wait for page to load
        WebDriverWait(driver, 30).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        
        time.sleep(5)
        
        # Check if page loaded successfully
        title = driver.title
        print(f"✅ Delta page loaded successfully! Title: {title}")
        
        # Take a screenshot for verification
        driver.save_screenshot("proxy_test_delta.png")
        print("📸 Screenshot saved as proxy_test_delta.png")
        
        return True
        
    except Exception as e:
        print(f"❌ Selenium proxy test failed: {e}")
        return False
    finally:
        if driver:
            driver.quit()
            print("🔄 Browser closed")


def test_selenium_with_manual_proxy():
    """Test Selenium with manual proxy configuration"""
    print("🔄 Testing Selenium with manual proxy configuration...")
    
    driver = None
    try:
        from selenium.webdriver.common.proxy import Proxy, ProxyType
        
        # Create proxy object
        proxy = Proxy()
        proxy.proxy_type = ProxyType.MANUAL
        proxy.http_proxy = "pr.oxylabs.io:10000"
        proxy.ssl_proxy = "pr.oxylabs.io:10000"
        
        # Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1280,720")
        
        # Add proxy to capabilities
        capabilities = webdriver.DesiredCapabilities.CHROME
        proxy.add_to_capabilities(capabilities)
        
        # Initialize driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(
            service=service, 
            options=chrome_options,
            desired_capabilities=capabilities
        )
        
        print("✅ Chrome driver initialized with manual proxy")
        
        # Test navigation
        driver.get("http://httpbin.org/ip")
        time.sleep(3)
        
        print("✅ Manual proxy test completed")
        return True
        
    except Exception as e:
        print(f"❌ Manual proxy test failed: {e}")
        return False
    finally:
        if driver:
            driver.quit()


def main():
    """Run all proxy tests"""
    print("🧪 PROXY TESTING SUITE")
    print("=" * 50)
    
    tests = [
        ("Basic Proxy Connection", test_proxy_connection),
        ("Selenium with Proxy Arguments", test_selenium_with_proxy),
        ("Selenium with Manual Proxy", test_selenium_with_manual_proxy)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        print("-" * 30)
        try:
            result = test_func()
            results[test_name] = "✅ PASSED" if result else "❌ FAILED"
        except Exception as e:
            results[test_name] = f"❌ ERROR: {e}"
        
        time.sleep(2)  # Brief pause between tests
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    for test_name, result in results.items():
        print(f"{test_name}: {result}")
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS:")
    passed_tests = [name for name, result in results.items() if "PASSED" in result]
    
    if passed_tests:
        print(f"✅ Working methods: {', '.join(passed_tests)}")
        print("🚀 Ready to integrate proxy into Delta automation!")
    else:
        print("❌ No proxy methods worked. Check:")
        print("   - Proxy URL and port are correct")
        print("   - Proxy requires authentication")
        print("   - Network/firewall restrictions")
    
    input("\n⏸️ Press Enter to exit...")


if __name__ == "__main__":
    main()
