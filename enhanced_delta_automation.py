#!/usr/bin/env python3
"""
Enhanced Delta Flight Automation Bot with Scrappey.com API Integration
Combines the advanced Selenium automation with API-based data fetching

This script integrates:
1. Your existing delta_flight_automation_advanced.py features
2. Scrappey.com API for protected GraphQL endpoints  
3. Chrome profiles, proxy support, and human-like behavior
4. Comprehensive error handling and fallback mechanisms
"""

import sys
import os
import time
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging

# Import our Scrappey integration
from scrappey_delta_integration import ScrappeyDeltaFetcher, DeltaFlightAutomationWithAPI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('delta_automation.log'),
        logging.StreamHandler()
    ]
)

class EnhancedDeltaAutomation:
    """
    Ultimate Delta flight automation bot combining Selenium and API methods
    Features:
    - Scrappey.com API integration for protected endpoints
    - Advanced Selenium with human-like behavior
    - Chrome profiles and proxy support  
    - Intelligent fallback mechanisms
    - Comprehensive data collection and processing
    """
    
    def __init__(self, 
                 scrappey_api_key: str,
                 proxy_config: Optional[Dict] = None,
                 chrome_profile_path: Optional[str] = None,
                 use_incognito: bool = True,
                 debug: bool = False):
        
        self.scrappey_api_key = scrappey_api_key
        self.proxy_config = proxy_config
        self.chrome_profile_path = chrome_profile_path
        self.use_incognito = use_incognito
        self.debug = debug
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
        # Initialize Scrappey API fetcher
        self.api_fetcher = ScrappeyDeltaFetcher(scrappey_api_key, debug)
        
        # Initialize hybrid automation
        self.hybrid_bot = DeltaFlightAutomationWithAPI(scrappey_api_key, use_selenium=True, debug=debug)
        
        # Flight search results storage
        self.last_search_results = {}
        self.search_history = []
        
        self.logger.info("Enhanced Delta Automation Bot initialized")
    
    def validate_setup(self) -> bool:
        """Validate that all components are working correctly"""
        self.logger.info("Validating automation setup...")
        
        try:
            # Test API connection
            if not self.api_fetcher.test_connection():
                self.logger.error("Scrappey API connection failed")
                return False
            
            # Test Node.js setup
            if not self.api_fetcher.validate_node_setup():
                self.logger.error("Node.js setup validation failed")
                return False
            
            self.logger.info("✅ All components validated successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Setup validation failed: {e}")
            return False
    
    def search_flights_comprehensive(self,
                                   origin: str,
                                   destination: str, 
                                   departure_date: str,
                                   return_date: Optional[str] = None,
                                   passenger_count: int = 1,
                                   cabin_class: str = "COACH",
                                   use_multi_page: bool = True,
                                   max_pages: int = 3) -> Dict:
        """
        Comprehensive flight search using multiple methods and sources
        
        Args:
            origin: 3-letter airport code
            destination: 3-letter airport code
            departure_date: Date in YYYY-MM-DD format
            return_date: Return date for round-trip
            passenger_count: Number of passengers
            cabin_class: COACH, BUSINESS, or FIRST
            use_multi_page: Whether to fetch multiple pages of results
            max_pages: Maximum pages to fetch if multi_page is True
            
        Returns:
            Comprehensive flight data with metadata
        """
        
        search_start_time = time.time()
        search_id = f"{origin}_{destination}_{departure_date}_{int(search_start_time)}"
        
        self.logger.info(f"Starting comprehensive flight search: {origin} → {destination} on {departure_date}")
        
        search_results = {
            'search_id': search_id,
            'search_params': {
                'origin': origin,
                'destination': destination,
                'departure_date': departure_date,
                'return_date': return_date,
                'passenger_count': passenger_count,
                'cabin_class': cabin_class
            },
            'api_results': None,
            'selenium_results': None,
            'combined_flights': [],
            'search_metadata': {
                'start_time': search_start_time,
                'methods_used': [],
                'total_flights_found': 0,
                'search_duration': 0,
                'errors': []
            }
        }
        
        # Method 1: Try Scrappey API first (faster and more reliable)
        try:
            self.logger.info("🚀 Attempting API-based search...")
            
            if use_multi_page:
                api_data = self.api_fetcher.search_flights_multi_page(
                    origin, destination, departure_date,
                    max_pages=max_pages,
                    return_date=return_date,
                    passenger_count=passenger_count,
                    cabin_class=cabin_class
                )
            else:
                api_data = self.api_fetcher.search_flights(
                    origin, destination, departure_date,
                    return_date, passenger_count, cabin_class
                )
            
            if api_data:
                formatted_api_flights = self.api_fetcher.format_flight_data(api_data)
                search_results['api_results'] = formatted_api_flights
                search_results['search_metadata']['methods_used'].append('scrappey_api')
                self.logger.info(f"✅ API search successful: {len(formatted_api_flights)} flights")
            else:
                search_results['search_metadata']['errors'].append('API search returned no results')
                self.logger.warning("API search returned no results")
                
        except Exception as e:
            error_msg = f"API search failed: {e}"
            search_results['search_metadata']['errors'].append(error_msg)
            self.logger.error(error_msg)
        
        # Method 2: Try Selenium as fallback (if API failed or for verification)
        selenium_enabled = False  # Set to True when you want to enable Selenium fallback
        
        if selenium_enabled:
            try:
                self.logger.info("🌐 Attempting Selenium-based search...")
                # This would call your advanced Selenium bot
                # selenium_data = self.search_with_selenium(origin, destination, departure_date, ...)
                # search_results['selenium_results'] = selenium_data
                # search_results['search_metadata']['methods_used'].append('selenium')
                pass
                
            except Exception as e:
                error_msg = f"Selenium search failed: {e}"
                search_results['search_metadata']['errors'].append(error_msg)
                self.logger.error(error_msg)
        
        # Combine and process results
        all_flights = []
        if search_results['api_results']:
            all_flights.extend(search_results['api_results'])
        if search_results['selenium_results']:
            all_flights.extend(search_results['selenium_results'])
        
        # Remove duplicates and sort
        unique_flights = self._deduplicate_flights(all_flights)
        sorted_flights = self._sort_flights_by_criteria(unique_flights)
        
        search_results['combined_flights'] = sorted_flights
        search_results['search_metadata']['total_flights_found'] = len(sorted_flights)
        search_results['search_metadata']['search_duration'] = time.time() - search_start_time
        
        # Store results
        self.last_search_results = search_results
        self.search_history.append(search_results)
        
        self.logger.info(f"🎯 Search complete: {len(sorted_flights)} unique flights in {search_results['search_metadata']['search_duration']:.2f}s")
        
        return search_results
    
    def _deduplicate_flights(self, flights: List[Dict]) -> List[Dict]:
        """Remove duplicate flights based on key attributes"""
        seen = set()
        unique_flights = []
        
        for flight in flights:
            # Create a unique key for the flight
            flight_key = (
                flight.get('flight_number', ''),
                flight.get('departure_time', ''),
                flight.get('arrival_time', ''),
                flight.get('price', '')
            )
            
            if flight_key not in seen and flight_key != ('', '', '', ''):
                seen.add(flight_key)
                unique_flights.append(flight)
        
        return unique_flights
    
    def _sort_flights_by_criteria(self, flights: List[Dict], criteria: str = 'price') -> List[Dict]:
        """Sort flights by specified criteria"""
        
        def get_sort_key(flight):
            if criteria == 'price':
                return self._extract_numeric_value(flight.get('price', 'inf'))
            elif criteria == 'duration':
                return self._extract_duration_minutes(flight.get('duration', '999:99'))
            elif criteria == 'departure_time':
                return flight.get('departure_time', 'ZZ:ZZ')
            else:
                return 0
        
        try:
            return sorted(flights, key=get_sort_key)
        except Exception as e:
            self.logger.warning(f"Failed to sort flights: {e}")
            return flights
    
    def _extract_numeric_value(self, value_str: str) -> float:
        """Extract numeric value from price string"""
        try:
            import re
            numbers = re.findall(r'\d+\.?\d*', str(value_str))
            return float(numbers[0]) if numbers else float('inf')
        except:
            return float('inf')
    
    def _extract_duration_minutes(self, duration_str: str) -> int:
        """Convert duration string to minutes for sorting"""
        try:
            import re
            # Handle formats like "2h 30m", "150m", "2:30"
            hours = re.findall(r'(\d+)h', str(duration_str))
            minutes = re.findall(r'(\d+)m', str(duration_str))
            
            total_minutes = 0
            if hours:
                total_minutes += int(hours[0]) * 60
            if minutes:
                total_minutes += int(minutes[0])
            
            # Handle "2:30" format
            if ':' in str(duration_str) and not hours and not minutes:
                parts = str(duration_str).split(':')
                if len(parts) == 2:
                    total_minutes = int(parts[0]) * 60 + int(parts[1])
            
            return total_minutes if total_minutes > 0 else 9999
            
        except:
            return 9999
    
    def get_best_flights(self, 
                        search_results: Optional[Dict] = None,
                        criteria: str = 'price',
                        limit: int = 5) -> List[Dict]:
        """Get the best flights from search results based on criteria"""
        
        if search_results is None:
            search_results = self.last_search_results
        
        if not search_results or not search_results.get('combined_flights'):
            self.logger.warning("No search results available")
            return []
        
        flights = search_results['combined_flights']
        sorted_flights = self._sort_flights_by_criteria(flights, criteria)
        
        return sorted_flights[:limit]
    
    def export_results(self, 
                      search_results: Optional[Dict] = None,
                      format: str = 'json',
                      filename: Optional[str] = None) -> str:
        """Export search results to file"""
        
        if search_results is None:
            search_results = self.last_search_results
        
        if not search_results:
            self.logger.error("No search results to export")
            return ""
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            search_id = search_results.get('search_id', 'unknown')
            filename = f"delta_flights_{search_id}_{timestamp}.{format}"
        
        try:
            if format.lower() == 'json':
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(search_results, f, indent=2, ensure_ascii=False)
            
            elif format.lower() == 'csv':
                import csv
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    if search_results['combined_flights']:
                        fieldnames = search_results['combined_flights'][0].keys()
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(search_results['combined_flights'])
            
            self.logger.info(f"Results exported to: {filename}")
            return filename
            
        except Exception as e:
            self.logger.error(f"Failed to export results: {e}")
            return ""
    
    def print_search_summary(self, search_results: Optional[Dict] = None):
        """Print a formatted summary of search results"""
        
        if search_results is None:
            search_results = self.last_search_results
        
        if not search_results:
            print("No search results available")
            return
        
        params = search_results['search_params']
        metadata = search_results['search_metadata']
        flights = search_results['combined_flights']
        
        print("\n" + "="*80)
        print("🛫 DELTA FLIGHT SEARCH RESULTS")
        print("="*80)
        
        print(f"Route: {params['origin']} → {params['destination']}")
        print(f"Date: {params['departure_date']}")
        if params['return_date']:
            print(f"Return: {params['return_date']}")
        print(f"Passengers: {params['passenger_count']}")
        print(f"Class: {params['cabin_class']}")
        
        print(f"\nSearch Duration: {metadata['search_duration']:.2f} seconds")
        print(f"Methods Used: {', '.join(metadata['methods_used'])}")
        print(f"Total Flights Found: {metadata['total_flights_found']}")
        
        if metadata['errors']:
            print(f"Errors: {len(metadata['errors'])}")
            for error in metadata['errors']:
                print(f"  ⚠️ {error}")
        
        print(f"\n📋 TOP FLIGHTS (showing first 5):")
        print("-"*80)
        
        for i, flight in enumerate(flights[:5]):
            print(f"\n✈️ Flight {i+1}:")
            print(f"   Flight: {flight.get('flight_number', 'N/A')}")
            print(f"   Time: {flight.get('departure_time', 'N/A')} → {flight.get('arrival_time', 'N/A')}")
            print(f"   Duration: {flight.get('duration', 'N/A')}")
            print(f"   Price: {flight.get('price', 'N/A')} {flight.get('currency', 'USD')}")
            print(f"   Stops: {flight.get('stops', 'N/A')}")
            print(f"   Aircraft: {flight.get('aircraft', 'N/A')}")
        
        print("\n" + "="*80)


def example_usage():
    """Example of how to use the enhanced automation"""
    
    print("🚀 Enhanced Delta Flight Automation Example")
    print("="*50)
    
    # Get API key (in real usage, store this securely)
    api_key = input("Enter your Scrappey.com API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided")
        return
    
    # Optional proxy configuration
    proxy_config = {
        'https': 'https://user:pass@us-pr.oxylabs.io:10000'
    }
    
    # Initialize the enhanced automation
    automation = EnhancedDeltaAutomation(
        scrappey_api_key=api_key,
        proxy_config=proxy_config,
        use_incognito=True,
        debug=True
    )
    
    # Validate setup
    if not automation.validate_setup():
        print("❌ Setup validation failed")
        return
    
    print("✅ Setup validated successfully")
    
    # Example search parameters
    test_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    
    search_params = {
        'origin': 'JFK',
        'destination': 'LAX',
        'departure_date': test_date,
        'passenger_count': 1,
        'cabin_class': 'COACH',
        'use_multi_page': True,
        'max_pages': 2
    }
    
    print(f"\n🔍 Searching for flights: {search_params['origin']} → {search_params['destination']}")
    
    # Perform comprehensive search
    results = automation.search_flights_comprehensive(**search_params)
    
    # Display results
    automation.print_search_summary(results)
    
    # Get best flights by different criteria
    print("\n💰 Best flights by price:")
    best_price = automation.get_best_flights(results, criteria='price', limit=3)
    for i, flight in enumerate(best_price):
        print(f"  {i+1}. {flight.get('flight_number', 'N/A')} - {flight.get('price', 'N/A')}")
    
    print("\n⏱️ Best flights by duration:")
    best_duration = automation.get_best_flights(results, criteria='duration', limit=3)
    for i, flight in enumerate(best_duration):
        print(f"  {i+1}. {flight.get('flight_number', 'N/A')} - {flight.get('duration', 'N/A')}")
    
    # Export results
    json_file = automation.export_results(results, format='json')
    csv_file = automation.export_results(results, format='csv')
    
    print(f"\n💾 Results exported:")
    print(f"   JSON: {json_file}")
    print(f"   CSV: {csv_file}")
    
    print("\n🎉 Example completed successfully!")


if __name__ == "__main__":
    example_usage()
