# Quick Database Setup Guide

## The Issue

The API is working correctly, but the `doctors` table doesn't exist in your database yet. That's why you're seeing the error.

## Solution: Create the Database Table

### Option 1: Using MySQL Workbench (Recommended)

1. Open **MySQL Workbench**
2. Connect to your database:
   - Host: `localhost`
   - User: `root`
   - Password: `3012`
   - Database: `anxi`

3. Click on **Query** tab and paste this SQL:

```sql
CREATE TABLE IF NOT EXISTS doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    otp VARCHAR(255) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

4. Click **Execute** (⚡ icon)

5. Add a test doctor:

```sql
INSERT INTO doctors (username, email) 
VALUES ('Dr. Test', 'test@doctor.com');
```

### Option 2: Using Command Line

If you have MySQL in your PATH:

```bash
mysql -u root -p3012 -D anxi -e "CREATE TABLE IF NOT EXISTS doctors (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(100) NOT NULL, email VARCHAR(120) NOT NULL UNIQUE, otp VARCHAR(255) NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"
```

## After Creating the Table

### Test with Registered Email:
```powershell
Invoke-WebRequest -Uri "http://localhost:5000/api/doctor/send-otp" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{"email": "test@doctor.com"}'
```
**Expected:** ✅ Returns OTP

### Test with Unregistered Email:
```powershell
Invoke-WebRequest -Uri "http://localhost:5000/api/doctor/send-otp" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{"email": "notregistered@doctor.com"}'
```
**Expected:** ❌ "Email not registered. Please contact administrator."

## Current Status

✅ Flask server running on http://127.0.0.1:5000  
✅ Code updated with user validation  
⏳ **Waiting for database table creation**

Once you create the table, the validation will work perfectly!
