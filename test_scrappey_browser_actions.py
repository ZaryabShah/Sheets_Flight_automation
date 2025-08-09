"""
🧪 Scrappey Browser Actions Test
===============================
Test basic browser actions workflow to verify the format is working
"""

import requests
import json

def test_basic_workflow():
    """Test basic browser workflow with simple actions"""
    
    scrappey_key = "CPLgrNtC9kgMlgvBpMLydXJU3wIYVhD9bvxKn0ZO8SRWPNJvpgu4Ezhwki1U"
    scrappey_url = "https://publisher.scrappey.com/api/v1"
    
    # Simple test workflow
    test_workflow = {
        "cmd": "request.get",
        "url": "https://httpbin.rs/get",
        "browserActions": [
            {
                "type": "goto",
                "url": "https://example.com"
            },
            {
                "type": "wait",
                "wait": 3
            },
            {
                "type": "wait_for_selector",
                "cssSelector": "body",
                "timeout": 10000
            }
        ]
    }
    
    headers = {'Content-Type': 'application/json'}
    params = {'key': scrappey_key}
    
    print("🧪 Testing basic browser actions workflow...")
    print(f"📊 Test workflow has {len(test_workflow['browserActions'])} actions")
    
    try:
        response = requests.post(
            scrappey_url, 
            params=params, 
            headers=headers, 
            json=test_workflow,
            timeout=60
        )
        
        print(f"📡 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            if "solution" in result:
                solution = result["solution"]
                http_status = solution.get("status", 0)
                response_html = solution.get("response", "")
                
                print(f"✅ Workflow executed!")
                print(f"📊 HTTP Status: {http_status}")
                print(f"📄 Response length: {len(response_html)} characters")
                
                if http_status == 200 and response_html:
                    print("✅ Basic browserActions workflow is working!")
                    print(f"📄 First 200 chars: {response_html[:200]}")
                    return True
                else:
                    print(f"❌ HTTP error: {http_status}")
                    if response_html:
                        print(f"📄 Error content: {response_html[:500]}")
                    return False
            else:
                error_msg = result.get("error", "Unknown error")
                print(f"❌ Scrappey error: {error_msg}")
                return False
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_delta_simple():
    """Test simple Delta page access"""
    
    scrappey_key = "CPLgrNtC9kgMlgvBpMLydXJU3wIYVhD9bvxKn0ZO8SRWPNJvpgu4Ezhwki1U"
    scrappey_url = "https://publisher.scrappey.com/api/v1"
    
    # Simple Delta access
    delta_workflow = {
        "cmd": "request.get",
        "url": "https://www.delta.com/",
        "browserActions": [
            {
                "type": "goto",
                "url": "https://www.delta.com/"
            },
            {
                "type": "wait",
                "wait": 5
            },
            {
                "type": "wait_for_selector",
                "cssSelector": "body",
                "timeout": 15000
            }
        ]
    }
    
    headers = {'Content-Type': 'application/json'}
    params = {'key': scrappey_key}
    
    print("\n🧪 Testing simple Delta page access...")
    
    try:
        response = requests.post(
            scrappey_url, 
            params=params, 
            headers=headers, 
            json=delta_workflow,
            timeout=120
        )
        
        print(f"📡 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            if "solution" in result:
                solution = result["solution"]
                http_status = solution.get("status", 0)
                response_html = solution.get("response", "")
                
                print(f"📊 HTTP Status: {http_status}")
                print(f"📄 Response length: {len(response_html)} characters")
                
                if http_status == 200 and response_html:
                    print("✅ Delta page access working!")
                    
                    # Check for Delta-specific content
                    has_delta = "delta" in response_html.lower()
                    has_booking = any(word in response_html.lower() for word in 
                                    ["book", "flight", "search", "airport"])
                    
                    print(f"🔍 Contains Delta branding: {has_delta}")
                    print(f"🔍 Contains booking elements: {has_booking}")
                    
                    # Save for inspection
                    with open("delta_simple_test.html", "w", encoding="utf-8") as f:
                        f.write(response_html)
                    print("💾 HTML saved to: delta_simple_test.html")
                    
                    return True
                else:
                    print(f"❌ HTTP error: {http_status}")
                    return False
            else:
                error_msg = result.get("error", "Unknown error")
                print(f"❌ Scrappey error: {error_msg}")
                return False
        else:
            print(f"❌ Request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    print("🧪 SCRAPPEY BROWSER ACTIONS TESTING")
    print("=" * 50)
    
    # Test 1: Basic workflow
    basic_success = test_basic_workflow()
    
    # Test 2: Delta access
    delta_success = test_delta_simple()
    
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY:")
    print(f"   Basic browserActions: {'✅ PASS' if basic_success else '❌ FAIL'}")
    print(f"   Delta page access: {'✅ PASS' if delta_success else '❌ FAIL'}")
    
    if basic_success and delta_success:
        print("\n🎉 All tests passed! browserActions format is working correctly")
        print("💡 The issue with Delta automation is likely proxy connectivity, not workflow format")
    elif basic_success:
        print("\n⚠️ Basic actions work but Delta access failed")
        print("💡 This could be proxy blocking or Delta's anti-bot measures")
    else:
        print("\n❌ Basic browserActions not working")
        print("💡 Check Scrappey API key or service status")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
