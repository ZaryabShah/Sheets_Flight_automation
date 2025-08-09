#!/usr/bin/env python3
"""
Comprehensive test script for Delta flight automation with Scrappey.com API integration
Tests both the Node.js API fetcher and Python integration layer
"""

import sys
import os
import json
import time
from datetime import datetime, timedelta

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

from scrappey_delta_integration import ScrappeyDeltaFetcher, DeltaFlightAutomationWithAPI

def test_node_setup():
    """Test Node.js environment and dependencies"""
    print("🔧 Testing Node.js setup...")
    
    try:
        import subprocess
        
        # Check Node.js version
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js: {result.stdout.strip()}")
        else:
            print("❌ Node.js not found")
            return False
        
        # Check npm version  
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ npm: {result.stdout.strip()}")
        else:
            print("❌ npm not found")
            return False
        
        # Check if scrappey-wrapper is installed
        if os.path.exists(os.path.join(os.path.dirname(__file__), "node_modules", "scrappey-wrapper")):
            print("✅ scrappey-wrapper package installed")
        else:
            print("❌ scrappey-wrapper package not found")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Node.js setup test failed: {e}")
        return False

def test_scrappey_fetcher(api_key: str):
    """Test the Scrappey Delta fetcher"""
    print("\n🛫 Testing Scrappey Delta fetcher...")
    
    try:
        # Initialize fetcher with debug mode
        fetcher = ScrappeyDeltaFetcher(api_key, debug=True)
        
        # Test connection first
        print("📡 Testing API connection...")
        if not fetcher.test_connection():
            print("❌ API connection test failed")
            return False
        
        print("✅ API connection successful")
        
        # Test basic flight search
        print("🔍 Testing flight search...")
        
        # Use a date 30 days from now
        test_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        
        results = fetcher.search_flights(
            origin="JFK",
            destination="LAX", 
            departure_date=test_date,
            passenger_count=1,
            cabin_class="COACH"
        )
        
        if results:
            print(f"✅ Flight search successful")
            print(f"📊 Raw data keys: {list(results.keys())}")
            
            # Format the data
            formatted_flights = fetcher.format_flight_data(results)
            print(f"✅ Formatted {len(formatted_flights)} flights")
            
            # Display sample flights
            if formatted_flights:
                print(f"\n📋 Sample flights (showing first 3):")
                for i, flight in enumerate(formatted_flights[:3]):
                    print(f"  Flight {i+1}:")
                    print(f"    Number: {flight.get('flight_number', 'N/A')}")
                    print(f"    Route: {flight.get('origin', 'N/A')} → {flight.get('destination', 'N/A')}")
                    print(f"    Time: {flight.get('departure_time', 'N/A')} → {flight.get('arrival_time', 'N/A')}")
                    print(f"    Price: {flight.get('price', 'N/A')} {flight.get('currency', 'USD')}")
                    print(f"    Duration: {flight.get('duration', 'N/A')}")
                    print(f"    Stops: {flight.get('stops', 'N/A')}")
                    print()
            
            return True
        else:
            print("❌ Flight search returned no results")
            return False
            
    except Exception as e:
        print(f"❌ Scrappey fetcher test failed: {e}")
        return False

def test_multi_page_search(api_key: str):
    """Test multi-page flight search"""
    print("\n📄 Testing multi-page search...")
    
    try:
        fetcher = ScrappeyDeltaFetcher(api_key, debug=True)
        
        test_date = (datetime.now() + timedelta(days=45)).strftime("%Y-%m-%d")
        
        results = fetcher.search_flights_multi_page(
            origin="MCO",  # Orlando
            destination="BCN",  # Barcelona
            departure_date=test_date,
            max_pages=2,  # Limit to 2 pages for testing
            passenger_count=1,
            cabin_class="COACH"
        )
        
        if results:
            total_flights = len(results.get('flights', []))
            pages_fetched = results.get('pages_fetched', 1)
            print(f"✅ Multi-page search successful: {total_flights} flights from {pages_fetched} pages")
            return True
        else:
            print("❌ Multi-page search failed")
            return False
            
    except Exception as e:
        print(f"❌ Multi-page search test failed: {e}")
        return False

def test_hybrid_automation(api_key: str):
    """Test the hybrid automation system"""
    print("\n🤖 Testing hybrid automation...")
    
    try:
        # Initialize hybrid system (API-only mode for now)
        hybrid_bot = DeltaFlightAutomationWithAPI(
            scrappey_api_key=api_key,
            use_selenium=False,  # Disable Selenium for this test
            debug=True
        )
        
        test_date = (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d")
        
        results = hybrid_bot.search_flights_hybrid(
            origin="LAX",
            destination="JFK", 
            departure_date=test_date,
            use_api_fallback=True
        )
        
        print(f"✅ Hybrid search completed")
        print(f"📊 Sources used: {results.get('sources_used', [])}")
        print(f"📊 API flights found: {len(results.get('api_flights', []))}")
        print(f"📊 Combined flights: {len(results.get('combined_flights', []))}")
        
        return True
        
    except Exception as e:
        print(f"❌ Hybrid automation test failed: {e}")
        return False

def test_error_handling(api_key: str):
    """Test error handling and edge cases"""
    print("\n🚫 Testing error handling...")
    
    try:
        fetcher = ScrappeyDeltaFetcher(api_key, debug=True)
        
        # Test with invalid airport codes
        print("🔍 Testing invalid airport codes...")
        results = fetcher.search_flights("XXX", "YYY", "2025-12-25")
        
        if results is None:
            print("✅ Invalid airport codes handled correctly")
        else:
            print("⚠️ Invalid airport codes returned unexpected results")
        
        # Test with past date
        print("🔍 Testing past date...")
        past_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        results = fetcher.search_flights("JFK", "LAX", past_date)
        
        if results is None:
            print("✅ Past date handled correctly")
        else:
            print("⚠️ Past date returned unexpected results")
        
        return True
        
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False

def main():
    """Main test runner"""
    print("🚀 Starting comprehensive Delta flight automation tests")
    print("=" * 60)
    
    # Check if API key is provided
    api_key = input("Please enter your Scrappey.com API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided. Exiting...")
        return False
    
    # Store API key for potential reuse
    with open(".env.test", "w") as f:
        f.write(f"SCRAPPEY_API_KEY={api_key}\n")
    print("💾 API key saved to .env.test file")
    
    test_results = {}
    
    # Run all tests
    test_results['node_setup'] = test_node_setup()
    
    if test_results['node_setup']:
        test_results['scrappey_fetcher'] = test_scrappey_fetcher(api_key)
        test_results['multi_page_search'] = test_multi_page_search(api_key) 
        test_results['hybrid_automation'] = test_hybrid_automation(api_key)
        test_results['error_handling'] = test_error_handling(api_key)
    else:
        print("❌ Node.js setup failed, skipping other tests")
        return False
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
    
    all_passed = all(test_results.values())
    
    if all_passed:
        print("\n🎉 All tests passed! Your Delta automation with Scrappey API is ready to use.")
        print("\n📚 Next steps:")
        print("1. Integrate with your main delta_flight_automation_advanced.py")
        print("2. Add the Scrappey fetcher to your automation workflow")
        print("3. Configure your preferred search parameters")
        print("4. Test with real flight searches")
    else:
        print("\n⚠️ Some tests failed. Please check the errors above and fix issues before proceeding.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
