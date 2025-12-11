"""Test API endpoints."""

import requests
import json
from pathlib import Path

API_BASE_URL = "http://localhost:8000"


def test_health():
    """Test health endpoint."""
    print("🏥 Testing health endpoint...")
    response = requests.get(f"{API_BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200


def test_researcher():
    """Test researcher endpoint."""
    print("\n🔍 Testing researcher endpoint...")
    data = {"business_id": 1}
    response = requests.post(
        f"{API_BASE_URL}/api/v1/agents/researcher",
        json=data
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Researcher endpoint working")
    else:
        print(f"❌ Error: {response.text}")
    return response.status_code == 200


def test_status():
    """Test status endpoint."""
    print("\n📊 Testing status endpoint...")
    response = requests.get(f"{API_BASE_URL}/api/v1/status")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def main():
    """Run all tests."""
    print("🧪 Testing API endpoints...\n")
    
    try:
        test_health()
        test_status()
        # Uncomment to test agents (requires OpenAI API key)
        # test_researcher()
        
        print("\n✅ API tests completed!")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure it's running:")
        print("   uvicorn api.main:app --reload --port 8000")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    main()

