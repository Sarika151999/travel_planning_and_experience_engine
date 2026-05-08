# Vibe-Check Travel Agent - Quick Start Guide

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Python 3.8+
- Node.js 18+
- PostgreSQL 12+ (for local database)
- Google Cloud API keys

### Step 1: Database Setup

```bash
# Create PostgreSQL database
createdb travel_agent

# Or using psql:
psql -U postgres
CREATE DATABASE travel_agent;
```

### Step 2: Backend Setup

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure .env with your Google Cloud credentials
cp .env.example .env
# Edit .env with your:
# - GOOGLE_CLOUD_PROJECT_ID
# - GOOGLE_API_KEY (Gemini)
# - GOOGLE_MAPS_API_KEY
# - GCS_BUCKET_NAME
# - PINECONE_API_KEY (optional, for vector search)
# - DATABASE_URL (update if needed)
```

### Step 3: Frontend Setup

```bash
cd ../frontend
npm install
cp .env.example .env.local
```

### Step 4: Run Services

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python -m uvicorn app.main:app --reload
# Runs on http://localhost:8000
# API Docs: http://localhost:8000/docs
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
# Runs on http://localhost:5173
```

Open **http://localhost:5173** in your browser! 🎉

---

## 📋 Configuration Checklist

- [ ] Install PostgreSQL and create database
- [ ] Create Google Cloud Project
- [ ] Enable Gemini API
- [ ] Enable Google Maps API
- [ ] Create API keys for both
- [ ] Create Cloud Storage bucket
- [ ] Get/download service account key (optional)
- [ ] Setup Pinecone account (optional, for vector search)
- [ ] Fill `.env` in backend with all credentials
- [ ] Run backend
- [ ] Fill `.env.local` in frontend
- [ ] Run frontend

---

## 🧪 Testing

```bash
# Backend Tests
cd backend
pytest tests/ -v

# Frontend Tests
cd frontend
npm run test
```

---

## 🌐 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/v1/health` | Health check |
| POST | `/api/v1/itineraries/generate` | Generate itinerary |
| GET | `/api/v1/itineraries/{id}` | Retrieve itinerary |
| GET | `/api/v1/itineraries` | List recent |

📚 Full API docs: http://localhost:8000/docs

---

## 📱 Features

✅ AI-powered itinerary generation (Gemini API)
✅ Geographic optimization (Google Maps)
✅ Shareable URLs (Cloud Storage)
✅ Mobile-first responsive design
✅ Energy level-based personalization
✅ Budget tracking and breakdown
✅ Day-by-day activity planning
✅ Packing & transport tips

---

## 🔐 Security Features

✅ Input validation on all routes
✅ CORS configured
✅ Environment-based secrets
✅ GCS path sanitization
✅ Error handling middleware
✅ Rate limiting ready

---

## 📊 Tech Stack

**Frontend:**
- React 18 + TypeScript
- Tailwind CSS (mobile-first)
- Zustand (state management)
- Axios (API client)
- Vite (build tool)

**Backend:**
- Python 3.11
- FastAPI (web framework)
- Google Gemini API
- Google Maps API
- Google Cloud Storage

**Infrastructure:**
- Docker & Docker Compose
- Google Cloud Platform

---

## 🐛 Troubleshooting

**Backend won't start?**
```bash
# Check Python version
python --version  # Need 3.8+

# Check port 8000 is free
lsof -i :8000
```

**Frontend can't reach backend?**
```bash
# Verify backend is running
curl http://localhost:8000/api/v1/health

# Check CORS in backend .env
# Ensure http://localhost:5173 is in CORS_ORIGINS
```

**Google Cloud errors?**
```bash
# Verify APIs are enabled
gcloud services list --enabled

# Test API key
curl -X POST https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent?key=YOUR_KEY
```

---

## 📚 Documentation

- [API Documentation](./docs/API.md) - Detailed API reference
- [Setup Guide](./docs/SETUP.md) - Comprehensive setup instructions
- [Architecture](./docs/ARCHITECTURE.md) - System design overview

---

## 🎯 Next Steps

1. **Before Submission:**
   - [ ] Test all features
   - [ ] Run backend tests
   - [ ] Check error handling
   - [ ] Verify mobile responsiveness
   - [ ] Test Google services integration
   - [ ] Validate security practices

2. **Hackathon Submission:**
   - [ ] Document API usage
   - [ ] Include setup instructions
   - [ ] Add example itinerary responses
   - [ ] Highlight Google Services usage
   - [ ] Showcase accessibility features

3. **Post-Hackathon (Bonus):**
   - [ ] Add user authentication
   - [ ] Implement database persistence
   - [ ] Add CI/CD pipelines
   - [ ] Set up monitoring
   - [ ] Scale to production

---

## ❓ FAQ

**Q: Can I use this without Google Cloud?**
A: No, the Gemini API and Cloud Storage are core features.

**Q: Is there user authentication?**
A: Not in the base setup. Easy to add JWT later.

**Q: Can I deploy this?**
A: Yes! Dockerfiles included for both frontend and backend.

**Q: What about database?**
A: Docker Compose includes PostgreSQL. Update backend as needed.

---

## 🏆 Evaluation Criteria

This project covers:
- ✅ **Code Quality**: Type-safe, well-structured, modular design
- ✅ **Security**: Input validation, secrets management, CORS
- ✅ **Efficiency**: Async operations, optimized API calls
- ✅ **Testing**: Unit tests included, easy to expand
- ✅ **Accessibility**: WCAG 2.1, semantic HTML, keyboard nav
- ✅ **Google Services**: Gemini + Maps + Cloud Storage

---

## 📞 Support

For issues:
1. Check the troubleshooting section
2. Review logs in terminal
3. Check API docs at /docs
4. Consult architecture doc

---

**Good luck in the hackathon! 🚀**

May the best itinerary win! ✈️🌍
