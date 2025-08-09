import subprocess
import json
import os
import time
from typing import Dict, List, Optional, Tuple
import logging

class ScrappeyDeltaFetcher:
    """
    Python wrapper for Delta flight data fetching using Scrappey.com API
    Integrates seamlessly with the main automation bot
    """
    
    def __init__(self, api_key: str, debug: bool = False):
        self.api_key = api_key
        self.debug = debug
        self.script_path = os.path.join(os.path.dirname(__file__), "delta_flight_fetcher.js")
        
        # Setup logging
        logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def validate_node_setup(self) -> bool:
        """Validate Node.js and dependencies are properly installed"""
        try:
            # Check Node.js
            result = subprocess.run(['node', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                self.logger.error("Node.js is not installed or not in PATH")
                return False
            
            self.logger.info(f"Node.js version: {result.stdout.strip()}")
            
            # Check if dependencies are installed
            if not os.path.exists(os.path.join(os.path.dirname(__file__), "node_modules")):
                self.logger.warning("Dependencies not installed. Installing...")
                self.install_dependencies()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Node.js validation failed: {e}")
            return False
    
    def install_dependencies(self) -> bool:
        """Install required npm dependencies"""
        try:
            current_dir = os.path.dirname(__file__)
            result = subprocess.run(['npm', 'install'], 
                                  cwd=current_dir, 
                                  capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                self.logger.info("Dependencies installed successfully")
                return True
            else:
                self.logger.error(f"Failed to install dependencies: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Dependency installation failed: {e}")
            return False
    
    def search_flights(self, 
                      origin: str, 
                      destination: str, 
                      departure_date: str,
                      return_date: Optional[str] = None,
                      passenger_count: int = 1,
                      cabin_class: str = "COACH") -> Optional[Dict]:
        """
        Search for Delta flights using Scrappey API
        
        Args:
            origin: 3-letter airport code (e.g., 'JFK')
            destination: 3-letter airport code (e.g., 'LAX') 
            departure_date: Date in YYYY-MM-DD format
            return_date: Return date for round-trip (optional)
            passenger_count: Number of passengers (default: 1)
            cabin_class: Cabin class (COACH, BUSINESS, FIRST)
            
        Returns:
            Dict containing flight data or None if failed
        """
        
        if not self.validate_node_setup():
            self.logger.error("Node.js setup validation failed")
            return None
        
        try:
            # Prepare command arguments
            cmd = [
                'node', self.script_path,
                '--api-key', self.api_key,
                '--from', origin.upper(),
                '--to', destination.upper(), 
                '--date', departure_date,
                '--passengers', str(passenger_count),
                '--cabin', cabin_class.upper()
            ]
            
            if return_date:
                cmd.extend(['--return-date', return_date])
            
            if self.debug:
                cmd.append('--debug')
            
            self.logger.info(f"Executing flight search: {origin} → {destination} on {departure_date}")
            
            # Execute the Node.js script
            result = subprocess.run(cmd, 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=300,  # 5 minute timeout
                                  cwd=os.path.dirname(__file__))
            
            if result.returncode == 0:
                try:
                    # Parse the JSON response
                    flight_data = json.loads(result.stdout)
                    self.logger.info(f"Successfully fetched {len(flight_data.get('flights', []))} flights")
                    return flight_data
                    
                except json.JSONDecodeError as e:
                    self.logger.error(f"Failed to parse JSON response: {e}")
                    self.logger.debug(f"Raw output: {result.stdout}")
                    return None
            else:
                self.logger.error(f"Script execution failed: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            self.logger.error("Script execution timed out")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error during flight search: {e}")
            return None
    
    def search_flights_multi_page(self,
                                 origin: str,
                                 destination: str, 
                                 departure_date: str,
                                 max_pages: int = 3,
                                 **kwargs) -> Optional[Dict]:
        """
        Search multiple pages of flight results for comprehensive data
        
        Args:
            origin: 3-letter airport code
            destination: 3-letter airport code
            departure_date: Date in YYYY-MM-DD format
            max_pages: Maximum number of pages to fetch
            **kwargs: Additional arguments passed to search_flights
            
        Returns:
            Combined flight data from multiple pages
        """
        
        if not self.validate_node_setup():
            return None
        
        try:
            cmd = [
                'node', self.script_path,
                '--api-key', self.api_key,
                '--from', origin.upper(),
                '--to', destination.upper(),
                '--date', departure_date,
                '--multi-page',
                '--max-pages', str(max_pages)
            ]
            
            # Add optional parameters
            if kwargs.get('return_date'):
                cmd.extend(['--return-date', kwargs['return_date']])
            if kwargs.get('passenger_count'):
                cmd.extend(['--passengers', str(kwargs['passenger_count'])])
            if kwargs.get('cabin_class'):
                cmd.extend(['--cabin', kwargs['cabin_class'].upper()])
            if self.debug:
                cmd.append('--debug')
            
            self.logger.info(f"Executing multi-page search: {origin} → {destination}, max {max_pages} pages")
            
            result = subprocess.run(cmd,
                                  capture_output=True,
                                  text=True,
                                  timeout=600,  # 10 minute timeout for multi-page
                                  cwd=os.path.dirname(__file__))
            
            if result.returncode == 0:
                try:
                    flight_data = json.loads(result.stdout)
                    total_flights = len(flight_data.get('flights', []))
                    pages_fetched = flight_data.get('pages_fetched', 1)
                    self.logger.info(f"Multi-page search complete: {total_flights} flights from {pages_fetched} pages")
                    return flight_data
                    
                except json.JSONDecodeError as e:
                    self.logger.error(f"Failed to parse multi-page JSON response: {e}")
                    return None
            else:
                self.logger.error(f"Multi-page search failed: {result.stderr}")
                return None
                
        except Exception as e:
            self.logger.error(f"Multi-page search error: {e}")
            return None
    
    def format_flight_data(self, flight_data: Dict) -> List[Dict]:
        """
        Format raw flight data into structured format for the main bot
        
        Args:
            flight_data: Raw flight data from Scrappey API
            
        Returns:
            List of formatted flight dictionaries
        """
        
        if not flight_data or 'flights' not in flight_data:
            return []
        
        formatted_flights = []
        
        for flight in flight_data['flights']:
            try:
                formatted_flight = {
                    'airline': 'Delta',
                    'flight_number': flight.get('flightNumber', 'N/A'),
                    'departure_time': flight.get('departureTime', 'N/A'),
                    'arrival_time': flight.get('arrivalTime', 'N/A'),
                    'duration': flight.get('duration', 'N/A'),
                    'price': flight.get('price', 'N/A'),
                    'currency': flight.get('currency', 'USD'),
                    'origin': flight.get('origin', 'N/A'),
                    'destination': flight.get('destination', 'N/A'),
                    'stops': flight.get('stops', 0),
                    'aircraft': flight.get('aircraft', 'N/A'),
                    'cabin_class': flight.get('cabinClass', 'N/A'),
                    'availability': flight.get('availability', 'N/A'),
                    'booking_url': flight.get('bookingUrl', ''),
                    'raw_data': flight  # Keep original data for debugging
                }
                formatted_flights.append(formatted_flight)
                
            except Exception as e:
                self.logger.warning(f"Failed to format flight data: {e}")
                continue
        
        self.logger.info(f"Formatted {len(formatted_flights)} flights")
        return formatted_flights
    
    def test_connection(self) -> bool:
        """Test the Scrappey API connection"""
        try:
            cmd = [
                'node', self.script_path,
                '--api-key', self.api_key,
                '--test-connection'
            ]
            
            result = subprocess.run(cmd,
                                  capture_output=True,
                                  text=True,
                                  timeout=30,
                                  cwd=os.path.dirname(__file__))
            
            if result.returncode == 0:
                self.logger.info("Scrappey API connection test successful")
                return True
            else:
                self.logger.error(f"API connection test failed: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Connection test error: {e}")
            return False


# Example usage and integration helper
class DeltaFlightAutomationWithAPI:
    """
    Enhanced Delta flight automation bot with Scrappey API integration
    Combines Selenium automation with API-based data fetching
    """
    
    def __init__(self, scrappey_api_key: str, use_selenium: bool = True, debug: bool = False):
        self.scrappey_fetcher = ScrappeyDeltaFetcher(scrappey_api_key, debug)
        self.use_selenium = use_selenium
        self.debug = debug
        self.logger = logging.getLogger(__name__)
        
        # Import the main automation bot if needed
        if use_selenium:
            try:
                # This would import your main automation class
                # from delta_flight_automation_advanced import DeltaFlightAutomation
                # self.selenium_bot = DeltaFlightAutomation()
                pass
            except ImportError:
                self.logger.warning("Selenium bot not available, using API-only mode")
                self.use_selenium = False
    
    def search_flights_hybrid(self, 
                             origin: str, 
                             destination: str, 
                             departure_date: str,
                             use_api_fallback: bool = True) -> Dict:
        """
        Hybrid search using both Selenium and API methods
        
        Args:
            origin: Airport code
            destination: Airport code  
            departure_date: Date string
            use_api_fallback: Use API if Selenium fails
            
        Returns:
            Combined flight data from multiple sources
        """
        
        results = {
            'selenium_flights': [],
            'api_flights': [],
            'combined_flights': [],
            'sources_used': []
        }
        
        # Try Selenium first if enabled
        if self.use_selenium:
            try:
                self.logger.info("Attempting Selenium-based search...")
                # selenium_results = self.selenium_bot.search_flights(origin, destination, departure_date)
                # results['selenium_flights'] = selenium_results
                # results['sources_used'].append('selenium')
                pass
            except Exception as e:
                self.logger.warning(f"Selenium search failed: {e}")
        
        # Try API method
        try:
            self.logger.info("Attempting API-based search...")
            api_results = self.scrappey_fetcher.search_flights(origin, destination, departure_date)
            if api_results:
                formatted_flights = self.scrappey_fetcher.format_flight_data(api_results)
                results['api_flights'] = formatted_flights
                results['sources_used'].append('scrappey_api')
                
        except Exception as e:
            self.logger.error(f"API search failed: {e}")
        
        # Combine results
        all_flights = results['selenium_flights'] + results['api_flights']
        
        # Remove duplicates and sort by price
        unique_flights = self._deduplicate_flights(all_flights)
        results['combined_flights'] = sorted(unique_flights, 
                                           key=lambda x: self._extract_price(x.get('price', 'N/A')))
        
        self.logger.info(f"Hybrid search complete: {len(results['combined_flights'])} unique flights found")
        return results
    
    def _deduplicate_flights(self, flights: List[Dict]) -> List[Dict]:
        """Remove duplicate flights based on flight number and time"""
        seen = set()
        unique_flights = []
        
        for flight in flights:
            flight_key = (
                flight.get('flight_number', ''),
                flight.get('departure_time', ''),
                flight.get('price', '')
            )
            
            if flight_key not in seen:
                seen.add(flight_key)
                unique_flights.append(flight)
        
        return unique_flights
    
    def _extract_price(self, price_str: str) -> float:
        """Extract numeric price for sorting"""
        try:
            # Remove currency symbols and extract numbers
            import re
            numbers = re.findall(r'\d+\.?\d*', str(price_str))
            return float(numbers[0]) if numbers else float('inf')
        except:
            return float('inf')


if __name__ == "__main__":
    # Example usage
    API_KEY = "your_scrappey_api_key_here"
    
    # Test the Scrappey fetcher
    fetcher = ScrappeyDeltaFetcher(API_KEY, debug=True)
    
    # Test connection
    if fetcher.test_connection():
        print("✅ Scrappey API connection successful")
        
        # Test flight search
        results = fetcher.search_flights("JFK", "LAX", "2025-08-25")
        if results:
            formatted = fetcher.format_flight_data(results)
            print(f"✅ Found {len(formatted)} flights")
            
            # Print first few flights
            for i, flight in enumerate(formatted[:3]):
                print(f"\nFlight {i+1}:")
                print(f"  Flight: {flight['flight_number']}")
                print(f"  Time: {flight['departure_time']} → {flight['arrival_time']}")
                print(f"  Price: {flight['price']} {flight['currency']}")
                print(f"  Duration: {flight['duration']}")
        else:
            print("❌ Flight search failed")
    else:
        print("❌ Scrappey API connection failed")
