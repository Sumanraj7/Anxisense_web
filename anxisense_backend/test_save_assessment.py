import requests
import MySQLdb
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://127.0.0.1:5000/api"

def get_db_connection():
    return MySQLdb.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        passwd=os.getenv("DB_PASSWORD"),
        db=os.getenv("DB_NAME")
    )

def test_save_assessment():
    print("Testing Save Assessment API...")
    
    # 1. Get a valid Doctor and Patient ID
    db = get_db_connection()
    cursor = db.cursor()
    
    cursor.execute("SELECT id FROM doctors LIMIT 1")
    doctor_row = cursor.fetchone()
    if not doctor_row:
        print("No doctors found. Please register one first.")
        # Create a dummy doctor
        cursor.execute("INSERT INTO doctors (username, email) VALUES ('Test Doc', 'testdoc@example.com')")
        db.commit()
        doctor_id = cursor.lastrowid
    else:
        doctor_id = doctor_row[0]
        
    cursor.execute("SELECT id FROM patients WHERE doctorid=%s LIMIT 1", (doctor_id,))
    patient_row = cursor.fetchone()
    
    if not patient_row:
        print("No patients found for this doctor. Creating one...")
        cursor.execute("INSERT INTO patients (doctorid, fullname, patientid) VALUES (%s, 'Test Patient', 'TP-001')", (doctor_id,))
        db.commit()
        patient_id = cursor.lastrowid
    else:
        patient_id = patient_row[0]
        
    cursor.close()
    db.close()
    
    print(f"Using Doctor ID: {doctor_id}, Patient ID: {patient_id}")
    
    # 2. Prepare Payload
    payload = {
        "patient_id": patient_id,
        "doctor_id": doctor_id,
        "anxiety_score": 75.5,
        "anxiety_level": "High",
        "dominant_emotion": "fear"
    }
    
    # 3. Send Request
    try:
        resp = requests.post(f"{BASE_URL}/assessments", json=payload)
        print(f"Status Code: {resp.status_code}")
        print(f"Response: {resp.json()}")
        
        if resp.status_code == 201 and resp.json().get("success"):
            print("SUCCESS: Backend API is working correctly.")
        else:
            print("FAILURE: Backend API returned error.")
            
    except Exception as e:
        print(f"FAILURE: Request failed: {e}")

if __name__ == "__main__":
    test_save_assessment()
