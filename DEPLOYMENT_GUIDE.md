# F1 Telegram Bot - Complete Leapcell Deployment Guide

This guide provides step-by-step instructions to deploy your F1 Telegram Bot on Leapcell successfully.

## 🚀 Quick Start

### 1. Prerequisites

- **Telegram Bot Token**: Get one from [@BotFather](https://t.me/BotFather)
- **Leapcell Account**: Sign up at [leapcell.io](https://leapcell.io)
- **GitHub Repository**: Push this code to a GitHub repository

### 2. Repository Setup

1. **Clone and Push to GitHub**:
   ```bash
   git clone https://github.com/rufethidoaz-art/f1-bot-leapcell-test.git
   cd f1-bot-leapcell-test
   git add .
   git commit -m "Initial Leapcell deployment setup"
   git push origin main
   ```

2. **Verify Files**: Ensure all files are present:
   ```
   ├── leapcell_f1_bot.py      # Main bot application
   ├── leapcell.yaml           # Leapcell configuration
   ├── Dockerfile              # Container configuration
   ├── requirements.txt        # Python dependencies
   ├── optimized_scraper.py    # Live timing scraper
   ├── final_working_scraper.py # Fallback scraper
   ├── streams.txt             # Default stream links
   ├── user_streams.json       # User stream storage
   └── DEPLOYMENT_GUIDE.md     # This guide
   ```

## 🔧 Leapcell Deployment Steps

### Step 1: Connect Repository

1. Go to [Leapcell Dashboard](https://dashboard.leapcell.io)
2. Click **"Create Service"**
3. Select **"Connect GitHub"**
4. Choose your repository: `f1-bot-leapcell-test`
5. Click **"Connect"**

### Step 2: Configure Service

#### Basic Settings
- **Service Name**: `f1-bot-leapcell-test` (or your preferred name)
- **Region**: Choose closest to your location (e.g., N. Virginia, US East)
- **Branch**: `main` (or your primary branch)
- **Root Directory**: `./`

#### Build & Run Settings
- **Framework Preset**: `Python`
- **Runtime**: `python3.11-slim` (recommended)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn --bind :8080 --workers 1 --worker-class gthread --threads 4 --timeout 120 --keep-alive 5 --max-requests 1000 --max-requests-jitter 100 leapcell_f1_bot:app`
- **Serving Port**: `8080`

#### Environment Variables
Add these environment variables:

| Key | Value | Description |
|-----|-------|-------------|
| `TELEGRAM_BOT_TOKEN` | `YOUR_BOT_TOKEN_HERE` | Your Telegram bot token from @BotFather |
| `PORT` | `8080` | Application port |
| `PYTHON_VERSION` | `3.11.0` | Python version |
| `WORKER_CLASS` | `gthread` | Gunicorn worker class |
| `WORKERS` | `1` | Number of worker processes |
| `THREADS` | `4` | Number of threads per worker |
| `TIMEOUT` | `120` | Request timeout in seconds |
| `MAX_REQUESTS` | `1000` | Max requests per worker |
| `MAX_REQUESTS_JITTER` | `100` | Jitter for max requests |

### Step 3: Resource Configuration

#### Resource Limits
- **Memory**: `512 MB` (minimum), `1024 MB` (recommended)
- **CPU**: `500m` (minimum), `1000m` (recommended)

#### Auto-scaling
- **Enable Auto-scaling**: `Yes`
- **Min Replicas**: `1`
- **Max Replicas**: `3`
- **CPU Threshold**: `70%`
- **Memory Threshold**: `80%`

### Step 4: Advanced Settings

#### Health Checks
- **Health Check Path**: `/health`
- **Readiness Probe Path**: `/health`
- **Liveness Probe Path**: `/health`
- **Initial Delay**: `60 seconds`
- **Check Interval**: `30 seconds`

#### Storage
- **Persistent Storage**: Enable (1GB recommended)
- **Storage Class**: `standard`

### Step 5: Deploy

1. Click **"Deploy"**
2. Wait for build to complete (2-5 minutes)
3. Monitor deployment status in the dashboard

## ✅ Post-Deployment Verification

### 1. Check Service Status

Visit your service URL and verify these endpoints:

- **Health Check**: `https://your-service-url/health`
- **Home Page**: `https://your-service-url/`
- **Bot Status**: `https://your-service-url/status`

Expected responses:
```json
// /health
{"status": "healthy", "service": "F1 Telegram Bot Leapcell Test"}

// /
{
  "status": "F1 Telegram Bot (Leapcell Test) is running!",
  "version": "1.0.0-leapcell",
  "bot_running": true,
  "scrapers_available": {
    "optimized": true,
    "fallback": true
  }
}
```

### 2. Test Telegram Bot

1. **Find Your Bot**: Search for your bot on Telegram using `@YourBotName`
2. **Start Conversation**: Send `/start`
3. **Test Commands**:
   - `/standings` - Driver standings
   - `/constructors` - Constructor standings
   - `/nextrace` - Next race schedule
   - `/lastrace` - Last race results
   - `/live` - Live timing (during active sessions)

## 🔍 Troubleshooting

### Common Issues

#### 1. Bot Not Responding
**Symptoms**: Bot online but doesn't reply to commands
**Solutions**:
- Check `TELEGRAM_BOT_TOKEN` is correct
- Verify webhook is set properly (check logs)
- Ensure bot is running (check `/status` endpoint)

#### 2. Live Timing Not Working
**Symptoms**: `/live` command shows "No live timing data"
**Solutions**:
- Check if F1 session is active (only works during race weekends)
- Verify OpenF1 API access (check logs for API errors)
- Test during official F1 race weekends

#### 3. High Resource Usage
**Symptoms**: Service hitting resource limits
**Solutions**:
- Increase memory allocation to 1GB
- Reduce worker threads to 2
- Enable auto-scaling

#### 4. Build Failures
**Symptoms**: Container build fails
**Solutions**:
- Check Dockerfile syntax
- Verify all required files are present
- Ensure Python version compatibility

### Log Analysis

Check service logs for specific error messages:

```bash
# Common log locations in Leapcell dashboard
- Build logs: During deployment
- Runtime logs: After deployment
- Error logs: For debugging issues
```

### Performance Optimization

#### For Better Performance:
1. **Increase Resources**: 1GB RAM, 1 CPU core
2. **Enable Caching**: Bot uses in-memory caching (automatic)
3. **Optimize Workers**: 1 worker with 4 threads (configured)
4. **Use CDN**: For static assets if added later

#### For Cost Optimization:
1. **Reduce Resources**: 512MB RAM, 500m CPU
2. **Disable Auto-scaling**: Set replicas to 1
3. **Monitor Usage**: Adjust based on actual traffic

## 🛠️ Maintenance

### Updates

1. **Code Updates**: Push to GitHub, auto-deploy will trigger
2. **Dependency Updates**: Update `requirements.txt`, redeploy
3. **Configuration Updates**: Modify `leapcell.yaml`, redeploy

### Monitoring

1. **Health Checks**: Monitor `/health` endpoint
2. **Bot Status**: Check `/status` endpoint
3. **Resource Usage**: Monitor in Leapcell dashboard
4. **Error Logs**: Review logs regularly

### Backups

1. **User Data**: `user_streams.json` is automatically backed up
2. **Configuration**: Keep `leapcell.yaml` in version control
3. **Code**: GitHub repository serves as backup

## 📊 API Endpoints

### Bot Endpoints
- `GET /` - Service status and info
- `GET /health` - Health check
- `GET /status` - Bot status and features
- `POST /webhook` - Telegram webhook (auto-configured)

### Bot Commands
- `/start` - Welcome message
- `/menu` - Show menu
- `/standings` - Driver standings
- `/constructors` - Constructor standings
- `/lastrace` - Last race results
- `/nextrace` - Next race schedule
- `/live` - Live timing (during sessions)
- `/streams` - Stream links
- `/addstream` - Add personal stream
- `/removestream` - Remove stream
- `/playstream` - Get stream link
- `/streamhelp` - Stream help

## 🎯 Best Practices

1. **Environment Variables**: Use for all configuration
2. **Error Handling**: Bot includes comprehensive error handling
3. **Logging**: All important events are logged
4. **Resource Management**: Proper limits and scaling
5. **Security**: Non-root container user, secure dependencies

## 📞 Support

If you encounter issues:

1. **Check Logs**: Review service logs in Leapcell dashboard
2. **Test Endpoints**: Verify `/health` and `/status` endpoints
3. **Review Configuration**: Check environment variables
4. **Consult Documentation**: [Leapcell Docs](https://docs.leapcell.io)

---

**🎉 Congratulations! Your F1 Telegram Bot is now deployed on Leapcell!**

The bot includes:
- ✅ Live F1 timing during race weekends
- ✅ Driver and constructor standings
- ✅ Race schedules with weather forecasts
- ✅ Stream management for users
- ✅ Optimized container deployment
- ✅ Auto-scaling and health monitoring
- ✅ Comprehensive error handling

Start chatting with your bot and enjoy F1 updates in real-time! 🏎️💨