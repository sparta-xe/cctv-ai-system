@echo off
echo ========================================
echo GitHub Push Script
echo ========================================
echo.

REM Check if git is initialized
if not exist .git (
    echo Initializing Git repository...
    git init
    echo.
)

REM Add all files
echo Adding all files...
git add .
echo.

REM Commit
echo Creating commit...
set /p commit_message="Enter commit message (or press Enter for default): "
if "%commit_message%"=="" (
    git commit -m "Update: CCTV AI System with video playback and query highlighting"
) else (
    git commit -m "%commit_message%"
)
echo.

REM Check if remote exists
git remote -v | findstr origin >nul
if errorlevel 1 (
    echo.
    echo ========================================
    echo SETUP REQUIRED
    echo ========================================
    echo.
    echo 1. Go to: https://github.com/new
    echo 2. Create repository: cctv-ai-system
    echo 3. DO NOT initialize with README
    echo 4. Copy the repository URL
    echo.
    set /p repo_url="Enter your GitHub repository URL: "
    git remote add origin %repo_url%
    git branch -M main
    echo.
)

REM Push to GitHub
echo Pushing to GitHub...
git push -u origin main
echo.

if errorlevel 0 (
    echo ========================================
    echo SUCCESS!
    echo ========================================
    echo.
    echo Your code is now on GitHub!
    echo.
) else (
    echo ========================================
    echo PUSH FAILED
    echo ========================================
    echo.
    echo Possible issues:
    echo 1. Authentication failed - use personal access token
    echo 2. Remote not set - check repository URL
    echo 3. Network issue - check internet connection
    echo.
    echo Try manual push:
    echo git push -u origin main
    echo.
)

pause
