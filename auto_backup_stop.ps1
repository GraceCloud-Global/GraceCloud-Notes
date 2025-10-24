# Auto daily backup & shutdown
cd "C:\gracealoneaba"
git add .
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
git commit -m "Auto backup: $timestamp"
git push origin main
az webapp stop --name gracealone-api --resource-group gracealone-rg
