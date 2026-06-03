# 🎬 YouTube Video Summarizer

An AI-powered web application that automatically extracts transcripts from YouTube videos and generates concise, intelligent summaries using advanced NLP transformers.

**Live Demo:** [Coming Soon](#)  
**GitHub Repository:** [Your Repo Link](#)  

---

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

### Core Features
✅ **YouTube URL Input** - Accept any YouTube video URL  
✅ **Automatic Transcript Extraction** - Extract subtitles/captions automatically  
✅ **AI Summarization** - Generate concise summaries using facebook/bart-large-cnn  
✅ **Database Storage** - Save all summaries for future reference  
✅ **Summary History** - View and manage all previous summaries  
✅ **Dark Mode** - Comfortable viewing with built-in dark mode toggle  

### Advanced Features
🔹 **Compression Analytics** - Track how much text is reduced  
🔹 **Word Count Tracking** - Monitor transcript and summary lengths  
🔹 **Copy & Download** - Export summaries as text files  
🔹 **Search Functionality** - Find previous summaries easily  
🔹 **Statistics Dashboard** - View application-wide analytics  
🔹 **Responsive Design** - Works perfectly on desktop, tablet, and mobile  
🔹 **Error Handling** - Comprehensive error messages and recovery  
🔹 **Logging** - Complete activity logging for debugging  

---

## 🛠️ Tech Stack

### Backend
- **Python 3.8+** - Core programming language
- **Flask 2.3+** - Web framework
- **SQLite** - Database
- **youtube-transcript-api** - Transcript extraction
- **Transformers (HuggingFace)** - NLP models
- **PyTorch 2.0** - Deep learning framework
- **NLTK** - Natural language processing

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with dark mode
- **Vanilla JavaScript** - Interactive features
- **Responsive Design** - Mobile-first approach

### Development Tools
- **python-dotenv** - Environment configuration
- **logging** - Activity tracking

---

## 📁 Project Structure

```
YouTube-Summarizer/
│
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── summaries.db               # SQLite database
├── app.log                    # Application logs
├── .gitignore                 # Git ignore file
├── .env.example               # Environment variables template
├── README.md                  # Documentation
│
├── templates/                 # HTML templates
│   ├── index.html            # Home page with summarizer
│   ├── history.html          # Summary history and analytics
│   └── result.html           # Result display page
│
├── static/                    # Static assets
│   └── style.css             # Complete styling (with dark mode)
│
├── utils/                     # Utility modules
│   ├── __init__.py
│   ├── transcript.py         # Transcript extraction logic
│   └── summarizer.py         # AI summarization logic
│
└── database/                  # Database module
    ├── __init__.py
    └── db.py                 # Database operations
```

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional)
- ~2GB free disk space (for transformer models)

### Step 1: Clone Repository

```bash
# Clone the repository
git clone https://github.com/yourusername/YouTube-Summarizer.git
cd YouTube-Summarizer

# Or download as ZIP and extract
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt

# Download NLTK data (first run)
python -c "import nltk; nltk.download('punkt')"
```

### Step 4: Initialize Database

```bash
# Start Python interactive shell
python

# Inside Python shell:
from app import app
with app.app_context():
    from database.db import init_db
    init_db(app)
    print("Database initialized!")

# Exit Python shell
exit()
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```bash
# .env file
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE=summaries.db
LOG_LEVEL=INFO
MAX_CONTENT_LENGTH=16777216
```

### Configuration Options

**app.py** contains these settings:

```python
app.config['DATABASE'] = 'summaries.db'           # Database location
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max upload: 16MB
```

---

## 📖 Usage

### Running the Application

```bash
# Make sure virtual environment is activated
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# Run the Flask app
python app.py

# Or use Flask CLI:
flask run
```

The application will be available at:
```
http://localhost:5000
```

### Using the Web Interface

#### Home Page (/)
1. **Paste YouTube URL** in the input field
2. Click **"Summarize Video"** button
3. Wait for extraction and summarization
4. View the generated summary with statistics
5. **Copy** or **Download** the summary

#### History Page (/history)
1. View all previous summaries
2. **Search** for specific summaries
3. **View** full summary details in modal
4. **Download** individual summaries
5. **Delete** unwanted summaries

#### Features in Action

**Dark Mode Toggle**
- Click moon/sun icon in header
- Preference is saved to browser

**Statistics Dashboard**
- View total summaries created
- Track words processed
- Monitor average compression ratio
- See average summary length

---

## 🔌 API Documentation

### Endpoints

#### 1. Summarize Video
```http
POST /api/summarize
Content-Type: application/json

{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

**Response (Success - 200):**
```json
{
  "success": true,
  "status": "success",
  "data": {
    "summary": "...",
    "transcript": "...",
    "statistics": {
      "transcript": {
        "word_count": 2000,
        "character_count": 12000,
        "sentence_count": 150,
        "avg_word_length": 5.2,
        "avg_sentence_length": 13.3
      },
      "summary": {
        "word_count": 150,
        "character_count": 900,
        "sentence_count": 10,
        "avg_word_length": 5.4,
        "avg_sentence_length": 15
      },
      "compression_ratio": 92.5,
      "processing_time": "N/A"
    }
  }
}
```

**Response (Error - 400):**
```json
{
  "error": "Invalid YouTube URL...",
  "status": "error"
}
```

#### 2. Get History
```http
GET /api/history
```

**Response:**
```json
{
  "success": true,
  "count": 5,
  "data": [
    {
      "id": 1,
      "url": "https://youtube.com/watch?v=...",
      "video_id": "dQw4w9WgXcQ",
      "transcript": "...",
      "summary": "...",
      "transcript_length": 2000,
      "summary_length": 150,
      "compression_ratio": 92.5,
      "created_at": "2024-06-03T10:30:00"
    }
  ]
}
```

#### 3. Get Summary Details
```http
GET /api/summary/:id
```

#### 4. Delete Summary
```http
DELETE /api/delete/:id
```

#### 5. Get Analytics
```http
GET /api/analytics
```

**Response:**
```json
{
  "success": true,
  "data": {
    "total_summaries": 25,
    "total_words_processed": 50000,
    "average_compression_ratio": 87.3,
    "total_summary_words": 6250,
    "last_summary_time": "2024-06-03T15:45:00",
    "average_summary_length": 250
  }
}
```

#### 6. Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-06-03T15:45:00"
}
```

---

## 💾 Database Schema

### Summaries Table

```sql
CREATE TABLE summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    video_id TEXT UNIQUE,
    transcript TEXT NOT NULL,
    summary TEXT NOT NULL,
    transcript_length INTEGER DEFAULT 0,
    summary_length INTEGER DEFAULT 0,
    compression_ratio REAL DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_video_id ON summaries(video_id);
CREATE INDEX idx_created_at ON summaries(created_at);
```

---

## 🌍 Deployment

### Option 1: Deploy on Heroku

```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login

# Create Heroku app
heroku create your-app-name

# Set environment variables
heroku config:set FLASK_ENV=production

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

### Option 2: Deploy on PythonAnywhere

1. Sign up at [www.pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload your code
3. Create a new web app
4. Configure WSGI file
5. Set up virtual environment
6. Reload the app

**WSGI Configuration:**
```python
import sys
path = '/home/yourusername/YouTube-Summarizer'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

### Option 3: Deploy on Render

1. Push code to GitHub
2. Sign up at [render.com](https://render.com)
3. Create new Web Service
4. Connect GitHub repository
5. Set build command: `pip install -r requirements.txt`
6. Set start command: `python app.py`
7. Set PORT environment variable to `5000`

### Option 4: Deploy on Railway

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up
```

### Production Checklist

- [ ] Set `FLASK_ENV=production`
- [ ] Set `FLASK_DEBUG=False`
- [ ] Use strong `SECRET_KEY`
- [ ] Enable HTTPS/SSL
- [ ] Set up proper logging
- [ ] Configure database backups
- [ ] Monitor application performance
- [ ] Set up error alerts
- [ ] Configure rate limiting
- [ ] Use environment variables for secrets

---

## 🐛 Troubleshooting

### Common Issues

#### 1. "No module named 'transformers'"

**Solution:**
```bash
pip install transformers
pip install torch
```

#### 2. "youtube-transcript-api error"

**Cause:** Video might not have captions or be private

**Solution:**
- Check if video has subtitles/captions enabled
- Try a different video
- Ensure URL is correct

#### 3. "Database locked"

**Solution:**
```bash
# Delete and recreate database
rm summaries.db

# Reinitialize
python
>>> from app import app
>>> with app.app_context():
>>>     from database.db import init_db
>>>     init_db(app)
```

#### 4. "Port 5000 already in use"

**Solution:**
```bash
# Use different port
python app.py --port 5001

# Or in Flask:
app.run(port=5001)
```

#### 5. "NLTK punkt tokenizer not found"

**Solution:**
```bash
python
>>> import nltk
>>> nltk.download('punkt')
```

#### 6. "Out of Memory during summarization"

**Solution:**
- Reduce model size in `utils/summarizer.py`
- Use GPU if available
- Limit transcript length

#### 7. "SSL Certificate Error"

**Solution:**
```bash
# Install certifi
pip install certifi

# Or disable SSL (not recommended for production)
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
```

### Debugging

**Enable Debug Logging:**
```python
# In app.py, change logging level
logging.basicConfig(level=logging.DEBUG)
```

**Check Logs:**
```bash
# View application logs
tail -f app.log

# Clear logs
> app.log
```

**Test API Endpoints:**
```bash
# Using curl
curl http://localhost:5000/health

curl -X POST http://localhost:5000/api/summarize \
  -H "Content-Type: application/json" \
  -d '{"url":"https://youtube.com/watch?v=dQw4w9WgXcQ"}'
```

---

## 📚 NLP & Transformer Model Explanation

### How It Works

#### 1. **Transcript Extraction**
```
YouTube Video
    ↓
youtube-transcript-api
    ↓
Transcript Text
```

The app uses `youtube-transcript-api` to fetch video captions/subtitles.

#### 2. **Text Processing**
```
Raw Transcript
    ↓
Cleaning & Tokenization (NLTK)
    ↓
Processed Text
```

Text is cleaned and split into sentences using NLTK.

#### 3. **Summarization Pipeline**
```
Processed Text
    ↓
facebook/bart-large-cnn (Transformer Model)
    ↓
Abstractive Summary
```

**BART (Bidirectional Auto-Regressive Transformers)** is used for summarization.

### Key Concepts

**Abstractive Summarization:**
- Creates entirely new sentences that capture essence of original
- More natural than extractive
- Uses seq2seq transformer architecture

**Compression Ratio:**
- Percentage of text reduced
- Formula: `(1 - summary_words / original_words) * 100`
- Higher = more aggressive compression

**Transformer Architecture:**
- Encoder: Encodes input text into representations
- Decoder: Generates summary from encoded representations
- Attention mechanism: Focuses on relevant parts

---

## 🤝 Contributing

Contributions are welcome! Here's how to contribute:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Commit with clear messages**
   ```bash
   git commit -m "Add amazing feature"
   ```
5. **Push to branch**
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open a Pull Request**

### Areas for Contribution
- [ ] Support for more languages
- [ ] PDF summarization
- [ ] Export to PDF format
- [ ] Advanced filtering options
- [ ] User authentication
- [ ] API rate limiting
- [ ] Performance optimization
- [ ] Additional test coverage

---

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

---

## 🎯 Roadmap

### v1.1 (Next Release)
- [ ] User authentication & profiles
- [ ] Email export functionality
- [ ] Batch summarization
- [ ] API key system

### v1.2 (Future)
- [ ] PDF video support
- [ ] Multi-language support
- [ ] Custom summarization length
- [ ] Advanced analytics

### v2.0 (Long-term)
- [ ] Mobile app (React Native)
- [ ] Real-time collaboration
- [ ] Enterprise features
- [ ] Advanced AI models

---

## 📞 Support

For support, email support@yourdomain.com or open an issue on GitHub.

---

## 🙏 Acknowledgments

- [Hugging Face](https://huggingface.co/) for transformer models
- [NLTK](https://www.nltk.org/) for NLP toolkit
- [YouTube Transcript API](https://github.com/jderose9/youtube-transcript-api)
- [Flask](https://flask.palletsprojects.com/) web framework

---

**Star this project if you find it helpful! ⭐**

Last Updated: June 2024
