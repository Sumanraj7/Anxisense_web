import MySQLdb
import os
from dotenv import load_dotenv

load_dotenv()

def run_migration():
    try:
        db = MySQLdb.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            passwd=os.getenv("DB_PASSWORD"),
            db=os.getenv("DB_NAME")
        )
        cursor = db.cursor()
        
        filename = "alter_doctors_table.sql"
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                # Read the whole file and split by semicolon
                sql_commands = f.read().split(';')
                for command in sql_commands:
                    if command.strip():
                        try:
                            cursor.execute(command)
                            print(f"Executed command: {command[:50]}...")
                        except MySQLdb.OperationalError as e:
                            # Ignore "Duplicate column name" error (code 1060)
                            if e.args[0] == 1060:
                                print(f"Column already exists: {e}")
                            else:
                                raise e
            db.commit()
            print(f"Migration {filename} completed.")
        else:
            print(f"File not found: {filename}")

        cursor.close()
        db.close()

    except Exception as e:
        print(f"Migration failed: {e}")

if __name__ == "__main__":
    run_migration()
