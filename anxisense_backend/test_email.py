import smtplib
import ssl
from email.message import EmailMessage
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_email_sending():
    print("--- Testing Email Configuration ---")
    
    sender_email = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    
    # 1. Check if variables are loaded
    if not sender_email:
        print("ERROR: EMAIL_USER is missing or empty in .env")
        return
    if not password:
        print("ERROR: EMAIL_PASS is missing or empty in .env")
        return

    # Mask password for display
    masked_pass = f"{password[:2]}...{password[-2:]}" if len(password) > 4 else "****"
    print(f"Loaded EMAIL_USER: {sender_email}")
    print(f"Loaded EMAIL_PASS: {masked_pass} (Length: {len(password)})")

    # 2. Check for common mistakes
    if " " in password:
        print("WARNING: Your password contains spaces. App Passwords should usually be used without spaces in code.")
    if sender_email == "your_email@gmail.com":
        print("ERROR: You haven't changed the placeholder email in .env!")
        return

    # 3. Attempt connection
    print("\nAttempting to connect to Gmail SMTP...")
    
    msg = EmailMessage()
    msg.set_content("This is a test email from the debug script.")
    msg["Subject"] = "AnxiSense SMTP Test"
    msg["From"] = sender_email
    msg["To"] = sender_email # Send to self
    
    context = ssl.create_default_context()
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.set_debuglevel(1) # Show SMTP interaction details
            print("Connected via SSL. Attempting login...")
            server.login(sender_email, password)
            print("Login SUCCESSFUL!")
            
            server.send_message(msg)
            print("Email SENT successfully!")
            
    except smtplib.SMTPAuthenticationError as e:
        print("\n!!! AUTHENTICATION ERROR !!!")
        print(f"Server response: {e}")
        print("\nTroubleshooting tips:")
        print("1. Ensure 2-Step Verification is ON for your Google Account.")
        print("2. Use an 'App Password', NOT your regular Gmail password.")
        print("3. Check for typos in EMAIL_USER.")
        print("4. Ensure no leading/trailing spaces in .env values.")
        
    except Exception as e:
        print(f"\nERROR: {e}")

if __name__ == "__main__":
    test_email_sending()
