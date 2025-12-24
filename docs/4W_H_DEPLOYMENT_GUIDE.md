# CBSE Learning Platform - 4W+H Step-by-Step Deployment Guide

A comprehensive guide using the 4W+H framework (What, Why, When, Where, How) for deploying the low-cost CBSE Learning Platform.

---

## Table of Contents

1. [Overview: The 4W+H Framework](#overview-the-4wh-framework)
2. [Phase 1: Account Setup](#phase-1-account-setup)
3. [Phase 2: Firebase Configuration](#phase-2-firebase-configuration)
4. [Phase 3: Replicate AI Setup](#phase-3-replicate-ai-setup)
5. [Phase 4: Local Development](#phase-4-local-development)
6. [Phase 5: Cloud Run Deployment](#phase-5-cloud-run-deployment)
7. [Phase 6: Production Configuration](#phase-6-production-configuration)
8. [Troubleshooting Guide](#troubleshooting-guide)

---

## Overview: The 4W+H Framework

### WHAT is this project?

The CBSE Learning Platform is an AI-powered educational application for Indian students studying under the CBSE curriculum (grades 6-10). It provides:

- AI-driven quiz generation and doubt clearing
- Interactive learning with student persona modes (Dull/Average/Clever)
- Progress tracking with gamification elements
- Real-world application examples using Situated Cognition Theory

### WHY use this low-cost approach?

| Reason | Explanation |
|--------|-------------|
| **Budget Constraints** | Schools and individual developers often have limited budgets (< 1000 INR/month) |
| **Free Tier Optimization** | GCP, Firebase, and Replicate offer generous free tiers that can run small-medium deployments at zero cost |
| **Pay-Per-Use AI** | Replicate charges only for actual usage (~$0.05/million tokens) vs Vertex AI's higher pricing |
| **Scale-to-Zero** | Cloud Run charges nothing when idle, perfect for educational apps with variable usage |
| **No Vendor Lock-in** | Open-source models (Llama 3.1) can be self-hosted later if needed |

### WHEN to use each deployment option?

| Scenario | Recommended Setup | Monthly Cost |
|----------|-------------------|--------------|
| Development/Testing | Mock AI + In-memory DB | $0 |
| Personal Project | Replicate + Firestore | $0-2 |
| Small School (50 students) | Replicate + Firestore | $2-5 |
| Medium School (200 students) | Replicate + Firestore | $10-20 |
| Large Deployment (500+ students) | Vertex AI + Cloud SQL | $50-200 |

### WHERE are the components deployed?

| Component | Location | Service |
|-----------|----------|---------|
| Backend API | Google Cloud Run | asia-south1 (Mumbai) |
| Database | Firebase Firestore | asia-south1 |
| Authentication | Firebase Auth | Global |
| AI Processing | Replicate Cloud | US (auto-routed) |
| Frontend (optional) | Firebase Hosting | Global CDN |
| Container Images | Artifact Registry | asia-south1 |

### HOW does the architecture work?

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Frontend      │────▶│   Cloud Run     │────▶│   Replicate     │
│   (React PWA)   │     │   (FastAPI)     │     │   (Llama 3.1)   │
└─────────────────┘     └────────┬────────┘     └─────────────────┘
                                 │
                    ┌────────────┼────────────┐
                    ▼            ▼            ▼
            ┌───────────┐ ┌───────────┐ ┌───────────┐
            │ Firestore │ │  Firebase │ │   Cloud   │
            │ (Data)    │ │  Auth     │ │  Storage  │
            └───────────┘ └───────────┘ └───────────┘
```

---

## Phase 1: Account Setup

### Step 1.1: Create Google Cloud Account

**WHAT**: Create a GCP account to access Cloud Run, Firestore, and other services.

**WHY**: GCP provides $300 free credits for new accounts and generous always-free tiers.

**WHEN**: Before any other setup. This is the foundation.

**WHERE**: https://cloud.google.com/free

**HOW**:

1. Go to https://cloud.google.com/free
2. Click "Get started for free"
3. Sign in with your Google account (create new if needed for fresh credits)
4. Enter billing information:
   - Credit/debit card required (won't be charged during trial)
   - Address and phone verification
5. Accept terms and conditions
6. Wait for account activation (usually instant)

**Verification**:
```bash
# Install gcloud CLI if not already installed
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Login and verify
gcloud auth login
gcloud projects list
```

**Expected Output**: You should see your project listed with $300 credits available.

---

### Step 1.2: Create GCP Project

**WHAT**: Create a dedicated project for the CBSE Learning Platform.

**WHY**: Projects isolate resources, billing, and permissions.

**WHEN**: Immediately after account creation.

**WHERE**: GCP Console or CLI.

**HOW**:

```bash
# Create project
gcloud projects create cbse-learning-platform --name="CBSE Learning Platform"

# Set as default project
gcloud config set project cbse-learning-platform

# Enable billing (required for Cloud Run)
# Go to: https://console.cloud.google.com/billing
# Link your project to the billing account

# Enable required APIs
gcloud services enable \
  run.googleapis.com \
  firestore.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com
```

**Verification**:
```bash
gcloud services list --enabled
```

**Expected Output**: All four services should be listed as enabled.

---

### Step 1.3: Create Replicate Account

**WHAT**: Create a Replicate account for AI API access.

**WHY**: Replicate offers $5 free credits and pay-per-use pricing (~10x cheaper than Vertex AI).

**WHEN**: Before deploying to production (can skip for development with mock provider).

**WHERE**: https://replicate.com

**HOW**:

1. Go to https://replicate.com
2. Click "Sign up" (top right)
3. Sign up with GitHub or email
4. Verify email if required
5. Navigate to https://replicate.com/account/api-tokens
6. Click "Create token"
7. Copy the token (starts with `r8_`)
8. Store securely (you won't see it again)

**Verification**:
```bash
# Test API token
curl -s -H "Authorization: Bearer r8_YOUR_TOKEN" \
  https://api.replicate.com/v1/models/meta/meta-llama-3.1-8b-instruct
```

**Expected Output**: JSON response with model details (not an error).

---

## Phase 2: Firebase Configuration

### Step 2.1: Create Firebase Project

**WHAT**: Create a Firebase project linked to your GCP project.

**WHY**: Firebase provides free authentication and Firestore database.

**WHEN**: After GCP project is created.

**WHERE**: https://console.firebase.google.com

**HOW**:

1. Go to https://console.firebase.google.com
2. Click "Add project"
3. Select your existing GCP project: `cbse-learning-platform`
4. Disable Google Analytics (optional, reduces complexity)
5. Click "Create project"
6. Wait for setup to complete (~30 seconds)

**Verification**: You should see the Firebase console dashboard for your project.

---

### Step 2.2: Enable Firebase Authentication

**WHAT**: Set up user authentication with email/password.

**WHY**: Secure user accounts without building auth from scratch.

**WHEN**: After Firebase project creation.

**WHERE**: Firebase Console > Authentication

**HOW**:

1. In Firebase Console, click "Authentication" in sidebar
2. Click "Get started"
3. Click "Email/Password" under "Sign-in providers"
4. Toggle "Enable" to ON
5. Click "Save"
6. (Optional) Enable "Google" sign-in for social login

**Verification**: The "Email/Password" provider should show as "Enabled".

---

### Step 2.3: Set Up Firestore Database

**WHAT**: Create a Firestore database for storing user data, progress, and content.

**WHY**: Firestore offers 1GB free storage and 50K reads/day at no cost.

**WHEN**: After Firebase project creation.

**WHERE**: Firebase Console > Firestore Database

**HOW**:

1. In Firebase Console, click "Firestore Database" in sidebar
2. Click "Create database"
3. Select "Start in production mode" (we'll set rules later)
4. Choose location: `asia-south1 (Mumbai)` for Indian users
5. Click "Enable"
6. Wait for provisioning (~1 minute)

**Verification**: You should see an empty Firestore database console.

---

### Step 2.4: Download Service Account Key

**WHAT**: Download credentials for backend to access Firebase services.

**WHY**: The backend needs authenticated access to Firestore and Auth.

**WHEN**: After Firestore is set up.

**WHERE**: Firebase Console > Project Settings > Service Accounts

**HOW**:

1. Click the gear icon (Settings) in Firebase Console sidebar
2. Click "Project settings"
3. Click "Service accounts" tab
4. Click "Generate new private key"
5. Click "Generate key" in the confirmation dialog
6. Save the downloaded JSON file securely
7. Rename to `firebase-credentials.json`

**Verification**:
```bash
# Check the file contains required fields
cat firebase-credentials.json | jq '.project_id, .private_key_id'
```

**Expected Output**: Your project ID and a private key ID.

---

### Step 2.5: Configure Firestore Security Rules

**WHAT**: Set up security rules to protect user data.

**WHY**: Prevent unauthorized access to sensitive data.

**WHEN**: Before going to production.

**WHERE**: Firebase Console > Firestore Database > Rules

**HOW**:

1. In Firestore Database, click "Rules" tab
2. Replace the default rules with:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users can only access their own data
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Progress data - user-specific
    match /progress/{progressId} {
      allow read, write: if request.auth != null && 
        resource.data.user_id == request.auth.uid;
    }
    
    // Quizzes - user can read their own, create new
    match /quizzes/{quizId} {
      allow read: if request.auth != null && 
        resource.data.user_id == request.auth.uid;
      allow create: if request.auth != null;
    }
    
    // Doubts - user-specific
    match /doubts/{doubtId} {
      allow read, write: if request.auth != null && 
        resource.data.user_id == request.auth.uid;
    }
    
    // Public curriculum data (read-only for all authenticated users)
    match /curriculum/{document=**} {
      allow read: if request.auth != null;
      allow write: if false;
    }
    
    // Chapters - public read
    match /chapters/{chapterId} {
      allow read: if true;
      allow write: if false;
    }
  }
}
```

3. Click "Publish"

**Verification**: Rules should show "Published" status.

---

## Phase 3: Replicate AI Setup

### Step 3.1: Understand Replicate Pricing

**WHAT**: Learn how Replicate charges for AI API usage.

**WHY**: To estimate costs and choose the right model.

**WHEN**: Before enabling paid AI features.

**WHERE**: https://replicate.com/pricing

**HOW** (Cost Calculation):

| Model | Input Cost | Output Cost | Use Case |
|-------|------------|-------------|----------|
| Llama 3.1 8B | $0.05/M tokens | $0.05/M tokens | Best for low budget |
| Llama 3.1 70B | $0.65/M tokens | $0.80/M tokens | Better quality |
| Llama 3.1 405B | $5.00/M tokens | $15.00/M tokens | Highest quality |

**Example Cost Calculation**:
- Average quiz generation: ~500 tokens input, ~1000 tokens output
- Cost per quiz: (500/1M * $0.05) + (1000/1M * $0.05) = $0.000075
- 1000 quizzes/month: $0.075 (less than 1 cent!)

---

### Step 3.2: Configure Replicate in Application

**WHAT**: Set environment variables for Replicate API.

**WHY**: The application needs credentials to call Replicate.

**WHEN**: Before running with AI features.

**WHERE**: `.env` file or environment variables.

**HOW**:

```bash
# Create .env file in cbse-learning-backend/
cat > cbse-learning-backend/.env << 'EOF'
# AI Provider Configuration
AI_PROVIDER=replicate
REPLICATE_API_TOKEN=r8_YOUR_TOKEN_HERE
REPLICATE_MODEL=meta/meta-llama-3.1-8b-instruct

# Firebase Configuration
FIREBASE_CREDENTIALS_PATH=/path/to/firebase-credentials.json

# Application Configuration
APP_ENV=development
DEBUG=true
JWT_SECRET_KEY=your-secret-key-change-in-production

# GCP Configuration
GCP_PROJECT_ID=cbse-learning-platform
GCP_REGION=asia-south1
EOF
```

**Verification**:
```bash
# Check environment variables are set
source cbse-learning-backend/.env
echo $AI_PROVIDER  # Should print: replicate
```

---

### Step 3.3: Test Replicate Integration

**WHAT**: Verify the Replicate API works correctly.

**WHY**: Catch configuration issues before deployment.

**WHEN**: After setting up credentials.

**WHERE**: Local development environment.

**HOW**:

```python
# test_replicate.py
import os
import replicate

# Set your token
os.environ["REPLICATE_API_TOKEN"] = "r8_YOUR_TOKEN"

# Test the API
output = replicate.run(
    "meta/meta-llama-3.1-8b-instruct",
    input={
        "prompt": "What is a quadratic equation? Explain in 2 sentences.",
        "max_tokens": 100,
        "temperature": 0.7
    }
)

print("".join(output))
```

```bash
# Run the test
python test_replicate.py
```

**Expected Output**: A clear explanation of quadratic equations.

---

## Phase 4: Local Development

### Step 4.1: Clone the Repository

**WHAT**: Get the source code on your local machine.

**WHY**: To run and test the application locally.

**WHEN**: After all accounts are set up.

**WHERE**: Your local development machine.

**HOW**:

```bash
# Clone the repository
git clone https://github.com/sunkaramallikarjuna369/AICBESE.git
cd AICBESE

# Checkout the low-cost branch
git checkout devin/1766584808-low-cost-firebase-replicate
```

**Verification**:
```bash
ls -la
# Should show: cbse-learning-backend, cbse-learning-frontend, docs, infra, README.md
```

---

### Step 4.2: Set Up Backend Environment

**WHAT**: Install Python dependencies and configure the backend.

**WHY**: The backend needs all dependencies to run.

**WHEN**: After cloning the repository.

**WHERE**: `cbse-learning-backend/` directory.

**HOW**:

```bash
# Navigate to backend
cd cbse-learning-backend

# Install Poetry if not installed
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Copy environment template
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use your preferred editor
```

**Verification**:
```bash
poetry run python -c "from app.ai.provider import get_ai_provider; print('OK')"
```

**Expected Output**: `OK`

---

### Step 4.3: Run Backend Locally

**WHAT**: Start the FastAPI development server.

**WHY**: To test the application before deployment.

**WHEN**: After environment setup.

**WHERE**: Local machine, port 8000.

**HOW**:

```bash
# Start the server
cd cbse-learning-backend
poetry run fastapi dev app/main.py

# Or with uvicorn directly
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Verification**:
```bash
# In another terminal
curl http://localhost:8000/health
```

**Expected Output**: `{"status": "healthy"}`

---

### Step 4.4: Test API Endpoints

**WHAT**: Verify key API endpoints work correctly.

**WHY**: Ensure the application functions before deployment.

**WHEN**: After backend is running.

**WHERE**: http://localhost:8000/docs (Swagger UI)

**HOW**:

1. Open http://localhost:8000/docs in browser
2. Test these endpoints:
   - `GET /health` - Should return healthy status
   - `GET /curriculum/classes` - Should return class list
   - `POST /auth/register` - Create a test user
   - `POST /auth/login` - Get JWT token

```bash
# Test curriculum endpoint
curl http://localhost:8000/curriculum/classes

# Test with mock AI (no API calls)
curl -X POST http://localhost:8000/visualization-orchestrator/topics/topic-1/config \
  -H "Content-Type: application/json" \
  -d '{"student_mode": "average"}'
```

**Expected Output**: JSON responses with curriculum data and visual configs.

---

## Phase 5: Cloud Run Deployment

### Step 5.1: Create Artifact Registry Repository

**WHAT**: Create a container registry to store Docker images.

**WHY**: Cloud Run deploys from container images.

**WHEN**: Before first deployment.

**WHERE**: GCP Artifact Registry.

**HOW**:

```bash
# Create repository
gcloud artifacts repositories create cbse-app \
  --repository-format=docker \
  --location=asia-south1 \
  --description="CBSE Learning Platform containers"

# Configure Docker authentication
gcloud auth configure-docker asia-south1-docker.pkg.dev
```

**Verification**:
```bash
gcloud artifacts repositories list --location=asia-south1
```

**Expected Output**: `cbse-app` repository listed.

---

### Step 5.2: Build and Push Docker Image

**WHAT**: Create a container image of the backend.

**WHY**: Cloud Run runs containerized applications.

**WHEN**: After local testing passes.

**WHERE**: Local machine, then pushed to Artifact Registry.

**HOW**:

```bash
cd cbse-learning-backend

# Build the image
docker build -t asia-south1-docker.pkg.dev/cbse-learning-platform/cbse-app/backend:v1 .

# Push to Artifact Registry
docker push asia-south1-docker.pkg.dev/cbse-learning-platform/cbse-app/backend:v1
```

**Verification**:
```bash
gcloud artifacts docker images list \
  asia-south1-docker.pkg.dev/cbse-learning-platform/cbse-app
```

**Expected Output**: `backend:v1` image listed.

---

### Step 5.3: Deploy to Cloud Run

**WHAT**: Deploy the container to Cloud Run.

**WHY**: Cloud Run provides serverless, auto-scaling hosting.

**WHEN**: After image is pushed.

**WHERE**: GCP Cloud Run, asia-south1 region.

**HOW**:

```bash
gcloud run deploy cbse-learning-app \
  --image=asia-south1-docker.pkg.dev/cbse-learning-platform/cbse-app/backend:v1 \
  --platform=managed \
  --region=asia-south1 \
  --allow-unauthenticated \
  --memory=512Mi \
  --cpu=1 \
  --min-instances=0 \
  --max-instances=2 \
  --concurrency=80 \
  --timeout=60 \
  --cpu-throttling \
  --set-env-vars="AI_PROVIDER=replicate,APP_ENV=production"
```

**Verification**:
```bash
# Get the service URL
gcloud run services describe cbse-learning-app \
  --region=asia-south1 \
  --format='value(status.url)'

# Test the endpoint
curl https://YOUR-SERVICE-URL/health
```

**Expected Output**: `{"status": "healthy"}`

---

### Step 5.4: Configure Secrets

**WHAT**: Securely store sensitive credentials.

**WHY**: Never hardcode secrets in code or environment variables.

**WHEN**: Before production use.

**WHERE**: GCP Secret Manager.

**HOW**:

```bash
# Enable Secret Manager API
gcloud services enable secretmanager.googleapis.com

# Create secrets
echo -n "r8_YOUR_REPLICATE_TOKEN" | \
  gcloud secrets create replicate-api-token --data-file=-

echo -n "your-jwt-secret-key" | \
  gcloud secrets create jwt-secret-key --data-file=-

# Grant Cloud Run access to secrets
gcloud secrets add-iam-policy-binding replicate-api-token \
  --member="serviceAccount:YOUR-PROJECT-NUMBER-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

# Update Cloud Run to use secrets
gcloud run services update cbse-learning-app \
  --region=asia-south1 \
  --set-secrets="REPLICATE_API_TOKEN=replicate-api-token:latest,JWT_SECRET_KEY=jwt-secret-key:latest"
```

**Verification**:
```bash
gcloud run services describe cbse-learning-app \
  --region=asia-south1 \
  --format='yaml(spec.template.spec.containers[0].env)'
```

---

## Phase 6: Production Configuration

### Step 6.1: Set Up Custom Domain (Optional)

**WHAT**: Use your own domain instead of Cloud Run's default URL.

**WHY**: Professional appearance and easier to remember.

**WHEN**: After deployment is working.

**WHERE**: Cloud Run domain mapping.

**HOW**:

```bash
# Map custom domain
gcloud run domain-mappings create \
  --service=cbse-learning-app \
  --domain=api.yourdomain.com \
  --region=asia-south1

# Get DNS records to configure
gcloud run domain-mappings describe \
  --domain=api.yourdomain.com \
  --region=asia-south1
```

**Verification**: After DNS propagation, `https://api.yourdomain.com/health` should work.

---

### Step 6.2: Set Up Monitoring

**WHAT**: Configure alerts for errors and performance issues.

**WHY**: Know when something goes wrong before users complain.

**WHEN**: After production deployment.

**WHERE**: GCP Cloud Monitoring.

**HOW**:

1. Go to https://console.cloud.google.com/monitoring
2. Click "Alerting" > "Create Policy"
3. Add conditions:
   - Error rate > 1% for 5 minutes
   - Latency p95 > 5 seconds
   - Instance count > 2 (cost alert)
4. Add notification channels (email, Slack, etc.)
5. Save the policy

**Verification**: Trigger a test alert to verify notifications work.

---

### Step 6.3: Set Up Budget Alerts

**WHAT**: Get notified when spending approaches your budget.

**WHY**: Prevent unexpected charges.

**WHEN**: Immediately after deployment.

**WHERE**: GCP Billing > Budgets & alerts.

**HOW**:

1. Go to https://console.cloud.google.com/billing
2. Click "Budgets & alerts"
3. Click "Create budget"
4. Set budget amount: 1000 INR (~$12)
5. Set alert thresholds: 50%, 80%, 100%
6. Add email recipients
7. Click "Finish"

**Verification**: You should receive a confirmation email about the budget.

---

## Troubleshooting Guide

### Common Issues and Solutions

#### Issue: "REPLICATE_API_TOKEN not set"

**WHAT**: The application can't find the Replicate API token.

**WHY**: Environment variable not configured or secret not mounted.

**HOW to fix**:
```bash
# Check if variable is set
echo $REPLICATE_API_TOKEN

# If using Cloud Run, verify secret mounting
gcloud run services describe cbse-learning-app \
  --region=asia-south1 \
  --format='yaml(spec.template.spec.containers[0].env)'
```

---

#### Issue: "Firebase credentials not found"

**WHAT**: The application can't authenticate with Firebase.

**WHY**: Credentials file path is wrong or file is missing.

**HOW to fix**:
```bash
# Verify file exists
ls -la $FIREBASE_CREDENTIALS_PATH

# For Cloud Run, mount as secret
gcloud secrets create firebase-credentials \
  --data-file=firebase-credentials.json

gcloud run services update cbse-learning-app \
  --region=asia-south1 \
  --set-secrets="/secrets/firebase-credentials.json=firebase-credentials:latest"
```

---

#### Issue: "Exceeded Firestore free tier"

**WHAT**: You've hit the daily read/write limits.

**WHY**: Too many database operations.

**HOW to fix**:
1. Check usage in Firebase Console > Firestore > Usage
2. Implement caching to reduce reads
3. Batch writes where possible
4. Consider upgrading to Blaze plan (pay-as-you-go)

---

#### Issue: "Cloud Run cold start too slow"

**WHAT**: First request after idle takes 5-10 seconds.

**WHY**: Container needs to start from scratch.

**HOW to fix**:
```bash
# Option 1: Accept the trade-off (free)
# Show loading spinner in frontend

# Option 2: Keep one instance warm (~$15-30/month)
gcloud run services update cbse-learning-app \
  --region=asia-south1 \
  --min-instances=1

# Option 3: Use Cloud Scheduler to ping every 10 minutes (free)
gcloud scheduler jobs create http keep-warm \
  --schedule="*/10 * * * *" \
  --uri="https://YOUR-SERVICE-URL/health" \
  --http-method=GET
```

---

#### Issue: "AI responses are slow"

**WHAT**: Quiz generation or doubt clearing takes too long.

**WHY**: Network latency to Replicate or model processing time.

**HOW to fix**:
1. Use smaller model (Llama 3.1 8B instead of 70B)
2. Reduce max_tokens for faster responses
3. Implement response streaming
4. Cache common questions/answers

---

## Quick Reference Card

### Environment Variables

```bash
# Required
AI_PROVIDER=replicate              # mock, replicate, or vertex
REPLICATE_API_TOKEN=r8_xxx         # From replicate.com
FIREBASE_CREDENTIALS_PATH=/path    # Service account JSON
JWT_SECRET_KEY=xxx                 # Random secure string

# Optional
REPLICATE_MODEL=meta/meta-llama-3.1-8b-instruct
GCP_PROJECT_ID=cbse-learning-platform
GCP_REGION=asia-south1
DEBUG=false
```

### Useful Commands

```bash
# Local development
poetry run fastapi dev app/main.py

# Build Docker image
docker build -t cbse-backend .

# Deploy to Cloud Run
gcloud run deploy cbse-learning-app --image=IMAGE_URL

# View logs
gcloud run logs read --service=cbse-learning-app --region=asia-south1

# Check costs
gcloud billing accounts list
```

### Cost Monitoring URLs

- GCP Billing: https://console.cloud.google.com/billing
- Firebase Usage: https://console.firebase.google.com (Usage tab)
- Replicate Usage: https://replicate.com/account

---

## Summary

This 4W+H guide covered:

1. **WHAT**: A low-cost CBSE Learning Platform using Firebase and Replicate AI
2. **WHY**: 90%+ cost reduction compared to traditional cloud architecture
3. **WHEN**: Development ($0), Small deployments ($0-5), Production ($10-50)
4. **WHERE**: GCP Cloud Run (asia-south1), Firebase, Replicate Cloud
5. **HOW**: Step-by-step instructions for every phase of deployment

Total estimated time: 2-4 hours for first deployment

For questions or issues, refer to the troubleshooting section or open an issue on GitHub.
