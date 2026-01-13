# 📦 Deployment Resources

This directory contains all resources needed to deploy the AI Data Cleaning Assistant to Google Cloud Platform (GCP) using Cloud Run.

## 📁 Contents

### Configuration Files

- **`cloudrun-api.yaml`** - Cloud Run service configuration for FastAPI service
- **`cloudrun-mcp.yaml`** - Cloud Run service configuration for MCP service  
- **`cloudrun-n8n.yaml`** - Cloud Run service configuration for n8n service

### Deployment Scripts

- **`deploy.sh`** - Full automated deployment using Cloud Build (recommended)
- **`quick-deploy.sh`** - Quick deployment using gcloud's built-in build

### Documentation

- **`GCP_DEPLOYMENT.md`** - Comprehensive deployment guide with step-by-step instructions
- **`DEPLOYMENT_CHECKLIST.md`** - Complete checklist for production deployment
- **`QUICK_REFERENCE.md`** - Quick reference for common gcloud commands

## 🚀 Quick Start

### Prerequisites

1. **Install gcloud CLI**: https://cloud.google.com/sdk/docs/install
2. **Authenticate**: `gcloud auth login`
3. **Set project**: `gcloud config set project YOUR_PROJECT_ID`

### Deploy All Services

```bash
# From project root
cd deploy
./deploy.sh YOUR_PROJECT_ID us-central1
```

This will:
- Build Docker images for FastAPI and MCP services
- Deploy all three services to Cloud Run
- Configure service-to-service communication
- Output service URLs

## 📚 Documentation

### For First-Time Deployment
Start with **`GCP_DEPLOYMENT.md`** for detailed step-by-step instructions.

### For Production Deployment
Follow **`DEPLOYMENT_CHECKLIST.md`** to ensure nothing is missed.

### For Daily Operations
Use **`QUICK_REFERENCE.md`** for common commands and troubleshooting.

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         Google Cloud Platform           │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │   Cloud Run Services            │   │
│  │                                 │   │
│  │  ┌─────────────────────────┐   │   │
│  │  │  ai-data-cleaning-api   │   │   │
│  │  │  (FastAPI - Port 8000)  │◄──┼───┼── HTTPS Requests
│  │  └──────────┬──────────────┘   │   │
│  │             │                   │   │
│  │             ▼                   │   │
│  │  ┌─────────────────────────┐   │   │
│  │  │  ai-data-cleaning-mcp   │   │   │
│  │  │  (MCP - Port 9000)      │   │   │
│  │  └─────────────────────────┘   │   │
│  │                                 │   │
│  │  ┌─────────────────────────┐   │   │
│  │  │  ai-data-cleaning-n8n   │   │   │
│  │  │  (n8n - Port 5678)      │   │   │
│  │  └─────────────────────────┘   │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │   Cloud Build (CI/CD)           │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │   Container Registry (GCR)      │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

## 🔧 Service Details

### FastAPI Service (`ai-data-cleaning-api`)
- **Purpose**: Main backend API
- **Port**: 8000
- **Resources**: 2 CPU, 2GB RAM
- **Scaling**: 1-10 instances

### MCP Service (`ai-data-cleaning-mcp`)
- **Purpose**: Model Context Protocol server
- **Port**: 9000
- **Resources**: 1 CPU, 1GB RAM
- **Scaling**: 1-5 instances

### n8n Service (`ai-data-cleaning-n8n`)
- **Purpose**: Workflow automation
- **Port**: 5678
- **Resources**: 1 CPU, 1GB RAM
- **Scaling**: 1-3 instances

## 🔐 Security Notes

### Default Credentials
- **n8n**: admin/admin (⚠️ **CHANGE IN PRODUCTION**)

### Production Security Checklist
- [ ] Change n8n credentials
- [ ] Enable Cloud IAM authentication
- [ ] Use Secret Manager for sensitive data
- [ ] Configure VPC for service isolation
- [ ] Enable Cloud Armor for DDoS protection
- [ ] Set up audit logging

See `DEPLOYMENT_CHECKLIST.md` for complete security checklist.

## 🔄 CI/CD

Automated deployment via GitHub Actions is configured in:
```
.github/workflows/deploy-gcp.yml
```

Required GitHub secrets:
- `GCP_SA_KEY` - Service account JSON key
- `GCP_PROJECT_ID` - Your GCP project ID

## 💰 Cost Estimation

**Development** (minimal usage):
- ~$5-15/month with min-instances=0

**Production** (moderate traffic):
- ~$30-100/month with min-instances=1

**High Traffic**:
- Scales with usage, monitor via Cloud Console

Set up budget alerts in GCP Console to track spending.

## 🆘 Troubleshooting

### Common Issues

1. **Build Failures**
   - Check Dockerfile syntax
   - Verify all files are committed
   - Review Cloud Build logs

2. **Deployment Fails**
   - Ensure APIs are enabled
   - Check IAM permissions
   - Verify PROJECT_ID is correct

3. **Service Not Responding**
   - Check health endpoint: `curl https://SERVICE-URL/health`
   - Review logs: `gcloud run logs read SERVICE-NAME --region REGION`
   - Verify PORT environment variable

### Get Help

See the troubleshooting section in `GCP_DEPLOYMENT.md` for detailed solutions.

## 📞 Support

- **Documentation**: See files in this directory
- **GCP Support**: https://cloud.google.com/support
- **GitHub Issues**: Report bugs in the repository

## 🔗 Useful Links

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud Build Documentation](https://cloud.google.com/build/docs)
- [gcloud CLI Reference](https://cloud.google.com/sdk/gcloud/reference/run)
- [n8n Documentation](https://docs.n8n.io)

---

**Last Updated**: 2026-01-13

For questions or issues, please open a GitHub issue or consult the deployment documentation.
