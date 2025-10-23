# ======================================
#  GraceAlone API Dockerfile (v23)
# ======================================
FROM python:3.11-slim

# Set environment vars
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create work directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . /app/

# Expose port for gunicorn
EXPOSE 8000

#  Fix 1: Ensure correct startup path for Django
#  Fix 2: ALLOWED_HOSTS now includes Azure domain
ENV DJANGO_ALLOWED_HOSTS="localhost 127.0.0.1 gracealone-api.azurewebsites.net"

#  Start Gunicorn correctly
CMD ["gunicorn", "backend.core.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--log-level", "info"]
