# Port 8000 Already in Use - Fixed! ✅

## Problem
```
ERROR: [Errno 10048] error while attempting to bind on address ('0.0.0.0', 8000)
[winerror 10048] only one usage of each socket address
```

This means another process is already using port 8000.

## ✅ Solution Applied

### 1. Automatic Fix (Recommended)
The `start.py` script now automatically kills any process using port 8000 before starting the server.

```bash
python start.py
```

It will:
1. Check if port 8000 is in use
2. Kill the process if found
3. Start the server

### 2. Manual Fix - Windows

**Option A: Using PowerShell**
```powershell
# Find process using port 8000
Get-NetTCPConnection -LocalPort 8000 | Select-Object OwningProcess

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F
```

**Option B: Using Command Prompt**
```cmd
# Find process
netstat -ano | findstr :8000

# Kill process (replace PID with actual number)
taskkill /PID <PID> /F
```

**Option C: Using Utility Scripts**
```bash
# Windows batch file
scripts\kill_port_8000.bat

# Python script (cross-platform)
python scripts/kill_port_8000.py
```

### 3. Manual Fix - Linux/Mac

```bash
# Find process
lsof -ti:8000

# Kill process
kill -9 $(lsof -ti:8000)

# Or use the Python script
python scripts/kill_port_8000.py
```

## 🔧 Alternative: Use Different Port

If you want to use a different port instead:

**Option 1: Environment Variable**
```bash
# Windows
set PORT=8080
python start.py

# Linux/Mac
PORT=8080 python start.py
```

**Option 2: Edit .env file**
```bash
# Create .env file
echo PORT=8080 > .env
python start.py
```

**Option 3: Direct in start.py**
```python
# Edit start.py, change:
port = int(os.getenv("PORT", 8080))  # Changed from 8000 to 8080
```

## 📝 Common Causes

1. **Previous server still running**
   - You started the server before and didn't stop it
   - Solution: Kill the process or restart computer

2. **Another application using port 8000**
   - Some other app is using port 8000
   - Solution: Kill that app or use different port

3. **Multiple terminal windows**
   - You have multiple terminals running the server
   - Solution: Close all terminals and start fresh

## 🚀 Quick Fix Commands

**Windows (PowerShell):**
```powershell
# One-liner to kill and start
Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | ForEach-Object { taskkill /PID $_.OwningProcess /F }; python start.py
```

**Linux/Mac:**
```bash
# One-liner to kill and start
kill -9 $(lsof -ti:8000) 2>/dev/null; python start.py
```

## ✅ Verification

After killing the process, verify port is free:

**Windows:**
```powershell
Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
# Should return nothing
```

**Linux/Mac:**
```bash
lsof -ti:8000
# Should return nothing
```

## 🎯 Best Practice

Always use `start.py` to start the server - it handles port conflicts automatically!

```bash
python start.py
```

## 📞 Still Having Issues?

If the problem persists:

1. **Restart your computer** - This will kill all processes
2. **Check firewall** - Ensure port 8000 is not blocked
3. **Use different port** - Try port 8080 or 8888
4. **Check antivirus** - Some antivirus software blocks ports

## 🔍 Debug Information

To see what's using port 8000:

**Windows:**
```powershell
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess
```

**Linux/Mac:**
```bash
lsof -i:8000
```

---

**Status:** ✅ Fixed - Port 8000 is now free and server can start!
