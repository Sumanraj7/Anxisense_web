import os
import MySQLdb
from dotenv import load_dotenv

def log(file, message):
    print(message)
    file.write(message + "\n")

def check_patients_table():
    load_dotenv()
    with open("patients_table_check_result.txt", "w", encoding="utf-8") as f:
        try:
            db = MySQLdb.connect(
                host=os.getenv("DB_HOST", "localhost"),
                user=os.getenv("DB_USER", "root"),
                passwd=os.getenv("DB_PASSWORD", ""),
                db=os.getenv("DB_NAME", "anxi"),
                charset="utf8"
            )
            cursor = db.cursor()
            cursor.execute("SHOW TABLES LIKE 'patients'")
            result = cursor.fetchone()
            
            if result:
                log(f, "[SUCCESS] Table 'patients' exists.")
                cursor.execute("DESCRIBE patients")
                columns = [row[0] for row in cursor.fetchall()]
                log(f, f"Columns: {', '.join(columns)}")
                return True
            else:
                log(f, "[INFO] Table 'patients' does NOT exist.")
                return False
                
        except Exception as e:
            log(f, f"[ERROR] Database check failed: {e}")
            return False
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'db' in locals(): db.close()

if __name__ == "__main__":
    check_patients_table()
