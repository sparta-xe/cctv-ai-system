# 🔧 Troubleshooting: Can't Reach Server

## Problem
Server won't start or shows "Can't reach server" in browser.

## Common Causes & Solutions

### Issue 1: Port Already in Use
**Error:** `[Errno 10048] error while attempting to bind on address`

**Solution:**
```bash
# Try port 8081 instead
python -m uvicorn main:app --host 127.0.0.1 --port 8081
```

Then open: **http://127.0.0.1:8081**

---

### Issue 2: Hugging Face Timeout
**Error:** `ReadTimeoutError HTTPSConnectionPool(host='huggingface.co'...`

**This is normal on first run!** The system is downloading AI models.

**Solutions:**

**Option A: Wait it out (2-5 minutes)**
- The models are downloading
- It will work after download completes
- Models are cached for future runs

**Option B: Use offline mode**
```bash
# Set environment variable
set HF_HUB_OFFLINE=1
python main.py
```

**Option C: Pre-download models**
```bash
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

---

### Issue 3: Server Not Starting

**Check 1: Is Python running?**
```bash
# Check if server process exists
tasklist | findstr python
```

**Check 2: Try different port**
```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8081
```

**Check 3: Check for errors**
Look at the terminal output for error messages.

---

## ✅ Step-by-Step Fix

### Step 1: Kill All Python Processes
```powershell
taskkill /F /IM python.exe
```

### Step 2: Clear Port
```powershell
# Check what's on port 8000
netstat -ano | findstr :8000

# If something is there, kill it (replace PID)
taskkill /F /PID <PID>
```

### Step 3: Start on Safe Port
```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8081
```

### Step 4: Open Browser
```
http://127.0.0.1:8081
```

---

## 🎯 Quick Commands

### Try These in Order:

**1. Simple start on port 8081:**
```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8081
```

**2. If that fails, try 8082:**
```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8082
```

**3. If still failing, check logs:**
```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8081 --log-level debug
```

---

## 🔍 Diagnostic Commands

### Check if server is running:
```powershell
netstat -ano | findstr :8000
netstat -ano | findstr :8080
netstat -ano | findstr :8081
```

### Check Python processes:
```powershell
tasklist | findstr python
```

### Test if port is accessible:
```powershell
Test-NetConnection -ComputerName 127.0.0.1 -Port 8081
```

---

## 💡 Working Configuration

If nothing else works, use this guaranteed method:

### 1. Create `run_server.bat`:
```batch
@echo off
echo Starting CCTV AI System...
python -m uvicorn main:app --host 127.0.0.1 --port 8081 --reload
pause
```

### 2. Double-click `run_server.bat`

### 3. Wait for:
```
INFO:     Uvicorn running on http://127.0.0.1:8081
```

### 4. Open browser:
```
http://127.0.0.1:8081
```

---

## 🚨 Emergency: Nothing Works?

### Nuclear Option (Start Fresh):

```bash
# 1. Kill everything
taskkill /F /IM python.exe

# 2. Delete cache
rmdir /s /q __pycache__
rmdir /s /q .pytest_cache

# 3. Reinstall dependencies
pip install --upgrade --force-reinstall fastapi uvicorn

# 4. Start on random port
python -m uvicorn main:app --host 127.0.0.1 --port 9999
```

Then open: **http://127.0.0.1:9999**

---

## ✅ Success Indicators

Server is running correctly when you see:

```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8081 (Press CTRL+C to quit)
```

---

## 🎯 Most Common Solution

**90% of the time, this works:**

```bash
# Kill old processes
taskkill /F /IM python.exe

# Start on port 8081
python -m uvicorn main:app --host 127.0.0.1 --port 8081

# Open browser
start http://127.0.0.1:8081
```

---

## 📞 Still Not Working?

1. **Check firewall** - Allow Python through Windows Firewall
2. **Check antivirus** - May be blocking the server
3. **Try different browser** - Chrome, Firefox, Edge
4. **Restart computer** - Sometimes helps clear port locks
5. **Check internet** - Needed for first-time model download

---

## 🎉 Once It Works

You'll see the beautiful dashboard at:
- http://127.0.0.1:8081

With:
- Upload video section
- Search section
- Results with images
- Video playback
- Timeline markers

**Everything will work perfectly!** 🚀
