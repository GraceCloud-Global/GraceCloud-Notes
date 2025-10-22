# ==========================================
# Grace Alone ABA - Pre-Push Validation Script (Fixed)
# ==========================================

function Stop-Script {
    param(
        [string]$Message = "Script stopped manually"
    )
    Write-Host " $Message" -ForegroundColor Red
    exit 1
}

# --- CONFIGURATION ---
$ACR_NAME        = "gracealoneacr"
$IMAGE_NAME      = "gracealone-api"
$TAG             = "v22"
$RESOURCE_GROUP  = "gracealone-rg"
$FULL_IMAGE      = "${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${TAG}"

Write-Host " Starting Pre-Push Checks for $FULL_IMAGE ..." -ForegroundColor Cyan

# --- STEP 1: Build Docker image locally ---
docker build -t $FULL_IMAGE ./backend
if ($LASTEXITCODE -ne 0) { Stop-Script " Docker build failed." }

# --- STEP 2: Verify backend structure inside image ---
Write-Host " Checking backend folder structure inside image..."
docker run --rm $FULL_IMAGE sh -c "ls -R /app/backend | grep api" 2>$null
if ($LASTEXITCODE -ne 0) { Stop-Script " 'api' module not found inside /app/backend." }

# --- STEP 3: Push image to Azure Container Registry ---
Write-Host " Logging into Azure Container Registry..."
az acr login --name $ACR_NAME
if ($LASTEXITCODE -ne 0) { Stop-Script " Failed to authenticate with ACR." }

Write-Host " Pushing image to ACR: $FULL_IMAGE ..."
docker push $FULL_IMAGE
if ($LASTEXITCODE -ne 0) { Stop-Script " Docker push failed." }

Write-Host " Pre-push validation complete. Image successfully built and pushed to $FULL_IMAGE" -ForegroundColor Green
