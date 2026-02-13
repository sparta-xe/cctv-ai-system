# 🔧 Quick Fix: Port 8000 Already in Use

## Problem
```
ERROR: [Errno 10048] error while attempting to bind on address ('0.0.0.0', 8000)
```

This means port 8000 is already being used by another process (probably a previous instance of the server).

## ✅ Solution 1: Use Port 8080 (Easiest)

Just run on a different port:

```bash
python start_on_port_8080.py
```

Then open: **http://127.0.0.1:8080**

---

## ✅ Solution 2: Use the Fix Script

Run the interactive fixer:

```bash
python fix_port_issue.py
```

Choose option 1 to kill the old process and start fresh.

---

## ✅ Solution 3: Manual Fix (Windows)

### Step 1: Find the process
```powershell
netstat -ano | findstr :8000
```

You'll see something like:
```
TCP    0.0.0.0:8000    0.0.0.0:0    LISTENING    12345
```

The last number (12345) is the Process ID (PID).

### Step 2: Kill the process
```powershell
taskkill /F /PID 12345
```

Replace 12345 with your actual PID.

### Step 3: Start server
```bash
python main.py
```

---

## ✅ Solution 4: Use Different Port in Code

Edit `main.py` at the bottom:

```python
# Change this:
uvicorn.run(app, host="0.0.0.0", port=8000)

# To this:
uvicorn.run(app, host="0.0.0.0", port=8080)
```

Then run:
```bash
python main.py
```

Open: **http://127.0.0.1:8080**

---

## ✅ Solution 5: Use Command Line

Start with custom port:

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8080
```

Open: **http://127.0.0.1:8080**

---

## 🎯 Recommended: Use Port 8080

The easiest solution is to just use port 8080:

```bash
python start_on_port_8080.py
```

Everything works exactly the same, just on a different port!

---

## 🔍 Why This Happens

Common causes:
1. Previous server instance still running
2. Another application using port 8000
3. Server crashed but port not released
4. Multiple terminal windows running server

---

## 💡 Prevention

To avoid this in the future:

1. **Always stop server properly** (Ctrl+C)
2. **Check if server is running** before starting new one
3. **Close terminal** when done
4. **Use port 8080** as default to avoid conflicts

---

## ✅ Quick Commands

### Check if port is in use:
```powershell
netstat -ano | findstr :8000
```

### Kill all Python processes (careful!):
```powershell
taskkill /F /IM python.exe
```

### Start on port 8080:
```bash
python start_on_port_8080.py
```

---

## 🎉 After Fix

Once server starts successfully, you'll see:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Then open your browser and enjoy! 🚀
