# Railway Configuration Files for F1 Telegram Bot

This document provides all the configuration files needed to deploy your F1 Telegram Bot on Railway with proper Playwright/browser automation support.

## 📁 Required Configuration Files

### 1. `railway.toml` - Main Railway Configuration

Create this file in your project root:

```toml
# Railway deployment configuration for F1 Telegram Bot
[build]
builder = "NIXPACKS"
startCommand = "gunicorn --bind :8080 --workers 1 --worker-class gthread --threads 4 --timeout 120 --keep-alive 5 --max-requests 1000 --max-requests-jitter 100 leapcell_f1_bot:app"

[deploy]
startCommand = "gunicorn --bind :8080 --workers 1 --worker-class gthread --threads 4 --timeout 120 --keep-alive 5 --max-requests 1000 --max-requests-jitter 100 leapcell_f1_bot:app"
healthcheck = "/health"
healthcheckTimeout = 30
healthcheckInterval = 30
healthcheckStartPeriod = 60

[env]
PORT = "8080"
TELEGRAM_BOT_TOKEN = { fromSecret = "TELEGRAM_BOT_TOKEN" }
PYTHON_VERSION = "3.11.0"
WORKER_CLASS = "gthread"
WORKERS = "1"
THREADS = "4"
TIMEOUT = "120"
MAX_REQUESTS = "1000"
MAX_REQUESTS_JITTER = "100"

[storage]
name = "f1-bot-storage"
mountPath = "/app/storage"
```

### 2. Updated `Dockerfile` for Railway

Replace your current Dockerfile with this Railway-optimized version:

```dockerfile
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
# Railway provides better system support for these packages
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
CMD ["sh", "-c", "exec gunicorn --bind :8080 --workers 1 --worker-class gthread --threads 4 --timeout 120 --keep-alive 5 --max-requests 1000 --max-requests-jitter 100 leapcell_f1_bot:app"]
```

### 3. `Procfile` - Alternative Process Configuration

Create this file if you prefer Procfile over railway.toml:

```
web: gunicorn --bind :8080 --workers 1 --worker-class gthread --threads 4 --timeout 120 --keep-alive 5 --max-requests 1000 --max-requests-jitter 100 leapcell_f1_bot:app
```

### 4. `runtime.txt` - Python Version Specification

```
python-3.11.10
```

## 🔧 Environment Variables Setup

### Required Environment Variables

Set these in Railway dashboard under **Settings → Variables**:

| Variable Name | Value | Type | Description |
|---------------|-------|------|-------------|
| `PORT` | `8080` | Variable | Application port |
| `TELEGRAM_BOT_TOKEN` | `your_bot_token` | Secret | Telegram bot token from @BotFather |
| `PYTHON_VERSION` | `3.11.0` | Variable | Python version |
| `WORKER_CLASS` | `gthread` | Variable | Gunicorn worker class |
| `WORKERS` | `1` | Variable | Number of worker processes |
| `THREADS` | `4` | Variable | Number of threads per worker |
| `TIMEOUT` | `120` | Variable | Request timeout in seconds |
| `MAX_REQUESTS` | `1000` | Variable | Max requests per worker |
| `MAX_REQUESTS_JITTER` | `100` | Variable | Jitter for max requests |

### Optional Environment Variables

| Variable Name | Value | Type | Description |
|---------------|-------|------|-------------|
| `DEBUG` | `False` | Variable | Enable debug mode |
| `LOG_LEVEL` | `INFO` | Variable | Logging level |
| `CACHE_TTL` | `300` | Variable | Cache time-to-live in seconds |
| `PLAYWRIGHT_TIMEOUT` | `30000` | Variable | Playwright timeout in milliseconds |

## 📋 Deployment Checklist

### Pre-Deployment

- [ ] Update Dockerfile with Railway optimizations
- [ ] Create `railway.toml` configuration file
- [ ] Add `runtime.txt` for Python version
- [ ] Test Docker build locally: `docker build -t f1-bot .`
- [ ] Push all changes to GitHub

### Railway Setup

- [ ] Sign up at [railway.app](https://railway.app)
- [ ] Connect GitHub repository
- [ ] Set environment variables in Railway dashboard
- [ ] Configure build settings
- [ ] Deploy initial version

### Post-Deployment

- [ ] Verify application starts successfully
- [ ] Test health check endpoint: `/health`
- [ ] Test basic bot commands
- [ ] Update Telegram webhook URL
- [ ] Monitor resource usage and costs

## 🚀 Railway Dashboard Configuration

### Build Settings

1. **Build Command**: 
   ```
   pip install -r requirements.txt && playwright install chromium
   ```

2. **Start Command**:
   ```
   gunicorn --bind :8080 --workers 1 --worker-class gthread --threads 4 --timeout 120 --keep-alive 5 --max-requests 1000 --max-requests-jitter 100 leapcell_f1_bot:app
   ```

3. **Port**: `8080`

4. **Healthcheck Path**: `/health`

### Environment Variables

Configure these in **Settings → Variables**:

```bash
PORT=8080
TELEGRAM_BOT_TOKEN=[YOUR_BOT_TOKEN]
PYTHON_VERSION=3.11.0
WORKER_CLASS=gthread
WORKERS=1
THREADS=4
TIMEOUT=120
MAX_REQUESTS=1000
MAX_REQUESTS_JITTER=100
```

## 🔍 Monitoring & Debugging

### Health Check Endpoints

Test these endpoints after deployment:

1. **Health Check**: `https://your-service.up.railway.app/health`
   ```json
   {
     "status": "healthy",
     "service": "F1 Telegram Bot Railway Deployment"
   }
   ```

2. **Bot Status**: `https://your-service.up.railway.app/status`
   ```json
   {
     "status": "running",
     "bot_running": true,
     "scrapers_available": {
       "optimized": true,
       "fallback": true
     },
     "timestamp": "2024-01-01T00:00:00.000Z"
   }
   ```

3. **Service Info**: `https://your-service.up.railway.app/`
   ```json
   {
     "status": "F1 Telegram Bot (Railway) is running!",
     "version": "1.0.0-railway",
     "deployment": "Railway",
     "features": {
       "containerized": true,
       "webhook_mode": true,
       "optimized_scraping": true,
       "enhanced_error_handling": true
     }
   }
   ```

### Railway Logs

Monitor logs in Railway dashboard for:

- Build process success
- Application startup
- Playwright installation
- Bot initialization
- Webhook processing
- Error tracking

### Resource Monitoring

Check Railway dashboard for:

- Memory usage (should be under 512MB for low traffic)
- CPU usage (should be under 50% for low traffic)
- Monthly credits usage
- Container restarts

## 🛠️ Troubleshooting

### Common Issues

#### Build Failures
```bash
# Check if Playwright dependencies are missing
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libnss3 \
    libxss1 \
    libasound2 \
    libappindicator1 \
    libu2f-udev
```

#### Application Startup Issues
```bash
# Ensure proper user permissions
USER app
# Check if files are properly copied
COPY --chown=app:app . /app/
```

#### Playwright Browser Issues
```bash
# Add Xvfb for headless browser support
RUN apt-get install -y xvfb
# Set display environment
ENV DISPLAY=:99
```

#### Memory Issues
```bash
# Reduce worker threads
ENV THREADS=2
# Optimize Playwright usage
ENV PLAYWRIGHT_TIMEOUT=15000
```

## 📞 Support

### Railway Support
- [Railway Documentation](https://docs.railway.app)
- [Railway Community](https://railway-community discord)
- [Railway Status](https://status.railway.app)

### Bot Support
- Check existing documentation in repository
- Use validation script: `python validate_deployment.py`
- Review deployment guides for troubleshooting

---

This configuration provides everything needed for a successful Railway deployment with proper Playwright/browser automation support for your F1 Telegram Bot!