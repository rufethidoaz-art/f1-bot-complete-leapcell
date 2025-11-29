# Use Python 3.11 slim image optimized for Railway deployment
FROM python:3.11-slim

# Set environment variables for Railway
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Set working directory
WORKDIR /app

# Install system dependencies for Playwright and Python packages
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    gcc \
    python3-dev \
    build-essential \
    curl \
    unzip \
    libglib2.0-0 \
    libnss3 \
    libxss1 \
    libasound2 \
    libappindicator1 \
    libu2f-udev \
    fonts-liberation \
    # Add additional packages for better Railway compatibility
    ca-certificates \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies with error handling
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers with Railway-specific optimizations
RUN playwright install chromium && \
    playwright install-deps chromium

# Create non-root user for security (Railway best practice)
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app

# Switch to non-root user
USER app

# Copy application code
COPY --chown=app:app . /app/

# Expose port (Railway automatically detects this)
EXPOSE 8080

# Health check for Railway monitoring
HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Railway-specific start command
CMD ["sh", "-c", "exec gunicorn --bind :8080 --workers 1 --worker-class gthread --threads 4 --timeout 120 --keep-alive 5 --max-requests 1000 --max-requests-jitter 100 f1_bot:app"]