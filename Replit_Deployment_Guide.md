# F1 Telegram Bot - Replit Deployment Guide

## 🚀 Completely Free Hosting on Replit

This guide provides step-by-step instructions to deploy your F1 Telegram Bot on Replit with proper Playwright/browser automation support.

## 🎯 Why Replit?

### Perfect for Your F1 Bot Requirements:
- ✅ **Completely free** hosting with generous resource limits
- ✅ **Excellent Playwright support** with full browser automation
- ✅ **Always-on availability** for 24/7 Telegram bot functionality
- ✅ **Easy setup** with minimal configuration required
- ✅ **Built-in package management** with Replit's package manager
- ✅ **Live debugging** and real-time monitoring

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
```

### Environment Variables Needed:
- `TELEGRAM_BOT_TOKEN` - Your Telegram bot token from @BotFather
- `REPL_SLUG` - Your Replit project name (auto-set)
- `REPL_OWNER` - Your Replit username (auto-set)

---

## 🔧 Phase 1: Replit Setup

### Step 1: Create Replit Account

1. Go to [replit.com](https://replit.com)
2. Sign up for a free account
3. Verify your email address
4. Log in to your account

### Step 2: Create New Python Repl

1. Click **"Create Repl"** (green button)
2. Select **"Python"** template
3. Name your repl: `f1-telegram-bot`
4. Choose **"Public"** (required for web hosting)
5. Click **"Create Repl"**

### Step 3: Import Your Code

#### Option A: GitHub Import (Recommended)
1. In your Replit project, click **"Import from GitHub"**
2. Enter your GitHub repository URL
3. Select the repository
4. Click **"Import"**

#### Option B: Manual Upload
1. Download all files from your local project
2. In Replit, delete the default `main.py`
3. Upload your files using the file manager
4. Ensure all 19 files are uploaded correctly

### Step 4: Install Dependencies

In Replit's shell (bottom panel), run:

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Verify installation
python -c "import playwright; print('✅ Playwright installed')"
```

---

## 🚀 Phase 2: Configuration

### Step 5: Update Main Files

#### Update `f1_bot.py` for Replit

Add Replit-specific configuration at the top of your `f1_bot.py`:

```python
# Replit-specific configuration
import os

# Get Replit environment variables
REPL_SLUG = os.getenv('REPL_SLUG', 'f1-telegram-bot')
REPL_OWNER = os.getenv('REPL_OWNER', 'your-username')
REPLIT_URL = f"https://{REPL_SLUG}.{REPL_OWNER}.repl.co"

# Use Replit URL for webhook if available
def get_webhook_url():
    if REPL_SLUG and REPL_OWNER:
        return f"{REPLIT_URL}/webhook"
    return "http://localhost:8080/webhook"
```

#### Update Webhook Configuration

In the `setup_bot()` function, update the webhook URL logic:

```python
def setup_webhook():
    try:
        # Get the webhook URL from Replit environment
        webhook_url = os.getenv("WEBHOOK_URL")
        if not webhook_url:
            # Use Replit URL if available
            if REPL_SLUG and REPL_OWNER:
                webhook_url = f"https://{REPL_SLUG}.{REPL_OWNER}.repl.co/webhook"
            else:
                webhook_url = "http://localhost:8080/webhook"

        logger.info(f"Setting up webhook: {webhook_url}")
        # ... rest of webhook setup
```

### Step 6: Configure Environment Variables

In Replit, click the **"Secrets"** button (lock icon) in the sidebar:

Add these environment variables:

| Key | Value | Description |
|-----|-------|-------------|
| `TELEGRAM_BOT_TOKEN` | `your_bot_token` | Your Telegram bot token from @BotFather |
| `PORT` | `8080` | Application port (Replit standard) |
| `REPL_SLUG` | `f1-telegram-bot` | Your repl name (auto-set) |
| `REPL_OWNER` | `your-username` | Your Replit username (auto-set) |

### Step 7: Create Replit Configuration Files

#### Create `.replit` file

Create a `.replit` file in your project root:

```toml
# Replit configuration for F1 Telegram Bot
run = "python f1_bot.py"
language = "python"
env = ["PORT=8080"]

# Enable web preview
web-preview = true
web-preview-port = 8080

# Enable persistent storage
storage = true
```

#### Update `requirements.txt` for Replit

Ensure your `requirements.txt` includes all necessary packages:

```txt
python-telegram-bot==20.7
flask==2.3.3
gunicorn==21.2.0
requests==2.31.0
playwright==1.40.0
beautifulsoup4==4.12.2
lxml==4.9.3
python-dateutil==2.8.2
orjson==3.9.10
```

---

## 🧪 Phase 3: Testing & Validation

### Step 8: Test Local Functionality

In Replit's shell, test your bot:

```bash
# Test Python imports
python -c "
import f1_bot
import optimized_scraper
import fallback_scraper
print('✅ All imports successful')
"

# Test basic functionality
python -c "
from f1_bot import get_current_standings
result = get_current_standings()
print('✅ Standings function works' if result else '❌ Failed')
"

# Test Playwright
python -c "
from optimized_scraper import get_optimized_live_timing
import asyncio
data = asyncio.run(get_optimized_live_timing())
print('✅ Playwright works' if data else '⚠️ No data (may be normal)')
"
```

### Step 9: Start Your Bot

In Replit's shell, start your bot:

```bash
# Start the bot
python f1_bot.py
```

You should see:
```
✅ Bot setup completed successfully!
🤖 Bot is ready and waiting for webhook updates...
```

### Step 10: Test Web Endpoints

Click the **"Web Preview"** button in Replit to open your bot's web interface:

Test these endpoints:
- `https://f1-telegram-bot.your-username.repl.co/health`
- `https://f1-telegram-bot.your-username.repl.co/status`
- `https://f1-telegram-bot.your-username.repl.co/`

Expected responses:
```json
// Health endpoint
{"status": "healthy", "service": "F1 Telegram Bot Replit Deployment"}

// Status endpoint
{"status": "running", "bot_running": true, "features": ["live_timing", "standings"]}
```

---

## 🤖 Phase 4: Telegram Integration

### Step 11: Configure Telegram Webhook

In Replit's shell, configure your Telegram webhook:

```bash
# Replace with your actual bot token and Replit URL
BOT_TOKEN="your_bot_token_here"
REPLIT_URL="https://f1-telegram-bot.your-username.repl.co"

# Set webhook
curl -X POST "https://api.telegram.org/bot$BOT_TOKEN/setWebhook" \
  -d "url=$REPLIT_URL/webhook"

# Verify webhook
curl "https://api.telegram.org/bot$BOT_TOKEN/getWebhookInfo"
```

Expected response:
```json
{
  "ok": true,
  "result": {
    "url": "https://f1-telegram-bot.your-username.repl.co/webhook",
    "has_custom_certificate": false,
    "pending_update_count": 0,
    "ip_address": "xxx.xxx.xxx.xxx",
    "last_error_date": 0,
    "last_error_message": "",
    "max_connections": 40,
    "allowed_updates": []
  }
}
```

### Step 12: Test Your Telegram Bot

1. Find your bot on Telegram: `@YourBotName`
2. Send `/start` to begin
3. Test these commands:
   - `/standings` - Driver standings
   - `/constructors` - Constructor standings
   - `/nextrace` - Next race schedule
   - `/lastrace` - Last race results

### Step 13: Test Live Timing

During an F1 session (if available):
- Send `/live` to test live timing
- Verify real-time updates work
- Check that Playwright browser automation functions properly

---

## 📊 Phase 5: Monitoring & Optimization

### Step 14: Enable Always-On (Replit Pro)

For 24/7 availability:

1. **Upgrade to Replit Pro** (free tier has sleep limitations)
2. In your repl settings, enable **"Always On"**
3. This prevents your bot from sleeping when inactive

### Step 15: Monitor Resource Usage

In Replit dashboard:
- **Memory usage**: Should stay under 512MB
- **CPU usage**: Monitor for optimization needs
- **Storage**: Track persistent storage usage
- **Uptime**: Monitor bot availability

### Step 16: Set Up Alerts

Enable notifications in Replit:
- **Email notifications** for errors
- **Discord/Slack integration** (if available)
- **Uptime monitoring** with external services

---

## 🔧 Troubleshooting

### Common Issues & Solutions

#### Bot Not Responding
```bash
# Error: Bot not responding to commands
Solution: Check webhook configuration and Replit URL
Check: Ensure "Always On" is enabled (Pro feature)
```

#### Playwright Errors
```bash
# Error: Browser automation failed
Solution: Reinstall Playwright browsers in Replit shell
Command: playwright install chromium
```

#### High Resource Usage
```bash
# Error: Memory/CPU limits exceeded
Solution: Optimize bot functions and reduce worker threads
Check: Monitor in Replit dashboard
```

#### Webhook Not Working
```bash
# Error: Webhook not receiving updates
Solution: Verify Replit URL is accessible
Check: Test webhook URL with curl
```

### Replit-Specific Debugging

1. **Check Replit logs** in the shell output
2. **Test endpoints** using Web Preview
3. **Monitor resource usage** in Replit dashboard
4. **Use Replit's debugging tools** for Python

---

## 💰 Cost Analysis

### Replit Pricing for Your Usage

**Free Tier:**
- ✅ **Free hosting** with limitations
- ⚠️ **Sleeps after 30 minutes** of inactivity (bad for Telegram bots)
- ⚠️ **Limited resources** (may struggle with Playwright)

**Pro Tier ($7/month):**
- ✅ **Always-On** availability (no sleeping)
- ✅ **Better resources** for Playwright/browser automation
- ✅ **Priority support** and features
- ✅ **Custom domains** (optional)

**Recommended:** **Replit Pro** for reliable Telegram bot hosting

### Cost Comparison

| Platform | Free Tier | Pro Tier | Always-On | Playwright Support |
|----------|-----------|----------|-----------|-------------------|
| **Replit** | Free | $7/month | Pro only | ✅ Excellent |
| Railway | Free | Pay-as-you-go | ✅ Free | ✅ Excellent |
| Render | Free | $7+/month | Free (sleeps) | ✅ Good |
| Fly.io | Free | $10+/month | ✅ Free | ✅ Good |

---

## 📈 Performance Optimization

### For Better Performance on Replit

1. **Optimize Playwright usage**:
   - Cache browser instances
   - Limit concurrent scraping
   - Use efficient selectors

2. **Reduce resource usage**:
   - Implement proper cleanup
   - Use efficient data structures
   - Limit API calls

3. **Improve response times**:
   - Enable caching for API responses
   - Optimize database queries
   - Use async/await properly

### Replit-Specific Optimizations

1. **Use Replit's built-in package manager**
2. **Enable "Always On"** for consistent availability
3. **Monitor resource usage** and optimize accordingly
4. **Use persistent storage** for user data

---

## 📞 Support Resources

### Replit Documentation
- [Replit Docs](https://docs.replit.com)
- [Python Hosting Guide](https://docs.replit.com/hosting/python)
- [Environment Variables](https://docs.replit.com/programming-ide/storing-sensitive-information)

### Telegram Bot Resources
- [Telegram Bot API Documentation](https://core.telegram.org/bots/api)
- [python-telegram-bot Library](https://python-telegram-bot.org/)

### F1 API Resources
- [OpenF1 API](https://api.openf1.org/)
- [Jolpica F1 API](https://jolpica.com/)
- [Ergast API](http://ergast.com/mrd/)

---

## ✅ Success Checklist

### Before Going Live
- [ ] Replit account created and verified
- [ ] Project imported and configured
- [ ] Dependencies installed successfully
- [ ] Environment variables set
- [ ] Bot starts without errors
- [ ] Web endpoints respond correctly
- [ ] Telegram webhook configured
- [ ] All bot commands working
- [ ] Playwright scraper functional
- [ ] "Always On" enabled (Pro required)

### After Deployment
- [ ] Bot responding from Replit URL
- [ ] Users report no issues
- [ ] Performance is acceptable
- [ ] Resource usage is within limits
- [ ] No unexpected errors in logs

---

## 🎉 You're All Set!

Your F1 Telegram Bot is now ready for deployment on Replit with:

✅ **Completely free hosting** (with Pro for "Always On")
✅ **Excellent Playwright/browser automation** support
✅ **Always-on availability** for instant Telegram responses
✅ **Easy management** through Replit interface
✅ **Real-time debugging** and monitoring capabilities

### Next Steps:
1. **Test thoroughly** using the steps above
2. **Upgrade to Pro** if needed for "Always On" availability
3. **Configure webhook** and start using your bot
4. **Monitor performance** and optimize as needed

**Ready to deploy?** Follow this guide step-by-step for a successful Replit deployment! 🏎️💨

---

## 📞 Need Help?

If you encounter issues during deployment:

1. **Check Replit logs** in the shell output
2. **Test endpoints** using Web Preview
3. **Verify webhook configuration** with curl commands
4. **Review troubleshooting** section
5. **Consult Replit documentation** for platform-specific issues

**You've got this!** Replit provides an excellent platform for hosting your F1 Telegram Bot with proper Playwright support and easy management. 🚀
