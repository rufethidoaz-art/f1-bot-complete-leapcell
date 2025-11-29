# F1 Telegram Bot - Complete Migration Playbook

## 🎯 Your Solution: From Leapcell to Railway

**Problem Solved**: Technical limitations with Playwright/scraper on Leapcell + usage limits → **Solution**: Completely free, better hosting on Railway with proper browser automation support.

---

## 📋 Quick Start Summary

### The Solution
- **Platform**: Railway (recommended)
- **Cost**: $0 (covered by $5/month free credit)
- **Benefits**: 
  - ✅ Playwright/browser automation works properly
  - ✅ Always-on availability for Telegram bot
  - ✅ Better performance and reliability
  - ✅ Professional monitoring and debugging
  - ✅ Zero cost for your usage level

### Migration Timeline
- **Preparation**: 1-2 hours
- **Setup & Deployment**: 1-2 hours  
- **Testing & Validation**: 2-3 hours
- **Total Time**: 4-7 hours

---

## 🚀 Phase 1: Immediate Setup (Today)

### Step 1: Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub OAuth
3. Install Railway GitHub app
4. Accept repository permissions

### Step 2: Prepare Your Repository
Ensure these files are in your GitHub repository:
```
✅ leapcell_f1_bot.py (main bot application)
✅ requirements.txt (Python dependencies)
✅ optimized_scraper.py (live timing scraper)
✅ final_working_scraper.py (fallback scraper)
✅ streams.txt (default stream links)
✅ user_streams.json (user data)
✅ Dockerfile (container configuration)
```

### Step 3: Add Railway Configuration Files

#### Create `railway.toml`
```toml
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
```

#### Update `Dockerfile` (Railway Optimized)
```dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    wget gnupg gcc python3-dev build-essential curl unzip \
    libglib2.0-0 libnss3 libxss1 libasound2 libappindicator1 \
    libu2f-udev fonts-liberation ca-certificates xvfb \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

RUN playwright install chromium && \
    playwright install-deps chromium

RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app

USER app
COPY --chown=app:app . /app/
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=30s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

CMD ["sh", "-c", "exec gunicorn --bind :8080 --workers 1 --worker-class gthread --threads 4 --timeout 120 --keep-alive 5 --max-requests 1000 --max-requests-jitter 100 leapcell_f1_bot:app"]
```

### Step 4: Deploy to Railway
1. In Railway dashboard, click **"New Project"**
2. Select **"Deploy from GitHub Repo"**
3. Choose your F1 bot repository
4. Click **"Deploy"**

### Step 5: Configure Environment Variables
In Railway dashboard → **Settings → Variables**:
```
PORT=8080
TELEGRAM_BOT_TOKEN=[your_bot_token] (set as Secret)
PYTHON_VERSION=3.11.0
WORKER_CLASS=gthread
WORKERS=1
THREADS=4
TIMEOUT=120
MAX_REQUESTS=1000
MAX_REQUESTS_JITTER=100
```

---

## 🧪 Phase 2: Testing & Validation (Next 2-3 Hours)

### Step 6: Monitor Initial Deployment
Check Railway dashboard for:
- ✅ Build completed successfully
- ✅ Playwright installation successful
- ✅ Container started without errors
- ✅ Health checks passing

### Step 7: Test Endpoints
```bash
# Test health check
curl https://your-service.up.railway.app/health

# Test bot status
curl https://your-service.up.railway.app/status

# Test service info
curl https://your-service.up.railway.app/
```

Expected responses:
```json
// Health check
{"status": "healthy", "service": "F1 Telegram Bot Railway Deployment"}

// Bot status
{"status": "running", "bot_running": true, "scrapers_available": {"optimized": true, "fallback": true}}

// Service info
{"status": "F1 Telegram Bot (Railway) is running!", "version": "1.0.0-railway"}
```

### Step 8: Test Bot Functionality
Test these commands with your Telegram bot:
```
/start - Welcome message
/standings - Driver standings  
/constructors - Constructor standings
/nextrace - Next race schedule
/lastrace - Last race results
```

### Step 9: Test Playwright/Scraper
During an F1 session (if available):
```
/live - Live timing (tests Playwright scraper)
```
- Verify real-time updates work
- Check logs for successful browser automation
- Confirm auto-updates every 30 seconds

---

## 🔄 Phase 3: Migration Execution (When Ready)

### Step 10: Final Validation
Before switching webhook, ensure:
- ✅ All basic commands work correctly
- ✅ Live timing works during F1 sessions
- ✅ Health checks pass consistently
- ✅ No errors in logs for 24 hours
- ✅ Performance is acceptable
- ✅ Playwright scraper works properly

### Step 11: Update Telegram Webhook
**IMPORTANT**: Only after confirming Railway works perfectly!

```bash
# Get new Railway webhook URL
NEW_WEBHOOK="https://your-service.up.railway.app/webhook"

# Update webhook using Bot API
curl -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/setWebhook" \
  -d "url=$NEW_WEBHOOK"
```

### Step 12: Verify Migration
```bash
# Check webhook status
curl "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getWebhookInfo"
```
Should show your Railway URL.

Test bot commands again to confirm responses come from Railway.

---

## 📊 Phase 4: Post-Migration (Ongoing)

### Step 13: Monitor Performance
In Railway dashboard:
- **Resource Usage**: Should be under 512MB memory
- **Monthly Credits**: Track usage vs $5 free credit
- **Uptime**: Should be 99%+
- **Response Times**: Should be under 2 seconds

### Step 14: Keep Leapcell as Backup
Keep your Leapcell deployment running for 1 week as backup:
- Monitor Railway stability
- Have rollback option if needed
- Compare performance between platforms

### Step 15: Cleanup
After 1 week of successful Railway operation:
- [ ] Archive Leapcell deployment
- [ ] Update documentation
- [ ] Celebrate successful migration! 🎉

---

## 💰 Cost Analysis

### Your Expected Costs
```
Railway Free Credit: $5/month
Your Usage: ~$2-3/month (low traffic)
Net Cost: $0/month
Annual Cost: $0
```

### Savings vs Other Options
- **vs Paid hosting**: $60-120/year saved
- **vs Leapcell usage limits**: Unlimited usage within free tier
- **vs Other free hosts**: Better reliability + features

---

## 🚨 Troubleshooting

### Common Issues & Solutions

#### Build Failures
```bash
# Error: Playwright installation failed
Solution: Ensure system dependencies in Dockerfile are correct
```

#### Bot Not Responding
```bash
# Error: Webhook not receiving updates
Solution: Verify webhook URL is correctly set to Railway endpoint
```

#### High Resource Usage
```bash
# Error: Container hitting memory limits
Solution: Reduce worker threads to 2, optimize Playwright usage
```

#### Playwright Timeout
```bash
# Error: Browser automation timing out
Solution: Increase timeout settings, ensure sufficient memory
```

### Emergency Rollback
If issues arise after webhook switch:
```bash
# Revert to Leapcell
curl -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/setWebhook" \
  -d "url=https://your-leapcell-url/webhook"
```

---

## 📞 Support Resources

### Railway Documentation
- [Railway Docs](https://docs.railway.app)
- [Python Deployment](https://docs.railway.app/deploys/python)
- [Environment Variables](https://docs.railway.app/environment-variables)

### F1 Bot Support
- [`DEPLOYMENT_GUIDE.md`](DEPLOYMENT_GUIDE.md) - Original deployment guide
- [`DEPLOYMENT_FIX_GUIDE.md`](DEPLOYMENT_FIX_GUIDE.md) - Troubleshooting
- [`validate_deployment.py`](validate_deployment.py) - Validation script

### Migration Guides Created
- [`Railway_Migration_Guide.md`](Railway_Migration_Guide.md) - Complete migration process
- [`Railway_Configuration_Files.md`](Railway_Configuration_Files.md) - Configuration details
- [`Railway_Testing_Guide.md`](Railway_Testing_Guide.md) - Testing procedures
- [`Hosting_Comparison_Analysis.md`](Hosting_Comparison_Analysis.md) - Platform comparison

---

## ✅ Success Checklist

### Before Migration
- [ ] Railway account created
- [ ] Repository updated with Railway files
- [ ] Environment variables configured
- [ ] Initial deployment successful
- [ ] All tests pass
- [ ] Playwright scraper working

### After Migration
- [ ] Webhook updated to Railway
- [ ] Bot responding from new platform
- [ ] Users report no issues
- [ ] Performance improved
- [ ] Costs are $0
- [ ] Technical limitations resolved

---

## 🎯 Final Outcome

**Before Migration:**
- ❌ Playwright scraper not working on Leapcell
- ❌ Technical limitations and usage issues
- ❌ Poor browser automation support
- ❌ Usage limits causing problems

**After Migration:**
- ✅ **Completely free hosting** with $5/month credit
- ✅ **Always-on availability** for Telegram bot
- ✅ **Proper Playwright support** for F1 live timing
- ✅ **Better performance** and reliability
- ✅ **Zero cost** for your usage level
- ✅ **Resolved all technical limitations**

**Ready to migrate?** Follow this playbook step-by-step for a successful transition to Railway! 🚀

---

## 📞 Need Help?

If you encounter issues during migration:

1. **Check logs** in Railway dashboard
2. **Test endpoints** using curl commands above
3. **Review troubleshooting** section
4. **Use validation scripts** provided
5. **Keep Leapcell as backup** during transition
6. **Rollback is always possible** if needed

**You've got this!** The migration will resolve your Playwright issues and provide completely free, better hosting for your F1 Telegram Bot. 🏎️💨