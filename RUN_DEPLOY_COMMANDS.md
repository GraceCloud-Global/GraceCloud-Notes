# Grace Alone ABA - Run & Deploy Commands

## Prerequisites

### Required Software
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Redis 7+

### Required Environment Variables
Create `.env` files based on these templates.

---

## LOCAL DEVELOPMENT

### Backend Setup

```bash
# Navigate to backend directory
cd C:\gracealoneaba\backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
.\venv\Scripts\activate

# Activate virtual environment (Unix/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file for local development
copy .env.example .env
# Edit .env with your local settings
```

### Backend .env Template (Local)
```env
# Django Settings
DJANGO_SETTINGS_MODULE=core.settings.dev
DEBUG=True
SECRET_KEY=your-local-secret-key-change-in-production

# Database (Local PostgreSQL)
DATABASE_URL=postgresql://postgres:password@localhost:5432/gracealoneaba

# Redis (Local)
REDIS_URL=redis://localhost:6379/0

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7

# Field Encryption (HIPAA)
FIELD_ENCRYPTION_KEY=your-32-byte-base64-encoded-key

# Azure Storage (Optional for local - uses local file storage)
USE_AZURE_STORAGE=false

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

### Database Setup

```bash
# Create PostgreSQL database
psql -U postgres
CREATE DATABASE gracealoneaba;
\q

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load initial data (optional)
python manage.py loaddata initial_data
```

### Run Backend Server

```bash
# Development server
python manage.py runserver 8000

# With auto-reload
python manage.py runserver 0.0.0.0:8000

# Check for issues
python manage.py check
python manage.py check --deploy  # Security checks
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd C:\gracealoneaba\frontend

# Install dependencies
npm install

# Create .env file
copy .env.example .env
# Edit .env
```

### Frontend .env Template (Local)
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=Grace Alone ABA
VITE_ENVIRONMENT=development
```

### Run Frontend Server

```bash
# Development server with hot reload
npm run dev

# Build for production (testing)
npm run build

# Preview production build
npm run preview

# Type checking
npm run typecheck

# Linting
npm run lint
```

### Run Both (Development)

Open two terminals:

**Terminal 1 - Backend:**
```bash
cd C:\gracealoneaba\backend
.\venv\Scripts\activate
python manage.py runserver 8000
```

**Terminal 2 - Frontend:**
```bash
cd C:\gracealoneaba\frontend
npm run dev
```

Access:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/api/v1/
- Admin: http://localhost:8000/admin/

---

## TESTING

### Backend Tests

```bash
cd C:\gracealoneaba\backend
.\venv\Scripts\activate

# Run all tests
python manage.py test

# Run with coverage
pip install coverage
coverage run manage.py test
coverage report -m
coverage html  # Generate HTML report

# Run specific app tests
python manage.py test clients
python manage.py test sessions
python manage.py test billing

# Run with verbose output
python manage.py test -v 2

# Run specific test class
python manage.py test clients.tests.ClientModelTests
```

### Frontend Tests

```bash
cd C:\gracealoneaba\frontend

# Run tests
npm run test

# Run with coverage
npm run test:coverage

# Run in watch mode
npm run test:watch
```

---

## PRODUCTION DEPLOYMENT (Azure)

### Prerequisites
- Azure subscription
- Azure CLI installed
- Azure App Service plan (B2 minimum for HIPAA)
- Azure Database for PostgreSQL
- Azure Blob Storage
- Azure Redis Cache
- Azure Key Vault

### Azure CLI Login

```bash
az login
az account set --subscription "Your Subscription Name"
```

### Create Azure Resources

```bash
# Variables
RESOURCE_GROUP="gracealoneaba-prod"
LOCATION="eastus"
APP_NAME="gracealoneaba"

# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create PostgreSQL server
az postgres flexible-server create \
  --resource-group $RESOURCE_GROUP \
  --name $APP_NAME-db \
  --location $LOCATION \
  --sku-name Standard_B2s \
  --tier Burstable \
  --storage-size 32 \
  --admin-user dbadmin \
  --admin-password "YourSecurePassword123!" \
  --version 14

# Create database
az postgres flexible-server db create \
  --resource-group $RESOURCE_GROUP \
  --server-name $APP_NAME-db \
  --database-name gracealoneaba

# Create storage account
az storage account create \
  --name ${APP_NAME}storage \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --sku Standard_LRS \
  --kind StorageV2 \
  --https-only true

# Create Redis cache
az redis create \
  --name $APP_NAME-redis \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --sku Basic \
  --vm-size C1

# Create App Service plan (B2 for production)
az appservice plan create \
  --name $APP_NAME-plan \
  --resource-group $RESOURCE_GROUP \
  --sku B2 \
  --is-linux

# Create Web App for backend
az webapp create \
  --resource-group $RESOURCE_GROUP \
  --plan $APP_NAME-plan \
  --name $APP_NAME-api \
  --runtime "PYTHON:3.11"

# Create Static Web App for frontend
az staticwebapp create \
  --name $APP_NAME-web \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION
```

### Configure App Settings

```bash
# Backend environment variables
az webapp config appsettings set \
  --resource-group $RESOURCE_GROUP \
  --name $APP_NAME-api \
  --settings \
    DJANGO_SETTINGS_MODULE=core.settings.prod \
    DEBUG=False \
    SECRET_KEY="@Microsoft.KeyVault(SecretUri=https://your-keyvault.vault.azure.net/secrets/django-secret-key)" \
    DATABASE_URL="postgresql://dbadmin:password@$APP_NAME-db.postgres.database.azure.com:5432/gracealoneaba?sslmode=require" \
    REDIS_URL="rediss://:password@$APP_NAME-redis.redis.cache.windows.net:6380/0" \
    AZURE_STORAGE_CONNECTION_STRING="@Microsoft.KeyVault(SecretUri=...)" \
    FIELD_ENCRYPTION_KEY="@Microsoft.KeyVault(SecretUri=...)" \
    ALLOWED_HOSTS="$APP_NAME-api.azurewebsites.net" \
    CORS_ALLOWED_ORIGINS="https://$APP_NAME-web.azurestaticapps.net"
```

### Deploy Backend

```bash
cd C:\gracealoneaba\backend

# Create requirements.txt if not exists
pip freeze > requirements.txt

# Deploy using Azure CLI
az webapp up \
  --resource-group $RESOURCE_GROUP \
  --name $APP_NAME-api \
  --runtime "PYTHON:3.11" \
  --sku B2

# Or using zip deployment
zip -r deploy.zip . -x "venv/*" -x "__pycache__/*" -x "*.pyc"
az webapp deploy \
  --resource-group $RESOURCE_GROUP \
  --name $APP_NAME-api \
  --src-path deploy.zip \
  --type zip

# Run migrations (SSH into app)
az webapp ssh --resource-group $RESOURCE_GROUP --name $APP_NAME-api
# Then: python manage.py migrate --noinput
```

### Deploy Frontend

```bash
cd C:\gracealoneaba\frontend

# Build for production
npm run build

# Deploy to Azure Static Web Apps
# Option 1: GitHub Actions (recommended)
# Connect your repo and Azure will auto-deploy

# Option 2: CLI deployment
az staticwebapp deploy \
  --name $APP_NAME-web \
  --resource-group $RESOURCE_GROUP \
  --source ./dist \
  --env production
```

### Frontend Production .env
```env
VITE_API_BASE_URL=https://gracealoneaba-api.azurewebsites.net
VITE_APP_NAME=Grace Alone ABA
VITE_ENVIRONMENT=production
```

---

## PRODUCTION SECURITY CHECKLIST

### Before Go-Live

```bash
# Run Django security check
python manage.py check --deploy

# Verify settings
# ✓ DEBUG = False
# ✓ SECURE_SSL_REDIRECT = True
# ✓ SESSION_COOKIE_SECURE = True
# ✓ CSRF_COOKIE_SECURE = True
# ✓ SECURE_HSTS_SECONDS > 0
# ✓ X_FRAME_OPTIONS = 'DENY'
```

### Required for HIPAA Compliance
1. ✓ TLS 1.2+ enforced
2. ✓ Data encrypted at rest (Azure handles this)
3. ✓ Field-level encryption for PHI
4. ✓ Audit logging enabled
5. ✓ BAA signed with Azure
6. ✓ Access controls implemented
7. ✓ Session timeout configured
8. ✓ Password policy enforced

---

## MAINTENANCE COMMANDS

### Database

```bash
# Backup database
pg_dump -h hostname -U username -d gracealoneaba > backup.sql

# Restore database
psql -h hostname -U username -d gracealoneaba < backup.sql

# Create new migration
python manage.py makemigrations

# Show migration SQL
python manage.py sqlmigrate app_name 0001

# Rollback migration
python manage.py migrate app_name 0001
```

### Logs

```bash
# View Azure logs
az webapp log tail --resource-group $RESOURCE_GROUP --name $APP_NAME-api

# Download logs
az webapp log download --resource-group $RESOURCE_GROUP --name $APP_NAME-api
```

### Scaling

```bash
# Scale up (more resources)
az appservice plan update \
  --name $APP_NAME-plan \
  --resource-group $RESOURCE_GROUP \
  --sku P1v2

# Scale out (more instances)
az webapp scale \
  --resource-group $RESOURCE_GROUP \
  --name $APP_NAME-api \
  --instance-count 3
```

---

## TROUBLESHOOTING

### Common Issues

**CORS errors:**
- Verify CORS_ALLOWED_ORIGINS includes frontend URL
- Check for trailing slashes

**Database connection failed:**
- Verify DATABASE_URL format
- Check firewall rules on Azure PostgreSQL
- Verify SSL mode

**Static files not loading:**
- Run `python manage.py collectstatic`
- Verify STATIC_URL and STATIC_ROOT settings

**502 Bad Gateway:**
- Check application logs
- Verify startup command
- Check memory limits

### Health Check Endpoints

```bash
# Backend health
curl https://your-api.azurewebsites.net/api/v1/health/

# Database connectivity
curl https://your-api.azurewebsites.net/api/v1/health/db/
```

---

## CONTACT

For deployment issues:
- Check Azure Portal for diagnostics
- Review application insights
- Contact DevOps team
