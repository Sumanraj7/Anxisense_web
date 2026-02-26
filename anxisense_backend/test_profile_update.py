import requests
import json

BASE_URL = "http://127.0.0.1:5000/api"

def test_profile_flow():
    print("Testing Doctor Profile Flow...")
    
    # 1. Login to get a valid doctor ID (assuming a doctor exists from previous steps)
    # Since I don't have login handy in script, I'll use a known doctor ID if possible, 
    # or register a new one for testing. 
    # Let's assume doctor ID 1 exists as "Dr. Suman" from previous contexts or I'll register one.
    
    email = "test_profile@example.com"
    username = "Dr. Profile Test"
    
    # Register/Ensure doctor exists
    # Note: Register endpoint might fail if exists, that's fine.
    try:
        requests.post(f"{BASE_URL}/doctor/register", json={"email": email, "username": username})
    except:
        pass

    # Manually get doctor ID from DB or via verify-otp flow? 
    # To keep it simple, I'll use the 'send-otp' -> 'verify-otp' flow
    print(f"1. Sending OTP to {email}...")
    resp = requests.post(f"{BASE_URL}/doctor/send-otp", json={"email": email})
    if resp.status_code != 200:
        print("Failed to send OTP (or email not configures). logic might fail here if email not working.")
        # If email fails, I can't easily get the ID without DB access. 
        # I'll rely on my knowledge that I can query DB locally if needed. 
        # But wait, run_migration.py worked, so I can query DB from python!
    
    import MySQLdb
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    db = MySQLdb.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        passwd=os.getenv("DB_PASSWORD"),
        db=os.getenv("DB_NAME")
    )
    cursor = db.cursor()
    cursor.execute("SELECT id FROM doctors WHERE email=%s", (email,))
    row = cursor.fetchone()
    
    if not row:
        print("Doctor not found in DB. Registering now...")
        cursor.execute("INSERT INTO doctors (username, email) VALUES (%s, %s)", (username, email))
        db.commit()
        doctor_id = cursor.lastrowid
    else:
        doctor_id = row[0]
        
    print(f"Using Doctor ID: {doctor_id}")
    
    # 2. Update Profile
    print("\n2. Updating Profile...")
    update_data = {
        "doctorid": doctor_id,
        "fullname": "Updated Name",
        "phone": "1234567890",
        "specialization": "Neurology",
        "clinic_name": "Brain Clinic"
    }
    resp = requests.put(f"{BASE_URL}/doctor/profile", json=update_data)
    print(f"Update Response: {resp.status_code} - {resp.json()}")
    assert resp.status_code == 200
    assert resp.json()['success'] == True
    
    # 3. Get Profile
    print("\n3. Fetching Profile...")
    resp = requests.get(f"{BASE_URL}/doctor/profile", params={"doctorid": doctor_id})
    print(f"Get Response: {resp.status_code} - {resp.json()}")
    assert resp.status_code == 200
    data = resp.json()['data']
    
    # Verify Data
    assert data['fullname'] == "Updated Name"
    assert data['phone'] == "1234567890"
    assert data['specialization'] == "Neurology"
    assert data['clinic_name'] == "Brain Clinic"
    
    print("\nSUCCESS: Profile flow verified!")

if __name__ == "__main__":
    test_profile_flow()
