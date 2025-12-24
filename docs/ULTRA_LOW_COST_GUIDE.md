# Ultra Low-Cost Deployment Guide

This guide provides comprehensive strategies for deploying the CBSE Learning Platform with minimal costs, leveraging free tiers, trials, and cost-effective alternatives.

## Table of Contents

1. [Cost Overview](#cost-overview)
2. [Free Tier Strategy](#free-tier-strategy)
3. [Trial Credits Guide](#trial-credits-guide)
4. [AI Provider Comparison](#ai-provider-comparison)
5. [Firebase Complete Setup](#firebase-complete-setup)
6. [Replicate AI Setup](#replicate-ai-setup)
7. [Cloud Run Optimization](#cloud-run-optimization)
8. [Monthly Cost Breakdown](#monthly-cost-breakdown)
9. [Scaling Path](#scaling-path)

---

## Cost Overview

### Target Budget: 0-1000 INR/month (~$0-12 USD)

This deployment strategy achieves near-zero costs by:
- Using Firebase/Firestore instead of Cloud SQL (saves ~$10-50/month)
- Using Replicate API instead of Vertex AI (pay-per-use, ~10x cheaper)
- Running on Cloud Run with scale-to-zero (free for low traffic)
- Leveraging free tiers and trial credits strategically

### Architecture Comparison

| Component | Original (High Cost) | Optimized (Low Cost) | Savings |
|-----------|---------------------|---------------------|---------|
| Database | Cloud SQL (~$10-50/mo) | Firestore (FREE tier) | $10-50/mo |
| AI API | Vertex AI Gemini (~$5-50/mo) | Replicate Llama (~$0.50-5/mo) | 90% |
| Compute | Cloud Run (min-instances=1) | Cloud Run (scale-to-zero) | $15-30/mo |
| Cache | Memorystore (~$30/mo) | In-memory (FREE) | $30/mo |
| **Total** | **$55-160/month** | **$0-10/month** | **90%+** |

---

## Free Tier Strategy

### Google Cloud Platform Free Tier

GCP offers generous free tiers that reset monthly:

| Service | Free Allowance | Our Usage |
|---------|----------------|-----------|
| Cloud Run | 2M requests/mo, 360K GB-seconds | Single service, scale-to-zero |
| Firestore | 1 GB storage, 50K reads/day, 20K writes/day | User data, progress |
| Cloud Storage | 5 GB storage | Frontend assets, PDFs |
| Artifact Registry | 500 MB storage | Docker images |
| Cloud Build | 120 build-minutes/day | CI/CD |
| Cloud Logging | 50 GB/month | Application logs |

### Firebase Free Tier (Spark Plan)

| Feature | Free Limit | Notes |
|---------|------------|-------|
| Authentication | 50,000 MAU | Email/Password, Google Sign-In |
| Firestore | 1 GB storage | 50K reads, 20K writes, 20K deletes per day |
| Cloud Storage | 5 GB | For file uploads |
| Hosting | 10 GB/month | Static frontend hosting |
| Cloud Functions | 2M invocations/month | Serverless functions |

### Replicate Free Tier

| Feature | Free Allowance | Notes |
|---------|----------------|-------|
| New Account | $5 free credits | One-time signup bonus |
| Open Source Models | Pay-per-use | No minimum charges |
| Llama 3.1 8B | ~$0.05/million tokens | Very cost-effective |

---

## Trial Credits Guide

### How to Maximize Free Credits

#### 1. Google Cloud Platform ($300 Free Credits)

**Eligibility**: New GCP accounts get $300 free credits valid for 90 days.

**How to Get**:
1. Go to https://cloud.google.com/free
2. Click "Get started for free"
3. Sign in with a Google account (use a new one if needed)
4. Enter billing information (credit card required but won't be charged)
5. Credits are automatically applied

**Best Practices**:
- Use credits for experimentation and testing
- Set up budget alerts at 50%, 80%, 100%
- Disable billing after trial to avoid charges
- Credits cover ALL GCP services including Vertex AI

**Timeline Strategy**:
- Month 1-2: Use trial credits for development and testing
- Month 3: Transition to free tier services only
- Ongoing: Stay within free tier limits

#### 2. Firebase (No Trial Needed - Generous Free Tier)

Firebase's Spark plan is permanently free with generous limits:
- No credit card required to start
- Automatic upgrade path to Blaze (pay-as-you-go) when needed
- Free tier limits are per-project, so you can create multiple projects

#### 3. Replicate ($5 Free Credits)

**How to Get**:
1. Go to https://replicate.com
2. Sign up with GitHub or email
3. $5 credits are automatically added
4. No credit card required initially

**Maximizing Credits**:
- Use Llama 3.1 8B (~$0.05/million tokens) instead of larger models
- Implement aggressive caching to reduce API calls
- Use mock provider for development/testing

#### 4. GitHub Student Developer Pack (If Eligible)

Students can get additional free credits:
- $100 GCP credits (on top of $300 trial)
- Various other cloud credits
- Apply at https://education.github.com/pack

#### 5. Google for Startups Cloud Program

If you're building a startup:
- Up to $100,000 in GCP credits
- Apply at https://cloud.google.com/startup

---

## AI Provider Comparison

### Cost Comparison (per 1 million tokens)

| Provider | Model | Input Cost | Output Cost | Notes |
|----------|-------|------------|-------------|-------|
| Mock | N/A | FREE | FREE | Pre-defined responses |
| Replicate | Llama 3.1 8B | ~$0.05 | ~$0.05 | Best for low budget |
| Replicate | Llama 3.1 70B | ~$0.65 | ~$0.80 | Better quality |
| Vertex AI | Gemini 1.5 Flash | ~$0.075 | ~$0.30 | Requires GCP project |
| Vertex AI | Gemini 1.5 Pro | ~$1.25 | ~$5.00 | Highest quality |
| OpenAI | GPT-4o-mini | ~$0.15 | ~$0.60 | Alternative option |

### Recommendation by Budget

| Monthly Budget | Recommended Provider | Expected AI Cost |
|----------------|---------------------|------------------|
| $0 | Mock | $0 |
| $0-5 | Replicate (Llama 3.1 8B) | $0.50-5 |
| $5-20 | Replicate (Llama 3.1 70B) | $5-20 |
| $20+ | Vertex AI (Gemini) | $20+ |

### Setting Up AI Provider

```bash
# For Mock (free, development/testing)
export AI_PROVIDER=mock

# For Replicate (low-cost production)
export AI_PROVIDER=replicate
export REPLICATE_API_TOKEN=your_token_here
export REPLICATE_MODEL=meta/meta-llama-3.1-8b-instruct

# For Vertex AI (higher cost, requires GCP)
export AI_PROVIDER=vertex
export VERTEX_AI_PROJECT=your-project-id
export VERTEX_AI_LOCATION=us-central1
```

---

## Firebase Complete Setup

### Step 1: Create Firebase Project

1. Go to https://console.firebase.google.com/
2. Click "Create a project"
3. Enter project name: `cbse-learning-platform`
4. Disable Google Analytics (optional, reduces complexity)
5. Click "Create project"

### Step 2: Enable Authentication

1. In Firebase Console, click "Authentication"
2. Click "Get started"
3. Enable "Email/Password" provider
4. Optionally enable "Google" sign-in

### Step 3: Set Up Firestore

1. Click "Firestore Database" in sidebar
2. Click "Create database"
3. Select "Start in production mode"
4. Choose location: `asia-south1` (Mumbai) for Indian users
5. Click "Enable"

### Step 4: Download Service Account Key

1. Go to Project Settings > Service accounts
2. Click "Generate new private key"
3. Save the JSON file securely
4. Set environment variable:
   ```bash
   export FIREBASE_CREDENTIALS_PATH=/path/to/credentials.json
   ```

### Step 5: Security Rules

Set up Firestore security rules:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users can only access their own data
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Progress data
    match /progress/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Public curriculum data (read-only)
    match /curriculum/{document=**} {
      allow read: if true;
      allow write: if false;
    }
  }
}
```

---

## Replicate AI Setup

### Step 1: Create Account

1. Go to https://replicate.com
2. Sign up with GitHub or email
3. You'll receive $5 free credits

### Step 2: Get API Token

1. Go to https://replicate.com/account/api-tokens
2. Click "Create token"
3. Copy the token (starts with `r8_`)

### Step 3: Configure Application

```bash
# Set environment variables
export AI_PROVIDER=replicate
export REPLICATE_API_TOKEN=r8_your_token_here
export REPLICATE_MODEL=meta/meta-llama-3.1-8b-instruct
```

### Step 4: Test the Integration

```python
import replicate

# Test API connection
output = replicate.run(
    "meta/meta-llama-3.1-8b-instruct",
    input={"prompt": "What is 2+2?", "max_tokens": 100}
)
print("".join(output))
```

### Cost Optimization Tips

1. **Use Caching**: The application caches AI responses to avoid repeated calls
2. **Use Mock for Development**: Set `AI_PROVIDER=mock` during development
3. **Batch Requests**: Generate multiple quiz questions in one API call
4. **Use Smaller Models**: Llama 3.1 8B is sufficient for most educational content

---

## Cloud Run Optimization

### Optimal Configuration for Low Cost

```bash
gcloud run deploy cbse-learning-app \
  --image=asia-south1-docker.pkg.dev/PROJECT_ID/cbse-app/backend:v1 \
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

### Key Settings Explained

| Setting | Value | Cost Impact |
|---------|-------|-------------|
| `min-instances=0` | Scale to zero | FREE when idle |
| `max-instances=2` | Limit scaling | Prevents runaway costs |
| `memory=512Mi` | Minimum needed | Lower memory = lower cost |
| `cpu=1` | Single CPU | Sufficient for most loads |
| `cpu-throttling` | Enabled | Reduces CPU cost when idle |
| `concurrency=80` | High concurrency | Fewer instances needed |

### Cold Start Mitigation

With `min-instances=0`, the first request after idle takes 2-5 seconds. Mitigate with:

1. **Frontend Loading State**: Show loading spinner during cold start
2. **Health Check Warming**: Use Cloud Scheduler to ping every 10 minutes (within free tier)
3. **Accept Trade-off**: For low-budget, cold starts are acceptable

---

## Monthly Cost Breakdown

### Scenario 1: Development/Testing ($0/month)

| Component | Usage | Cost |
|-----------|-------|------|
| Cloud Run | < 2M requests | FREE |
| Firestore | < 50K reads/day | FREE |
| AI Provider | Mock | FREE |
| **Total** | | **$0** |

### Scenario 2: Small School (50 students, ~$2-5/month)

| Component | Usage | Cost |
|-----------|-------|------|
| Cloud Run | ~100K requests | FREE |
| Firestore | ~10K reads/day | FREE |
| Replicate AI | ~50K tokens/day | ~$2-5 |
| **Total** | | **~$2-5** |

### Scenario 3: Medium School (200 students, ~$10-20/month)

| Component | Usage | Cost |
|-----------|-------|------|
| Cloud Run | ~500K requests | FREE |
| Firestore | ~30K reads/day | FREE |
| Replicate AI | ~200K tokens/day | ~$10-20 |
| **Total** | | **~$10-20** |

---

## Scaling Path

### Level 1: Free Tier (0-50 users)
- Mock AI provider
- Firestore free tier
- Cloud Run scale-to-zero
- **Cost: $0/month**

### Level 2: Low Budget (50-200 users)
- Replicate AI (Llama 3.1 8B)
- Firestore free tier
- Cloud Run scale-to-zero
- **Cost: $2-10/month**

### Level 3: Growing (200-500 users)
- Replicate AI (Llama 3.1 70B)
- Firestore (may exceed free tier)
- Cloud Run min-instances=1
- **Cost: $20-50/month**

### Level 4: Production (500+ users)
- Vertex AI Gemini
- Cloud SQL for complex queries
- Cloud Run with auto-scaling
- **Cost: $50-200/month**

---

## Quick Start Checklist

1. [ ] Create GCP account and claim $300 free credits
2. [ ] Create Firebase project (free)
3. [ ] Create Replicate account and get $5 free credits
4. [ ] Set up budget alerts in GCP
5. [ ] Deploy with `AI_PROVIDER=mock` first
6. [ ] Test thoroughly before enabling paid AI
7. [ ] Switch to `AI_PROVIDER=replicate` for production
8. [ ] Monitor costs weekly

---

## Environment Variables Reference

```bash
# Required
AI_PROVIDER=replicate  # or mock, vertex

# For Replicate (recommended for low budget)
REPLICATE_API_TOKEN=r8_your_token
REPLICATE_MODEL=meta/meta-llama-3.1-8b-instruct

# For Firebase
FIREBASE_CREDENTIALS_PATH=/path/to/credentials.json

# For Vertex AI (optional, higher cost)
VERTEX_AI_PROJECT=your-project-id
VERTEX_AI_LOCATION=us-central1

# Application
APP_ENV=production
JWT_SECRET_KEY=your-secret-key
```

---

## Troubleshooting

### "Replicate API token not set"
```bash
export REPLICATE_API_TOKEN=r8_your_token_here
```

### "Firebase credentials not found"
```bash
export FIREBASE_CREDENTIALS_PATH=/absolute/path/to/credentials.json
```

### "Exceeded Firestore free tier"
- Check daily read/write counts in Firebase Console
- Implement more aggressive caching
- Consider upgrading to Blaze plan (pay-as-you-go)

### "Cloud Run cold start too slow"
- Accept 2-5 second delay for first request
- Or set `min-instances=1` (adds ~$15-30/month)

---

## Summary

This low-cost deployment strategy achieves:

1. **90%+ cost reduction** compared to traditional cloud architecture
2. **Near-zero costs** for development and small deployments
3. **Pay-per-use AI** with Replicate (no minimum charges)
4. **Free database** with Firebase/Firestore
5. **Free compute** with Cloud Run scale-to-zero
6. **Easy scaling path** as your user base grows

Start with the free tier, use trial credits strategically, and only pay for what you use!
