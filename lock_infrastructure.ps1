# ============================================
#  GraceAlone API Infrastructure Lockdown
# ============================================
# Enforce correct Django environment, secure secrets, and default settings.
az webapp config appsettings set --name gracealone-api --resource-group gracealone-rg --settings `
    DJANGO_SETTINGS_MODULE=backend.core.settings `
    DJANGO_DEBUG=False `
    ALLOWED_HOSTS="gracealone-api.azurewebsites.net,localhost" `
    SECRET_KEY=$(New-Guid).Guid `
    PYTHONUNBUFFERED=1 `
    PYTHONDONTWRITEBYTECODE=1 `
    LOGGING_LEVEL=INFO

# Enforce system identity for secure ACR pulls
az webapp identity assign --name gracealone-api --resource-group gracealone-rg

# Force HTTPS and disable public FTP access
az webapp update --https-only true --name gracealone-api --resource-group gracealone-rg
az webapp config set --ftps-state Disabled --name gracealone-api --resource-group gracealone-rg
