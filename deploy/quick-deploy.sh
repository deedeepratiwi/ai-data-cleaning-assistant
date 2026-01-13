#!/bin/bash
# Quick deployment script using gcloud directly (without Cloud Build)
# Usage: ./quick-deploy.sh [PROJECT_ID] [REGION]

set -e

PROJECT_ID=${1:-"your-gcp-project-id"}
REGION=${2:-"us-central1"}

# Generate a random password for n8n or use environment variable
N8N_PASSWORD=${N8N_PASSWORD:-"admin"}

echo "🚀 Quick deploying to GCP Cloud Run"
echo ""
if [ "$N8N_PASSWORD" = "admin" ]; then
    echo "⚠️  WARNING: Using default n8n password 'admin'"
    echo "⚠️  For production, set N8N_PASSWORD environment variable:"
    echo "    export N8N_PASSWORD='your-secure-password'"
    echo "    or pass it via: N8N_PASSWORD='your-password' ./quick-deploy.sh"
    echo ""
fi

# Step 1: Deploy MCP service
echo "📦 Deploying MCP service..."
gcloud run deploy ai-data-cleaning-mcp \
    --source=. \
    --dockerfile=mcp/Dockerfile \
    --region=$REGION \
    --project=$PROJECT_ID \
    --allow-unauthenticated \
    --port=9000 \
    --cpu=1 \
    --memory=1Gi \
    --max-instances=5 \
    --min-instances=1 \
    --timeout=300

# Get MCP URL
MCP_URL=$(gcloud run services describe ai-data-cleaning-mcp \
    --region=$REGION \
    --project=$PROJECT_ID \
    --format='value(status.url)')

echo "✅ MCP deployed at: $MCP_URL"

# Step 2: Deploy n8n service
echo "📦 Deploying n8n service..."
gcloud run deploy ai-data-cleaning-n8n \
    --image=n8nio/n8n:latest \
    --region=$REGION \
    --project=$PROJECT_ID \
    --allow-unauthenticated \
    --port=5678 \
    --cpu=1 \
    --memory=1Gi \
    --max-instances=3 \
    --min-instances=1 \
    --timeout=300 \
    --set-env-vars="N8N_BASIC_AUTH_ACTIVE=true,N8N_BASIC_AUTH_USER=admin,N8N_BASIC_AUTH_PASSWORD=$N8N_PASSWORD,N8N_HOST=0.0.0.0,N8N_PORT=5678,N8N_PROTOCOL=https"

N8N_URL=$(gcloud run services describe ai-data-cleaning-n8n \
    --region=$REGION \
    --project=$PROJECT_ID \
    --format='value(status.url)')

echo "✅ n8n deployed at: $N8N_URL"

# Step 3: Deploy FastAPI service
echo "📦 Deploying FastAPI service..."
gcloud run deploy ai-data-cleaning-api \
    --source=. \
    --dockerfile=docker/Dockerfile \
    --region=$REGION \
    --project=$PROJECT_ID \
    --allow-unauthenticated \
    --port=8000 \
    --cpu=2 \
    --memory=2Gi \
    --max-instances=10 \
    --min-instances=1 \
    --timeout=300 \
    --set-env-vars="MCP_URL=$MCP_URL,DATABASE_URL=sqlite:///./data.db"

API_URL=$(gcloud run services describe ai-data-cleaning-api \
    --region=$REGION \
    --project=$PROJECT_ID \
    --format='value(status.url)')

echo ""
echo "✅ All services deployed successfully!"
echo ""
echo "📋 Service URLs:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🌐 API Service:  $API_URL"
echo "🔧 MCP Service:  $MCP_URL"
echo "⚡ n8n Service:  $N8N_URL"
echo ""
if [ "$N8N_PASSWORD" = "admin" ]; then
    echo "📝 n8n credentials: admin/admin"
    echo "⚠️  IMPORTANT: Change the n8n password in production!"
else
    echo "📝 n8n credentials: admin/$N8N_PASSWORD"
fi
