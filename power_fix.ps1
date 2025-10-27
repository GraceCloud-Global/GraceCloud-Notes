# --- FRONTEND PATCH ---
 = 'C:\gracealoneaba\frontend\src\context\AuthContext.tsx'
 = Get-Content 
# unify any /token reference
 =  -replace 'http://127\.0\.0\.1:8000/token/?', 'http://127.0.0.1:8000/api/token/'
 =  -replace 'fetch\(	oken/\)', 'fetch(http://127.0.0.1:8000/api/token/)'
Set-Content -Path  -Value  -Force

# --- BACKEND URLS RESET ---
 = 'C:\gracealoneaba\backend\core\urls.py'
@'
from django.contrib import admin
from django.urls import path, re_path
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

def health(request):
    return JsonResponse({"status": "ok", "service": "GraceAlone API"})

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^health/?$', health),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
'@ | Set-Content -Path  -Force

# --- RESTART BACKEND ---
cd C:\gracealoneaba\backend
Start-Job -ScriptBlock { python manage.py runserver 127.0.0.1:8000 }

# --- RESTART FRONTEND ---
cd C:\gracealoneaba\frontend
Start-Job -ScriptBlock { npm run dev }

Write-Host "
 Grace Alone ABA fully powered up with /api/token/ active and frontend synced."
