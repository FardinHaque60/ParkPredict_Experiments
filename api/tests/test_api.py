import requests
import json
from datetime import datetime, timedelta
import os
import sys

# Add the parent directory to path so we can import from api
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_URL = "http://localhost:5001"

def test_home():
    """Test the home endpoint"""
    print("\n=== Testing Home Endpoint ===")
    response = requests.get(f"{BASE_URL}/")
    try:
        data = response.json()
        print(json.dumps(data, indent=2))
        assert response.status_code == 200
        assert "status" in data
        assert "endpoints" in data
    except requests.exceptions.JSONDecodeError:
        print("Error: Response is not valid JSON")
        print(f"Response content: {response.text}")
        raise
def test_prediction():
    """Test the prediction endpoint"""
    prediction_data = {
        "timestamp": "2025-03-10T12:00:00",  # Use a timestamp within our training data range
        "garage": "North Garage",
        "model": "sinusoidal"
    }
    
    print("\n=== Testing Prediction Endpoint ===")
    response = requests.post(f"{BASE_URL}/predict", json=prediction_data)
    print(json.dumps(response.json(), indent=2))
    assert response.status_code == 200

def test_predictions_history():
    """Test getting prediction history"""
    print("\n=== Testing Predictions History ===")
    response = requests.get(f"{BASE_URL}/predictions")
    print(json.dumps(response.json(), indent=2))
    assert response.status_code == 200

def test_garage_predictions():
    """Test getting predictions for specific garage"""
    print("\n=== Testing Garage-Specific Predictions ===")
    response = requests.get(f"{BASE_URL}/predictions/North Garage")
    print(json.dumps(response.json(), indent=2))
    assert response.status_code == 200

def test_weights():
    """Test getting model weights"""
    print("\n=== Testing Weights Endpoint ===")
    response = requests.get(f"{BASE_URL}/weights")
    print(json.dumps(response.json(), indent=2))
    assert response.status_code == 200

def run_all_tests():
    """Run all test functions"""
    try:
        test_home()
        test_prediction()
        test_predictions_history()
        test_garage_predictions()
        test_weights()
        print("\n=== All tests passed! ===")
    except AssertionError as e:
        print(f"\n=== Test failed: {str(e)} ===")
    except requests.exceptions.ConnectionError:
        print("\n=== Error: Could not connect to the API. Make sure it's running on localhost:5001 ===")

if __name__ == "__main__":
    run_all_tests()