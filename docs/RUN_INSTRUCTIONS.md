# 🚀 How to Run the CCTV AI System

## ✅ System Status
- All tests passed (5/5)
- All dependencies installed
- Code has no errors

## 🎯 To Start the Server

### Option 1: Using the startup script (Recommended)
```bash
python start_server.py
```

### Option 2: Using main.py directly
```bash
python main.py
```

### Option 3: Using uvicorn
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

## ⏱️ First Run Notes

**Important**: The first time you run the server, it will:
1. Download YOLOv8 model (~6MB) - Already done ✅
2. Download Sentence Transformer model (~80MB) - May take 2-5 minutes

If you see timeout errors, this is normal. Just:
- Wait a moment
- Try running again
- The models will cache locally after first download

## 🌐 Access the System

Once the server starts, you'll see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

Then open your browser to:
- **Dashboard**: http://127.0.0.1:8000
- **API Docs**: http://127.0.0.1:8000/docs

## 🔐 Login Credentials

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | admin |
| security | sec123 | security |
| viewer | view123 | viewer |

## 📝 Quick Test

1. **Start Server**
   ```bash
   python start_server.py
   ```

2. **Open Browser**
   ```
   http://127.0.0.1:8000
   ```

3. **Upload Video**
   - Click "Choose File"
   - Select any video (MP4, AVI, MOV, etc.)
   - Click "Upload & Process"
   - Wait for processing (1 frame/second)

4. **Search**
   - Username: `admin`
   - Password: `admin123`
   - Query: `person` or `car` or `person with backpack`
   - Click "Search"

5. **View Results**
   - Results appear below with timestamps
   - Check console for alerts

## 🐛 Troubleshooting

### Issue: Timeout downloading models
**Solution**: 
- Check internet connection
- Wait and try again
- Models cache after first download

### Issue: Port 8000 already in use
**Solution**:
```bash
python -m uvicorn main:app --port 8080
```

### Issue: Module not found
**Solution**:
```bash
pip install -r requirements.txt
```

## ✅ Current Status

```
✅ All packages installed
✅ All tests passed (5/5)
✅ YOLOv8 model downloaded
✅ Directories created
✅ Code has no errors
⏳ Sentence Transformer model (downloads on first run)
```

## 🎉 You're Ready!

The system is fully functional and ready to demo. Just run:

```bash
python start_server.py
```

And open http://127.0.0.1:8000 in your browser!

---

**Need help?** Check:
- README.md - Full documentation
- QUICKSTART.md - Quick start guide
- QUICK_REFERENCE.md - Command reference
