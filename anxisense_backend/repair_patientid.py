import MySQLdb
import os
from dotenv import load_dotenv

load_dotenv()

try:
    db = MySQLdb.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        passwd=os.getenv("DB_PASSWORD"),
        db=os.getenv("DB_NAME")
    )
    cursor = db.cursor()
    
    print("Finding alphanumeric patients...")
    cursor.execute("SELECT id, patientid FROM patients")
    patients = cursor.fetchall()
    
    to_delete = []
    for pid_db, pid_code in patients:
        try:
            int(pid_code)
        except (ValueError, TypeError):
            to_delete.append(pid_db)
    
    if to_delete:
        print(f"Deleting {len(to_delete)} alphanumeric records and their assessments...")
        # Convert to tuple for SQL IN clause
        ids_str = ",".join(map(str, to_delete))
        cursor.execute(f"DELETE FROM assessments WHERE patient_id IN ({ids_str})")
        cursor.execute(f"DELETE FROM patients WHERE id IN ({ids_str})")
        db.commit()
    
    print("Reverting patientid column to INT...")
    cursor.execute("ALTER TABLE patients MODIFY COLUMN patientid INT")
    db.commit()
    print("Success! Backend/DB is now back to INT for Android compatibility.")
    
    cursor.close()
    db.close()
except Exception as e:
    print(f"Repair failed: {e}")
