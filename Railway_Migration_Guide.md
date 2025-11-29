# F1 Telegram Bot - Railway Migration Guide

## 🚀 Complete Migration from Leapcell to Railway

This guide provides step-by-step instructions to migrate your F1 Telegram Bot from Leapcell to Railway, ensuring better Playwright/browser automation support and zero cost hosting.

## 📋 Pre-Migration Checklist

### Current Issues to Resolve
- ❌ Playwright scraper not working properly on Leapcell
- ❌ Technical limitations with browser automation
- ❌ Usage limits causing problems
- ✅ Moving to better, completely free hosting option

### Benefits of Railway
- ✅ **Free $5/month credit** (sufficient for low traffic)
- ✅ **Always-on containers** (no sleeping like other free hosts)
- ✅ **Excellent Playwright support** with proper system dependencies
- ✅ **Telegram bot optimized** with webhook support
- ✅ **Easy GitHub integration** for automatic deployments
- ✅ **Better resource allocation** for browser automation

## 🔧 Phase 1: Code Preparation

### Step 1: Update Dockerfile for Railway

Your current [`Dockerfile`](Dockerfile) needs minor optimizations for Railway:

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

### Step 2: Create Railway Configuration File

Create a new file called `railway.toml` in your project root:

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

### Step 3: Update Environment Variables

Key environment variables needed for Railway:

| Variable | Value | Description |
|----------|-------|-------------|
| `TELEGRAM_BOT_TOKEN` | `YOUR_BOT_TOKEN` | Your Telegram bot token from @BotFather |
| `PORT` | `8080` | Application port (Railway standard) |
| `PYTHON_VERSION` | `3.11.0` | Python version |
| `WORKER_CLASS` | `gthread` | Gunicorn worker class |
| `WORKERS` | `1` | Number of worker processes |
| `THREADS` | `4` | Number of threads per worker |
| `TIMEOUT` | `120` | Request timeout in seconds |
| `MAX_REQUESTS` | `1000` | Max requests per worker |
| `MAX_REQUESTS_JITTER` | `100` | Jitter for max requests |

## 🚀 Phase 2: Railway Setup

### Step 4: Create Railway Account

1. Go to [Railway.app](https://railway.app)
2. Sign up using GitHub OAuth (recommended)
3. Install Railway GitHub app when prompted
4. Accept permissions for your repository

### Step 5: Connect Your Repository

1. In Railway dashboard, click **"New Project"**
2. Select **"Deploy from GitHub Repo"**
3. Choose your F1 bot repository
4. Click **"Deploy"**

### Step 6: Configure Environment Variables

1. Go to your project settings in Railway
2. Navigate to **"Settings"** → **"Variables"**
3. Add the environment variables listed above
4. Set `TELEGRAM_BOT_TOKEN` as a **Secret** (not public)

### Step 7: Configure Build Settings

1. Go to **"Settings"** → **"Builds"**
2. Set **Build Command**: `pip install -r requirements.txt && playwright install chromium`
3. Set **Start Command**: `gunicorn --bind :8080 --workers 1 --worker-class gthread --threads 4 --timeout 120 --keep-alive 5 --max-requests 1000 --max-requests-jitter 100 leapcell_f1_bot:app`
4. Set **Port**: `8080`

## 🧪 Phase 3: Testing & Validation

### Step 8: Monitor Initial Deployment

1. **Watch the build logs** in Railway dashboard
2. **Check for Playwright installation success**
3. **Verify application starts without errors**
4. **Test health check endpoint**: `https://your-service.up.railway.app/health`

Expected success indicators:
```
✅ Build completed successfully
✅ Playwright browsers installed
✅ Application started on port 8080
✅ Health check passing
✅ Container running stable
```

### Step 9: Test Bot Functionality

1. **Test basic commands**:
   - `/start` - Welcome message
   - `/standings` - Driver standings
   - `/nextrace` - Next race schedule

2. **Test during F1 session** (if available):
   - `/live` - Live timing (tests Playwright scraper)
   - Verify real-time updates work

3. **Test webhook functionality**:
   - Send various commands
   - Ensure responses are timely
   - Check logs for any errors

### Step 10: Update Telegram Webhook

**IMPORTANT**: Only update webhook after confirming Railway deployment works!

1. Get your new Railway URL: `https://your-service.up.railway.app`
2. Update webhook URL in your bot settings:
   ```
   https://your-service.up.railway.app/webhook
   ```

3. Test webhook by sending a command to your bot

## 📊 Phase 4: Migration Completion

### Step 11: Monitor Performance & Costs

Railway provides excellent monitoring:

1. **Check resource usage** in Railway dashboard
2. **Monitor monthly credits** usage
3. **Set up alerts** for high usage
4. **Optimize if needed** based on actual traffic

**Expected Costs for Your Usage:**
- **Low traffic estimate**: $2-3/month
- **Railway free credit**: $5/month
- **Net cost**: $0 (covered by free credit)

### Step 12: Cleanup & Optimization

1. **Keep Leapcell deployment running** for 1 week as backup
2. **Monitor Railway stability** during this period
3. **Backup user data** (`user_streams.json`)
4. **Optimize resource usage** if needed

## 🔧 Troubleshooting

### Common Issues & Solutions

#### **Build Failures**
```
Error: Playwright installation failed
Solution: Ensure system dependencies are installed in Dockerfile
```

#### **Bot Not Responding**
```
Error: Webhook not receiving updates
Solution: Verify webhook URL is correctly set to Railway endpoint
```

#### **Playwright Timeout**
```
Error: Browser automation timing out
Solution: Increase timeout settings and ensure sufficient memory allocation
```

#### **High Resource Usage**
```
Error: Container hitting limits
Solution: Reduce worker threads or optimize scraping frequency
```

### Railway-Specific Debugging

1. **Check Railway logs**: Dashboard → Logs
2. **Test health endpoints**: `/health`, `/status`
3. **Monitor resource usage**: Dashboard → Metrics
4. **Use Railway console**: Direct container access for debugging

## 📈 Performance Optimization

### For Better Performance on Railway

1. **Optimize Playwright usage**:
   - Cache browser instances
   - Limit concurrent scraping
   - Use efficient selectors

2. **Reduce memory usage**:
   - Limit worker threads to 2-4
   - Implement proper cleanup
   - Use efficient data structures

3. **Improve response times**:
   - Enable caching for API responses
   - Optimize database queries
   - Use async/await properly

## 🔄 Rollback Plan

If issues arise, you can rollback:

1. **Keep Leapcell deployment active** during transition
2. **Revert Telegram webhook** to Leapcell URL
3. **Compare performance** between platforms
4. **Choose best option** based on stability

## 📞 Support Resources

### Railway Documentation
- [Railway Docs](https://docs.railway.app)
- [Python Deployment Guide](https://docs.railway.app/deploys/python)
- [Environment Variables](https://docs.railway.app/environment-variables)

### F1 Bot Support
- Check [`DEPLOYMENT_GUIDE.md`](DEPLOYMENT_GUIDE.md) for bot-specific help
- Review [`DEPLOYMENT_FIX_GUIDE.md`](DEPLOYMENT_FIX_GUIDE.md) for common issues
- Use [`validate_deployment.py`](validate_deployment.py) to test setup

---

## ✅ Migration Summary

**Before Migration:**
- ❌ Playwright not working on Leapcell
- ❌ Technical limitations and usage issues
- ❌ Poor browser automation support

**After Migration:**
- ✅ **Free hosting** with $5/month credit
- ✅ **Always-on availability** for Telegram bot
- ✅ **Proper Playwright support** for F1 live timing
- ✅ **Better performance** and reliability
- ✅ **Zero cost** for your usage level

**Ready to migrate?** Follow this guide step-by-step for a smooth transition to Railway! 🚀