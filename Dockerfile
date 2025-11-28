# Use Python 3.11 slim image optimized for Leapcell deployment
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

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
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers with proper dependencies
RUN playwright install chromium && \
    playwright install-deps chromium

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app

# Switch to non-root user
USER app

# Copy application code
COPY --chown=app:app leapcell_f1_bot.py /app/
COPY --chown=app:app streams.txt /app/
COPY --chown=app:app user_streams.json /app/

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run with Gunicorn for production
CMD ["sh", "-c", "exec gunicorn --bind :8080 --workers 1 --worker-class gthread --threads 4 --timeout 120 --keep-alive 5 --max-requests 1000 --max-requests-jitter 100 leapcell_f1_bot:app"]