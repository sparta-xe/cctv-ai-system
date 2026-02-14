@echo off
REM Kill process using port 8000
echo Checking for process on port 8000...

for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do (
    echo Found process: %%a
    taskkill /PID %%a /F
    echo Process killed successfully!
    goto :done
)

echo No process found on port 8000

:done
pause
