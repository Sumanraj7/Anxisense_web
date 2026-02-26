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
    
    print("Attempting raw SQL insert into patients...")
    # Using 1 for doctorid which definitely exists
    cursor.execute("""
        INSERT INTO patients 
        (patientid, doctorid, fullname, age, gender) 
        VALUES (%s, %s, %s, %s, %s)
    """, ("RAW_001", 1, "Raw Test Patient", 40, "Non-binary"))
    
    db.commit()
    print(f"Success! Last ID: {cursor.lastrowid}")
    
    cursor.close()
    db.close()
except Exception as e:
    print(f"Raw insert failed: {e}")
