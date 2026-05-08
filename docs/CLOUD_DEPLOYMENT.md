# Cloud Run Deployment Guide - Vibe-Check Travel Agent

## 🚀 Phase 2: Production Deployment with Google Cloud

This guide walks you through deploying to Google Cloud Run with advanced Google services integration.

---

## 📋 Step 1: Set Up Google Cloud Project

### 1.1 Create/Select Project
```bash
# Create new project
gcloud projects create vibe-check-travel --name="Vibe-Check Travel Agent"

# Set as active
gcloud config set project vibe-check-travel

# Get project ID
gcloud config get-value project
# Output: vibe-check-travel
```

### 1.2 Enable Required APIs
```bash
# Enable all necessary APIs
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  generativeai.googleapis.com \
  maps-backend.googleapis.com \
  storage-api.googleapis.com \
  firestore.googleapis.com \
  logging.googleapis.com \
  monitoring.googleapis.com \
  cloudtasks.googleapis.com
```

### 1.3 Set Up Billing
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Select your project
3. Click on **Billing** in sidebar
4. Link a billing account
5. **Note**: You get $300 free credits for first 90 days!

---

## 🔑 Step 2: Get All Required API Keys & Credentials

### 2.1 Gemini API Key
```bash
# Go to: https://aistudio.google.com/app/apikey
# Click "Get API Key"
# Copy the key
export GEMINI_API_KEY="your-key-here"
```

### 2.2 Google Maps API Key
```bash
# Go to: https://console.cloud.google.com/google/maps-apis
# Click "CREATE CREDENTIALS"
# Select "API Key"
# Restrict to:
#   - Maps SDK for Android (if needed)
#   - Maps SDK for iOS (if needed)
#   - Places API
#   - Maps JavaScript API
# Copy the key
export MAPS_API_KEY="your-key-here"
```

### 2.3 Service Account Key (for Cloud Storage)
```bash
# Create service account
gcloud iam service-accounts create travel-agent-sa \
  --display-name="Travel Agent Service Account"

# Create and download key
gcloud iam service-accounts keys create sa-key.json \
  --iam-account=travel-agent-sa@vibe-check-travel.iam.gserviceaccount.com

# Grant necessary permissions
gcloud projects add-iam-policy-binding vibe-check-travel \
  --member=serviceAccount:travel-agent-sa@vibe-check-travel.iam.gserviceaccount.com \
  --role=roles/storage.admin

gcloud projects add-iam-policy-binding vibe-check-travel \
  --member=serviceAccount:travel-agent-sa@vibe-check-travel.iam.gserviceaccount.com \
  --role=roles/firestore.user

gcloud projects add-iam-policy-binding vibe-check-travel \
  --member=serviceAccount:travel-agent-sa@vibe-check-travel.iam.gserviceaccount.com \
  --role=roles/logging.logWriter
```

### 2.4 Pinecone API Key (for Vector Search)
```bash
# Go to: https://app.pinecone.io
# Sign up (free tier available)
# Create organization
# Create API Key
# Get Environment name (e.g., us-west4-gcp-free)
# Create index: travel-itineraries (dimension: 1536)
export PINECONE_API_KEY="your-key-here"
export PINECONE_ENV="us-west4-gcp-free"
```

---

## 🏗️ Step 3: Create Google Cloud Storage Bucket

```bash
# Create bucket
gsutil mb -l us-central1 gs://vibe-check-travel-itineraries

# Make it publicly readable (for shareable URLs)
gsutil iam ch allUsers:objectViewer gs://vibe-check-travel-itineraries

# Set CORS for web access
cat > cors.json <<EOF
[
  {
    "origin": ["*"],
    "method": ["GET", "HEAD", "DELETE"],
    "responseHeader": ["Content-Type"],
    "maxAgeSeconds": 3600
  }
]
EOF

gsutil cors set cors.json gs://vibe-check-travel-itineraries
```

---

## 🔐 Step 4: Update Backend for Cloud Run

### 4.1 Add Cloud Logging & Monitoring

Update `backend/app/utils/logger.py` to use Google Cloud Logging:
```python
from google.cloud import logging as cloud_logging
import logging

def setup_cloud_logging():
    """Setup Google Cloud Logging."""
    client = cloud_logging.Client()
    client.setup_logging()
```

### 4.2 Create `backend/cloudbuild.yaml`

This file tells Cloud Build how to build and deploy:

```yaml
steps:
  # Step 1: Build the Docker image
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'build'
      - '-t'
      - 'gcr.io/$PROJECT_ID/travel-agent-backend:$SHORT_SHA'
      - '-t'
      - 'gcr.io/$PROJECT_ID/travel-agent-backend:latest'
      - '.'

  # Step 2: Push to Artifact Registry
  - name: 'gcr.io/cloud-builders/docker'
    args:
      - 'push'
      - 'gcr.io/$PROJECT_ID/travel-agent-backend:$SHORT_SHA'

  # Step 3: Deploy to Cloud Run
  - name: 'gcr.io/cloud-builders/gke-deploy'
    args:
      - 'run'
      - '--filename=.'
      - '--image=gcr.io/$PROJECT_ID/travel-agent-backend:$SHORT_SHA'
      - '--location=us-central1'
      - '--output=/workspace/output'

images:
  - 'gcr.io/$PROJECT_ID/travel-agent-backend:$SHORT_SHA'
  - 'gcr.io/$PROJECT_ID/travel-agent-backend:latest'

options:
  machineType: 'N1_HIGHCPU_8'
```

### 4.3 Create `backend/Dockerfile` for Cloud Run

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Cloud Run requires PORT env var
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/api/v1/health')"

CMD exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

## 🚀 Step 5: Deploy Backend to Cloud Run

### 5.1 Using gcloud CLI (Recommended)

```bash
# From backend directory
cd backend

# Set environment variables
gcloud secrets create gemini-api-key --data-file=- <<< "your-gemini-key"
gcloud secrets create maps-api-key --data-file=- <<< "your-maps-key"
gcloud secrets create pinecone-api-key --data-file=- <<< "your-pinecone-key"
gcloud secrets create db-url --data-file=- <<< "your-database-url"

# Grant Cloud Run service access to secrets
gcloud projects add-iam-policy-binding vibe-check-travel \
  --member=serviceAccount:vibe-check-travel@appspot.gserviceaccount.com \
  --role=roles/secretmanager.secretAccessor

# Deploy
gcloud run deploy travel-agent-backend \
  --source . \
  --platform managed \
  --region us-central1 \
  --memory 2Gi \
  --cpu 2 \
  --timeout 3600 \
  --set-env-vars=ENVIRONMENT=production,DEBUG=false \
  --set-secrets=GOOGLE_API_KEY=gemini-api-key:latest,GOOGLE_MAPS_API_KEY=maps-api-key:latest,PINECONE_API_KEY=pinecone-api-key:latest,DATABASE_URL=db-url:latest \
  --allow-unauthenticated
```

### 5.2 Manual Build & Deploy

```bash
# Build image
docker build -t travel-agent-backend .

# Tag for Google Cloud
docker tag travel-agent-backend gcr.io/vibe-check-travel/travel-agent-backend

# Push to Container Registry
docker push gcr.io/vibe-check-travel/travel-agent-backend

# Deploy to Cloud Run
gcloud run deploy travel-agent-backend \
  --image gcr.io/vibe-check-travel/travel-agent-backend \
  --platform managed \
  --region us-central1 \
  --memory 2Gi \
  --cpu 2 \
  --allow-unauthenticated
```

---

## 🎨 Step 6: Deploy Frontend to Cloud Run / Vercel / Netlify

### Option A: Cloud Run (Recommended)

Create `frontend/Dockerfile.prod`:
```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:18-alpine
WORKDIR /app
RUN npm install -g serve
COPY --from=builder /app/dist ./dist
EXPOSE 3000
CMD ["serve", "-s", "dist", "-l", "3000"]
```

Deploy:
```bash
cd frontend

gcloud run deploy travel-agent-frontend \
  --source . \
  --platform managed \
  --region us-central1 \
  --memory 1Gi \
  --allow-unauthenticated \
  --set-env-vars=VITE_API_URL=https://travel-agent-backend-XXXXX.a.run.app/api/v1
```

### Option B: Vercel (Easiest for Frontend)

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
cd frontend
vercel --prod

# Set environment variables in Vercel dashboard
# VITE_API_URL=https://travel-agent-backend-XXXXX.a.run.app/api/v1
```

### Option C: Netlify

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Deploy
cd frontend
netlify deploy --prod --dir=dist
```

---

## 📊 Step 7: Cloud Monitoring & Logging

### 7.1 View Logs
```bash
# Real-time logs
gcloud run services describe travel-agent-backend --region us-central1

# Stream logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=travel-agent-backend" --limit 50 --format json

# Go to: https://console.cloud.google.com/logs
```

### 7.2 Set Up Alerts
```bash
# Go to Cloud Console > Monitoring > Alerting Policies
# Create alerts for:
# - High error rate
# - High latency
# - Low success rate
```

---

## 🔄 Step 8: Set Up CI/CD with GitHub

### 8.1 Connect GitHub to Cloud Build

```bash
# Go to: https://console.cloud.google.com/cloud-build/repositories
# Click "CONNECT REPOSITORY"
# Select GitHub
# Authorize Google Cloud Build
# Select your repo
```

### 8.2 Create `backend/.gcloudignore`
```
node_modules/
.env
__pycache__/
*.pyc
.pytest_cache/
```

### 8.3 Auto-deploy on Push
```bash
# Create Cloud Build trigger
gcloud builds triggers create github \
  --repo-name=travel_planning_and_experience_engine \
  --repo-owner=Sarika151999 \
  --branch-pattern="^main$" \
  --build-config=cloudbuild.yaml \
  --name=deploy-backend
```

---

## 📦 Step 9: Database Setup

### 9.1 Using Cloud Firestore (Recommended for scalability)

```bash
# Create Firestore database
gcloud firestore databases create --region=us-central1

# Update backend to use Firestore:
# pip install firebase-admin
```

### 9.2 Using Cloud SQL (PostgreSQL)

```bash
# Create Cloud SQL instance
gcloud sql instances create travel-agent-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=us-central1

# Create database
gcloud sql databases create travel_agent \
  --instance=travel-agent-db

# Create user
gcloud sql users create postgres \
  --instance=travel-agent-db \
  --password

# Get connection string
gcloud sql instances describe travel-agent-db --format='value(connectionNames)'
```

---

## ✅ Verification Checklist

- [ ] APIs enabled in Google Cloud
- [ ] Service account created with permissions
- [ ] API keys generated (Gemini, Maps, Pinecone)
- [ ] Cloud Storage bucket created
- [ ] Backend deployed to Cloud Run
- [ ] Frontend deployed (Vercel/Netlify/Cloud Run)
- [ ] Environment variables set in Cloud Run
- [ ] Database configured (Firestore or Cloud SQL)
- [ ] Health check passing
- [ ] Logs appearing in Cloud Logging
- [ ] API responding at Cloud Run URL

---

## 🌐 Your Deployed URLs

After deployment, you'll have:

```
Backend:  https://travel-agent-backend-XXXXX.a.run.app
Frontend: https://travel-agent-frontend.vercel.app
API Docs: https://travel-agent-backend-XXXXX.a.run.app/docs
```

---

## 💰 Cost Optimization

### Free Tier Benefits
- Cloud Run: 2M requests/month free
- Cloud Storage: 5GB free
- Cloud Logging: 50GB ingested logs/month free
- Cloud Build: 120 build-minutes/day free
- Cloud Firestore: 1GB storage free

### Reducing Costs
1. Set Cloud Run memory to 512MB if sufficient
2. Use Cloud Storage lifecycle policies to archive old data
3. Use Firestore for smaller scale (cheaper than Cloud SQL)
4. Set up budget alerts

---

## 📱 Next Steps

1. Deploy backend to Cloud Run
2. Deploy frontend to Vercel/Netlify
3. Set up custom domain (optional)
4. Configure CI/CD automation
5. Monitor performance and costs
6. Gather metrics and optimize

