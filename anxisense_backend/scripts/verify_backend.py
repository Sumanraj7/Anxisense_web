import os
import MySQLdb
from dotenv import load_dotenv

def log(file, message):
    print(message)
    file.write(message + "\n")

def verify_backend():
    with open("verification_result.txt", "w", encoding="utf-8") as f:
        log(f, "----------------------------------------------------------------")
        log(f, "Running AnxiSense Backend Verification...")
        log(f, "----------------------------------------------------------------")

        # 1. Check Environment Variables
        load_dotenv()
        required_vars = ["DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME", "EMAIL_USER", "EMAIL_PASS", "SECRET_KEY"]
        missing_vars = []
        
        log(f, "\n[INFO] Checking Environment Variables...")
        
        for var in required_vars:
            value = os.getenv(var)
            if not value:
                missing_vars.append(var)
            else:
                # Mask sensitive data in output
                display_val = "******" if "PASS" in var or "KEY" in var else value
                log(f, f"  OK: {var} = {display_val}")

        if missing_vars:
            log(f, f"\n[ERROR] Missing required environment variables: {', '.join(missing_vars)}")
            log(f, "  Please check your .env file.")
            return False
        else:
            log(f, "  [SUCCESS] All environment variables present.")

        # 2. Check Database Connection
        log(f, "\n[INFO] Checking Database Connection...")
        try:
            db = MySQLdb.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                passwd=os.getenv("DB_PASSWORD"),
                db=os.getenv("DB_NAME"),
                charset="utf8"
            )
            log(f, "  [SUCCESS] Connected to database.")
        except Exception as e:
            log(f, f"  [ERROR] Database connection failed: {e}")
            return False

        # 3. Check Doctors Table and OTP Column
        log(f, "\n[INFO] Checking 'doctors' Table Schema...")
        cursor = db.cursor()
        try:
            cursor.execute("DESCRIBE doctors")
            columns = [row[0] for row in cursor.fetchall()]
            
            log(f, f"  Found columns: {', '.join(columns)}")

            if "otp" in columns:
                log(f, "  [SUCCESS] 'otp' column exists in 'doctors' table.")
            else:
                log(f, "  [ERROR] 'otp' column MISSING in 'doctors' table.")
                log(f, "  Run 'create_doctors_table.sql' to update the schema.")
                return False

        except Exception as e:
            log(f, f"  [ERROR] Failed to describe 'doctors' table: {e}")
            return False
        finally:
            cursor.close()
            db.close()

        log(f, "\n----------------------------------------------------------------")
        log(f, "[SUCCESS] Backend verification completed successfully!")
        log(f, "----------------------------------------------------------------")
        return True

if __name__ == "__main__":
    verify_backend()
