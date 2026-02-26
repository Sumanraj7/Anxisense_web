import requests
import json

BASE_URL = "http://127.0.0.1:5000/api"

def test_flow():
    # 1. Register Patient
    patient_data = {
        "doctorid": 1,
        "patientid": "T001",
        "fullname": "Terminal Test Patient",
        "age": 30,
        "gender": "Female",
        "proceduretype": "Surgery",
        "healthissue": "N/A",
        "previousanxietyhistory": "None"
    }
    
    print("Testing Patient Registration...")
    resp = requests.post(f"{BASE_URL}/patients", json=patient_data)
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.text}")
    
    if resp.status_code == 200:
        p_id = resp.json()['data']['id']
        print(f"Patient saved with DB ID: {p_id}")
        
        # 2. Save Assessment
        assessment_data = {
            "patient_id": p_id,
            "doctor_id": 1,
            "anxiety_score": "45",
            "anxiety_level": "Moderate",
            "dominant_emotion": "Neutral"
        }
        
        print("\nTesting Assessment Auto-Save...")
        resp = requests.post(f"{BASE_URL}/assessments", json=assessment_data)
        print(f"Status: {resp.status_code}")
        print(f"Response: {resp.text}")
        
        # 3. Verify in patient list
        print("\nVerifying updated record...")
        resp = requests.get(f"{BASE_URL}/patients?doctorid=1")
        data = resp.json()['data']
        for p in data:
            if p['patientid'] == 'T001':
                print(f"Found patient: {p['fullname']}")
                print(f"Latest Score: {p['latest_anxiety_score']}% ({p['latest_anxiety_level']})")
                return True
    return False

if __name__ == "__main__":
    test_flow()
