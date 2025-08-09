"""
🎯 Delta Flight Automation with Scrappey Browser Workflow
========================================================
This uses Scrappey's browserActions API to automate Delta flight search
and return the complete raw HTML response.
"""

import requests
import json
import argparse
from datetime import datetime
import time

class DeltaScrappeyBrowserWorkflow:
    def __init__(self):
        self.scrappey_key = "CPLgrNtC9kgMlgvBpMLydXJU3wIYVhD9bvxKn0ZO8SRWPNJvpgu4Ezhwki1U"
        self.scrappey_url = "https://publisher.scrappey.com/api/v1"
        
    def create_delta_workflow(self, from_airport="DEL", to_airport="BCN", departure_date="08/21/2025", trip_type="ONE_WAY"):
        """
        Create the complete Delta flight search workflow using browserActions
        """
        print(f"🔄 Creating Delta workflow: {from_airport} → {to_airport} on {departure_date}")
        
        # Parse date for aria-label format
        try:
            date_obj = datetime.strptime(departure_date, "%m/%d/%Y")
            day = date_obj.day
            month = date_obj.strftime("%B")  # Full month name
            year = date_obj.year
            weekday = date_obj.strftime("%A")  # Full weekday name
            aria_label = f"{day} {month} {year}, {weekday}"
            date_data_attr = f"{departure_date}|{date_obj.strftime('%a, %b %d')}|{aria_label}"
            print(f"📅 Target date: {aria_label}")
        except:
            print("❌ Invalid date format. Using default.")
            day = "21"
            aria_label = "21 August 2025, Thursday"
            date_data_attr = "08/21/2025|T, Aug 21|21 August 2025, Thursday"
        
        workflow = {
            "cmd": "request.get",
            "url": "https://www.delta.com/",
            "browserActions": [
                # Step 1: Navigate to Delta homepage
                {
                    "type": "goto",
                    "url": "https://www.delta.com/"
                },
                
                # Step 2: Wait for page to load
                {
                    "type": "wait",
                    "wait": 5
                },
                
                # Step 3: Wait for main booking form to be visible
                {
                    "type": "wait_for_selector",
                    "cssSelector": "#fromAirportName",
                    "timeout": 30000
                },
                
                # Step 4: Click on FROM airport field
                {
                    "type": "click",
                    "cssSelector": "#fromAirportName"
                },
                
                # Step 5: Wait for airport search modal
                {
                    "type": "wait_for_selector",
                    "cssSelector": "#search_input",
                    "timeout": 10000
                },
                
                # Step 6: Type FROM airport code
                {
                    "type": "type",
                    "cssSelector": "#search_input",
                    "text": from_airport
                },
                
                # Step 7: Wait for suggestions
                {
                    "type": "wait",
                    "wait": 2
                },
                
                # Step 8: Click first airport suggestion
                {
                    "type": "click",
                    "cssSelector": ".airportLookup-list"
                },
                
                # Step 9: Wait and click TO airport field
                {
                    "type": "wait",
                    "wait": 2
                },
                
                {
                    "type": "click",
                    "cssSelector": "#toAirportName"
                },
                
                # Step 10: Wait for airport search modal again
                {
                    "type": "wait_for_selector",
                    "cssSelector": "#search_input",
                    "timeout": 10000
                },
                
                # Step 11: Clear and type TO airport code
                {
                    "type": "type",
                    "cssSelector": "#search_input",
                    "text": to_airport
                },
                
                # Step 12: Wait for suggestions
                {
                    "type": "wait",
                    "wait": 2
                },
                
                # Step 13: Click first airport suggestion
                {
                    "type": "click",
                    "cssSelector": ".airportLookup-list"
                },
                
                # Step 14: Select trip type if needed (One Way)
                {
                    "type": "wait",
                    "wait": 2
                },
                
                {
                    "type": "click",
                    "cssSelector": "#selectTripType_chosen"
                },
                
                {
                    "type": "wait",
                    "wait": 1
                },
                
                {
                    "type": "click",
                    "cssSelector": "#ui-list-selectTripType1"  # One Way option
                },
                
                # Step 15: Click on date field
                {
                    "type": "wait",
                    "wait": 2
                },
                
                {
                    "type": "click",
                    "cssSelector": "#input_departureDate_1"
                },
                
                # Step 16: Wait for calendar to open
                {
                    "type": "wait_for_selector",
                    "cssSelector": ".dl-state-default",
                    "timeout": 10000
                },
                
                # Step 17: Click on specific date (try multiple selectors)
                {
                    "type": "click",
                    "cssSelector": f"a[aria-label*='{day} {month} {year}']"
                },
                
                # Step 18: Click Done button in calendar
                {
                    "type": "wait",
                    "wait": 1
                },
                
                {
                    "type": "click",
                    "cssSelector": ".donebutton"
                },
                
                # Step 19: Click Search button
                {
                    "type": "wait",
                    "wait": 2
                },
                
                {
                    "type": "click",
                    "cssSelector": "#btn-book-submit"
                },
                
                # Step 20: Wait for results page to load completely
                {
                    "type": "wait",
                    "wait": 15
                },
                
                # Step 21: Wait for flight results
                {
                    "type": "wait_for_selector",
                    "cssSelector": ".flight-results-grid, [class*='flight-card'], [class*='flight-results']",
                    "timeout": 60000
                },
                
                # Step 22: Additional wait for complete page load
                {
                    "type": "wait",
                    "wait": 10
                }
            ]
        }
        
        return workflow
    
    def execute_workflow(self, workflow):
        """
        Execute the browser workflow using Scrappey API
        """
        try:
            print("🚀 Executing Delta flight search workflow...")
            
            headers = {
                'Content-Type': 'application/json',
            }
            
            params = {
                'key': self.scrappey_key,
            }
            
            print(f"📊 Workflow has {len(workflow['browserActions'])} actions")
            
            # Execute the workflow
            response = requests.post(
                self.scrappey_url, 
                params=params, 
                headers=headers, 
                json=workflow,
                timeout=300  # 5 minutes timeout
            )
            
            print(f"📡 Response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                
                if "solution" in result:
                    solution = result["solution"]
                    http_status = solution.get("status", 0)
                    response_html = solution.get("response", "")
                    
                    print(f"✅ Workflow executed successfully!")
                    print(f"📊 HTTP Status: {http_status}")
                    print(f"📄 Response length: {len(response_html)} characters")
                    
                    if http_status == 200 and response_html:
                        return {
                            "success": True,
                            "status": http_status,
                            "html": response_html,
                            "length": len(response_html)
                        }
                    else:
                        print(f"❌ HTTP error: {http_status}")
                        return {
                            "success": False,
                            "status": http_status,
                            "error": f"HTTP {http_status}",
                            "html": response_html[:1000] if response_html else ""
                        }
                else:
                    error_msg = result.get("error", "Unknown error")
                    print(f"❌ Scrappey error: {error_msg}")
                    return {
                        "success": False,
                        "error": error_msg
                    }
            else:
                print(f"❌ Request failed: {response.status_code}")
                return {
                    "success": False,
                    "error": f"Request failed: {response.status_code}"
                }
                
        except Exception as e:
            print(f"❌ Workflow execution failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def save_results(self, result, from_airport, to_airport, departure_date):
        """
        Save the HTML results to files
        """
        try:
            if not result.get("success"):
                print("❌ No successful results to save")
                return False
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"delta_scrappey_results_{from_airport}_{to_airport}_{departure_date.replace('/', '-')}_{timestamp}.html"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(result["html"])
            
            print(f"💾 Results saved to: {filename}")
            print(f"📊 File size: {len(result['html'])} characters")
            
            # Also save a summary
            summary_filename = f"delta_scrappey_summary_{timestamp}.json"
            summary = {
                "search_params": {
                    "from": from_airport,
                    "to": to_airport,
                    "date": departure_date
                },
                "result": {
                    "success": result["success"],
                    "status": result.get("status"),
                    "html_length": len(result["html"]),
                    "timestamp": timestamp
                }
            }
            
            with open(summary_filename, 'w') as f:
                json.dump(summary, f, indent=2)
            
            print(f"📋 Summary saved to: {summary_filename}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to save results: {e}")
            return False
    
    def search_flights(self, from_airport="DEL", to_airport="BCN", departure_date="08/21/2025", trip_type="ONE_WAY"):
        """
        Complete flight search process
        """
        print("🎯 DELTA FLIGHT SEARCH WITH SCRAPPEY BROWSER WORKFLOW")
        print("=" * 60)
        print(f"📍 Route: {from_airport} → {to_airport}")
        print(f"📅 Date: {departure_date}")
        print(f"✈️ Trip Type: {trip_type}")
        print("=" * 60)
        
        # Create workflow
        workflow = self.create_delta_workflow(from_airport, to_airport, departure_date, trip_type)
        
        # Execute workflow
        result = self.execute_workflow(workflow)
        
        # Save results
        if result.get("success"):
            self.save_results(result, from_airport, to_airport, departure_date)
            print("\n🎉 SUCCESS: Flight search completed and results saved!")
        else:
            print(f"\n❌ FAILED: {result.get('error', 'Unknown error')}")
        
        return result

def main():
    """
    Main function with command line arguments
    """
    parser = argparse.ArgumentParser(description='Delta Flight Search with Scrappey Browser Workflow')
    parser.add_argument('--from', dest='from_airport', default='DEL', help='Origin airport code (default: DEL)')
    parser.add_argument('--to', dest='to_airport', default='BCN', help='Destination airport code (default: BCN)')
    parser.add_argument('--date', dest='departure_date', default='08/21/2025', help='Departure date (MM/DD/YYYY, default: 08/21/2025)')
    parser.add_argument('--trip', dest='trip_type', default='ONE_WAY', choices=['ONE_WAY', 'ROUND_TRIP', 'MULTICITY'], help='Trip type (default: ONE_WAY)')
    
    args = parser.parse_args()
    
    # Validate date format
    try:
        datetime.strptime(args.departure_date, '%m/%d/%Y')
    except ValueError:
        print("❌ Invalid date format. Use MM/DD/YYYY")
        return
    
    # Create and run automation
    automation = DeltaScrappeyBrowserWorkflow()
    result = automation.search_flights(
        from_airport=args.from_airport,
        to_airport=args.to_airport,
        departure_date=args.departure_date,
        trip_type=args.trip_type
    )
    
    # Print final status
    if result.get("success"):
        print(f"\n✅ COMPLETED: Raw HTML response captured ({result.get('length', 0)} chars)")
    else:
        print(f"\n❌ FAILED: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()
