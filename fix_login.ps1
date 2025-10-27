# FRONTEND: AuthContext.tsx
export const loginUser = async (username: string, password: string) => {
  const response = await fetch('http://127.0.0.1:8000/api/token/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  });
  if (!response.ok) throw new Error('Login failed');
  return await response.json();
};

# FRONTEND: .env.local
VITE_API_URL=http://127.0.0.1:8000

# BACKEND: settings.py
INSTALLED_APPS = [
    'corsheaders',
    'rest_framework',
    ...
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]
