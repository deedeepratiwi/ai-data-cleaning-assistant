# 🚀 Deployment Checklist

Use this checklist to ensure a successful deployment to GCP Cloud Run.

## 📋 Pre-Deployment

### GCP Account Setup
- [ ] Google Cloud account created with billing enabled
- [ ] GCP project created
- [ ] Project ID noted and saved
- [ ] gcloud CLI installed and authenticated
- [ ] Appropriate IAM permissions granted (Cloud Run Admin, Cloud Build Editor, Storage Admin)

### Required APIs
- [ ] Cloud Run API enabled
- [ ] Cloud Build API enabled
- [ ] Container Registry API enabled
- [ ] Artifact Registry API enabled
- [ ] Cloud SQL Admin API enabled (if using Cloud SQL)
- [ ] Secret Manager API enabled (if using secrets)

### Code Preparation
- [ ] All code changes committed to Git
- [ ] Tests passing locally
- [ ] Dockerfiles tested locally
- [ ] Environment variables documented
- [ ] Secrets prepared (API keys, passwords, etc.)

## 🔧 Configuration

### Environment Variables
- [ ] `.env.example` reviewed
- [ ] Production environment variables prepared
- [ ] Database URL configured
- [ ] MCP_URL will be set automatically (verify after deployment)
- [ ] n8n credentials changed from defaults
- [ ] CORS origins configured if needed

### Security
- [ ] n8n password changed from default (admin/admin)
- [ ] API authentication configured (if required)
- [ ] Secrets stored in Secret Manager (not in code)
- [ ] Service accounts configured with least privilege
- [ ] IAM policies reviewed

### Database
- [ ] Decide: SQLite (development) or Cloud SQL (production)
- [ ] If Cloud SQL: Instance created and configured
- [ ] If Cloud SQL: Database created
- [ ] If Cloud SQL: Connection name noted
- [ ] Database initialization script prepared

### Storage
- [ ] Decide: Local storage or Cloud Storage
- [ ] If Cloud Storage: Bucket created
- [ ] If Cloud Storage: Bucket permissions configured
- [ ] File upload size limits configured

## 🚀 Deployment

### Initial Deployment
- [ ] Clone repository to local machine
- [ ] Navigate to project root directory
- [ ] Run deployment script: `cd deploy && ./deploy.sh PROJECT_ID REGION`
- [ ] Monitor deployment progress in terminal
- [ ] Check for any errors in output

### Verify Deployment
- [ ] All three services deployed successfully
- [ ] Service URLs obtained and noted
- [ ] API health endpoint responds: `curl https://API-URL/health`
- [ ] MCP health endpoint responds: `curl https://MCP-URL/health`
- [ ] n8n interface accessible: `https://N8N-URL`

### Configuration Updates
- [ ] API service has correct MCP_URL
- [ ] Test API → MCP communication
- [ ] Update application URLs in documentation
- [ ] Update service URLs in client applications

## ✅ Post-Deployment

### Testing
- [ ] Health endpoints return 200 OK
- [ ] Upload test CSV file via API
- [ ] Verify data cleaning pipeline works
- [ ] Download cleaned file
- [ ] Check cleaning report generation
- [ ] Test n8n workflows (if applicable)
- [ ] Verify error handling and logging

### Monitoring Setup
- [ ] Cloud Monitoring configured
- [ ] Log queries created
- [ ] Alert policies created:
  - [ ] High error rate alert
  - [ ] High latency alert
  - [ ] CPU/memory threshold alerts
  - [ ] Cost threshold alerts
- [ ] Uptime checks configured

### Performance
- [ ] Load test performed (optional but recommended)
- [ ] Response times acceptable
- [ ] Auto-scaling tested
- [ ] Cold start times acceptable
- [ ] Concurrency settings optimized

### Documentation
- [ ] Service URLs documented
- [ ] API documentation updated
- [ ] Deployment runbook created
- [ ] Incident response procedures documented
- [ ] Rollback procedures documented

### Security Hardening
- [ ] Remove `--allow-unauthenticated` if authentication required
- [ ] Configure VPC connector (for private services)
- [ ] Enable Cloud Armor (for DDoS protection)
- [ ] Review and restrict service account permissions
- [ ] Configure secrets in Secret Manager
- [ ] Enable audit logging

### Cost Management
- [ ] Budget alerts configured
- [ ] Cost allocation labels added
- [ ] Resource limits reviewed
- [ ] Auto-scaling limits appropriate
- [ ] min-instances set appropriately (0 for dev, >0 for prod)

## 🔄 CI/CD Setup

### GitHub Actions
- [ ] GitHub repository connected
- [ ] Service account key created for GitHub Actions
- [ ] `GCP_SA_KEY` secret added to GitHub
- [ ] `GCP_PROJECT_ID` secret added to GitHub
- [ ] `.github/workflows/deploy-gcp.yml` configured
- [ ] Test deployment workflow
- [ ] Branch protection rules configured

### Workflow Testing
- [ ] Push to main branch triggers deployment
- [ ] Deployment succeeds
- [ ] Automated health checks pass
- [ ] Rollback works if deployment fails

## 🗄️ Production Database (Optional)

If using Cloud SQL:
- [ ] Cloud SQL instance created
- [ ] Database created
- [ ] User accounts created
- [ ] Passwords stored in Secret Manager
- [ ] Connection name configured in API service
- [ ] Database migrations run
- [ ] Backup schedule configured
- [ ] Point-in-time recovery enabled

## 📦 Production Storage (Optional)

If using Cloud Storage:
- [ ] Storage bucket created
- [ ] Bucket permissions configured
- [ ] Lifecycle policies configured
- [ ] CORS configuration added (if needed)
- [ ] Signed URLs configured (for private files)
- [ ] Application code updated to use GCS

## 🌐 Custom Domain (Optional)

- [ ] Domain name purchased
- [ ] Domain mapping created in Cloud Run
- [ ] DNS records configured
- [ ] SSL certificate verified
- [ ] Domain verified in Cloud Run
- [ ] Old URLs redirected to new domain

## 📱 Monitoring Dashboard

- [ ] Custom dashboard created in Cloud Monitoring
- [ ] Key metrics added:
  - [ ] Request count
  - [ ] Error rate
  - [ ] Response time (p50, p95, p99)
  - [ ] CPU utilization
  - [ ] Memory utilization
  - [ ] Active instances
  - [ ] Cold starts
- [ ] Dashboard shared with team

## 🔔 Stakeholder Communication

- [ ] Deployment completed notification sent
- [ ] Service URLs shared
- [ ] Known issues documented
- [ ] Support channels established
- [ ] Feedback mechanism created

## 📝 Final Verification

- [ ] All services running
- [ ] All tests passing
- [ ] Monitoring working
- [ ] Logs accessible
- [ ] Backups configured
- [ ] Documentation complete
- [ ] Team trained on new deployment

## 🎉 Deployment Complete!

Once all items are checked:
- [ ] Mark deployment as successful
- [ ] Update status page (if applicable)
- [ ] Celebrate! 🎊

---

## 📞 Support Resources

- **GCP Documentation**: https://cloud.google.com/run/docs
- **Troubleshooting Guide**: See `deploy/GCP_DEPLOYMENT.md`
- **GitHub Issues**: Report problems in repository
- **Team Contact**: [Add your team contact info]

---

## 🔄 Regular Maintenance

After deployment, schedule:
- [ ] Weekly: Review logs and metrics
- [ ] Monthly: Review costs and optimize
- [ ] Quarterly: Update dependencies
- [ ] Yearly: Review and update security policies
