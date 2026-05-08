# 🔑 Getting All Google Cloud Credentials - Complete Guide

This guide shows you exactly where to get every API key and credential needed for deployment.

---

## 📋 Pre-Requisites

1. **Google Account** - Create at [google.com](https://google.com)
2. **Credit Card** - Needed to enable paid APIs (but you get $300 free credits!)
3. **Local Tools**:
   ```bash
   # Install gcloud CLI
   # macOS: brew install google-cloud-sdk
   # Windows: https://cloud.google.com/sdk/docs/install-windows
   # Linux: https://cloud.google.com/sdk/docs/install-linux
   
   # After installation:
   gcloud init
   gcloud auth application-default login
   ```

---

## 🚀 Step 1: Create Google Cloud Project

### 1.1 Via Web Console (Easiest)

1. Go to **[Google Cloud Console](https://console.cloud.google.com)**
2. Click **"Select a Project"** (top left)
3. Click **"NEW PROJECT"**
4. Enter:
   - **Project name**: `vibe-check-travel`
   - **Organization**: Leave blank if personal
   - Click **"CREATE"**

5. Wait for creation (usually 1-2 minutes)
6. You'll see: `PROJECT_ID: vibe-check-travel-XXXXX`

### 1.2 Via Command Line

```bash
gcloud projects create vibe-check-travel --name="Vibe-Check Travel Agent"
gcloud config set project vibe-check-travel

# Get your project ID
PROJECT_ID=$(gcloud config get-value project)
echo $PROJECT_ID
```

---

## 💰 Step 2: Enable Billing & Get Free Credits

### 2.1 Link Billing Account

1. Go to [Google Cloud Console - Billing](https://console.cloud.google.com/billing)
2. Click **"Create Account"** or select existing billing account
3. Link billing account to your project

### 2.2 Claim $300 Free Credits

1. Go to [Google Cloud Free Trial](https://cloud.google.com/free)
2. Click **"Get started for free"**
3. Follow verification steps (2-factor, credit card verification)
4. You get **$300 free credits** for 90 days!

⚠️ **Important**: Set up billing alerts to avoid surprise charges:
1. Go to **Billing → Budgets & Alerts**
2. Create alert at $100, $200, $299

---

## 🔑 Step 3: Get Gemini API Key

### 3.1 Quickest Way (AI Studio)

1. Go to **[AI Studio](https://aistudio.google.com/app/apikey)**
2. Click **"Get API Key"**
3. Click **"Create API Key"** (or **"Create API Key in new project"**)
4. Copy the key

### 3.2 Via Google Cloud Console

1. Go to **[Google Cloud Console](https://console.cloud.google.com)**
2. Select your project
3. Go to **APIs & Services → Credentials**
4. Click **"Create Credentials" → "API Key"**
5. Copy the key
6. (Optional) Restrict to **Generative AI API**

### Save it:
```bash
export GEMINI_API_KEY="AIzaSy..."
```

---

## 🗺️ Step 4: Get Google Maps API Key

### 4.1 Enable Maps API

1. Go to **[Google Cloud Console](https://console.cloud.google.com)**
2. Select your project
3. Go to **APIs & Services → Library**
4. Search for:
   - **"Places API"** → Click → **"Enable"**
   - **"Maps JavaScript API"** → Click → **"Enable"**
   - **"Distance Matrix API"** → Click → **"Enable"**
5. Wait for enabling (1-2 minutes)

### 4.2 Create API Key

1. Go to **APIs & Services → Credentials**
2. Click **"Create Credentials" → "API Key"**
3. Copy the key
4. (Recommended) Restrict the key:
   - Click on the key
   - Under **"API restrictions"** select:
     - Google Maps Platform APIs
   - Click **"Save"**

### Save it:
```bash
export MAPS_API_KEY="AIzaSy..."
```

---

## 🪣 Step 5: Create Cloud Storage Bucket

### 5.1 Via Console

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Go to **Cloud Storage → Buckets**
3. Click **"Create"**
4. Fill:
   - **Name**: `vibe-check-travel-itineraries` (globally unique!)
   - **Region**: `us-central1`
   - **Storage class**: `Standard`
5. Click **"Create"**

### 5.2 Via Command Line

```bash
# Create bucket
gsutil mb -l us-central1 gs://vibe-check-travel-itineraries

# Make publicly readable (for shareable URLs)
gsutil iam ch allUsers:objectViewer \
  gs://vibe-check-travel-itineraries

# Set CORS
cat > cors.json <<EOF
[{
  "origin": ["*"],
  "method": ["GET", "HEAD", "DELETE"],
  "responseHeader": ["Content-Type"],
  "maxAgeSeconds": 3600
}]
EOF

gsutil cors set cors.json gs://vibe-check-travel-itineraries
```

### Save it:
```bash
export GCS_BUCKET_NAME="vibe-check-travel-itineraries"
```

---

## 🔐 Step 6: Create Service Account (for Cloud Run)

### 6.1 Via Console

1. Go to **IAM & Admin → Service Accounts**
2. Click **"Create Service Account"**
3. Fill:
   - **Service account name**: `travel-agent-sa`
   - **ID**: Auto-generated
4. Click **"Create and Continue"**
5. Grant roles:
   - **Storage Admin** (for Cloud Storage)
   - **Cloud Run Developer** (for Cloud Run)
   - **Logging Log Writer** (for Cloud Logging)
6. Click **"Continue"** → **"Done"**

### 6.2 Download JSON Key

1. Go to **IAM & Admin → Service Accounts**
2. Click on your service account
3. Go to **Keys** tab
4. Click **"Add Key" → "Create new key"**
5. Select **"JSON"**
6. Click **"Create"**
7. A JSON file downloads automatically

### 6.3 Via Command Line

```bash
# Create service account
gcloud iam service-accounts create travel-agent-sa \
  --display-name="Travel Agent Service Account"

# Create JSON key
gcloud iam service-accounts keys create sa-key.json \
  --iam-account=travel-agent-sa@vibe-check-travel.iam.gserviceaccount.com

# Grant permissions
gcloud projects add-iam-policy-binding vibe-check-travel \
  --member=serviceAccount:travel-agent-sa@vibe-check-travel.iam.gserviceaccount.com \
  --role=roles/storage.admin

gcloud projects add-iam-policy-binding vibe-check-travel \
  --member=serviceAccount:travel-agent-sa@vibe-check-travel.iam.gserviceaccount.com \
  --role=roles/run.developer

gcloud projects add-iam-policy-binding vibe-check-travel \
  --member=serviceAccount:travel-agent-sa@vibe-check-travel.iam.gserviceaccount.com \
  --role=roles/logging.logWriter
```

### Save the file:
```bash
# Copy sa-key.json to backend/gcs-key.json
cp sa-key.json backend/gcs-key.json
```

---

## 🔍 Step 7: Optional - Pinecone for Vector Search

### 7.1 Create Pinecone Account

1. Go to **[Pinecone](https://app.pinecone.io)**
2. Click **"Sign Up"**
3. Sign up with email or Google account
4. Create organization name

### 7.2 Create API Key

1. Go to **Organization** (bottom left)
2. Click **"Copy API Key"**
3. Copy both **API Key** and **Environment name**

### 7.3 Create Index

1. Go to **Indexes**
2. Click **"Create Index"**
3. Fill:
   - **Name**: `travel-itineraries`
   - **Dimension**: `384` (for all-MiniLM-L6-v2)
   - **Metric**: `cosine`
4. Click **"Create Index"**

### Save it:
```bash
export PINECONE_API_KEY="your-key-here"
export PINECONE_ENVIRONMENT="us-west4-gcp-free"  # or your region
```

---

## 📝 Step 8: Configure Your .env File

Create `backend/.env`:

```bash
# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT_ID=vibe-check-travel
GOOGLE_API_KEY=AIzaSy...  # From Step 3
GOOGLE_MAPS_API_KEY=AIzaSy...  # From Step 4
GCS_BUCKET_NAME=vibe-check-travel-itineraries  # From Step 5
GCS_JSON_KEY_PATH=./gcs-key.json  # From Step 6

# Backend Configuration
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Database (optional, for local development)
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/travel_agent

# Pinecone (optional, if using vector search)
PINECONE_API_KEY=your-key-here  # From Step 7
PINECONE_ENVIRONMENT=us-west4-gcp-free  # From Step 7

# Security
SECRET_KEY=your-secret-key-here
```

---

## ✅ Verification Checklist

Run these to verify everything is set up:

```bash
# 1. Verify gcloud project
gcloud config get-value project

# 2. Verify APIs are enabled
gcloud services list --enabled | grep -E "run|build|storage|generativeai"

# 3. Verify service account exists
gcloud iam service-accounts list

# 4. Verify Cloud Storage bucket
gsutil ls gs://vibe-check-travel-itineraries

# 5. Verify credentials file
ls -la backend/gcs-key.json
```

---

## 🚀 Next Steps

1. Update `.env` file with all credentials
2. Follow [CLOUD_DEPLOYMENT.md](CLOUD_DEPLOYMENT.md) for deployment
3. Deploy backend to Cloud Run
4. Deploy frontend to Vercel/Netlify
5. Test the live deployment

---

## ⚠️ Security Tips

✅ **DO:**
- Store `.env` in `.gitignore`
- Use Google Cloud Secret Manager in production
- Rotate API keys regularly
- Set up billing alerts

❌ **DON'T:**
- Commit `.env` to GitHub
- Share API keys in Slack/email
- Use same key for multiple apps
- Leave billing account unmonitored

---

## 💬 Common Issues

### "API not enabled" error?
```bash
gcloud services enable generativeai.googleapis.com
```

### "Bucket name already exists"?
```bash
# Use a unique name like:
gsutil mb -l us-central1 gs://vibe-check-travel-$(date +%s)
```

### "Permission denied" error?
```bash
# Grant permissions to current user:
gcloud projects add-iam-policy-binding vibe-check-travel \
  --member=user:your-email@gmail.com \
  --role=roles/editor
```

### "Invalid API key" error?
- Make sure you copied the entire key
- Check for trailing spaces
- Regenerate the key if needed

---

## 📞 Help Links

- **GCP Console**: https://console.cloud.google.com
- **Gemini API**: https://aistudio.google.com/app/apikey
- **Maps API**: https://cloud.google.com/maps-platform
- **Cloud Storage**: https://cloud.google.com/storage
- **Pinecone**: https://app.pinecone.io
- **GCP Docs**: https://cloud.google.com/docs

---

**You're all set! Proceed to CLOUD_DEPLOYMENT.md for deployment.** 🎉
