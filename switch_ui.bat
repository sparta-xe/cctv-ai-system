@echo off
echo ========================================
echo UI Switcher - CCTV AI System
echo ========================================
echo.

echo Current UI options:
echo 1. Classic UI (Original)
echo 2. Futuristic AI Cyber Theme (NEW)
echo.

set /p choice="Select UI (1 or 2): "

if "%choice%"=="1" (
    echo.
    echo Switching to Classic UI...
    if exist templates\dashboard_old.html (
        copy /Y templates\dashboard_old.html templates\dashboard.html >nul
        echo ✅ Classic UI activated
    ) else (
        echo ⚠️  Classic UI backup not found
    )
) else if "%choice%"=="2" (
    echo.
    echo Switching to Futuristic AI Cyber Theme...
    if exist templates\dashboard_v2.html (
        if not exist templates\dashboard_old.html (
            copy templates\dashboard.html templates\dashboard_old.html >nul
        )
        copy /Y templates\dashboard_v2.html templates\dashboard.html >nul
        echo ✅ Futuristic UI activated
    ) else (
        echo ⚠️  New UI file not found
    )
) else (
    echo ❌ Invalid choice
)

echo.
echo Restart server to see changes:
echo python -m uvicorn main:app --host 127.0.0.1 --port 8081
echo.
pause
