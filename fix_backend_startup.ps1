az webapp config set 
  --name gracealone-api 
  --resource-group gracealone-rg 
  --startup-file "gunicorn backend.core.wsgi:application --bind 0.0.0.0:8000 --workers 3"

az webapp restart 
  --name gracealone-api 
  --resource-group gracealone-rg
