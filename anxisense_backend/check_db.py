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
    
    print("\n--- Doctors Columns ---")
    try:
        cursor.execute("DESCRIBE doctors")
        for col in cursor.fetchall(): print(f"{col[0]} - {col[1]}")
    except Exception as e: print(f"Error: {e}")

    print("\n--- Patients Columns ---")
    try:
        cursor.execute("DESCRIBE patients")
        for col in cursor.fetchall(): print(f"{col[0]} - {col[1]}")
    except Exception as e: print(f"Error: {e}")

    print("\n--- Assessments Columns ---")
    try:
        cursor.execute("DESCRIBE assessments")
        for col in cursor.fetchall(): print(f"{col[0]} - {col[1]}")
    except Exception as e: print(f"Error: {e}")

    cursor.close()
    db.close()

except Exception as e:
    print(f"Connection failed: {e}")
