"""
Quick Date Picker Test - Run this to test just the date selection
================================================================
"""

from delta_flight_automation_advanced import DeltaFlightAutomationAdvanced

def test_date_picker_only():
    """Test just the date picker functionality"""
    automation = None
    
    try:
        print("🧪 Testing Date Picker Only")
        print("=" * 40)
        
        # Initialize automation
        automation = DeltaFlightAutomationAdvanced(headless=False)
        
        # Navigate to Delta
        if not automation.navigate_to_delta():
            print("❌ Failed to navigate to Delta")
            return
        
        # Test specific date selection
        print("\n🎯 Testing specific date selection...")
        if automation.select_departure_date("09/24/25"):
            print("✅ Specific date selection worked!")
        else:
            print("❌ Specific date selection failed")
        
        # Test next available date selection
        print("\n🎯 Testing next available date selection...")
        if automation.select_next_available_date():
            print("✅ Next available date selection worked!")
        else:
            print("❌ Next available date selection failed")
        
        input("\n🔍 Check the calendar state, then press Enter to close...")
        
    except Exception as e:
        print(f"💥 Test failed: {e}")
    finally:
        if automation:
            automation.close()

if __name__ == "__main__":
    test_date_picker_only()
