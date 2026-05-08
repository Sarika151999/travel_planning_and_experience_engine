# Setup Guide - Vibe-Check Travel Agent

## Prerequisites

- Python 3.8+ (for backend)
- Node.js 18+ (for frontend)
- Google Cloud Project with:
  - Gemini API enabled
  - Google Maps API key
  - Cloud Storage bucket created
- npm or yarn

---

## Backend Setup

### 1. Install Python Dependencies

```bash
cd backend
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your Google Cloud credentials:

```bash
cp .env.example .env
```

Edit `.env`:
```
GOOGLE_CLOUD_PROJECT_ID=your-project-id
GOOGLE_API_KEY=your-gemini-api-key
GOOGLE_MAPS_API_KEY=your-google-maps-key
GCS_BUCKET_NAME=your-gcs-bucket-name
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### 3. Set Up Google Cloud Storage

**Option A: Using Service Account Key**
```bash
# Download service account JSON from Google Cloud Console
# Place in backend/ directory as gcs-key.json
```

**Option B: Using Application Default Credentials**
```bash
gcloud auth application-default login
```

### 4. Run Backend

```bash
python -m uvicorn app.main:app --reload
```

Backend will be available at `http://localhost:8000`

- API docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/api/v1/health`

---

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env.local`:

```bash
cp .env.example .env.local
```

Edit `.env.local` (optional, defaults work):
```
VITE_API_URL=http://localhost:8000/api/v1
```

### 3. Run Development Server

```bash
npm run dev
```

Frontend will be available at `http://localhost:5173`

### 4. Build for Production

```bash
npm run build
npm run preview
```

---

## Environment Variables Reference

### Backend (.env)

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| GOOGLE_CLOUD_PROJECT_ID | Yes | GCP Project ID | my-project-123456 |
| GOOGLE_API_KEY | Yes | Gemini API Key | AIzaSyD... |
| GOOGLE_MAPS_API_KEY | Yes | Maps API Key | AIzaSyD... |
| GCS_BUCKET_NAME | Yes | Cloud Storage Bucket | my-travel-bucket |
| ENVIRONMENT | No | Environment | development/production |
| DEBUG | No | Debug mode | true/false |
| LOG_LEVEL | No | Logging level | INFO/DEBUG/WARNING |
| CORS_ORIGINS | No | Allowed origins | http://localhost:3000 |
| GCS_JSON_KEY_PATH | No | Path to service account key | ./gcs-key.json |

### Frontend (.env.local)

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| VITE_API_URL | No | API base URL | http://localhost:8000/api/v1 |
| VITE_ENVIRONMENT | No | Environment | development/production |

---

## Google Cloud Setup

### 1. Create a GCP Project

```bash
gcloud projects create vibe-check-travel
gcloud config set project vibe-check-travel
```

### 2. Enable Required APIs

```bash
# Enable Gemini API
gcloud services enable generativeai.googleapis.com

# Enable Maps API
gcloud services enable maps.googleapis.com

# Enable Cloud Storage
gcloud services enable storage-api.googleapis.com
```

### 3. Create API Keys

**For Gemini API:**
```bash
# Go to Google Cloud Console > APIs & Services > Credentials
# Create API key (restrict to Gemini API)
```

**For Google Maps:**
```bash
# Go to Google Cloud Console > APIs & Services > Credentials
# Create API key (restrict to Maps API)
```

### 4. Create Cloud Storage Bucket

```bash
gsutil mb gs://my-travel-bucket

# Set bucket to allow public reads for shareable URLs
gsutil iam ch serviceAccount:your-service-account@project.iam.gserviceaccount.com:roles/storage.admin gs://my-travel-bucket
```

### 5. Create Service Account (Optional)

```bash
gcloud iam service-accounts create travel-agent-sa

gcloud iam service-accounts keys create gcs-key.json \
  --iam-account=travel-agent-sa@vibe-check-travel.iam.gserviceaccount.com
```

---

## Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app

# Run specific test file
pytest tests/test_backend.py -v
```

### Frontend Tests

```bash
cd frontend

# Run tests
npm run test

# Run with coverage
npm run test -- --coverage
```

---

## Deployment

### Deploy Backend to Google Cloud Run

```bash
cd backend

# Build Docker image
docker build -t gcr.io/PROJECT_ID/travel-agent .

# Push to Container Registry
docker push gcr.io/PROJECT_ID/travel-agent

# Deploy to Cloud Run
gcloud run deploy travel-agent \
  --image gcr.io/PROJECT_ID/travel-agent \
  --platform managed \
  --region us-central1 \
  --set-env-vars="GOOGLE_CLOUD_PROJECT_ID=PROJECT_ID,GOOGLE_API_KEY=YOUR_KEY,..."
```

### Deploy Frontend to Vercel/Netlify

```bash
cd frontend

# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

Or with Netlify:
```bash
npm i -g netlify-cli
netlify deploy
```

---

## Troubleshooting

### Backend not starting?

1. Check Python version: `python --version` (need 3.8+)
2. Verify virtual environment: `which python` (should show venv path)
3. Check requirements: `pip list | grep fastapi`
4. Check port 8000 is not in use: `lsof -i :8000`

### Frontend not connecting to backend?

1. Ensure backend is running: `curl http://localhost:8000/api/v1/health`
2. Check CORS configuration in `.env`
3. Check network tab in browser dev tools for 403 errors
4. Verify API URL in `.env.local`

### Google Cloud errors?

1. Verify API keys are correct
2. Check APIs are enabled: `gcloud services list --enabled`
3. Verify service account has necessary permissions
4. Check Cloud Storage bucket exists: `gsutil ls gs://my-travel-bucket`

---

## Next Steps

1. Customize the UI with your branding
2. Add user authentication
3. Implement user history/favorites
4. Add real-time itinerary updates
5. Set up CI/CD pipelines
6. Configure analytics and monitoring
