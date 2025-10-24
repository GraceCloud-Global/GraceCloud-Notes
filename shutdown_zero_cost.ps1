# Stop all App Services in the resource group
az webapp stop --name gracealone-api --resource-group gracealone-rg
az webapp stop --name gracecloudglobal --resource-group gracealone-rg
az webapp stop --name gracecloud-notes --resource-group gracealone-rg

# Optionally stop the App Service Plans (no active app = no runtime billing)
az appservice plan stop --name gracealone-app-plan --resource-group gracealone-rg
az appservice plan stop --name gracealone-plan --resource-group gracealone-rg
az appservice plan stop --name GraceAppServicePlan --resource-group gracealone-rg

# Disable container registry tasks to avoid background image builds
az acr update --name gracealoneacr --resource-group gracealone-rg --admin-enabled false
