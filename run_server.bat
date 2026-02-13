@echo off
echo ========================================
echo CCTV AI System - Starting Server
echo ========================================
echo.

REM Kill any existing Python processes
echo Cleaning up old processes...
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul

echo.
echo Starting server on port 8081...
echo.
echo Open your browser to:
echo http://127.0.0.1:8081
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Start server
python -m uvicorn main:app --host 127.0.0.1 --port 8081

pause
