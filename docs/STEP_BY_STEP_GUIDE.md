# CBSE Learning Platform - Complete 4W+H Implementation Guide

A comprehensive step-by-step guide using the 4W+H framework (What, Why, When, Where, How) for implementing and deploying the CBSE Learning Platform on Google Cloud Platform.

---

## Table of Contents

1. [Executive Summary: 4W+H Overview](#executive-summary-4wh-overview)
2. [Phase 1: Account Creation](#phase-1-account-creation)
3. [Phase 2: Project Setup](#phase-2-project-setup)
4. [Phase 3: Tool Installation](#phase-3-tool-installation)
5. [Phase 4: Repository Setup](#phase-4-repository-setup)
6. [Phase 5: Container Registry](#phase-5-container-registry)
7. [Phase 6: Cloud Run Deployment](#phase-6-cloud-run-deployment)
8. [Phase 7: Firebase Setup](#phase-7-firebase-setup)
9. [Phase 8: Database Configuration](#phase-8-database-configuration)
10. [Phase 9: Storage Setup](#phase-9-storage-setup)
11. [Phase 10: AI Configuration](#phase-10-ai-configuration)
12. [Phase 11: CI/CD Pipeline](#phase-11-cicd-pipeline)
13. [Phase 12: Content Upload](#phase-12-content-upload)
14. [Phase 13: Monitoring](#phase-13-monitoring)
15. [Troubleshooting Reference](#troubleshooting-reference)

---

## Executive Summary: 4W+H Overview

### WHAT is this project?

The CBSE Learning Platform is an AI-powered educational application designed for Indian students studying under the Central Board of Secondary Education (CBSE) curriculum for grades 6-10. The platform provides:

| Feature | Description |
|---------|-------------|
| AI Quiz Generation | Automatically generate quizzes aligned with CBSE syllabus |
| Doubt Clearing | Instant AI-powered explanations for student questions |
| Progress Tracking | Monitor learning advancement with gamification |
| Student Modes | Adaptive content for Dull/Average/Clever learners |
| Real-World Applications | Situated Cognition Theory implementation |

### WHY deploy this platform?

| Benefit | Explanation |
|---------|-------------|
| Cost-Effective | 90%+ savings using Firebase + Replicate vs traditional cloud |
| Scalable | Cloud Run auto-scales from 0 to handle any load |
| CBSE-Aligned | Content matches official NCERT curriculum |
| AI-Powered | Modern LLMs provide personalized learning |
| Free Tier Friendly | Can run entirely on GCP/Firebase free tiers |

### WHEN to use this guide?

| Scenario | Recommended Action |
|----------|-------------------|
| New to GCP | Start from Phase 1 (Account Creation) |
| Have GCP Account | Start from Phase 2 (Project Setup) |
| Have Project Ready | Start from Phase 5 (Container Registry) |
| Updating Existing | Jump to specific phase as needed |

**Time Required**: 2-4 hours for complete setup from scratch

### WHERE are components deployed?

| Component | Service | Location |
|-----------|---------|----------|
| Backend API | Cloud Run | asia-south1 (Mumbai) |
| Container Images | Artifact Registry | asia-south1 |
| User Database | Firestore | asia-south1 |
| Authentication | Firebase Auth | Global |
| File Storage | Cloud Storage | asia-south1 |
| AI Processing | Replicate/Vertex AI | US/Global |
| Secrets | Secret Manager | Global |

### HOW does the system work?

```
┌──────────────┐     HTTPS      ┌──────────────┐     API      ┌──────────────┐
│   Student    │───────────────▶│  Cloud Run   │─────────────▶│  Replicate   │
│   Browser    │                │  (FastAPI)   │              │  (Llama 3.1) │
└──────────────┘                └──────┬───────┘              └──────────────┘
                                       │
                    ┌──────────────────┼──────────────────┐
                    ▼                  ▼                  ▼
             ┌───────────┐      ┌───────────┐      ┌───────────┐
             │ Firestore │      │  Firebase │      │   Cloud   │
             │  (Data)   │      │   Auth    │      │  Storage  │
             └───────────┘      └───────────┘      └───────────┘
```

---

## Cost Summary by Phase

*Pricing as of December 2024, region: asia-south1 (Mumbai). Prices may vary.*

| Phase | Setup Cost | Monthly Cost | Free Tier | Cost Reduction Alternative |
|-------|------------|--------------|-----------|---------------------------|
| 1. Account Creation | Rs.0 | Rs.0 | $300 credits (90 days) | Use new account for fresh credits |
| 2. Project Setup | Rs.0 | Rs.0 | Unlimited projects | Separate dev/prod projects |
| 3. Tool Installation | Rs.0 | Rs.0 | All tools free | Use Cloud Shell (free) |
| 4. Repository Setup | Rs.0 | Rs.0 | GitHub free tier | Use GitLab/Bitbucket free |
| 5. Container Registry | Rs.0 | Rs.5-50/mo | ~0.5GB free | Use Docker Hub public |
| 6. Cloud Run | Rs.0 | Rs.0-500/mo | 2M requests/mo free | min-instances=0, low memory |
| 7. Firebase Auth | Rs.0 | Rs.0 | 50K MAU free | Avoid SMS/phone auth |
| 8. Firestore | Rs.0 | Rs.0-200/mo | 50K reads/day free | Denormalize, cache reads |
| 9. Cloud Storage | Rs.0 | Rs.0-100/mo | 5GB (US regions) | Compress files, use CDN |
| 10. AI (Replicate) | Rs.0 | Rs.50-500/mo | $5 free credits | Use mock provider, cache |
| 11. CI/CD | Rs.0 | Rs.0-100/mo | 120 min/day free | Build locally, use GitHub Actions |
| 12. Content Upload | Rs.0 | Rs.0 | N/A | Process offline |
| 13. Monitoring | Rs.0 | Rs.0-50/mo | Basic metrics free | Reduce log retention |

**Total Estimated Monthly Cost**:
- **Development/Testing**: Rs.0 (using free tiers + mock AI)
- **Small Production** (50 users): Rs.100-300/mo
- **Medium Production** (200 users): Rs.500-1000/mo

### Key Cost Drivers (What Actually Moves Your Bill)

| Cost Driver | Impact | How to Control |
|-------------|--------|----------------|
| Cloud Run min-instances | High | Set to 0 (accept cold starts) |
| AI API calls | High | Use mock for testing, cache responses |
| Firestore reads | Medium | Denormalize data, batch reads |
| Cloud Storage egress | Medium | Use CDN, compress files |
| Cloud Logging | Low-Medium | Set log level to WARN in prod |
| Network egress | Low | Keep data in same region |

### Warning: Hidden Cost Traps

1. **Region Matters**: Free tiers are often US-only. asia-south1 may not qualify for all free quotas.
2. **Logging Costs**: Debug logs can accumulate quickly. Set retention to 7 days in prod.
3. **Egress Fees**: Serving large files from Cloud Run is expensive. Use Cloud Storage + CDN.
4. **AI Abuse**: Public endpoints without auth can be abused, causing unexpected AI costs.

---

## Phase 1: Account Creation

### COST for Phase 1

| Item | Current Cost | Free Tier | Ongoing Cost |
|------|--------------|-----------|--------------|
| Google Account | Rs.0 | Forever free | Rs.0 |
| GCP Account | Rs.0 | $300 credits (90 days) | Rs.0 until you exceed free tier |
| Card Verification | Rs.2 (refunded) | N/A | Rs.0 |

**Cost Reduction Alternatives**:
1. **Use a new Google account** for fresh $300 credits if your existing account already used the trial
2. **Stay on Firebase Spark plan** (no billing) if you only need Firebase Auth + Firestore (but can't use Cloud Run)
3. **Use multiple accounts** for different projects to maximize free credits (check Google's terms)

**When to Upgrade**: Only enable billing when you need Cloud Run or Artifact Registry. Firebase-only projects can stay on Spark plan indefinitely.

---

### Step 1.1: Create Google Account

#### WHAT
Create a Google account to access all Google Cloud services.

#### WHY
Google account is the foundation for GCP, Firebase, and all related services. A new account gets $300 free credits.

#### WHEN
First step if you don't have a Google account. Skip if you already have one.

#### WHERE
https://accounts.google.com/signup

#### HOW

1. **Navigate to signup page**
   - Open browser: https://accounts.google.com/signup
   - Click "Create account" then "For myself"

2. **Enter personal information**
   ```
   First name: [Your first name]
   Last name: [Your last name]
   ```
   - Click "Next"

3. **Set birthday and gender**
   ```
   Birthday: [Your date of birth]
   Gender: [Select option]
   ```
   - Click "Next"

4. **Choose email address**
   - Option A: Create new Gmail (recommended for fresh credits)
   - Option B: Use existing email
   - Suggested format: `yourname.cbse.learning@gmail.com`

5. **Create strong password**
   ```
   Requirements:
   - Minimum 8 characters
   - Mix of letters, numbers, symbols
   - Example: Cbse@Learn2024!
   ```

6. **Verify phone number**
   - Enter phone number with country code (+91 for India)
   - Enter SMS verification code
   - Click "Verify"

7. **Accept terms**
   - Review Terms of Service
   - Click "I agree"

**Verification**: You should see Google account dashboard.

---

### Step 1.2: Create GCP Account with Free Trial

#### WHAT
Activate Google Cloud Platform with $300 free credits valid for 90 days.

#### WHY
Free credits allow full experimentation without cost. After trial, you only pay for what you use beyond free tier.

#### WHEN
Immediately after Google account creation.

#### WHERE
https://console.cloud.google.com/freetrial

#### HOW

1. **Navigate to GCP Console**
   - Go to: https://console.cloud.google.com/
   - Sign in with your Google account

2. **Accept Terms of Service**
   ```
   [x] I agree to Google Cloud Platform Terms of Service
   [x] Email updates (optional)
   Country: India
   ```
   - Click "AGREE AND CONTINUE"

3. **Start Free Trial**
   - Click "Activate" or "Try for free" button
   - Or go directly to: https://console.cloud.google.com/freetrial

4. **Account Information (Step 1/2)**
   ```
   Country: India
   Organization type: Personal project
   [x] Terms of Service agreement
   ```
   - Click "CONTINUE"

5. **Payment Information (Step 2/2)**
   ```
   Account type: Individual
   Name: [Your full name]
   Address: [Your complete address]
   City: [Your city]
   State: [Your state]
   PIN code: [Your postal code]
   
   Payment method:
   - Credit/Debit Card, OR
   - UPI ID (for Indian users)
   ```
   - Click "START MY FREE TRIAL"

6. **Identity Verification**
   - Google may charge Rs.2 for verification (refunded)
   - Complete any additional verification steps

**Verification**: 
```bash
gcloud auth list
# Should show your account as active
```

**What You Get**:
- $300 USD free credits (~Rs.25,000)
- 90 days validity
- No automatic charges after trial

---

## Phase 2: Project Setup

### COST for Phase 2

| Item | Current Cost | Free Tier | Ongoing Cost |
|------|--------------|-----------|--------------|
| Creating Projects | Rs.0 | Unlimited projects | Rs.0 |
| Budget Alerts | Rs.0 | Unlimited alerts | Rs.0 |
| Enabling APIs | Rs.0 | Free to enable | Rs.0 (usage may cost) |

**Cost Reduction Alternatives**:
1. **Separate dev/prod projects** - Isolate experiments from production to prevent dev costs affecting prod budget
2. **Only enable APIs you need** - Don't enable Vertex AI, BigQuery unless required
3. **Set aggressive budget alerts** - Set at Rs.500, Rs.800, Rs.1000 to catch issues early
4. **Restrict IAM permissions** - Only allow yourself to enable new APIs to prevent accidental enablement

**When to Upgrade**: Projects themselves are free. Costs come from the services you use within them.

**Pro Tip**: Create a "sandbox" project for experiments with a Rs.100 budget to test without risk.

---

### Step 2.1: Create GCP Project

#### WHAT
Create a dedicated GCP project to isolate resources, billing, and permissions.

#### WHY
Projects provide logical separation. Each project has its own billing, APIs, and access controls.

#### WHEN
After GCP account activation.

#### WHERE
https://console.cloud.google.com/projectcreate

#### HOW

1. **Open Project Selector**
   - Click project dropdown in top navigation bar
   - Click "NEW PROJECT"

2. **Configure Project**
   ```
   Project name: cbse-learning-platform
   Project ID: [auto-generated, can customize]
   Location: No organization (for personal)
   ```
   - Click "CREATE"

3. **Wait for Creation**
   - Watch notification bell for progress
   - Takes 30-60 seconds

4. **Select Project**
   - Click notification or project selector
   - Select "cbse-learning-platform"

5. **Note Project ID**
   - Go to: https://console.cloud.google.com/home/dashboard
   - Find "Project info" card
   - Copy Project ID (e.g., `cbse-learning-platform-12345`)

**Verification**:
```bash
gcloud config set project cbse-learning-platform
gcloud config get-value project
# Output: cbse-learning-platform
```

---

### Step 2.2: Set Budget Alerts

#### WHAT
Configure spending alerts to prevent unexpected charges.

#### WHY
Budget alerts notify you before costs exceed your limit. Essential for cost control.

#### WHEN
Immediately after project creation.

#### WHERE
https://console.cloud.google.com/billing/budgets

#### HOW

1. **Navigate to Budgets**
   - Click hamburger menu (three lines icon)
   - Click "Billing"
   - Select your billing account
   - Click "Budgets & alerts"

2. **Create Budget**
   - Click "CREATE BUDGET"
   ```
   Name: CBSE Learning Budget
   Time range: Monthly
   Projects: cbse-learning-platform
   ```
   - Click "NEXT"

3. **Set Amount**
   ```
   Budget type: Specified amount
   Target amount: 1000 (INR)
   ```
   - Click "NEXT"

4. **Configure Alerts**
   ```
   Thresholds:
   - 50% of budget
   - 80% of budget
   - 100% of budget
   
   Notifications:
   [x] Email alerts to billing admins
   Additional emails: [your-email@gmail.com]
   ```
   - Click "FINISH"

**Verification**: Budget should appear in list with Rs.0.00 current spend.

---

### Step 2.3: Enable Required APIs

#### WHAT
Enable GCP APIs needed for Cloud Run, Firestore, Storage, and AI services.

#### WHY
APIs must be explicitly enabled before use. This is a security feature.

#### WHEN
Before deploying any services.

#### WHERE
GCP Console or gcloud CLI.

#### HOW

```bash
# Set project
gcloud config set project cbse-learning-platform

# Enable all required APIs (run each command)
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable firestore.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable secretmanager.googleapis.com
gcloud services enable identitytoolkit.googleapis.com

# Optional: Enable Vertex AI (higher cost)
gcloud services enable aiplatform.googleapis.com
```

**Verification**:
```bash
gcloud services list --enabled | grep -E "(run|artifact|firestore|storage)"
# Should list all enabled services
```

---

## Phase 3: Tool Installation

### COST for Phase 3

| Item | Current Cost | Free Tier | Ongoing Cost |
|------|--------------|-----------|--------------|
| Google Cloud SDK | Rs.0 | Forever free | Rs.0 |
| Docker Desktop | Rs.0 | Free for personal use | Rs.0 (paid for enterprise) |
| Git | Rs.0 | Forever free | Rs.0 |

**Cost Reduction Alternatives**:
1. **Use Google Cloud Shell** - Free browser-based terminal with gcloud pre-installed (avoid local installation)
2. **Use Podman instead of Docker** - 100% free, no licensing concerns
3. **Build in Cloud Build** - Skip local Docker entirely, build directly in cloud (uses free tier minutes)

**When to Upgrade**: These tools are free. Docker Desktop requires paid license only for large enterprises (>250 employees).

**Pro Tip**: Cloud Shell gives you a free VM with 5GB persistent storage - great for quick deployments without local setup.

---

### Step 3.1: Install Google Cloud SDK

#### WHAT
Install gcloud CLI to interact with GCP from your terminal.

#### WHY
CLI enables scripted deployments, automation, and easier management than web console.

#### WHEN
Before any deployment operations.

#### WHERE
Your local development machine.

#### HOW

**For Windows:**
```powershell
# Download installer from:
# https://cloud.google.com/sdk/docs/install

# Run GoogleCloudSDKInstaller.exe
# Follow wizard with default options
# Check "Run gcloud init" at end
```

**For macOS:**
```bash
# Install via curl
curl https://sdk.cloud.google.com | bash

# Restart terminal
exec -l $SHELL

# Initialize
gcloud init
```

**For Linux (Ubuntu/Debian):**
```bash
# Add Google Cloud SDK repository
sudo apt-get update
sudo apt-get install apt-transport-https ca-certificates gnupg curl

curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | \
  sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg

echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] \
  https://packages.cloud.google.com/apt cloud-sdk main" | \
  sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

sudo apt-get update && sudo apt-get install google-cloud-cli
```

**Initialize gcloud:**
```bash
gcloud init

# When prompted:
# 1. Log in: Y (browser opens)
# 2. Select project: cbse-learning-platform
# 3. Default region: asia-south1
```

**Verification**:
```bash
gcloud config list
# Output should show:
# [core]
# account = your-email@gmail.com
# project = cbse-learning-platform
```

---

### Step 3.2: Install Docker

#### WHAT
Install Docker to build and run container images.

#### WHY
Cloud Run deploys containerized applications. Docker builds these containers.

#### WHEN
Before building application images.

#### WHERE
Your local development machine.

#### HOW

**For Windows:**
1. Download from: https://www.docker.com/products/docker-desktop/
2. Run installer
3. Restart computer
4. Start Docker Desktop
5. Wait for whale icon in system tray

**For macOS:**
1. Download from: https://www.docker.com/products/docker-desktop/
2. Open .dmg file
3. Drag Docker to Applications
4. Open Docker from Applications
5. Wait for initialization

**For Linux (Ubuntu):**
```bash
# Install prerequisites
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg lsb-release

# Add Docker GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Add repository
echo "deb [arch=$(dpkg --print-architecture) \
  signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io

# Add user to docker group (run without sudo)
sudo usermod -aG docker $USER

# Log out and back in for group changes
```

**Verification**:
```bash
docker --version
# Output: Docker version 24.x.x, build ...

docker run hello-world
# Should print "Hello from Docker!"
```

---

### Step 3.3: Install Git

#### WHAT
Install Git for version control and repository cloning.

#### WHY
Git is required to clone the project repository and manage code changes.

#### WHEN
Before cloning the repository.

#### WHERE
Your local development machine.

#### HOW

**For Windows:**
1. Download from: https://git-scm.com/download/win
2. Run installer with default options

**For macOS:**
```bash
# Usually pre-installed, if not:
xcode-select --install
```

**For Linux:**
```bash
sudo apt-get install git
```

**Verification**:
```bash
git --version
# Output: git version 2.x.x
```

---

## Phase 4: Repository Setup

### COST for Phase 4

| Item | Current Cost | Free Tier | Ongoing Cost |
|------|--------------|-----------|--------------|
| GitHub Repository | Rs.0 | Unlimited public repos | Rs.0 |
| Cloning Code | Rs.0 | Unlimited | Rs.0 |
| Environment Config | Rs.0 | N/A | Rs.0 |

**Cost Reduction Alternatives**:
1. **Use GitHub free tier** - Unlimited public repositories, 500MB packages storage
2. **Use GitLab/Bitbucket** - Similar free tiers, good alternatives
3. **Self-host Gitea** - Free, but requires server (not recommended for cost savings)

**Security Cost Risk**: Accidentally committing secrets (API keys, credentials) can lead to:
- Leaked Replicate tokens = unauthorized AI usage = unexpected bills
- Leaked Firebase credentials = database abuse = Firestore costs

**When to Upgrade**: GitHub free tier is sufficient for most projects. Paid plans needed only for private repos with large teams.

**Pro Tip**: Use `.gitignore` to exclude `.env` files. Store secrets only in Secret Manager.

---

### Step 4.1: Clone Repository

#### WHAT
Download the CBSE Learning Platform source code.

#### WHY
You need the source code to build and deploy the application.

#### WHEN
After all tools are installed.

#### WHERE
Your local development machine.

#### HOW

```bash
# Create projects directory
mkdir -p ~/projects
cd ~/projects

# Clone repository
git clone https://github.com/sunkaramallikarjuna369/AICBESE.git
cd AICBESE

# Checkout low-cost branch
git checkout devin/1766584808-low-cost-firebase-replicate
```

**Verification**:
```bash
ls -la
# Should show:
# cbse-learning-backend/
# cbse-learning-frontend/
# docs/
# infra/
# README.md
```

---

### Step 4.2: Configure Environment

#### WHAT
Set up environment variables for the application.

#### WHY
Environment variables configure database connections, API keys, and feature flags.

#### WHEN
Before running or deploying the application.

#### WHERE
`cbse-learning-backend/.env` file.

#### HOW

```bash
cd cbse-learning-backend

# Copy template
cp .env.example .env

# Edit configuration
nano .env  # or use your preferred editor
```

**Minimum Configuration**:
```bash
# AI Provider (start with mock for free testing)
AI_PROVIDER=mock

# Application
APP_ENV=development
DEBUG=true
JWT_SECRET_KEY=your-secret-key-change-in-production

# GCP (will be set after project creation)
GCP_PROJECT_ID=cbse-learning-platform
GCP_REGION=asia-south1
```

**Production Configuration** (add later):
```bash
# For Replicate AI (low-cost)
AI_PROVIDER=replicate
REPLICATE_API_TOKEN=r8_your_token_here
REPLICATE_MODEL=meta/meta-llama-3.1-8b-instruct

# Firebase credentials path
FIREBASE_CREDENTIALS_PATH=/path/to/firebase-credentials.json
```

**Verification**:
```bash
cat .env | grep AI_PROVIDER
# Output: AI_PROVIDER=mock
```

---

## Phase 5: Container Registry

### COST for Phase 5

| Item | Current Cost | Free Tier | Ongoing Cost |
|------|--------------|-----------|--------------|
| Artifact Registry Storage | Rs.0 setup | ~0.5GB free | Rs.1.70/GB/month after free tier |
| Image Pulls | Rs.0 | Free within GCP | Rs.0 (same region) |
| Network Egress | Rs.0 | Free within GCP | Rs.8-12/GB outside GCP |

**Cost Reduction Alternatives**:
1. **Optimize Docker images** - Use slim base images (python:3.11-slim vs python:3.11) to reduce storage
2. **Use multi-stage builds** - Final image contains only runtime, not build tools
3. **Delete old images** - Set up lifecycle policies to auto-delete images older than 30 days
4. **Use Docker Hub public** - Free unlimited public images (but slower pulls from GCP)
5. **Build with Cloud Build** - Images stored directly, no local push bandwidth

**Image Size Impact**:
| Base Image | Size | Monthly Cost (10 versions) |
|------------|------|---------------------------|
| python:3.11 | ~1GB | Rs.17/month |
| python:3.11-slim | ~150MB | Rs.2.5/month |
| python:3.11-alpine | ~50MB | Rs.0.85/month |

**When to Upgrade**: Free tier is usually sufficient. Costs increase with many large images or frequent deployments.

**Pro Tip**: Add this to your Dockerfile to reduce image size:
```dockerfile
FROM python:3.11-slim
# Instead of FROM python:3.11
```

---

### Step 5.1: Create Artifact Registry Repository

#### WHAT
Create a Docker container registry to store application images.

#### WHY
Cloud Run deploys from container images stored in Artifact Registry.

#### WHEN
Before building Docker images.

#### WHERE
GCP Artifact Registry, asia-south1 region.

#### HOW

```bash
# Create repository
gcloud artifacts repositories create cbse-app \
  --repository-format=docker \
  --location=asia-south1 \
  --description="CBSE Learning Platform Docker images"

# Configure Docker authentication
gcloud auth configure-docker asia-south1-docker.pkg.dev
# Enter Y when prompted
```

**Verification**:
```bash
gcloud artifacts repositories list --location=asia-south1
# Output:
# REPOSITORY  FORMAT  DESCRIPTION
# cbse-app    DOCKER  CBSE Learning Platform Docker images
```

---

### Step 5.2: Build Docker Image

#### WHAT
Build a container image of the backend application.

#### WHY
Container images package the application with all dependencies for consistent deployment.

#### WHEN
After repository setup and code configuration.

#### WHERE
Local machine, then pushed to Artifact Registry.

#### HOW

```bash
# Navigate to backend
cd ~/projects/AICBESE/cbse-learning-backend

# Set project ID
export PROJECT_ID=$(gcloud config get-value project)

# Build image
docker build -t asia-south1-docker.pkg.dev/$PROJECT_ID/cbse-app/backend:v1 .
```

**Build takes 5-10 minutes on first run.**

**Verification**:
```bash
docker images | grep cbse-app
# Should show your image with tag v1
```

---

### Step 5.3: Push Image to Registry

#### WHAT
Upload the built container image to Artifact Registry.

#### WHY
Cloud Run needs to pull the image from a registry to deploy.

#### WHEN
After successful local build.

#### WHERE
From local machine to asia-south1 Artifact Registry.

#### HOW

```bash
# Push image
docker push asia-south1-docker.pkg.dev/$PROJECT_ID/cbse-app/backend:v1
```

**Push takes 2-5 minutes depending on internet speed.**

**Verification**:
```bash
gcloud artifacts docker images list \
  asia-south1-docker.pkg.dev/$PROJECT_ID/cbse-app
# Should list backend:v1
```

---

## Phase 6: Cloud Run Deployment

### COST for Phase 6

| Item | Current Cost | Free Tier | Ongoing Cost |
|------|--------------|-----------|--------------|
| CPU | Rs.0 | 180,000 vCPU-seconds/month | Rs.0.0024/vCPU-second after |
| Memory | Rs.0 | 360,000 GiB-seconds/month | Rs.0.00025/GiB-second after |
| Requests | Rs.0 | 2 million requests/month | Rs.0.40/million after |
| Networking | Rs.0 | 1GB egress/month | Rs.0.12/GB after |

**This is the LARGEST cost driver in your stack!**

**Cost Reduction Alternatives**:
1. **Set min-instances=0** - CRITICAL! This enables scale-to-zero (no cost when idle)
2. **Use 256Mi memory** instead of 512Mi - Halves memory cost
3. **Enable CPU throttling** - CPU only allocated during request processing
4. **Set max-instances=2** - Prevents runaway scaling during traffic spikes
5. **Use concurrency=80** - Handle more requests per instance
6. **Avoid always-on** - Don't set min-instances > 0 unless you need instant response

**Cost Comparison (50 users, 1000 requests/day)**:
| Configuration | Monthly Cost |
|---------------|--------------|
| min-instances=0, 256Mi | Rs.0-50 |
| min-instances=0, 512Mi | Rs.0-100 |
| min-instances=1, 512Mi | Rs.500-800 |
| min-instances=2, 1Gi | Rs.1500-2500 |

**Cold Start Trade-off**: min-instances=0 means first request after idle takes 2-5 seconds. For educational apps, this is usually acceptable.

**When to Upgrade**: Only increase min-instances if users complain about slow first loads. Start with 0 and monitor.

**Pro Tip**: Use this exact deploy command for lowest cost:
```bash
gcloud run deploy cbse-learning-app \
  --min-instances=0 --max-instances=2 \
  --memory=256Mi --cpu=1 --cpu-throttling \
  --concurrency=80
```

---

### Step 6.1: Deploy Application

#### WHAT
Deploy the container to Cloud Run serverless platform.

#### WHY
Cloud Run provides auto-scaling, HTTPS, and pay-per-use pricing with scale-to-zero.

#### WHEN
After image is pushed to registry.

#### WHERE
Cloud Run, asia-south1 region.

#### HOW

```bash
# Deploy to Cloud Run
gcloud run deploy cbse-learning-app \
  --image=asia-south1-docker.pkg.dev/$PROJECT_ID/cbse-app/backend:v1 \
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
  --set-env-vars="AI_PROVIDER=mock,APP_ENV=production"
```

**Deployment takes 1-2 minutes.**

**Verification**:
```bash
# Get service URL
export APP_URL=$(gcloud run services describe cbse-learning-app \
  --region=asia-south1 --format='value(status.url)')
echo "Your app URL: $APP_URL"

# Test health endpoint
curl $APP_URL/health
# Output: {"status": "healthy"}
```

---

### Step 6.2: Test Deployment

#### WHAT
Verify the deployed application works correctly.

#### WHY
Catch deployment issues before configuring additional services.

#### WHEN
Immediately after deployment.

#### WHERE
Your deployed Cloud Run URL.

#### HOW

```bash
# Test API root
curl $APP_URL/
# Should return JSON with available services

# Test health endpoint
curl $APP_URL/health
# Output: {"status": "healthy"}

# Test curriculum endpoint
curl $APP_URL/curriculum/classes
# Should return list of classes

# Open API documentation
echo "Open in browser: $APP_URL/docs"
```

**Browser Test**:
1. Open `$APP_URL` in browser
2. You should see the login page
3. Test credentials: `user` / `dd058af30a635609e894c13b4e524841`

---

## Phase 7: Firebase Setup

### COST for Phase 7

| Item | Current Cost | Free Tier | Ongoing Cost |
|------|--------------|-----------|--------------|
| Email/Password Auth | Rs.0 | 50,000 MAU free | Rs.0 (within free tier) |
| Google Sign-In | Rs.0 | 50,000 MAU free | Rs.0 (within free tier) |
| Phone Auth (SMS) | Rs.0 | 10 SMS/day free | Rs.0.06/SMS after (EXPENSIVE!) |
| Anonymous Auth | Rs.0 | Unlimited | Rs.0 |

**MAU = Monthly Active Users** (users who sign in at least once per month)

**Cost Reduction Alternatives**:
1. **Use Email/Password only** - Completely free up to 50K MAU
2. **AVOID Phone/SMS Auth** - This is the #1 hidden cost trap! 10 SMS/day free, then Rs.0.06/SMS
3. **Use Google Sign-In** - Free and reduces friction for users
4. **Avoid Firebase Extensions** - Many extensions have hidden costs

**Phone Auth Cost Example**:
| Users | SMS/month | Monthly Cost |
|-------|-----------|--------------|
| 50 | 50 | Rs.0 (within free) |
| 500 | 500 | Rs.29/month |
| 5000 | 5000 | Rs.299/month |

**When to Upgrade**: Firebase Auth free tier (50K MAU) is sufficient for most schools. Only pay if you exceed 50K monthly active users.

**Pro Tip**: Disable phone authentication in Firebase Console unless absolutely required. Use email + Google Sign-In instead.

---

### Step 7.1: Create Firebase Project

#### WHAT
Link Firebase to your GCP project for authentication and database services.

#### WHY
Firebase provides free authentication (50K MAU) and Firestore database.

#### WHEN
After Cloud Run deployment is working.

#### WHERE
https://console.firebase.google.com

#### HOW

1. **Navigate to Firebase Console**
   - Go to: https://console.firebase.google.com
   - Sign in with your Google account

2. **Add Firebase to GCP Project**
   - Click "Add project"
   - Click "Add Firebase to a Google Cloud project"
   - Select: `cbse-learning-platform`
   - Click "Continue"

3. **Configure Analytics (Optional)**
   - Toggle OFF "Enable Google Analytics" (simplifies setup)
   - Click "Add Firebase"

4. **Wait for Setup**
   - Takes about 1 minute
   - Click "Continue" when done

**Verification**: You should see Firebase Console dashboard for your project.

---

### Step 7.2: Enable Authentication

#### WHAT
Configure Firebase Authentication with email/password sign-in.

#### WHY
Secure user authentication without building auth from scratch.

#### WHEN
After Firebase project is created.

#### WHERE
Firebase Console > Authentication.

#### HOW

1. **Navigate to Authentication**
   - Click "Build" in sidebar
   - Click "Authentication"
   - Click "Get started"

2. **Enable Email/Password**
   - Click "Email/Password" provider
   - Toggle "Enable" to ON
   - Click "Save"

3. **Enable Google Sign-in (Optional)**
   - Click "Add new provider"
   - Click "Google"
   - Toggle "Enable" to ON
   - Enter support email
   - Click "Save"

**Verification**: Providers should show as "Enabled" in the list.

---

### Step 7.3: Download Service Account Key

#### WHAT
Download credentials for backend to access Firebase services.

#### WHY
The backend needs authenticated access to Firebase Auth and Firestore.

#### WHEN
After authentication is enabled.

#### WHERE
Firebase Console > Project Settings > Service Accounts.

#### HOW

1. **Navigate to Service Accounts**
   - Click gear icon in sidebar
   - Click "Project settings"
   - Click "Service accounts" tab

2. **Generate Key**
   - Click "Generate new private key"
   - Click "Generate key" in confirmation
   - Save downloaded JSON file securely
   - Rename to `firebase-credentials.json`

3. **Upload to Secret Manager**
   ```bash
   # Create secret from file
   gcloud secrets create firebase-credentials \
     --data-file=/path/to/firebase-credentials.json
   
   # Get project number
   PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID \
     --format='value(projectNumber)')
   
   # Grant Cloud Run access
   gcloud secrets add-iam-policy-binding firebase-credentials \
     --member="serviceAccount:$PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
     --role="roles/secretmanager.secretAccessor"
   ```

4. **Update Cloud Run**
   ```bash
   gcloud run services update cbse-learning-app \
     --region=asia-south1 \
     --set-secrets="FIREBASE_CREDENTIALS_PATH=firebase-credentials:latest"
   ```

**Verification**:
```bash
gcloud secrets list
# Should show firebase-credentials
```

---

## Phase 8: Database Configuration

### COST for Phase 8

| Item | Current Cost | Free Tier | Ongoing Cost |
|------|--------------|-----------|--------------|
| Document Reads | Rs.0 | 50,000/day | Rs.0.06/100K reads after |
| Document Writes | Rs.0 | 20,000/day | Rs.0.18/100K writes after |
| Document Deletes | Rs.0 | 20,000/day | Rs.0.02/100K deletes after |
| Storage | Rs.0 | 1 GB | Rs.0.18/GB/month after |
| Network Egress | Rs.0 | 10 GB/month | Rs.0.12/GB after |

**Cost Reduction Alternatives**:
1. **Denormalize data** - Store related data together to reduce reads (1 read vs 5 reads)
2. **Use subcollections wisely** - Avoid deep nesting that requires multiple reads
3. **Batch writes** - Group multiple writes into batches (counts as 1 write per doc)
4. **Cache on client** - Use Firestore offline persistence to reduce reads
5. **Avoid real-time listeners on large collections** - Each document change = 1 read

**Read Cost Example (Educational App)**:
| Operation | Reads/User/Day | 50 Users | 200 Users |
|-----------|----------------|----------|-----------|
| Login + Profile | 3 | 150 | 600 |
| View Progress | 5 | 250 | 1000 |
| Load Quiz | 10 | 500 | 2000 |
| **Total** | **18** | **900** | **3600** |

With 50K free reads/day, you can support ~2,700 active users before paying.

**When to Upgrade**: Free tier (50K reads/day) supports most small-medium schools. Monitor usage in Firebase Console > Usage tab.

**Pro Tip**: Structure data to minimize reads:
```javascript
// BAD: 5 reads
users/{userId}
users/{userId}/progress
users/{userId}/quizzes
users/{userId}/doubts
users/{userId}/settings

// GOOD: 1 read (denormalized)
users/{userId} {
  profile: {...},
  progress: {...},
  recentQuizzes: [...],
  settings: {...}
}
```

---

### Step 8.1: Create Firestore Database

#### WHAT
Create a Firestore NoSQL database for storing user data and progress.

#### WHY
Firestore offers 1GB free storage, 50K reads/day, 20K writes/day at no cost.

#### WHEN
After Firebase project is set up.

#### WHERE
Firebase Console or GCP Console.

#### HOW

1. **Navigate to Firestore**
   - Go to: https://console.cloud.google.com/firestore
   - Or Firebase Console > Build > Firestore Database

2. **Create Database**
   - Click "Create Database"
   - Select "Native mode" (recommended)
   - Click "Continue"

3. **Choose Location**
   - Select: `asia-south1 (Mumbai)`
   - Click "Create Database"

4. **Wait for Creation**
   - Takes 1-2 minutes
   - You'll see empty database browser when done

**Verification**: Firestore data browser should be visible with no collections.

---

### Step 8.2: Configure Security Rules

#### WHAT
Set up Firestore security rules to protect user data.

#### WHY
Security rules prevent unauthorized access to sensitive data.

#### WHEN
Before going to production.

#### WHERE
Firebase Console > Firestore > Rules.

#### HOW

1. **Navigate to Rules**
   - In Firestore Database, click "Rules" tab

2. **Update Rules**
   ```javascript
   rules_version = '2';
   service cloud.firestore {
     match /databases/{database}/documents {
       // Users can only access their own data
       match /users/{userId} {
         allow read, write: if request.auth != null && 
           request.auth.uid == userId;
       }
       
       // Progress data - user-specific
       match /progress/{progressId} {
         allow read, write: if request.auth != null && 
           resource.data.user_id == request.auth.uid;
       }
       
       // Quizzes - user can read own, create new
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
       
       // Public curriculum (read-only)
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

3. **Publish Rules**
   - Click "Publish"

**Verification**: Rules should show "Published" status.

---

## Phase 9: Storage Setup

### COST for Phase 9

| Item | Current Cost | Free Tier | Ongoing Cost |
|------|--------------|-----------|--------------|
| Storage | Rs.0 | 5 GB (US regions only!) | Rs.0.02/GB/month (Standard) |
| Class A Operations (write) | Rs.0 | 5,000/month | Rs.0.05/10K ops |
| Class B Operations (read) | Rs.0 | 50,000/month | Rs.0.004/10K ops |
| Network Egress | Rs.0 | 1 GB/month | Rs.0.12/GB |

**WARNING: Free tier is US regions only!** asia-south1 does NOT qualify for the 5GB free storage.

**Cost Reduction Alternatives**:
1. **Use US region for storage** - If latency is acceptable, use us-central1 for free tier
2. **Compress files** - Use PDF compression, image optimization before upload
3. **Use Cloud CDN** - Cache frequently accessed files to reduce egress costs
4. **Use Nearline/Coldline** - For rarely accessed files (Rs.0.01/GB vs Rs.0.02/GB)
5. **Set lifecycle policies** - Auto-delete old files after 90 days

**Storage Class Comparison**:
| Class | Cost/GB/month | Best For |
|-------|---------------|----------|
| Standard | Rs.0.02 | Frequently accessed (PDFs, images) |
| Nearline | Rs.0.01 | Monthly access (backups) |
| Coldline | Rs.0.004 | Quarterly access (archives) |
| Archive | Rs.0.0012 | Yearly access (compliance) |

**Cost Example (Educational Content)**:
| Content | Size | Monthly Cost (asia-south1) |
|---------|------|---------------------------|
| 100 NCERT PDFs | 500 MB | Rs.0.01 |
| 1000 Images | 2 GB | Rs.0.04 |
| Video Thumbnails | 500 MB | Rs.0.01 |
| **Total** | **3 GB** | **Rs.0.06** |

**When to Upgrade**: Storage costs are minimal. Focus on egress costs - serving large files directly from Cloud Run is expensive.

**Pro Tip**: Serve files via signed URLs from Cloud Storage instead of proxying through Cloud Run:
```python
# BAD: Proxy through Cloud Run (egress from Cloud Run)
@app.get("/pdf/{file}")
def get_pdf(file): return FileResponse(download_from_storage(file))

# GOOD: Signed URL (egress from Cloud Storage)
@app.get("/pdf/{file}")
def get_pdf_url(file): return {"url": generate_signed_url(file)}
```

---

### Step 9.1: Create Cloud Storage Bucket

#### WHAT
Create a storage bucket for PDFs, images, and generated content.

#### WHY
Cloud Storage provides 5GB free storage for static files.

#### WHEN
After database is configured.

#### WHERE
GCP Console > Cloud Storage.

#### HOW

1. **Navigate to Cloud Storage**
   - Go to: https://console.cloud.google.com/storage

2. **Create Bucket**
   - Click "CREATE BUCKET"
   ```
   Name: cbse-learning-platform-storage
   (Must be globally unique - add initials if taken)
   ```
   - Click "Continue"

3. **Choose Location**
   - Select: Region
   - Choose: asia-south1 (Mumbai)
   - Click "Continue"

4. **Choose Storage Class**
   - Select: Standard
   - Click "Continue"

5. **Access Control**
   - Select: Uniform
   - Click "Continue"

6. **Create**
   - Click "CREATE"

7. **Create Folder Structure**
   - Click bucket name
   - Click "CREATE FOLDER"
   - Create: `cbse/class-10/mathematics/quadratic-equations`

8. **Update Cloud Run**
   ```bash
   gcloud run services update cbse-learning-app \
     --region=asia-south1 \
     --update-env-vars="GCS_BUCKET=cbse-learning-platform-storage"
   ```

**Verification**:
```bash
gsutil ls gs://cbse-learning-platform-storage/
# Should show cbse/ folder
```

---

## Phase 10: AI Configuration

### COST for Phase 10

| Provider | Cost Model | Approximate Cost | Free Credits |
|----------|------------|------------------|--------------|
| Mock (Testing) | Rs.0 | Rs.0 | Unlimited |
| Replicate (Llama 3.1 8B) | Per-second GPU | ~$0.05/million tokens | $5 signup |
| Vertex AI (Gemini Flash) | Per-character | ~$0.0005/1K chars | $300 GCP credits |
| OpenAI (GPT-4) | Per-token | ~$0.03/1K tokens | None |

**This is the SECOND largest cost driver after Cloud Run!**

**Cost Reduction Alternatives**:
1. **Use Mock provider for development** - Rs.0 cost, returns placeholder responses
2. **Use Replicate over Vertex AI** - 10x cheaper for similar quality
3. **Cache AI responses** - Store common question answers in Firestore
4. **Rate limit AI calls** - Limit free users to 5 AI calls/day
5. **Use smaller models** - Llama 3.1 8B vs 70B (10x cheaper)
6. **Batch similar questions** - Group similar doubts into one AI call

**Cost Comparison (1000 AI calls/month)**:
| Provider | Model | Monthly Cost |
|----------|-------|--------------|
| Mock | N/A | Rs.0 |
| Replicate | Llama 3.1 8B | Rs.50-100 |
| Replicate | Llama 3.1 70B | Rs.500-1000 |
| Vertex AI | Gemini Flash | Rs.200-400 |
| Vertex AI | Gemini Pro | Rs.500-1000 |
| OpenAI | GPT-4 | Rs.2000-5000 |

**Replicate Pricing Details**:
- Charged per second of GPU time (not tokens)
- Llama 3.1 8B: ~$0.0001/second on A40 GPU
- Average request: 2-5 seconds = $0.0002-0.0005/request
- 1000 requests ≈ $0.20-0.50 ≈ Rs.17-42

**When to Upgrade**: Start with Mock for testing, then Replicate for production. Only use Vertex AI if you need Google's specific models or have GCP credits.

**Pro Tip**: Implement response caching:
```python
# Check cache before calling AI
cached = await firestore.get_cached_response(question_hash)
if cached:
    return cached  # Rs.0 cost

# Only call AI for new questions
response = await replicate.generate(question)
await firestore.cache_response(question_hash, response)
```

---

### Step 10.1: Configure Replicate AI (Recommended)

#### WHAT
Set up Replicate API for cost-effective AI inference.

#### WHY
Replicate costs ~$0.05/million tokens vs Vertex AI's higher pricing. 10x cheaper.

#### WHEN
When ready to enable AI features.

#### WHERE
https://replicate.com

#### HOW

1. **Create Replicate Account**
   - Go to: https://replicate.com
   - Sign up with GitHub or email
   - You get $5 free credits

2. **Get API Token**
   - Go to: https://replicate.com/account/api-tokens
   - Click "Create token"
   - Copy token (starts with `r8_`)

3. **Store Token in Secret Manager**
   ```bash
   # Create secret
   echo -n "r8_your_token_here" | \
     gcloud secrets create replicate-api-token --data-file=-
   
   # Grant access
   PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID \
     --format='value(projectNumber)')
   
   gcloud secrets add-iam-policy-binding replicate-api-token \
     --member="serviceAccount:$PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
     --role="roles/secretmanager.secretAccessor"
   ```

4. **Update Cloud Run**
   ```bash
   gcloud run services update cbse-learning-app \
     --region=asia-south1 \
     --update-env-vars="AI_PROVIDER=replicate,REPLICATE_MODEL=meta/meta-llama-3.1-8b-instruct" \
     --set-secrets="REPLICATE_API_TOKEN=replicate-api-token:latest"
   ```

**Verification**:
```bash
curl -X POST "$APP_URL/visualization-orchestrator/topics/topic-1/config" \
  -H "Content-Type: application/json" \
  -d '{"student_mode": "average"}'
# Should return AI-generated visual config
```

---

### Step 10.2: Configure Vertex AI (Alternative)

#### WHAT
Set up Google Vertex AI with Gemini model (higher cost option).

#### WHY
Vertex AI offers Google's latest models but at higher cost.

#### WHEN
If you have GCP credits or prefer Google's AI.

#### WHERE
GCP Console > Vertex AI.

#### HOW

1. **Enable Vertex AI API**
   ```bash
   gcloud services enable aiplatform.googleapis.com
   ```

2. **Grant Permissions**
   ```bash
   PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID \
     --format='value(projectNumber)')
   
   gcloud projects add-iam-policy-binding $PROJECT_ID \
     --member="serviceAccount:$PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
     --role="roles/aiplatform.user"
   ```

3. **Update Cloud Run**
   ```bash
   gcloud run services update cbse-learning-app \
     --region=asia-south1 \
     --update-env-vars="AI_PROVIDER=vertex,VERTEX_AI_PROJECT=$PROJECT_ID,VERTEX_AI_LOCATION=asia-south1"
   ```

**Note**: Using Vertex AI will incur costs. Use `AI_PROVIDER=mock` for free testing.

---

## Phase 11: CI/CD Pipeline

### COST for Phase 11

| Item | Current Cost | Free Tier | Ongoing Cost |
|------|--------------|-----------|--------------|
| Cloud Build | Rs.0 | 120 build-minutes/day | Rs.0.003/build-minute after |
| Build Storage | Rs.0 | Included in Artifact Registry | See Phase 5 |
| GitHub Connection | Rs.0 | Free | Rs.0 |

**Cost Reduction Alternatives**:
1. **Build locally, push image** - Skip Cloud Build entirely, use local Docker
2. **Use GitHub Actions** - 2000 minutes/month free (more than Cloud Build!)
3. **Optimize build time** - Use Docker layer caching, smaller base images
4. **Reduce build frequency** - Only build on main branch, not every PR
5. **Use Cloud Build substitutions** - Avoid rebuilding unchanged layers

**Build Time Comparison**:
| Build Type | Time | Daily Builds | Monthly Cost |
|------------|------|--------------|--------------|
| Full rebuild | 5 min | 24 | Rs.0 (within free) |
| Full rebuild | 5 min | 50 | Rs.45/month |
| Cached rebuild | 2 min | 50 | Rs.0 (within free) |
| Local build + push | 0 min | Unlimited | Rs.0 |

**GitHub Actions Alternative** (Recommended for cost savings):
```yaml
# .github/workflows/deploy.yml
name: Deploy to Cloud Run
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: google-github-actions/deploy-cloudrun@v2
        with:
          service: cbse-learning-app
          region: asia-south1
```
GitHub Actions: 2000 min/month free vs Cloud Build: 120 min/day (~3600 min/month)

**When to Upgrade**: Free tier is usually sufficient. Only pay if you have >24 builds/day or builds take >5 minutes.

**Pro Tip**: Add Docker layer caching to reduce build time:
```dockerfile
# Cache dependencies layer
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

# Copy source (changes frequently)
COPY . .
```

---

### Step 11.1: Connect GitHub Repository

#### WHAT
Connect your GitHub repository to Cloud Build for automatic deployments.

#### WHY
CI/CD automates testing and deployment when you push code changes.

#### WHEN
After manual deployment is working.

#### WHERE
GCP Console > Cloud Build.

#### HOW

1. **Navigate to Cloud Build**
   - Go to: https://console.cloud.google.com/cloud-build

2. **Connect Repository**
   - Click "Triggers" in sidebar
   - Click "CONNECT REPOSITORY"
   - Select "GitHub (Cloud Build GitHub App)"
   - Click "Continue"

3. **Authenticate**
   - Click "Authenticate"
   - Sign in to GitHub
   - Click "Authorize Google Cloud Build"

4. **Select Repository**
   - Select your GitHub account
   - Find and select `AICBESE` repository
   - Check consent checkbox
   - Click "Connect"

---

### Step 11.2: Create Build Trigger

#### WHAT
Create a trigger to automatically deploy on code push.

#### WHY
Automatic deployments reduce manual work and ensure consistency.

#### WHEN
After repository is connected.

#### WHERE
Cloud Build > Triggers.

#### HOW

1. **Create Trigger**
   - Click "CREATE TRIGGER"
   ```
   Name: deploy-on-push
   Description: Deploy to Cloud Run on push
   Event: Push to a branch
   Repository: sunkaramallikarjuna369/AICBESE
   Branch: ^devin/1766584808-low-cost-firebase-replicate$
   Configuration: Cloud Build configuration file
   Location: /infra/cloudbuild/cloudbuild-simple.yaml
   ```
   - Click "CREATE"

2. **Grant Permissions**
   ```bash
   PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID \
     --format='value(projectNumber)')
   
   # Grant Cloud Run Admin
   gcloud projects add-iam-policy-binding $PROJECT_ID \
     --member="serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com" \
     --role="roles/run.admin"
   
   # Grant Service Account User
   gcloud projects add-iam-policy-binding $PROJECT_ID \
     --member="serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com" \
     --role="roles/iam.serviceAccountUser"
   ```

**Verification**: Push a small change and watch Cloud Build > History for the build.

---

## Phase 12: Content Upload

### COST for Phase 12

| Item | Current Cost | Free Tier | Ongoing Cost |
|------|--------------|-----------|--------------|
| PDF Storage | Rs.0 | See Phase 9 | Rs.0.02/GB/month |
| PDF Processing (AI) | Rs.0-50 | Depends on AI provider | See Phase 10 |
| RAG Indexing | Rs.0 | SQLite FTS5 (local) | Rs.0 |
| Embeddings (if used) | Rs.50-500 | None | EXPENSIVE! |

**WARNING: Embeddings are a hidden cost trap!**

**Cost Reduction Alternatives**:
1. **Use SQLite FTS5 for search** - Free, local, no API calls (this project uses this!)
2. **AVOID vector embeddings** - Embedding APIs charge per token and add up fast
3. **Process PDFs offline** - Extract text locally before upload
4. **Compress PDFs** - Smaller files = less storage cost
5. **Batch uploads** - Upload during off-peak hours to avoid AI rate limits

**Embedding Cost Comparison (100 NCERT chapters)**:
| Method | Cost |
|--------|------|
| SQLite FTS5 (text search) | Rs.0 |
| OpenAI Embeddings | Rs.500-1000 |
| Vertex AI Embeddings | Rs.200-500 |
| Local Sentence Transformers | Rs.0 (but slow) |

**This project uses SQLite FTS5** - completely free text search without embeddings!

**Content Processing Cost Example**:
| Content | Storage | AI Processing | Total |
|---------|---------|---------------|-------|
| 10 PDFs (50MB) | Rs.0.001 | Rs.5 (Replicate) | Rs.5 |
| 100 PDFs (500MB) | Rs.0.01 | Rs.50 (Replicate) | Rs.50 |
| 1000 PDFs (5GB) | Rs.0.10 | Rs.500 (Replicate) | Rs.500 |

**When to Upgrade**: Content upload is mostly one-time. Ongoing costs are minimal unless you frequently reprocess content.

**Pro Tip**: Process PDFs locally and upload only the extracted text:
```python
# Process locally (Rs.0)
import PyPDF2
text = extract_text_from_pdf(pdf_path)

# Upload text only (smaller, faster)
upload_processed_text(text, metadata)
```

---

### Step 12.1: Upload NCERT PDFs

#### WHAT
Add CBSE curriculum content to the platform.

#### WHY
Students need actual NCERT content to learn from.

#### WHEN
After all services are configured.

#### WHERE
Via API endpoints.

#### HOW

1. **Download NCERT PDF**
   - Go to: https://ncert.nic.in/textbook.php
   - Select: Class X, Mathematics
   - Download Chapter 4: Quadratic Equations

2. **Get Authentication Token**
   ```bash
   TOKEN=$(curl -s -X POST "$APP_URL/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "user", "password": "dd058af30a635609e894c13b4e524841"}' \
     | jq -r '.access_token')
   
   echo "Token: $TOKEN"
   ```

3. **Upload PDF**
   ```bash
   curl -X POST "$APP_URL/pdf-ingestion/upload" \
     -H "Authorization: Bearer $TOKEN" \
     -F "file=@/path/to/quadratic-equations.pdf" \
     -F "class_level=10" \
     -F "subject=Mathematics" \
     -F "chapter=Quadratic Equations"
   ```

4. **Process PDF**
   ```bash
   # Get PDF_ID from upload response
   curl -X POST "$APP_URL/pdf-ingestion/process/YOUR_PDF_ID" \
     -H "Authorization: Bearer $TOKEN"
   ```

5. **Index for RAG**
   ```bash
   curl -X POST "$APP_URL/rag-agent/index/YOUR_PDF_ID" \
     -H "Authorization: Bearer $TOKEN"
   ```

**Verification**:
```bash
curl -X POST "$APP_URL/rag-agent/ask" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "pdf_id": "YOUR_PDF_ID",
    "question": "What is the quadratic formula?",
    "student_mode": "average"
  }'
# Should return AI-generated answer
```

---

## Phase 13: Monitoring

### COST for Phase 13

| Item | Current Cost | Free Tier | Ongoing Cost |
|------|--------------|-----------|--------------|
| Cloud Logging (ingestion) | Rs.0 | 50 GB/month | Rs.0.50/GB after |
| Cloud Logging (storage) | Rs.0 | 30 days retention | Rs.0.01/GB/month after |
| Cloud Monitoring | Rs.0 | Basic metrics free | Rs.0 for most use cases |
| Alerting | Rs.0 | Unlimited policies | Rs.0 |
| Uptime Checks | Rs.0 | 100 checks free | Rs.0.30/check after |

**WARNING: Logging is a hidden cost trap!**

**Cost Reduction Alternatives**:
1. **Set log level to WARN/ERROR in production** - DEBUG logs can generate GBs of data
2. **Reduce log retention** - Default 30 days is often too long, set to 7 days
3. **Use structured logging** - Easier to filter, less storage
4. **Exclude health check logs** - These generate noise every 30 seconds
5. **Sample logs** - Log only 10% of requests in high-traffic scenarios

**Log Volume Estimation**:
| Log Level | Logs/Request | 1000 req/day | Monthly Volume |
|-----------|--------------|--------------|----------------|
| DEBUG | 50 lines | 50,000 | ~1.5 GB |
| INFO | 10 lines | 10,000 | ~300 MB |
| WARN | 2 lines | 2,000 | ~60 MB |
| ERROR | 0.1 lines | 100 | ~3 MB |

**Cost Example**:
| Configuration | Monthly Log Volume | Monthly Cost |
|---------------|-------------------|--------------|
| DEBUG level, 30 days | 1.5 GB | Rs.0 (within free) |
| DEBUG level, 30 days | 100 GB | Rs.25 |
| INFO level, 7 days | 300 MB | Rs.0 |

**When to Upgrade**: Free tier (50 GB/month) is sufficient for most apps. Only pay if you have high traffic or need long retention.

**Pro Tip**: Configure log exclusion for health checks:
```bash
# Exclude health check logs (saves ~30% of log volume)
gcloud logging sinks create exclude-health-checks \
  --log-filter='NOT resource.labels.service_name="cbse-learning-app" OR NOT textPayload:"/health"' \
  --destination=logging.googleapis.com/projects/$PROJECT_ID/locations/global/buckets/_Default
```

**Set log level in production**:
```python
# In config.py
import logging
logging.basicConfig(level=logging.WARN if APP_ENV == "production" else logging.DEBUG)
```

---

### Step 13.1: View Application Logs

#### WHAT
Monitor application logs for errors and performance.

#### WHY
Logs help debug issues and understand application behavior.

#### WHEN
Ongoing, especially after deployment.

#### WHERE
Cloud Run logs or Cloud Logging.

#### HOW

```bash
# View recent logs
gcloud run services logs read cbse-learning-app \
  --region=asia-south1 --limit=100

# Stream logs in real-time
gcloud run services logs tail cbse-learning-app \
  --region=asia-south1
```

**Console Monitoring**:
1. Go to: https://console.cloud.google.com/run
2. Click `cbse-learning-app`
3. View: Metrics, Logs, Revisions

---

### Step 13.2: Set Up Alerts

#### WHAT
Configure alerts for errors, high latency, and budget thresholds.

#### WHY
Proactive alerts help catch issues before users complain.

#### WHEN
After deployment is stable.

#### WHERE
Cloud Monitoring.

#### HOW

1. **Navigate to Alerting**
   - Go to: https://console.cloud.google.com/monitoring/alerting

2. **Create Policy**
   - Click "CREATE POLICY"
   - Add conditions:
     - Error rate > 1% for 5 minutes
     - Latency p95 > 5 seconds
     - Instance count > 2 (cost alert)

3. **Add Notifications**
   - Add email channel
   - Save policy

---

### Step 13.3: Check Billing

#### WHAT
Monitor spending against your budget.

#### WHY
Prevent unexpected charges.

#### WHEN
Weekly or when alerts trigger.

#### WHERE
GCP Billing Console.

#### HOW

```bash
# Check billing accounts
gcloud billing accounts list

# View project billing
gcloud billing projects describe $PROJECT_ID
```

**Console**:
- Go to: https://console.cloud.google.com/billing
- View current charges and forecasts

---

## Troubleshooting Reference

### Issue: Permission Denied Errors

#### WHAT
Authentication or authorization failures.

#### WHY
Token expired, wrong project, or missing permissions.

#### HOW to Fix
```bash
# Re-authenticate
gcloud auth login
gcloud auth configure-docker asia-south1-docker.pkg.dev

# Verify project
gcloud config set project cbse-learning-platform
gcloud config get-value project
```

---

### Issue: Docker Build Fails

#### WHAT
Container build errors.

#### WHY
Docker not running, missing dependencies, or syntax errors.

#### HOW to Fix
```bash
# Check Docker is running
docker info

# On Linux, ensure user is in docker group
sudo usermod -aG docker $USER
# Log out and back in

# Rebuild with no cache
docker build --no-cache -t IMAGE_NAME .
```

---

### Issue: Cloud Run Deployment Fails

#### WHAT
Deployment errors or service not starting.

#### WHY
Image issues, configuration errors, or resource limits.

#### HOW to Fix
```bash
# Check logs
gcloud run services logs read cbse-learning-app \
  --region=asia-south1 --limit=50

# Check service status
gcloud run services describe cbse-learning-app \
  --region=asia-south1

# Verify image exists
gcloud artifacts docker images list \
  asia-south1-docker.pkg.dev/$PROJECT_ID/cbse-app
```

---

### Issue: API Returns 500 Error

#### WHAT
Internal server errors from the application.

#### WHY
Missing environment variables, database connection issues, or code bugs.

#### HOW to Fix
1. Check application logs for stack trace
2. Verify all environment variables are set
3. Check if required APIs are enabled
4. Test with `AI_PROVIDER=mock` to isolate AI issues

---

### Issue: Firebase Authentication Not Working

#### WHAT
Users can't sign in or token verification fails.

#### WHY
Missing credentials, wrong project, or misconfigured Firebase.

#### HOW to Fix
1. Verify Firebase credentials in Secret Manager
2. Check Cloud Run has access to secret
3. Verify Firebase project is linked to GCP project
4. Check Firebase Console for auth errors

---

### Issue: Slow Response Times

#### WHAT
API requests taking too long.

#### WHY
Cold starts, insufficient resources, or slow AI responses.

#### HOW to Fix
```bash
# Option 1: Accept cold starts (free)
# First request after idle takes 2-5 seconds

# Option 2: Keep instance warm (~Rs.1500-3000/month)
gcloud run services update cbse-learning-app \
  --region=asia-south1 --min-instances=1

# Option 3: Increase resources
gcloud run services update cbse-learning-app \
  --region=asia-south1 --memory=1Gi --cpu=2
```

---

### Issue: Budget Exceeded

#### WHAT
Spending more than expected.

#### WHY
Too many instances, AI usage, or storage costs.

#### HOW to Fix
```bash
# Scale to zero when idle
gcloud run services update cbse-learning-app \
  --region=asia-south1 --min-instances=0

# Use mock AI provider
gcloud run services update cbse-learning-app \
  --region=asia-south1 --update-env-vars="AI_PROVIDER=mock"

# Delete unused resources
gcloud run services delete cbse-learning-app \
  --region=asia-south1 --quiet
```

---

## Quick Reference Commands

```bash
# View deployed services
gcloud run services list

# View service logs
gcloud run services logs read cbse-learning-app --region=asia-south1

# Update service with new image
gcloud run deploy cbse-learning-app \
  --image=asia-south1-docker.pkg.dev/$PROJECT_ID/cbse-app/backend:v2 \
  --region=asia-south1

# Check billing
gcloud billing accounts list

# Check project info
gcloud projects describe $PROJECT_ID

# Delete everything (if needed)
gcloud run services delete cbse-learning-app --region=asia-south1 --quiet
gcloud artifacts repositories delete cbse-app --location=asia-south1 --quiet
```

---

## Summary

This 4W+H guide covered 13 phases:

| Phase | WHAT | WHY | Time |
|-------|------|-----|------|
| 1 | Account Creation | Foundation for all services | 15 min |
| 2 | Project Setup | Isolate resources and billing | 10 min |
| 3 | Tool Installation | Enable CLI operations | 20 min |
| 4 | Repository Setup | Get source code | 5 min |
| 5 | Container Registry | Store Docker images | 10 min |
| 6 | Cloud Run Deployment | Host the application | 15 min |
| 7 | Firebase Setup | Authentication service | 15 min |
| 8 | Database Configuration | Data persistence | 10 min |
| 9 | Storage Setup | File storage | 10 min |
| 10 | AI Configuration | Enable AI features | 15 min |
| 11 | CI/CD Pipeline | Automate deployments | 15 min |
| 12 | Content Upload | Add CBSE content | 20 min |
| 13 | Monitoring | Track health and costs | 10 min |

**Total Time**: 2-4 hours

**Your CBSE Learning Platform is now live and ready for students!**

---

## Next Steps

1. **Share with students**: Distribute the Cloud Run URL
2. **Upload more content**: Add chapters for other subjects
3. **Customize branding**: Modify frontend for your school
4. **Scale as needed**: Increase resources when usage grows
5. **Collect feedback**: Iterate based on student input

---

## Getting Help

- **GCP Documentation**: https://cloud.google.com/docs
- **Cloud Run Guide**: https://cloud.google.com/run/docs
- **Firebase Docs**: https://firebase.google.com/docs
- **Replicate Docs**: https://replicate.com/docs
- **Stack Overflow**: https://stackoverflow.com/questions/tagged/google-cloud-platform

---

*This 4W+H guide was created for the CBSE Learning Platform project. Last updated: December 2024*
