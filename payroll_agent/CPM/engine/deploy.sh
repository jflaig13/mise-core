#!/bin/bash
# Deploy payroll engine to Cloud Run from mise-core root

cd ~/mise-core

PROJECT_ID="automation-station-478103"
REGION="us-central1"
SERVICE="payroll-engine"
TAG=$(date +%s)
IMAGE="gcr.io/$PROJECT_ID/$SERVICE:$TAG"

echo "🔨 Building container from mise-core root..."
# Copy Dockerfile to root temporarily (gcloud looks for "Dockerfile" in build context)
cp payroll_agent/CPM/engine/Dockerfile ./Dockerfile

gcloud builds submit \
  --tag $IMAGE \
  .

# Clean up temp Dockerfile
rm -f Dockerfile

echo "🚀 Deploying to Cloud Run..."
gcloud run deploy $SERVICE \
  --image $IMAGE \
  --region $REGION \
  --platform managed \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10 \
  --timeout 300 \
  --allow-unauthenticated \
  --port 8080 \
  --no-use-http2

echo "✅ DONE! Updated roster deployed."
