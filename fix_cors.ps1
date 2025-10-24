cd C:\gracealoneaba\backend
pip install django-cors-headers
(Get-Content settings.py) -replace 'INSTALLED_APPS = \[', 'INSTALLED_APPS = [
    ''corsheaders'',' | Set-Content settings.py
(Get-Content settings.py) -replace 'MIDDLEWARE = \[', 'MIDDLEWARE = [
    ''corsheaders.middleware.CorsMiddleware'',' | Set-Content settings.py
Add-Content settings.py "
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
]
CORS_ALLOW_CREDENTIALS = True"
python manage.py runserver 0.0.0.0:8000
