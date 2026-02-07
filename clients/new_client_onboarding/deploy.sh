#!/bin/bash
set -e

echo "Building and deploying mise-onboard..."

# Build
gcloud builds submit --tag gcr.io/automation-station-478103/mise-onboard .

# Deploy
gcloud run deploy mise-onboard \
  --image gcr.io/automation-station-478103/mise-onboard:latest \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars SENDGRID_API_KEY=$SENDGRID_API_KEY

echo ""
echo "Deploy complete!"
echo "Service URL: https://mise-onboard-rdxbrrdtsa-uc.a.run.app"
echo ""
echo "To set up custom domain (first time only):"
echo "  gcloud beta run domain-mappings create --service mise-onboard --domain onboard.getmise.io --region us-central1"
