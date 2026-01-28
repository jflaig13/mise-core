# Mise App Deployment Guide

## Production Service
- **Service Name:** `mise`
- **Region:** `us-central1`
- **Domain:** https://app.getmise.io
- **API:** https://mise-transrouter-rdxbrrdtsa-uc.a.run.app

## Deploy Command

**IMPORTANT:** Always deploy using the Dockerfile to ensure correct dependencies are installed.

The deployment process requires building the image first, then deploying it:

```bash
cd ~/mise-core

# 1. Copy Dockerfile.mise to Dockerfile (required for gcloud builds)
cp Dockerfile.mise Dockerfile

# 2. Build the Docker image
gcloud builds submit --tag gcr.io/automation-station-478103/mise .

# 3. Deploy the image to Cloud Run
gcloud run deploy mise \
  --image gcr.io/automation-station-478103/mise:latest \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated

# 4. Clean up temporary file
rm Dockerfile
```

**Why this process?**
- `gcloud run deploy --source` uses buildpacks which may pick up the wrong `requirements.txt`
- Building with explicit Dockerfile ensures the root `requirements.txt` is used with all dependencies
- This prevents `ModuleNotFoundError: No module named 'requests'` and similar errors

## Important Rules

### ✅ DO
- Always deploy to the `mise` service in `us-central1`
- Use the exact service name: `mise` (not mise-app, mise2, etc.)
- Verify app.getmise.io works after deployment
- Check TRANSROUTER_URL environment variable is correct

### ❌ DO NOT
- Create new services (mise-app, mise2, etc.) - causes confusion and breaks the domain mapping
- Deploy to other regions (us-west1, etc.) - app.getmise.io is mapped to us-central1
- Change the service name from `mise`
- Deploy without testing on app.getmise.io first

## Verify Deployment

After deploying, verify:

1. **Health check:**
   ```bash
   curl https://app.getmise.io/health
   # Should return: {"status":"ok","app":"mise"}
   ```

2. **Domain mapping:**
   ```bash
   gcloud beta run domain-mappings list --region us-central1
   # Should show: app.getmise.io → mise
   ```

3. **Environment variables:**
   ```bash
   gcloud run services describe mise --region us-central1 --format='value(spec.template.spec.containers[0].env)' | grep TRANSROUTER
   # Should show: TRANSROUTER_URL = https://mise-transrouter-rdxbrrdtsa-uc.a.run.app
   ```

## Troubleshooting

**Problem:** app.getmise.io returns 404 or errors after deployment

**Solution:**
1. Check you deployed to the correct service: `mise` (not mise-app)
2. Check the region: `us-central1` (not us-west1)
3. Verify TRANSROUTER_URL environment variable is set correctly
4. Check logs: `gcloud run services logs read mise --region us-central1 --limit 50`

**Problem:** Domain doesn't resolve

**Solution:**
1. Verify domain mapping: `gcloud beta run domain-mappings list --region us-central1`
2. Domain should map to `mise` service, not any other service
3. Contact support if mapping is missing

## Related Services

- **Transrouter API:** `mise-transrouter` (us-central1)
  - Deploy: `cd ~/mise-core/transrouter && gcloud run deploy mise-transrouter --source . --region us-central1`
  - URL: https://mise-transrouter-rdxbrrdtsa-uc.a.run.app
