# 🚀 GCP Cloud Run Deployment Guide

This guide explains how to deploy the AI Data Cleaning Assistant to Google Cloud Platform using Cloud Run.

## 📋 Architecture Overview

The application consists of three services deployed on Cloud Run:

1. **FastAPI Service** (`ai-data-cleaning-api`) - Main backend API
   - Port: 8000
   - Resources: 2 CPU, 2GB RAM
   - Auto-scaling: 1-10 instances

2. **MCP Service** (`ai-data-cleaning-mcp`) - Model Context Protocol server
   - Port: 9000
   - Resources: 1 CPU, 1GB RAM
   - Auto-scaling: 1-5 instances

3. **n8n Service** (`ai-data-cleaning-n8n`) - Workflow automation
   - Port: 5678
   - Resources: 1 CPU, 1GB RAM
   - Auto-scaling: 1-3 instances

## 🔧 Prerequisites

1. **Google Cloud Account** with billing enabled
2. **gcloud CLI** installed ([Installation Guide](https://cloud.google.com/sdk/docs/install))
3. **Docker** installed (optional, for local testing)
4. **GCP Project** created

## 📦 Initial Setup

### 1. Install gcloud CLI

```bash
# macOS
brew install --cask google-cloud-sdk

# Linux
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Windows
# Download installer from https://cloud.google.com/sdk/docs/install
```

### 2. Authenticate and Set Project

```bash
# Login to your Google account
gcloud auth login

# Set your project
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable \
    cloudbuild.googleapis.com \
    run.googleapis.com \
    containerregistry.googleapis.com \
    artifactregistry.googleapis.com
```

## 🚀 Deployment Options

### Option 1: Automated Deployment (Recommended)

Uses Cloud Build to build and deploy all services:

```bash
# Deploy using the deployment script
cd deploy
./deploy.sh YOUR_PROJECT_ID us-central1
```

This script will:
- Build Docker images for FastAPI and MCP services
- Deploy all three services to Cloud Run
- Configure service-to-service communication
- Output the service URLs

### Option 2: Quick Manual Deployment

Uses gcloud's built-in build functionality:

```bash
cd deploy
./quick-deploy.sh YOUR_PROJECT_ID us-central1
```

### Option 3: Step-by-Step Manual Deployment

#### Step 1: Deploy MCP Service

```bash
gcloud run deploy ai-data-cleaning-mcp \
    --source=. \
    --dockerfile=mcp/Dockerfile \
    --region=us-central1 \
    --allow-unauthenticated \
    --port=9000 \
    --cpu=1 \
    --memory=1Gi \
    --max-instances=5 \
    --min-instances=1
```

#### Step 2: Get MCP URL

```bash
MCP_URL=$(gcloud run services describe ai-data-cleaning-mcp \
    --region=us-central1 \
    --format='value(status.url)')
echo "MCP URL: $MCP_URL"
```

#### Step 3: Deploy n8n Service

```bash
gcloud run deploy ai-data-cleaning-n8n \
    --image=n8nio/n8n:latest \
    --region=us-central1 \
    --allow-unauthenticated \
    --port=5678 \
    --cpu=1 \
    --memory=1Gi \
    --max-instances=3 \
    --min-instances=1 \
    --set-env-vars="N8N_BASIC_AUTH_ACTIVE=true,N8N_BASIC_AUTH_USER=admin,N8N_BASIC_AUTH_PASSWORD=admin,N8N_HOST=0.0.0.0,N8N_PORT=5678,N8N_PROTOCOL=https"
```

#### Step 4: Deploy FastAPI Service

```bash
gcloud run deploy ai-data-cleaning-api \
    --source=. \
    --dockerfile=docker/Dockerfile \
    --region=us-central1 \
    --allow-unauthenticated \
    --port=8000 \
    --cpu=2 \
    --memory=2Gi \
    --max-instances=10 \
    --min-instances=1 \
    --set-env-vars="MCP_URL=$MCP_URL,DATABASE_URL=sqlite:///./data.db"
```

## 🔐 Security Considerations

### Production Checklist

- [ ] **Change n8n credentials** - Default is admin/admin
- [ ] **Enable authentication** - Consider Cloud IAM or API keys
- [ ] **Use Cloud SQL** - Instead of SQLite for production
- [ ] **Add Cloud Storage** - For persistent file storage
- [ ] **Configure VPC** - For service-to-service security
- [ ] **Set up secrets** - Use Secret Manager for sensitive data
- [ ] **Enable Cloud Armor** - For DDoS protection
- [ ] **Configure domain** - Use custom domain with SSL

### Secure n8n Credentials

```bash
# Update n8n with secure credentials
gcloud run services update ai-data-cleaning-n8n \
    --region=us-central1 \
    --update-env-vars="N8N_BASIC_AUTH_PASSWORD=your-secure-password"
```

### Restrict Access

```bash
# Remove public access (require authentication)
gcloud run services remove-iam-policy-binding ai-data-cleaning-api \
    --member="allUsers" \
    --role="roles/run.invoker" \
    --region=us-central1
```

## 🗄️ Production Database Setup

For production, use Cloud SQL instead of SQLite:

### 1. Create Cloud SQL Instance

```bash
gcloud sql instances create ai-data-cleaning-db \
    --database-version=POSTGRES_15 \
    --tier=db-f1-micro \
    --region=us-central1
```

### 2. Create Database

```bash
gcloud sql databases create datacleaning \
    --instance=ai-data-cleaning-db
```

### 3. Update API Service

```bash
# Get Cloud SQL connection name
CONNECTION_NAME=$(gcloud sql instances describe ai-data-cleaning-db \
    --format='value(connectionName)')

# Update API service to use Cloud SQL
gcloud run services update ai-data-cleaning-api \
    --region=us-central1 \
    --add-cloudsql-instances=$CONNECTION_NAME \
    --update-env-vars="DATABASE_URL=postgresql://user:pass@/datacleaning?host=/cloudsql/$CONNECTION_NAME"
```

## 💾 Persistent Storage with Cloud Storage

For file uploads and downloads:

### 1. Create Storage Bucket

```bash
gsutil mb -l us-central1 gs://ai-data-cleaning-files
```

### 2. Grant Service Account Access

```bash
# Get service account email
SA_EMAIL=$(gcloud run services describe ai-data-cleaning-api \
    --region=us-central1 \
    --format='value(spec.template.spec.serviceAccountName)')

# Grant storage access
gsutil iam ch serviceAccount:$SA_EMAIL:objectAdmin \
    gs://ai-data-cleaning-files
```

### 3. Update Application Code

Update your application to use Cloud Storage for file operations instead of local filesystem.

## 📊 Monitoring and Logging

### View Logs

```bash
# View API logs
gcloud run logs read ai-data-cleaning-api --region=us-central1 --limit=50

# Stream logs in real-time
gcloud run logs tail ai-data-cleaning-api --region=us-central1

# View MCP logs
gcloud run logs read ai-data-cleaning-mcp --region=us-central1 --limit=50

# View n8n logs
gcloud run logs read ai-data-cleaning-n8n --region=us-central1 --limit=50
```

### Monitor Performance

```bash
# View service metrics in Cloud Console
gcloud run services describe ai-data-cleaning-api \
    --region=us-central1 \
    --format=yaml
```

### Set Up Alerts

Create alerting policies in Cloud Monitoring for:
- High error rates
- Slow response times
- CPU/memory usage
- Request counts

## 🔄 CI/CD Integration

### GitHub Actions Deployment

Create `.github/workflows/deploy-gcp.yml`:

```yaml
name: Deploy to GCP Cloud Run

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - id: auth
        uses: google-github-actions/auth@v1
        with:
          credentials_json: ${{ secrets.GCP_SA_KEY }}
      
      - name: Deploy to Cloud Run
        run: |
          gcloud builds submit --config cloudbuild.yaml
```

### Required Secrets

Add to GitHub repository secrets:
- `GCP_SA_KEY` - Service account JSON key with Cloud Run and Cloud Build permissions

## 🌐 Custom Domain Setup

### 1. Map Domain

```bash
gcloud run domain-mappings create \
    --service=ai-data-cleaning-api \
    --domain=api.yourdomain.com \
    --region=us-central1
```

### 2. Configure DNS

Add the DNS records shown by the previous command to your domain registrar.

## 💰 Cost Optimization

### Set Budget Alerts

```bash
# Create budget in Cloud Console
# Billing -> Budgets & alerts
```

### Optimize Resource Allocation

- Use `--min-instances=0` for dev environments
- Adjust CPU and memory based on actual usage
- Use `--concurrency` to handle more requests per instance
- Set appropriate timeout values

### Example Cost-Optimized Configuration

```bash
gcloud run deploy ai-data-cleaning-api \
    --region=us-central1 \
    --min-instances=0 \
    --max-instances=5 \
    --cpu=1 \
    --memory=512Mi \
    --concurrency=80 \
    --timeout=60
```

## 🐛 Troubleshooting

### Check Service Status

```bash
gcloud run services list --region=us-central1
```

### View Service Details

```bash
gcloud run services describe ai-data-cleaning-api --region=us-central1
```

### Common Issues

1. **Build Failures**
   - Check `cloudbuild.yaml` syntax
   - Verify Dockerfile paths
   - Check build logs: `gcloud builds log <BUILD_ID>`

2. **Service Not Responding**
   - Verify PORT environment variable
   - Check health endpoint: `curl https://SERVICE-URL/health`
   - Review logs for errors

3. **Permission Denied**
   - Ensure APIs are enabled
   - Check IAM permissions
   - Verify service account has required roles

4. **Database Connection Issues**
   - Verify Cloud SQL connection name
   - Check DATABASE_URL format
   - Ensure Cloud SQL Admin API is enabled

## 🔧 Update Existing Deployments

### Update API Service

```bash
gcloud run deploy ai-data-cleaning-api \
    --region=us-central1 \
    --source=. \
    --dockerfile=docker/Dockerfile
```

### Update Environment Variables

```bash
gcloud run services update ai-data-cleaning-api \
    --region=us-central1 \
    --update-env-vars="NEW_VAR=value"
```

### Scale Service

```bash
gcloud run services update ai-data-cleaning-api \
    --region=us-central1 \
    --max-instances=20 \
    --min-instances=2
```

## 🗑️ Clean Up Resources

### Delete Services

```bash
gcloud run services delete ai-data-cleaning-api --region=us-central1 --quiet
gcloud run services delete ai-data-cleaning-mcp --region=us-central1 --quiet
gcloud run services delete ai-data-cleaning-n8n --region=us-central1 --quiet
```

### Delete Images

```bash
gcloud container images delete gcr.io/PROJECT_ID/ai-data-cleaning-api --quiet
gcloud container images delete gcr.io/PROJECT_ID/ai-data-cleaning-mcp --quiet
```

## 📚 Additional Resources

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud Build Documentation](https://cloud.google.com/build/docs)
- [Cloud SQL Documentation](https://cloud.google.com/sql/docs)
- [Cloud Storage Documentation](https://cloud.google.com/storage/docs)
- [n8n Documentation](https://docs.n8n.io)

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review Cloud Run logs
3. Open an issue on GitHub
4. Consult GCP documentation
