# ==========================================
# GraceAlone API  Build v14 Clean Redeploy
# ==========================================

# Move to your project folder
Set-Location "C:\gracealoneaba"

# 1 Check Azure login
Write-Host "Checking Azure login..." -ForegroundColor Cyan
try { az account show | Out-Null }
catch { az login }

# 2 Login to Azure Container Registry
Write-Host "Logging into ACR graceacr..." -ForegroundColor Cyan
az acr login --name graceacr

# 3 Build Docker image
Write-Host "Building Docker image gracealone-api:v14 ..." -ForegroundColor Cyan
docker build -t graceacr.azurecr.io/gracealone-api:v14 .

# 4 Push image
Write-Host "Pushing image to ACR..." -ForegroundColor Cyan
docker push graceacr.azurecr.io/gracealone-api:v14

# 5 Update container configuration
Write-Host "Updating container settings on Web App..." -ForegroundColor Cyan
az webapp config container set --name gracealone-api --resource-group gracealone-rg 
  --docker-custom-image-name graceacr.azurecr.io/gracealone-api:v14 
  --docker-registry-server-url https://graceacr.azurecr.io

# 6 Update environment variables
Write-Host "Setting environment variables..." -ForegroundColor Cyan
az webapp config appsettings set --name gracealone-api --resource-group gracealone-rg 
  --settings WEBSITES_PORT=8000 PORT=8000 DJANGO_SETTINGS_MODULE=backend.settings PYTHONUNBUFFERED=1

# 7 Restart Web App
Write-Host "Restarting Web App..." -ForegroundColor Cyan
az webapp restart --name gracealone-api --resource-group gracealone-rg

# 8 Tail logs
Write-Host "Tailing logs... (Ctrl+C to stop)" -ForegroundColor Green
az webapp log tail --name gracealone-api --resource-group gracealone-rg
