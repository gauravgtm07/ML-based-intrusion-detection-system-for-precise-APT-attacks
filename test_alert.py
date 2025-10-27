import requests
import json

# Test the trigger-alert endpoint
url = "http://localhost:5000/api/trigger-alert"
payload = {
    "threat_type": "Test Attack",
    "severity": "Critical",
    "description": "Testing if alerts work"
}

try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
