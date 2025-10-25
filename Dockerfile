# Dockerfile for RCM_RECIPE_2
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip to latest version
RUN pip install --upgrade pip

# Copy requirements and install Python dependencies in stages
# First, install large packages with increased timeout
COPY requirements.txt .

# Install PyTorch separately with CPU-only version (smaller and faster)
RUN pip install --default-timeout=100 \
    torch==2.6.0 --index-url https://download.pytorch.org/whl/cpu

# Install transformers and other large packages
RUN pip install --default-timeout=100 \
    transformers==4.40.0 \
    sentencepiece==0.1.99

# Install remaining dependencies
RUN pip install --default-timeout=100 -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs data

# Expose port (Render will set PORT env var)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health', timeout=5).raise_for_status()"

# Run the application
# Note: Render will set PORT environment variable
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1