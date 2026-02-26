@echo off
cd /d "%~dp0"
echo Starting AnxiSense Backend...
echo IP Address for Android:
ipconfig | findstr /i "ipv4"
echo.
call venv\Scripts\activate
python server.py
pause
