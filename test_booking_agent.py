"""
Test script for AI Calendar Booking Agent
Run this to test the booking agent locally
"""

import asyncio
import httpx


async def test_booking():
    """Test the booking agent with sample requests."""
    
    base_url = "http://localhost:8000"
    
    test_cases = [
        "Schedule a dentist appointment on Friday at 3pm",
        "Book a meeting with john@example.com tomorrow at 2pm",
        "Create a team standup on Monday at 9am for 30 minutes",
    ]
    
    async with httpx.AsyncClient() as client:
        for i, test_request in enumerate(test_cases, 1):
            print(f"\n{'='*60}")
            print(f"Test {i}: {test_request}")
            print('='*60)
            
            try:
                response = await client.post(
                    f"{base_url}/",
                    json={"booking_request": test_request},
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ Success!")
                    print(f"Message: {result['message']}")
                    print(f"\nExtracted Info:")
                    for key, value in result['extracted_info'].items():
                        print(f"  {key}: {value}")
                else:
                    print(f"❌ Failed with status {response.status_code}")
                    print(f"Error: {response.text}")
                    
            except Exception as e:
                print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("🧪 Testing AI Calendar Booking Agent...")
    asyncio.run(test_booking())
