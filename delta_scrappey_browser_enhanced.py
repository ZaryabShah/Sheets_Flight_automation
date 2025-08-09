"""
🎯 Enhanced Delta Flight Automation with Scrappey Browser Workflow
================================================================
This version includes multiple fallback selectors and robust error handling
for Delta's dynamic UI elements.
"""

import requests
import json
import argparse
from datetime import datetime
import time

class DeltaScrappeyBrowserWorkflowEnhanced:
    def __init__(self):
        self.scrappey_key = "CPLgrNtC9kgMlgvBpMLydXJU3wIYVhD9bvxKn0ZO8SRWPNJvpgu4Ezhwki1U"
        self.scrappey_url = "https://publisher.scrappey.com/api/v1"
        
    def create_delta_workflow_robust(self, from_airport="DEL", to_airport="BCN", departure_date="08/21/2025", trip_type="ONE_WAY"):
        """
        Create a robust Delta flight search workflow with multiple fallback selectors
        """
        print(f"🔄 Creating robust Delta workflow: {from_airport} → {to_airport} on {departure_date}")
        
        # Parse date for multiple formats
        try:
            date_obj = datetime.strptime(departure_date, "%m/%d/%Y")
            day = str(date_obj.day)
            month = date_obj.strftime("%B")  # August
            month_short = date_obj.strftime("%b")  # Aug
            year = date_obj.year
            weekday = date_obj.strftime("%A")  # Thursday
            aria_label = f"{day} {month} {year}, {weekday}"
            print(f"📅 Target date: {aria_label}")
        except:
            print("❌ Invalid date format. Using default.")
            day = "21"
            month = "August"
            year = 2025
            weekday = "Thursday"
            aria_label = "21 August 2025, Thursday"
        
        workflow = {
            "cmd": "request.get",
            "url": "https://www.delta.com/",
            "browserActions": [
                # Step 1: Navigate to Delta homepage
                {
                    "type": "goto",
                    "url": "https://www.delta.com/"
                },
                
                # Step 2: Wait for initial page load
                {
                    "type": "wait",
                    "wait": 8
                },
                
                # Step 3: Wait for booking widget to be ready
                {
                    "type": "wait_for_selector",
                    "cssSelector": "#fromAirportName, .from-container, [id*='from']",
                    "timeout": 30000
                },
                
                # Step 4: Additional wait for full initialization
                {
                    "type": "wait",
                    "wait": 3
                },
                
                # === FROM AIRPORT SELECTION ===
                
                # Step 5: Click FROM airport field (multiple selectors)
                {
                    "type": "click",
                    "cssSelector": "#fromAirportName"
                },
                
                # Step 6: Wait for modal and input field
                {
                    "type": "wait_for_selector",
                    "cssSelector": "#search_input, input[placeholder*='airport'], input[placeholder*='Airport']",
                    "timeout": 15000
                },
                
                # Step 7: Additional wait for modal to stabilize
                {
                    "type": "wait",
                    "wait": 2
                },
                
                # Step 8: Clear and type FROM airport
                {
                    "type": "type",
                    "cssSelector": "#search_input",
                    "text": from_airport
                },
                
                # Step 9: Wait for search results
                {
                    "type": "wait",
                    "wait": 3
                },
                
                # Step 10: Click first airport suggestion
                {
                    "type": "click",
                    "cssSelector": ".airportLookup-list, .airport-option, li:first-child"
                },
                
                # === TO AIRPORT SELECTION ===
                
                # Step 11: Wait and click TO airport field
                {
                    "type": "wait",
                    "wait": 3
                },
                
                {
                    "type": "click",
                    "cssSelector": "#toAirportName"
                },
                
                # Step 12: Wait for modal again
                {
                    "type": "wait_for_selector",
                    "cssSelector": "#search_input, input[placeholder*='airport']",
                    "timeout": 15000
                },
                
                # Step 13: Wait for modal stabilization
                {
                    "type": "wait",
                    "wait": 2
                },
                
                # Step 14: Clear and type TO airport
                {
                    "type": "type",
                    "cssSelector": "#search_input",
                    "text": to_airport
                },
                
                # Step 15: Wait for suggestions
                {
                    "type": "wait",
                    "wait": 3
                },
                
                # Step 16: Click first suggestion
                {
                    "type": "click",
                    "cssSelector": ".airportLookup-list, .airport-option, li:first-child"
                },
                
                # === TRIP TYPE SELECTION ===
                
                # Step 17: Wait and handle trip type
                {
                    "type": "wait",
                    "wait": 3
                },
                
                # Try to click trip type dropdown (may not be necessary if default is One Way)
                {
                    "type": "click",
                    "cssSelector": "#selectTripType_chosen, .trip-type-dropdown, [id*='TripType']"
                },
                
                {
                    "type": "wait",
                    "wait": 2
                },
                
                # Select One Way option
                {
                    "type": "click",
                    "cssSelector": "#ui-list-selectTripType1, li[data*='ONE_WAY'], li:contains('One Way')"
                },
                
                # === DATE SELECTION ===
                
                # Step 18: Click date field
                {
                    "type": "wait",
                    "wait": 3
                },
                
                {
                    "type": "click",
                    "cssSelector": "#input_departureDate_1, .calDispValueCont, [id*='departureDate']"
                },
                
                # Step 19: Wait for calendar to open
                {
                    "type": "wait_for_selector",
                    "cssSelector": ".dl-state-default, .calendar-day, [class*='calendar'] a",
                    "timeout": 15000
                },
                
                # Step 20: Additional wait for calendar to stabilize
                {
                    "type": "wait",
                    "wait": 3
                },
                
                # Step 21: Try multiple date selection strategies
                {
                    "type": "click",
                    "cssSelector": f"a[aria-label*='{day} {month} {year}']"
                },
                
                # Step 22: Wait after date selection
                {
                    "type": "wait",
                    "wait": 2
                },
                
                # Step 23: Click Done button
                {
                    "type": "click",
                    "cssSelector": ".donebutton, button[value='done'], button:contains('Done')"
                },
                
                # === SEARCH EXECUTION ===
                
                # Step 24: Wait before search
                {
                    "type": "wait",
                    "wait": 3
                },
                
                # Step 25: Click search button
                {
                    "type": "click",
                    "cssSelector": "#btn-book-submit"
                },
                
                # === WAIT FOR RESULTS ===
                
                # Step 26: Initial wait for navigation
                {
                    "type": "wait",
                    "wait": 10
                },
                
                # Step 27: Wait for results page elements
                {
                    "type": "wait_for_selector",
                    "cssSelector": ".flight-results-grid, [class*='flight-card'], [class*='flight-results'], [class*='search-results']",
                    "timeout": 90000
                },
                
                # Step 28: Wait for complete page load
                {
                    "type": "wait",
                    "wait": 15
                },
                
                # Step 29: Try to click price tab if it exists
                {
                    "type": "click",
                    "cssSelector": "button:nth-child(2), .price-tab, [class*='price'] button"
                },
                
                # Step 30: Final wait for all content
                {
                    "type": "wait",
                    "wait": 10
                }
            ]
        }
        
        return workflow
    
    def create_fallback_date_workflow(self, from_airport, to_airport):
        """
        Create a workflow that selects any available date if specific date fails
        """
        return {
            "cmd": "request.get",
            "url": "https://www.delta.com/",
            "browserActions": [
                {"type": "goto", "url": "https://www.delta.com/"},
                {"type": "wait", "wait": 8},
                {"type": "wait_for_selector", "cssSelector": "#fromAirportName", "timeout": 30000},
                {"type": "wait", "wait": 3},
                
                # FROM airport
                {"type": "click", "cssSelector": "#fromAirportName"},
                {"type": "wait_for_selector", "cssSelector": "#search_input", "timeout": 15000},
                {"type": "wait", "wait": 2},
                {"type": "type", "cssSelector": "#search_input", "text": from_airport},
                {"type": "wait", "wait": 3},
                {"type": "click", "cssSelector": ".airportLookup-list"},
                
                # TO airport
                {"type": "wait", "wait": 3},
                {"type": "click", "cssSelector": "#toAirportName"},
                {"type": "wait_for_selector", "cssSelector": "#search_input", "timeout": 15000},
                {"type": "wait", "wait": 2},
                {"type": "type", "cssSelector": "#search_input", "text": to_airport},
                {"type": "wait", "wait": 3},
                {"type": "click", "cssSelector": ".airportLookup-list"},
                
                # Date - click any available date
                {"type": "wait", "wait": 3},
                {"type": "click", "cssSelector": "#input_departureDate_1"},
                {"type": "wait_for_selector", "cssSelector": ".dl-state-default", "timeout": 15000},
                {"type": "wait", "wait": 3},
                {"type": "click", "cssSelector": ".dl-state-default:not([class*='disabled'])"}, # Any available date
                {"type": "wait", "wait": 2},
                {"type": "click", "cssSelector": ".donebutton"},
                
                # Search
                {"type": "wait", "wait": 3},
                {"type": "click", "cssSelector": "#btn-book-submit"},
                {"type": "wait", "wait": 10},
                {"type": "wait_for_selector", "cssSelector": ".flight-results-grid, [class*='flight-card']", "timeout": 90000},
                {"type": "wait", "wait": 15}
            ]
        }
    
    def execute_workflow(self, workflow, workflow_name="Main"):
        """
        Execute workflow with detailed logging
        """
        try:
            print(f"🚀 Executing {workflow_name} workflow...")
            print(f"📊 Workflow has {len(workflow['browserActions'])} browser actions")
            
            headers = {'Content-Type': 'application/json'}
            params = {'key': self.scrappey_key}
            
            # Start execution
            start_time = time.time()
            response = requests.post(
                self.scrappey_url, 
                params=params, 
                headers=headers, 
                json=workflow,
                timeout=600  # 10 minutes timeout
            )
            
            execution_time = time.time() - start_time
            print(f"⏱️ Execution time: {execution_time:.1f} seconds")
            print(f"📡 HTTP Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                
                if "solution" in result:
                    solution = result["solution"]
                    http_status = solution.get("status", 0)
                    response_html = solution.get("response", "")
                    
                    print(f"✅ {workflow_name} workflow completed!")
                    print(f"📊 Final HTTP Status: {http_status}")
                    print(f"📄 Response length: {len(response_html):,} characters")
                    
                    # Check for Delta-specific content
                    if response_html:
                        has_flights = any(keyword in response_html.lower() for keyword in 
                                        ['flight-results', 'flight-card', 'price', 'departure', 'arrival'])
                        has_delta = 'delta' in response_html.lower()
                        print(f"🔍 Contains flight data: {has_flights}")
                        print(f"🔍 Contains Delta branding: {has_delta}")
                    
                    return {
                        "success": http_status == 200,
                        "status": http_status,
                        "html": response_html,
                        "length": len(response_html),
                        "execution_time": execution_time,
                        "workflow": workflow_name
                    }
                else:
                    error_msg = result.get("error", "Unknown Scrappey error")
                    print(f"❌ Scrappey error: {error_msg}")
                    return {"success": False, "error": error_msg, "workflow": workflow_name}
            else:
                print(f"❌ HTTP request failed: {response.status_code}")
                try:
                    error_detail = response.json()
                    print(f"Error details: {error_detail}")
                except:
                    print(f"Response text: {response.text[:500]}")
                return {"success": False, "error": f"HTTP {response.status_code}", "workflow": workflow_name}
                
        except Exception as e:
            print(f"❌ {workflow_name} workflow failed: {e}")
            return {"success": False, "error": str(e), "workflow": workflow_name}
    
    def save_results(self, result, from_airport, to_airport, departure_date):
        """
        Save results with detailed metadata
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Save HTML
            filename = f"delta_scrappey_{result['workflow'].lower()}_{from_airport}_{to_airport}_{departure_date.replace('/', '-')}_{timestamp}.html"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(result["html"])
            
            # Create metadata
            metadata = {
                "search_params": {
                    "from_airport": from_airport,
                    "to_airport": to_airport,
                    "departure_date": departure_date,
                    "timestamp": timestamp
                },
                "execution": {
                    "workflow": result["workflow"],
                    "success": result["success"],
                    "status": result.get("status"),
                    "execution_time": result.get("execution_time", 0),
                    "html_length": len(result["html"])
                },
                "analysis": {
                    "has_delta_branding": "delta" in result["html"].lower(),
                    "has_flight_data": any(kw in result["html"].lower() for kw in 
                                         ['flight-results', 'flight-card', 'price', 'departure']),
                    "likely_success": len(result["html"]) > 50000  # Rough heuristic
                }
            }
            
            # Save metadata
            meta_filename = f"delta_scrappey_metadata_{timestamp}.json"
            with open(meta_filename, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            print(f"💾 Results saved:")
            print(f"   📄 HTML: {filename} ({len(result['html']):,} chars)")
            print(f"   📋 Metadata: {meta_filename}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to save results: {e}")
            return False
    
    def search_flights_comprehensive(self, from_airport="DEL", to_airport="BCN", departure_date="08/21/2025"):
        """
        Comprehensive flight search with multiple strategies
        """
        print("🎯 COMPREHENSIVE DELTA FLIGHT SEARCH")
        print("=" * 70)
        print(f"📍 Route: {from_airport} → {to_airport}")
        print(f"📅 Date: {departure_date}")
        print("=" * 70)
        
        strategies = [
            ("Robust Workflow", lambda: self.create_delta_workflow_robust(from_airport, to_airport, departure_date)),
            ("Fallback Any Date", lambda: self.create_fallback_date_workflow(from_airport, to_airport))
        ]
        
        for strategy_name, workflow_creator in strategies:
            print(f"\n🔄 Trying {strategy_name}...")
            
            workflow = workflow_creator()
            result = self.execute_workflow(workflow, strategy_name)
            
            if result.get("success") and result.get("length", 0) > 10000:
                print(f"✅ {strategy_name} SUCCESS!")
                self.save_results(result, from_airport, to_airport, departure_date)
                return result
            else:
                print(f"❌ {strategy_name} failed or insufficient content")
                if result.get("html"):
                    # Save partial results for debugging
                    debug_filename = f"debug_{strategy_name.lower().replace(' ', '_')}_{datetime.now().strftime('%H%M%S')}.html"
                    with open(debug_filename, 'w', encoding='utf-8') as f:
                        f.write(result["html"])
                    print(f"🔍 Debug HTML saved: {debug_filename}")
        
        print("\n❌ All strategies failed to get comprehensive results")
        return {"success": False, "error": "All strategies exhausted"}

def main():
    parser = argparse.ArgumentParser(description='Enhanced Delta Flight Search with Scrappey Browser Workflow')
    parser.add_argument('--from', dest='from_airport', default='DEL', help='Origin airport code')
    parser.add_argument('--to', dest='to_airport', default='BCN', help='Destination airport code')
    parser.add_argument('--date', dest='departure_date', default='08/21/2025', help='Departure date (MM/DD/YYYY)')
    
    args = parser.parse_args()
    
    # Validate date
    try:
        datetime.strptime(args.departure_date, '%m/%d/%Y')
    except ValueError:
        print("❌ Invalid date format. Use MM/DD/YYYY")
        return
    
    # Execute comprehensive search
    automation = DeltaScrappeyBrowserWorkflowEnhanced()
    result = automation.search_flights_comprehensive(
        from_airport=args.from_airport,
        to_airport=args.to_airport,
        departure_date=args.departure_date
    )
    
    # Final summary
    print("\n" + "=" * 70)
    if result.get("success"):
        print(f"🎉 SUCCESS: Complete Delta flight data captured!")
        print(f"📊 Total content: {result.get('length', 0):,} characters")
    else:
        print(f"😞 FAILED: {result.get('error', 'Unknown error')}")
    print("=" * 70)

if __name__ == "__main__":
    main()
