#!/usr/bin/env python3
"""
Test script to verify WebRTC IP leak protection and proxy functionality.
"""

import sys
import os
import importlib.util

# Import the module with space in filename
spec = importlib.util.spec_from_file_location(
    "delta_flight_automation_advanced_copy", 
    "delta_flight_automation_advanced copy.py"
)
advanced_copy_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(advanced_copy_module)
DeltaFlightAutomationAdvanced = advanced_copy_module.DeltaFlightAutomationAdvanced

import time

def test_ip_leak_protection():
    """Test WebRTC IP leak protection with and without proxy"""
    print("🔒 Testing IP Leak Protection")
    print("=" * 60)
    
    # Test 1: With proxy (should show proxy IP only)
    print("\n1️⃣ Testing WITH PROXY")
    print("-" * 30)
    
    try:
        automation_proxy = DeltaFlightAutomationAdvanced(
            headless=False,
            use_proxy=True  # This should now actually work
        )
        
        print("🔍 Checking IP with proxy...")
        automation_proxy.driver.get("https://httpbin.org/ip")
        time.sleep(3)
        proxy_ip_content = automation_proxy.driver.page_source
        print("Proxy IP result:")
        print(proxy_ip_content[:500])
        
        print("\n🔍 Checking WebRTC with proxy...")
        webrtc_secure = automation_proxy.verify_webrtc()
        
        automation_proxy.close()
        
        print(f"✅ Proxy test completed. WebRTC secure: {webrtc_secure}")
        
    except Exception as e:
        print(f"❌ Proxy test failed: {e}")
    
    time.sleep(2)
    
    # Test 2: Without proxy (should show real IP but no WebRTC leaks)
    print("\n2️⃣ Testing WITHOUT PROXY")
    print("-" * 30)
    
    try:
        automation_no_proxy = DeltaFlightAutomationAdvanced(
            headless=False,
            use_proxy=False  # This should now actually disable proxy
        )
        
        print("🔍 Checking IP without proxy...")
        automation_no_proxy.driver.get("https://httpbin.org/ip")
        time.sleep(3)
        direct_ip_content = automation_no_proxy.driver.page_source
        print("Direct IP result:")
        print(direct_ip_content[:500])
        
        print("\n🔍 Checking WebRTC without proxy...")
        webrtc_secure = automation_no_proxy.verify_webrtc()
        
        automation_no_proxy.close()
        
        print(f"✅ No-proxy test completed. WebRTC secure: {webrtc_secure}")
        
    except Exception as e:
        print(f"❌ No-proxy test failed: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 IP Leak Protection Test Summary:")
    print("   - Proxy should show Oxylabs IP")
    print("   - No-proxy should show your real IP") 
    print("   - WebRTC should be secure in both cases")
    print("   - No ISP IP should leak through WebRTC when using proxy")

def test_browserleaks_comprehensive():
    """Comprehensive test using browserleaks.com"""
    print("\n🌐 Comprehensive BrowserLeaks Test")
    print("=" * 60)
    
    try:
        automation = DeltaFlightAutomationAdvanced(
            headless=False,
            use_proxy=True
        )
        
        print("🔍 Testing comprehensive leak detection...")
        automation.driver.get("https://browserleaks.com/ip")
        
        print("⏱️ Waiting 10 seconds for all tests to complete...")
        time.sleep(10)
        
        print("🔍 Results loaded. Please manually verify:")
        print("   ✅ HTTP IP should show Oxylabs proxy IP")
        print("   ✅ WebRTC should show NO public IP or proxy IP only")
        print("   ❌ Should NOT show your ISP's real IP anywhere")
        
        input("\n👁️ Please check the browser and press Enter when done...")
        
        automation.close()
        
    except Exception as e:
        print(f"❌ BrowserLeaks test failed: {e}")

if __name__ == "__main__":
    print("🚀 Starting IP Leak Protection Tests")
    print("This will test the fixes for:")
    print("  1. Constructor proxy bug (use_proxy=False now works)")
    print("  2. WebRTC IP leak protection")
    print("  3. Proper proxy configuration")
    print()
    
    # Run the tests
    test_ip_leak_protection()
    
    # Optional comprehensive test
    response = input("\n🌐 Run comprehensive BrowserLeaks test? (y/n): ")
    if response.lower() == 'y':
        test_browserleaks_comprehensive()
    
    print("\n🎉 Testing completed!")
    print("Key fixes applied:")
    print("  ✅ Fixed constructor bug: self.use_proxy = use_proxy")
    print("  ✅ Added WebRTC hardening: proxy_only policy")
    print("  ✅ Changed proxy format: http:// instead of https://")
    print("  ✅ Added WebRTC preferences for extra security")
    print("  ✅ Updated headless mode to --headless=new")
