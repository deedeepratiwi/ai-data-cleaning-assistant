#!/bin/bash
# Deploy AI Data Cleaning Assistant to Google Cloud Run
# Usage: ./deploy.sh [PROJECT_ID] [REGION]

set -e

PROJECT_ID=${1:-"your-gcp-project-id"}
REGION=${2:-"us-central1"}

echo "🚀 Deploying AI Data Cleaning Assistant to GCP Cloud Run"
echo "Project ID: $PROJECT_ID"
echo "Region: $REGION"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Error: gcloud CLI is not installed. Please install it first."
    echo "Visit: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Set the project
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "📦 Enabling required GCP APIs..."
gcloud services enable \
    cloudbuild.googleapis.com \
    run.googleapis.com \
    containerregistry.googleapis.com \
    artifactregistry.googleapis.com

# Build and push images using Cloud Build
echo "🔨 Building and deploying services using Cloud Build..."
# Get git commit SHA for image tagging
SHORT_SHA=$(git rev-parse --short HEAD 2>/dev/null || echo "latest")
echo "Using image tag: $SHORT_SHA"

gcloud builds submit \
    --config cloudbuild.yaml \
    --substitutions=_REGION=$REGION,SHORT_SHA=$SHORT_SHA \
    .

# Get service URLs
echo ""
echo "✅ Deployment complete!"
echo ""
echo "📋 Service URLs:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

API_URL=$(gcloud run services describe ai-data-cleaning-api --region $REGION --format 'value(status.url)')
MCP_URL=$(gcloud run services describe ai-data-cleaning-mcp --region $REGION --format 'value(status.url)')
N8N_URL=$(gcloud run services describe ai-data-cleaning-n8n --region $REGION --format 'value(status.url)')

echo "🌐 API Service:  $API_URL"
echo "🔧 MCP Service:  $MCP_URL"
echo "⚡ n8n Service:  $N8N_URL"
echo ""
echo "📝 Note: n8n credentials are admin/admin (change in production)"
echo ""
echo "🔍 View logs with:"
echo "  gcloud run logs read ai-data-cleaning-api --region $REGION --limit 50"
echo "  gcloud run logs read ai-data-cleaning-mcp --region $REGION --limit 50"
echo "  gcloud run logs read ai-data-cleaning-n8n --region $REGION --limit 50"
