# F1 Telegram Bot - Railway Deployment Guide

## 🚀 Completely Free Hosting with Playwright Support

This guide provides everything needed to deploy your F1 Telegram Bot on Railway with proper Playwright/browser automation support.

## 🎯 Why Railway?

### Perfect for Your F1 Bot Requirements:
- ✅ **Completely free** hosting ($5/month credit covers your usage)
- ✅ **Excellent Playwright support** with full browser automation
- ✅ **Always-on containers** for 24/7 Telegram bot availability
- ✅ **Better performance** than other free hosting options
- ✅ **Professional monitoring** and debugging tools
- ✅ **Easy GitHub integration** with automatic deployments

### Your Bot's Technical Needs Met:
- Python 3.11 with extensive dependencies
- Playwright with Chromium browser for F1 live timing scraping
- Flask web server for Telegram webhook handling
- Persistent storage for user stream data
- Always-on availability for instant bot responses

---

## 📋 Pre-Deployment Checklist

### Files Required in Your Repository:
```
✅ f1_bot.py (main bot application)
✅ requirements.txt (Python dependencies)
✅ optimized_scraper.py (live timing scraper)
✅ fallback_scraper.py (backup scraper)
✅ streams.txt (default stream links)
✅ user_streams.json (user data storage)
✅ Dockerfile (container configuration)
```

### Environment Variables Needed:
- `TELEGRAM_BOT_TOKEN` - Your Telegram bot token from @BotFather
- `PORT` - Application port (8080)
- Other configuration variables (see setup below)

---

## 🔧 Phase 1: Repository Setup

### Step 1: Create Railway Configuration

Create a file named `railway.toml` in your project root:

```toml
# Railway deployment configuration for F1 Telegram Bot
[build]
builder = "NIXPACKS"
startCommand = "gunicorn --bind :8080 --workers 1 --worker-class gthread --threads 4 --timeout 120 --keep-alive 5 --max-requests 1000 --max-requests-jitter 100 f1_bot:app"

[deploy]
startCommand = "gunicorn --bind :8080 --workers 1 --worker-class gthread --threads 4 --timeout 120 --keep-alive 5 --max-requests 1000 --max-requests-jitter 100 f1_bot:app"
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

### Step 2: Update Dockerfile for Railway

Create or update your `Dockerfile` with this Railway-optimized version:

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
```

### Step 3: Update Your Bot Application

Ensure your main bot file (rename from `leapcell_f1_bot.py` to `f1_bot.py`) has proper Railway compatibility:

```python
# Update import statements and configuration
import os
from flask import Flask

# Use PORT from environment (Railway standard)
PORT = int(os.getenv('PORT', 8080))

# Create Flask app
app = Flask(__name__)

# Ensure webhook URL uses Railway domain when deployed
def get_webhook_url():
    railway_url = os.getenv('RAILWAY_STATIC_URL')
    if railway_url:
        return f"{railway_url}/webhook"
    return "https://your-custom-domain.com/webhook"
```

---

## 🚀 Phase 2: Railway Setup

### Step 4: Create Railway Account

1. Go to [railway.app](https://railway.app)
2. Sign up using GitHub OAuth (recommended)
3. Install Railway GitHub app when prompted
4. Accept permissions for your repository

### Step 5: Deploy Your Project

1. In Railway dashboard, click **"New Project"**
2. Select **"Deploy from GitHub Repo"**
3. Choose your F1 bot repository
4. Click **"Deploy"**

### Step 6: Configure Environment Variables

In Railway dashboard → **Settings → Variables**, add:

| Variable | Value | Type | Description |
|----------|-------|------|-------------|
| `PORT` | `8080` | Variable | Application port |
| `TELEGRAM_BOT_TOKEN` | `YOUR_BOT_TOKEN` | Secret | Telegram bot token from @BotFather |
| `PYTHON_VERSION` | `3.11.0` | Variable | Python version |
| `WORKER_CLASS` | `gthread` | Variable | Gunicorn worker class |
| `WORKERS` | `1` | Variable | Number of worker processes |
| `THREADS` | `4` | Variable | Number of threads per worker |
| `TIMEOUT` | `120` | Variable | Request timeout in seconds |
| `MAX_REQUESTS` | `1000` | Variable | Max requests per worker |
| `MAX_REQUESTS_JITTER` | `100` | Variable | Jitter for max requests |

### Step 7: Configure Build Settings

In Railway dashboard → **Settings → Builds**:

- **Build Command**: `pip install -r requirements.txt && playwright install chromium`
- **Start Command**: `gunicorn --bind :8080 --workers 1 --worker-class gthread --threads 4 --timeout 120 --keep-alive 5 --max-requests 1000 --max-requests-jitter 100 f1_bot:app`
- **Port**: `8080`

---

## 🧪 Phase 3: Testing & Validation

### Step 8: Monitor Initial Deployment

Check Railway dashboard for successful deployment:

✅ **Build completed successfully**
✅ **Playwright installation successful**
✅ **Container started without errors**
✅ **Health checks passing**

### Step 9: Test Application Endpoints

Test these endpoints after deployment:

```bash
# Replace with your actual Railway URL
RAILWAY_URL="https://your-service.up.railway.app"

# Test health check
curl $RAILWAY_URL/health

# Test bot status
curl $RAILWAY_URL/status

# Test service info
curl $RAILWAY_URL/
```

Expected responses:

```json
// Health check response
{
  "status": "healthy",
  "service": "F1 Telegram Bot Railway Deployment",
  "timestamp": "2024-01-01T00:00:00.000Z"
}

// Bot status response
{
  "status": "running",
  "bot_running": true,
  "scrapers_available": {
    "optimized": true,
    "fallback": true
  },
  "features": [
    "live_timing",
    "standings",
    "race_schedule",
    "weather_forecast",
    "stream_management"
  ]
}
```

### Step 10: Set Up Telegram Bot

1. **Get Your Railway Webhook URL**:
   ```
   https://your-service.up.railway.app/webhook
   ```

2. **Configure Telegram Webhook**:
   ```bash
   curl -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/setWebhook" \
     -d "url=https://your-service.up.railway.app/webhook"
   ```

3. **Verify Webhook Configuration**:
   ```bash
   curl "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getWebhookInfo"
   ```

### Step 11: Test Bot Functionality

Test these commands with your Telegram bot:

```
/start - Welcome message with menu
/standings - Driver standings
/constructors - Constructor standings  
/lastrace - Last race results
/nextrace - Next race schedule with weather
/streams - Available stream links
```

### Step 12: Test Playwright/Scraper

During an F1 session:

```
/live - Live timing (tests Playwright browser automation)
```

Verify:
- ✅ Real-time updates work
- ✅ Auto-updates every 30 seconds
- ✅ Browser automation successful
- ✅ No timeout errors

---

## 📊 Phase 4: Monitoring & Optimization

### Step 13: Monitor Performance

In Railway dashboard, monitor:

- **Resource Usage**: Should be under 512MB memory for low traffic
- **Monthly Credits**: Track usage vs $5 free credit
- **Uptime**: Should be 99%+
- **Response Times**: Should be under 2 seconds
- **Error Logs**: Check for any issues

### Step 14: Optimize for Cost Efficiency

Expected costs for your usage:
```
Railway Free Credit: $5/month
Your Usage: ~$2-3/month (low traffic)
Net Cost: $0/month
```

Optimization tips:
- Reduce worker threads to 2 if memory usage is high
- Implement efficient caching for API responses
- Monitor Playwright resource usage during F1 sessions

### Step 15: Set Up Alerts

In Railway dashboard → **Settings → Alerts**:

Enable notifications for:
- Service downtime
- High resource usage
- Build failures
- Monthly credit usage

---

## 🔧 Troubleshooting

### Common Issues & Solutions

#### Build Failures
```bash
# Error: Playwright installation failed
Solution: Ensure system dependencies are in Dockerfile
Check: libglib2.0-0, libnss3, libxss1, libasound2 packages
```

#### Bot Not Responding
```bash
# Error: Webhook not receiving updates
Solution: Verify webhook URL configuration
Check: Telegram Bot API response for webhook status
```

#### High Resource Usage
```bash
# Error: Container hitting memory limits
Solution: Reduce worker threads, optimize Playwright usage
Check: Railway dashboard metrics
```

#### Playwright Timeout
```bash
# Error: Browser automation timing out
Solution: Increase timeout settings, ensure sufficient memory
Check: Bot logs for timeout errors
```

### Railway-Specific Debugging

1. **Check Railway logs** in dashboard
2. **Test health endpoints**: `/health`, `/status`
3. **Monitor resource usage** in real-time
4. **Use Railway console** for direct container access

---

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

---

## 📞 Support Resources

### Railway Documentation
- [Railway Docs](https://docs.railway.app)
- [Python Deployment Guide](https://docs.railway.app/deploys/python)
- [Environment Variables](https://docs.railway.app/environment-variables)

### Telegram Bot Resources
- [Telegram Bot API Documentation](https://core.telegram.org/bots/api)
- [python-telegram-bot Library](https://python-telegram-bot.org/)

### F1 API Resources
- [OpenF1 API](https://api.openf1.org/)
- [Jolpica F1 API](https://jolpica.com/)
- [Ergast API](http://ergast.com/mrd/)

---

## ✅ Success Checklist

- [ ] Railway account created and GitHub connected
- [ ] Repository contains all required files
- [ ] `railway.toml` and updated `Dockerfile` added
- [ ] Environment variables configured in Railway
- [ ] Initial deployment successful
- [ ] Health checks passing
- [ ] Telegram webhook configured
- [ ] All bot commands working
- [ ] Playwright scraper functional during F1 sessions
- [ ] Performance monitoring set up
- [ ] Cost tracking enabled

---

## 🎉 You're All Set!

Your F1 Telegram Bot is now ready for deployment on Railway with:

✅ **Completely free hosting** ($5/month credit covers your usage)
✅ **Proper Playwright/browser automation** support
✅ **Always-on availability** for instant Telegram responses
✅ **Professional monitoring** and debugging tools
✅ **Better performance** than other free hosting options

**Ready to deploy?** Follow this guide step-by-step for a successful Railway deployment! 🏎️💨