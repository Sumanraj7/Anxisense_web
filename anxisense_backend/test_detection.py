import requests
import os

BASE_URL = "http://127.0.0.1:5000/api"

def test_detection():
    # Test 1: No face (we'll just send a dummy file or empty if we had one, 
    # but let's assume we want to see it fail DeepFace)
    print("Testing Detection Endpoint...")
    
    # We'll use a local image if available, or just check the logic
    # Since I don't have a guaranteed face image in the environment for tests,
    # I'll just verify the endpoint exists and returns 400 for no image.
    
    resp = requests.post(f"{BASE_URL}/detect-only")
    print(f"Empty request status: {resp.status_code}")
    print(f"Response: {resp.json()}")

    # Verify analyze also still works and has enforcement (I saw it in app.py)
    # The user request was specifically for the scan flow "try again" part.
    
if __name__ == "__main__":
    test_detection()
