# 📌 GCP Cloud Run Quick Reference

Quick commands and URLs for managing your Cloud Run deployment.

## 🚀 Common Commands

### Deploy Services
```bash
# Full deployment (all services)
cd deploy && ./deploy.sh YOUR_PROJECT_ID us-central1

# Quick deployment (alternative)
cd deploy && ./quick-deploy.sh YOUR_PROJECT_ID us-central1

# Deploy via Cloud Build
gcloud builds submit --config cloudbuild.yaml
```

### View Service URLs
```bash
# Get API URL
gcloud run services describe ai-data-cleaning-api \
  --region us-central1 \
  --format 'value(status.url)'

# Get MCP URL
gcloud run services describe ai-data-cleaning-mcp \
  --region us-central1 \
  --format 'value(status.url)'

# Get n8n URL
gcloud run services describe ai-data-cleaning-n8n \
  --region us-central1 \
  --format 'value(status.url)'

# Get all URLs
gcloud run services list --region us-central1 --format 'table(name,status.url)'
```

### Update Services
```bash
# Update API service
gcloud run deploy ai-data-cleaning-api \
  --source=. \
  --dockerfile=docker/Dockerfile \
  --region=us-central1

# Update environment variable
gcloud run services update ai-data-cleaning-api \
  --region=us-central1 \
  --update-env-vars="NEW_VAR=value"

# Update MCP URL in API
gcloud run services update ai-data-cleaning-api \
  --region=us-central1 \
  --update-env-vars="MCP_URL=https://your-mcp-url"
```

### Scale Services
```bash
# Scale API
gcloud run services update ai-data-cleaning-api \
  --region=us-central1 \
  --max-instances=20 \
  --min-instances=2

# Scale down to zero (dev only)
gcloud run services update ai-data-cleaning-api \
  --region=us-central1 \
  --min-instances=0
```

### View Logs
```bash
# Stream API logs
gcloud run logs tail ai-data-cleaning-api --region=us-central1

# View last 50 log entries
gcloud run logs read ai-data-cleaning-api --region=us-central1 --limit=50

# View logs with timestamp
gcloud run logs read ai-data-cleaning-api \
  --region=us-central1 \
  --format='table(timestamp,log)' \
  --limit=20

# Filter error logs
gcloud run logs read ai-data-cleaning-api \
  --region=us-central1 \
  --log-filter='severity>=ERROR' \
  --limit=50
```

### Service Management
```bash
# List all services
gcloud run services list --region=us-central1

# Describe service details
gcloud run services describe ai-data-cleaning-api \
  --region=us-central1

# Delete service
gcloud run services delete ai-data-cleaning-api \
  --region=us-central1 \
  --quiet
```

### Health Checks
```bash
# Check API health
curl https://YOUR-API-URL/health

# Check MCP health
curl https://YOUR-MCP-URL/health

# Test API endpoint
curl https://YOUR-API-URL/jobs

# Test with authentication
curl -H "Authorization: Bearer TOKEN" https://YOUR-API-URL/health
```

## 🔧 Service Configuration

### Resource Limits
```bash
# Update CPU and memory
gcloud run services update ai-data-cleaning-api \
  --region=us-central1 \
  --cpu=2 \
  --memory=2Gi

# Update timeout
gcloud run services update ai-data-cleaning-api \
  --region=us-central1 \
  --timeout=300
```

### Concurrency
```bash
# Set concurrent requests per instance
gcloud run services update ai-data-cleaning-api \
  --region=us-central1 \
  --concurrency=80
```

### Network
```bash
# Add VPC connector
gcloud run services update ai-data-cleaning-api \
  --region=us-central1 \
  --vpc-connector=my-connector

# Set ingress (all, internal, internal-and-cloud-load-balancing)
gcloud run services update ai-data-cleaning-api \
  --region=us-central1 \
  --ingress=all
```

## 🔐 Security Commands

### IAM Permissions
```bash
# Make service public (unauthenticated access)
gcloud run services add-iam-policy-binding ai-data-cleaning-api \
  --region=us-central1 \
  --member="allUsers" \
  --role="roles/run.invoker"

# Remove public access
gcloud run services remove-iam-policy-binding ai-data-cleaning-api \
  --region=us-central1 \
  --member="allUsers" \
  --role="roles/run.invoker"

# Grant access to service account
gcloud run services add-iam-policy-binding ai-data-cleaning-api \
  --region=us-central1 \
  --member="serviceAccount:SA_EMAIL" \
  --role="roles/run.invoker"
```

### Secrets Management
```bash
# Create secret
gcloud secrets create api-key --data-file=./api-key.txt

# Update service with secret
gcloud run services update ai-data-cleaning-api \
  --region=us-central1 \
  --update-secrets=API_KEY=api-key:latest

# Mount secret as volume
gcloud run services update ai-data-cleaning-api \
  --region=us-central1 \
  --update-secrets=/secrets/api-key=api-key:latest
```

## 🗄️ Database Commands

### Cloud SQL
```bash
# Create instance
gcloud sql instances create ai-data-cleaning-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=us-central1

# Create database
gcloud sql databases create datacleaning \
  --instance=ai-data-cleaning-db

# Connect service to Cloud SQL
gcloud run services update ai-data-cleaning-api \
  --region=us-central1 \
  --add-cloudsql-instances=PROJECT:REGION:INSTANCE

# Get connection name
gcloud sql instances describe ai-data-cleaning-db \
  --format='value(connectionName)'
```

## 💾 Storage Commands

### Cloud Storage
```bash
# Create bucket
gsutil mb -l us-central1 gs://ai-data-cleaning-files

# Grant service access
gsutil iam ch serviceAccount:SA_EMAIL:objectAdmin \
  gs://ai-data-cleaning-files

# List buckets
gsutil ls

# View bucket details
gsutil ls -L gs://ai-data-cleaning-files
```

## 📊 Monitoring Commands

### Metrics
```bash
# View request count
gcloud monitoring time-series list \
  --filter='metric.type="run.googleapis.com/request_count"' \
  --format=json

# View billable instance time
gcloud monitoring time-series list \
  --filter='metric.type="run.googleapis.com/container/billable_instance_time"' \
  --format=json
```

### Alerts
```bash
# List alert policies
gcloud alpha monitoring policies list

# Create alert policy (use Cloud Console for easier setup)
```

## 🔄 Rollback Commands

### Revert to Previous Revision
```bash
# List revisions
gcloud run revisions list \
  --service=ai-data-cleaning-api \
  --region=us-central1

# Update traffic to previous revision
gcloud run services update-traffic ai-data-cleaning-api \
  --region=us-central1 \
  --to-revisions=REVISION_NAME=100

# Gradual rollout (canary deployment)
gcloud run services update-traffic ai-data-cleaning-api \
  --region=us-central1 \
  --to-revisions=new-revision=20,old-revision=80
```

## 🧹 Cleanup Commands

### Delete Services
```bash
# Delete all services
gcloud run services delete ai-data-cleaning-api --region=us-central1 --quiet
gcloud run services delete ai-data-cleaning-mcp --region=us-central1 --quiet
gcloud run services delete ai-data-cleaning-n8n --region=us-central1 --quiet
```

### Delete Images
```bash
# List images
gcloud container images list --repository=gcr.io/PROJECT_ID

# Delete image
gcloud container images delete gcr.io/PROJECT_ID/ai-data-cleaning-api:latest --quiet

# Delete all tags of an image
gcloud container images delete gcr.io/PROJECT_ID/ai-data-cleaning-api --quiet
```

### Delete Old Revisions
```bash
# List revisions
gcloud run revisions list --service=ai-data-cleaning-api --region=us-central1

# Delete specific revision
gcloud run revisions delete REVISION_NAME --region=us-central1 --quiet

# Delete all revisions except active ones (use script)
```

## 🐛 Troubleshooting Commands

### Debug Service
```bash
# Get service details
gcloud run services describe ai-data-cleaning-api \
  --region=us-central1 \
  --format=yaml

# Get latest revision
gcloud run revisions describe \
  $(gcloud run services describe ai-data-cleaning-api \
    --region=us-central1 \
    --format='value(status.latestReadyRevisionName)') \
  --region=us-central1

# Check conditions
gcloud run services describe ai-data-cleaning-api \
  --region=us-central1 \
  --format='value(status.conditions)'
```

### Test Connectivity
```bash
# Test from Cloud Shell
curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
  https://YOUR-SERVICE-URL/health

# Test with verbose output
curl -v https://YOUR-SERVICE-URL/health
```

## 💰 Cost Commands

### View Billing
```bash
# Requires billing API enabled and appropriate permissions
gcloud billing projects describe PROJECT_ID

# Export to BigQuery for detailed analysis
# (Set up in Cloud Console: Billing > Billing Export)
```

## 🔗 Useful URLs

### Cloud Console URLs
- **Cloud Run**: https://console.cloud.google.com/run
- **Cloud Build**: https://console.cloud.google.com/cloud-build
- **Logs**: https://console.cloud.google.com/logs
- **Monitoring**: https://console.cloud.google.com/monitoring
- **IAM**: https://console.cloud.google.com/iam-admin
- **Secret Manager**: https://console.cloud.google.com/security/secret-manager

### Documentation
- **Cloud Run Docs**: https://cloud.google.com/run/docs
- **gcloud Reference**: https://cloud.google.com/sdk/gcloud/reference/run
- **Pricing**: https://cloud.google.com/run/pricing

## 📝 Environment Variables Reference

### API Service
- `MCP_URL` - URL of MCP service
- `DATABASE_URL` - Database connection string
- `PORT` - Service port (set by Cloud Run)
- `ENVIRONMENT` - Environment name

### MCP Service
- `PORT` - Service port (set by Cloud Run)

### n8n Service
- `N8N_BASIC_AUTH_ACTIVE` - Enable basic auth
- `N8N_BASIC_AUTH_USER` - Username
- `N8N_BASIC_AUTH_PASSWORD` - Password
- `N8N_HOST` - Host binding
- `N8N_PORT` - Port number
- `N8N_PROTOCOL` - Protocol (http/https)

## 🎯 Quick Start Workflow

1. **Initial setup**: `gcloud auth login && gcloud config set project PROJECT_ID`
2. **Deploy**: `cd deploy && ./deploy.sh PROJECT_ID us-central1`
3. **Get URLs**: `gcloud run services list --region us-central1`
4. **Test**: `curl https://API-URL/health`
5. **Monitor**: `gcloud run logs tail ai-data-cleaning-api --region us-central1`

---

💡 **Tip**: Save commonly used commands as shell aliases:
```bash
alias gcr='gcloud run'
alias gcrls='gcloud run services list --region us-central1'
alias gcrlogs='gcloud run logs tail'
```
