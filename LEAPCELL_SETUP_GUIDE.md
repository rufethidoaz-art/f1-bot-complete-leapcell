# Leapcell Setup Guide for F1 Telegram Bot

Complete step-by-step instructions to configure your F1 Telegram Bot on Leapcell.

## 🚀 Step 1: Access Leapcell Dashboard

1. Go to [https://dashboard.leapcell.io](https://dashboard.leapcell.io)
2. Sign in with your account (or create one)
3. Click **"Create Service"** button

## 🔗 Step 2: Connect GitHub Repository

### Option A: Automatic Connection
1. Click **"Connect GitHub"**
2. Select your repository: `f1-bot-leapcell-test`
3. Click **"Connect"**

### Option B: Manual Connection
1. Click **"Deploy from Git"**
2. Enter repository URL: `https://github.com/YOUR-USERNAME/f1-bot-leapcell-test.git`
3. Click **"Connect"**

## ⚙️ Step 3: Configure Service Settings

### Basic Settings
- **Service Name**: `f1-bot-leapcell-test` (or your preferred name)
- **Region**: Choose closest to your location
  - **Recommended**: N. Virginia (US East) for best performance
  - **Alternative**: Ireland (EU) for European users
- **Branch**: `main`
- **Root Directory**: `./`

### Build & Run Settings
- **Framework Preset**: `Python`
- **Runtime**: `python3.11-slim` (recommended)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: 
  ```
  gunicorn --bind :8080 --workers 1 --worker-class gthread --threads 4 --timeout 120 --keep-alive 5 --max-requests 1000 --max-requests-jitter 100 leapcell_f1_bot:app
  ```
- **Serving Port**: `8080`

**⚠️ IMPORTANT**: The start command format is critical:
- Use exactly `leapcell_f1_bot:app` (not `your_app.wsgi`)
- This tells Gunicorn to load the Flask app from `leapcell_f1_bot.py`

## 🔧 Step 4: Environment Variables

Click **"Add Environment Variable"** and add these:

| Variable Name | Value | Description |
|---------------|-------|-------------|
| `TELEGRAM_BOT_TOKEN` | `YOUR_BOT_TOKEN_HERE` | Your bot token from @BotFather |
| `PORT` | `8080` | Application port |
| `PYTHON_VERSION` | `3.11.0` | Python version |
| `WORKER_CLASS` | `gthread` | Gunicorn worker class |
| `WORKERS` | `1` | Number of worker processes |
| `THREADS` | `4` | Number of threads per worker |
| `TIMEOUT` | `120` | Request timeout in seconds |
| `MAX_REQUESTS` | `1000` | Max requests per worker |
| `MAX_REQUESTS_JITTER` | `100` | Jitter for max requests |

### How to Get Your Telegram Bot Token
1. Open Telegram and search for **@BotFather**
2. Send `/newbot`
3. Follow the instructions to create your bot
4. BotFather will give you a token like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`
5. Copy this token and paste it in the `TELEGRAM_BOT_TOKEN` field

## 📊 Step 5: Resource Configuration

### Resource Limits
- **Memory**: `512 MB` (minimum) or `1024 MB` (recommended)
- **CPU**: `500m` (minimum) or `1000m` (recommended)

### Auto-scaling Settings
- **Enable Auto-scaling**: `Yes`
- **Min Replicas**: `1`
- **Max Replicas**: `3`
- **CPU Threshold**: `70%`
- **Memory Threshold**: `80%`

## 🏥 Step 6: Health Checks

### Health Check Configuration
- **Health Check Path**: `/health`
- **Readiness Probe Path**: `/health`
- **Liveness Probe Path**: `/health`
- **Initial Delay**: `60 seconds`
- **Check Interval**: `30 seconds`
- **Timeout**: `30 seconds`
- **Failure Threshold**: `3`
- **Success Threshold**: `1`

### Storage Configuration
- **Enable Persistent Storage**: `Yes`
- **Storage Size**: `1 GB`
- **Storage Class**: `standard`

## 🌐 Step 7: Network & Advanced Settings

### Network Configuration
- **Public Access**: `Enabled`
- **HTTPS**: `Auto-enabled`
- **Custom Domain**: Leave empty (use default URL)

### Deployment Strategy
- **Strategy**: `RollingUpdate`
- **Max Unavailable**: `25%`
- **Max Surge**: `25%`

## 🚀 Step 8: Deploy

1. **Review Configuration**: Double-check all settings
2. **Click "Deploy"**: Start the deployment process
3. **Wait for Build**: This takes 2-5 minutes
4. **Monitor Progress**: Watch the deployment logs

## 📋 Step 9: Post-Deployment Verification

### Check Service Status
1. Go to your service dashboard
2. Verify status shows **"Running"**
3. Note your service URL (format: `https://service-name-random-string.leapcell.dev`)

### Test Endpoints
Test these URLs in your browser:

1. **Health Check**: `https://your-service-url/health`
   ```json
   {"status": "healthy", "service": "F1 Telegram Bot Leapcell Test"}
   ```

2. **Home Page**: `https://your-service-url/`
   ```json
   {
     "status": "F1 Telegram Bot (Leapcell Test) is running!",
     "version": "1.0.0-leapcell",
     "bot_running": true
   }
   ```

3. **Bot Status**: `https://your-service-url/status`

### Test Your Telegram Bot
1. Find your bot on Telegram using `@YourBotName`
2. Send `/start` command
3. Test other commands:
   - `/standings` - Driver standings
   - `/constructors` - Constructor standings
   - `/nextrace` - Next race schedule
   - `/lastrace` - Last race results

## 🔧 Troubleshooting Common Issues

### Bot Not Responding
- **Check**: `TELEGRAM_BOT_TOKEN` is correct
- **Verify**: Bot is running (check `/status` endpoint)
- **Test**: Webhook is set properly

### Service Not Starting
- **Check**: Build logs for errors
- **Verify**: All required files are in repository
- **Confirm**: Start command is exactly as specified

### High Resource Usage
- **Increase**: Memory allocation to 1GB
- **Monitor**: Resource usage in dashboard
- **Adjust**: Worker threads if needed

### 502/503 Errors
- **Wait**: For deployment to complete
- **Check**: Application logs
- **Verify**: Port configuration (should be 8080)

## 📊 Monitoring & Maintenance

### Monitor These Metrics
- **CPU Usage**: Should be below 70%
- **Memory Usage**: Should be below 80%
- **Response Time**: Should be under 2 seconds
- **Error Rate**: Should be 0%

### Regular Maintenance
- **Update**: Bot token if expired
- **Monitor**: Logs for errors
- **Check**: Dependencies are up to date
- **Test**: All bot commands regularly

## 🎯 Success! 

Your F1 Telegram Bot is now deployed on Leapcell with:
- ✅ Professional container deployment
- ✅ Auto-scaling and health monitoring
- ✅ Complete error handling and logging
- ✅ Optimized performance settings
- ✅ Live timing and all F1 features

**Start chatting with your bot and enjoy live F1 updates!** 🏎️💨

---

**Need Help?** Check the service logs in Leapcell dashboard or refer to `DEPLOYMENT_GUIDE.md` for detailed troubleshooting.