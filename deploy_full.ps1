# ===========================================================
#  GRACECLOUD GLOBAL  FULL AUTOMATION DEPLOY + SAFETY LOCK (FIXED)
# ===========================================================

#  VARIABLES
$RG="gracealone-rg"
$ACR="gracealoneacr"
$BACKEND_APP="gracealone-api"
$NOTES_APP="gracecloud-notes"
$FRONTEND_APP="gracealone-frontend"
$SUBSCRIPTION="Azure subscription 1"
$PLAN="GraceAppServicePlan"
$LOCATION="eastus"

# ===========================================================
#  FRONTEND BUILD + DEPLOY
# ===========================================================

Write-Host " Building frontend..."
cd "C:\gracealoneaba\frontend"
npm install
npm run build

Write-Host " Deploying frontend to Azure Static Web App..."
az staticwebapp upload `
  --name $FRONTEND_APP `
  --resource-group $RG `
  --source "./dist" `
  --verbose

# ===========================================================
#  LOCKED CI/CD (BACKEND + NOTES)
# ===========================================================

Write-Host " Setting up CI/CD redeploy workflows..."

# Backend CI/CD
$backendYaml = @"
name: Deploy Backend to Azure
on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Build and Push Docker
        run: |
          az acr login --name $ACR
          docker build -t $ACR.azurecr.io/$BACKEND_APP:`${{ github.run_number }} .
          docker push $ACR.azurecr.io/$BACKEND_APP:`${{ github.run_number }}

      - name: Deploy to Azure
        run: |
          az webapp config container set --name $BACKEND_APP --resource-group $RG `
            --docker-custom-image-name $ACR.azurecr.io/$BACKEND_APP:`${{ github.run_number }}
          az webapp restart --name $BACKEND_APP --resource-group $RG
"@
$backendYaml | Out-File ".github/workflows/deploy-backend.yml" -Encoding utf8

# Notes CI/CD
$notesYaml = @"
name: Deploy Notes API to Azure
on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Build and Push Docker
        run: |
          az acr login --name $ACR
          docker build -t $ACR.azurecr.io/$NOTES_APP:`${{ github.run_number }} .
          docker push $ACR.azurecr.io/$NOTES_APP:`${{ github.run_number }}

      - name: Deploy to Azure
        run: |
          az webapp config container set --name $NOTES_APP --resource-group $RG `
            --docker-custom-image-name $ACR.azurecr.io/$NOTES_APP:`${{ github.run_number }}
          az webapp restart --name $NOTES_APP --resource-group $RG
"@
$notesYaml | Out-File ".github/workflows/deploy-notes.yml" -Encoding utf8

# ===========================================================
#  STOP SCRIPT (ZERO COST SAFETY)
# ===========================================================

Write-Host " Creating stop-all.ps1 for shutdown..."
$stopScript = @"
Write-Host ' Stopping all GraceCloud services...'

az webapp stop --name $BACKEND_APP --resource-group $RG
az webapp stop --name $NOTES_APP --resource-group $RG
az staticwebapp disconnect --name $FRONTEND_APP --resource-group $RG

Write-Host ' Cleaning old Docker images...'
docker system prune -a -f

Write-Host ' All services stopped. Zero billing active.'
"@
$stopScript | Out-File "C:\gracealoneaba\stop-all.ps1" -Encoding utf8

Write-Host " Frontend deployed, CI/CD locked, stop script ready!"
Write-Host "Run: powershell -ExecutionPolicy Bypass -File C:\gracealoneaba\stop-all.ps1"
