# 🚀 QUICK START GUIDE

Get YouTube Summarizer running in 5 minutes!

## Prerequisites
- Python 3.8+
- pip
- ~2GB disk space

## Step-by-Step Setup

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Initialize Database
```bash
python -c "from app import app; from database.db import init_db; app.app_context().push(); init_db(app); print('✅ Database ready!')"
```

### 3️⃣ Download Models (First Run)
```bash
python -c "from utils.summarizer import summarizer; print('✅ Models loaded!')"
```

### 4️⃣ Run the Application
```bash
python app.py
```

### 5️⃣ Open in Browser
```
http://localhost:5000
```

## 🎯 Quick Test

1. Copy a YouTube URL: `https://youtube.com/watch?v=jNQXAC9IVRw`
2. Paste into the input field
3. Click "Summarize Video"
4. Wait for processing (15-30 seconds first time)
5. View your summary! 📊

## Troubleshooting Quick Fixes

| Problem | Fix |
|---------|-----|
| "No module named..." | `pip install -r requirements.txt` |
| Port already in use | Change port: `app.run(port=5001)` |
| Model download error | Check internet connection |
| Database locked | Delete summaries.db and reinitialize |

## Next Steps

- 📖 Read [README.md](README.md) for full documentation
- 🏗️ Read [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
- ⚙️ Copy `.env.example` to `.env` and customize settings
- 🚀 Deploy using [Deployment Guide](README.md#-deployment)

---

**Enjoy summarizing! 🎬**
