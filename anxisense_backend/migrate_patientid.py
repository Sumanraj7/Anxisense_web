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
    
    print("Migrating patientid to VARCHAR(50)...")
    cursor.execute("ALTER TABLE patients MODIFY COLUMN patientid VARCHAR(50)")
    db.commit()
    print("Migration successful!")
    
    cursor.close()
    db.close()
except Exception as e:
    print(f"Migration failed: {e}")
