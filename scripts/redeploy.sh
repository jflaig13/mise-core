cd ~/ps-auto

PROJECT_ID="automation-station-478103"
REGION="us-central1"
SERVICE="payroll-engine"
TAG=$(date +%s)
IMAGE="gcr.io/$PROJECT_ID/$SERVICE:$TAG"

gcloud builds submit \
  --tag $IMAGE \
  .

gcloud run deploy $SERVICE \
  --image $IMAGE \
  --region $REGION \
  --platform managed \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10 \
  --allow-unauthenticated

echo "🚀 DONE"