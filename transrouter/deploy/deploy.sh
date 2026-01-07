#!/bin/bash
# =============================================================================
# Deploy Mise Transrouter to Cloud Run
# =============================================================================
#
# Prerequisites:
#   1. gcloud CLI installed and authenticated
#   2. Docker installed (for local builds)
#   3. GCP project configured
#
# Usage:
#   ./deploy/deploy.sh
#
# Environment variables:
#   GCP_PROJECT   - GCP project ID (required)
#   GCP_REGION    - Cloud Run region (default: us-central1)
#   SERVICE_NAME  - Cloud Run service name (default: mise-transrouter)
#
# =============================================================================

set -e  # Exit on error

# Configuration
GCP_PROJECT="${GCP_PROJECT:?Error: GCP_PROJECT environment variable is required}"
GCP_REGION="${GCP_REGION:-us-central1}"
SERVICE_NAME="${SERVICE_NAME:-mise-transrouter}"
IMAGE_NAME="gcr.io/${GCP_PROJECT}/${SERVICE_NAME}"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
IMAGE_TAG="${IMAGE_NAME}:${TIMESTAMP}"

echo "============================================="
echo "Deploying Mise Transrouter to Cloud Run"
echo "============================================="
echo "Project:  ${GCP_PROJECT}"
echo "Region:   ${GCP_REGION}"
echo "Service:  ${SERVICE_NAME}"
echo "Image:    ${IMAGE_TAG}"
echo "============================================="
echo ""

# Navigate to repo root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
cd "${REPO_ROOT}"

echo "📦 Building Docker image..."
docker build -t "${IMAGE_TAG}" -t "${IMAGE_NAME}:latest" -f transrouter/Dockerfile .

echo ""
echo "📤 Pushing to Container Registry..."
docker push "${IMAGE_TAG}"
docker push "${IMAGE_NAME}:latest"

echo ""
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy "${SERVICE_NAME}" \
  --image "${IMAGE_TAG}" \
  --region "${GCP_REGION}" \
  --platform managed \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --timeout 300 \
  --concurrency 80 \
  --min-instances 0 \
  --max-instances 10 \
  --set-env-vars "CORS_ORIGINS=*"

echo ""
echo "✅ Deployment complete!"
echo ""

# Get the service URL
SERVICE_URL=$(gcloud run services describe "${SERVICE_NAME}" \
  --region "${GCP_REGION}" \
  --format "value(status.url)")

echo "============================================="
echo "Service URL: ${SERVICE_URL}"
echo "============================================="
echo ""
echo "Test with:"
echo "  curl ${SERVICE_URL}/api/v1/health"
echo ""
echo "⚠️  Remember to set secrets:"
echo "  gcloud run services update ${SERVICE_NAME} \\"
echo "    --region ${GCP_REGION} \\"
echo "    --set-env-vars \"MISE_API_KEYS=your-key:your-client\" \\"
echo "    --set-env-vars \"ANTHROPIC_API_KEY=sk-ant-...\""
echo ""
