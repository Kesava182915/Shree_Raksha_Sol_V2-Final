@echo off
cd /d "%~dp0"
echo ============================================================
echo   SHREERAKSHA SOLUTIONS - GST INVOICE & ENTERPRISE SUITE
echo   Starting Backend Database & Production Web Server...
echo ============================================================
start "" "http://127.0.0.1:8080"
python server.py
