Write-Host " Stopping all GraceCloud services..."

az webapp stop --name gracealone-api --resource-group gracealone-rg
az webapp stop --name gracecloud-notes --resource-group gracealone-rg
az staticwebapp disconnect --name gracealone-frontend --resource-group gracealone-rg

Write-Host " Cleaning old Docker images..."
docker system prune -a -f

Write-Host " All services stopped. Zero billing active."
