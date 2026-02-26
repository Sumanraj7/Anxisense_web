import requests
import json

BASE_URL = "http://127.0.0.1:5000/api"

# 1. Get Doctor ID (assuming one exists, e.g., ID 1)
# Note: In a real test we might register/login, but let's assume valid data for now 
# or check against the DB manually.
DOCTOR_ID = 1

# 2. Get Patients for this Doctor
print(f"Fetching patients for doctor {DOCTOR_ID}...")
try:
    resp = requests.get(f"{BASE_URL}/patients?doctorid={DOCTOR_ID}")
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.text}")
    
    data = resp.json()
    if not data['success'] or not data['data']:
        print("No patients found. Creating one...")
        # Create Patient
        patient_payload = {
            "doctorid": DOCTOR_ID,
            "fullname": "Test Patient",
            "patientid": "P-TEST-001",
            "age": 30,
            "gender": "Male"
        }
        resp = requests.post(f"{BASE_URL}/patients", json=patient_payload)
        print(f"Create Patient Response: {resp.text}")
        patient_internal_id = resp.json()['data']['id']
    else:
        patient_internal_id = data['data'][0]['id']
        print(f"Using Patient ID: {patient_internal_id}")

    # 3. Save Assessment
    print("\nSaving Assessment...")
    assessment_payload = {
        "patient_id": patient_internal_id,
        "doctor_id": DOCTOR_ID,
        "anxiety_score": 75.5,
        "anxiety_level": "High",
        "dominant_emotion": "fear"
    }
    resp = requests.post(f"{BASE_URL}/assessments", json=assessment_payload)
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.text}")

    # 4. Get Assessments
    print("\nFetching Assessments History...")
    resp = requests.get(f"{BASE_URL}/assessments?doctorid={DOCTOR_ID}")
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.text}")

except Exception as e:
    print(f"Test Failed: {e}")
