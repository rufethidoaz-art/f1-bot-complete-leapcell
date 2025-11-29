# F1 Telegram Bot - Diagnostic Guide

This guide helps you diagnose and fix Telegram communication issues in your Render deployment.

## 🚨 Problem Analysis

Based on your description, the bot works locally and on Railway but not on Render. Here are the most likely causes:

### 1. **Webhook Configuration Issues** (Most Likely)
- Render uses different environment variables than Railway
- Webhook URL not properly constructed for Render
- Bot token not being set correctly in Render environment

### 2. **Environment Variable Problems**
- `TELEGRAM_BOT_TOKEN` not set in Render dashboard
- `PORT` variable conflicts (Render uses port 10000 by default)
- Missing `RENDER_EXTERNAL_HOSTNAME`

### 3. **Network/Connectivity Issues**
- Render's network restrictions blocking Telegram API
- Firewall blocking outbound connections
- DNS resolution issues

### 4. **Application Startup Problems**
- Bot setup failing silently
- Flask app not starting properly
- Import/module loading issues

## 🔍 Diagnostic Tools Added

### 1. **Comprehensive Logging** (`f1_bot.py`)
Added diagnostic logging throughout the bot:
- Environment variable checks
- Bot setup progress tracking
- Webhook request/response logging
- API connectivity monitoring
- Command handler execution tracking

### 2. **Diagnostic Test Script** (`diagnostic_test.py`)
Standalone script that tests:
- Python environment and imports
- API connectivity
- Flask app functionality
- Telegram bot setup
- Webhook simulation

### 3. **Diagnostic Runner** (`run_diagnostics.py`)
Orchestrates diagnostic testing and provides summary.

## 📋 Step-by-Step Diagnosis

### Step 1: Run Local Diagnostics

```bash
# Set your bot token
export TELEGRAM_BOT_TOKEN="your-bot-token-here"

# Run diagnostics
python run_diagnostics.py
```

This will:
- Test all components
- Create `bot_diagnostics.log`
- Show any issues found

### Step 2: Check the Diagnostics Log

After running diagnostics, check `bot_diagnostics.log` for:
- Environment variable issues
- API connectivity problems
- Import errors
- Webhook configuration problems

### Step 3: Deploy with Diagnostics

1. **Upload files to Render**:
   - `f1_bot.py` (with diagnostic logging)
   - `diagnostic_test.py`
   - `run_diagnostics.py`
   - `requirements.txt`
   - All other bot files

2. **Set Environment Variables in Render Dashboard**:
   ```
   TELEGRAM_BOT_TOKEN=your-bot-token-here
   PORT=10000
   ```

3. **Deploy and Monitor**:
   - Check Render logs for diagnostic messages
   - Look for "DIAGNOSTIC" entries
   - Identify any errors or warnings

### Step 4: Test After Deployment

1. **Run diagnostics in Render**:
   - Use Render's console or add to startup script
   - Check the output for issues

2. **Test your bot**:
   - Send `/start` to your bot
   - Check if commands work
   - Monitor `bot_diagnostics.log`

## 🎯 Common Fixes

### Fix 1: Webhook URL Issues
The bot now automatically detects Render and constructs the correct webhook URL:
```python
render_url = os.getenv("RENDER_EXTERNAL_HOSTNAME")
if render_url:
    webhook_url = f"https://{render_url}/webhook"
```

### Fix 2: Environment Variables
Ensure these are set in Render:
- `TELEGRAM_BOT_TOKEN`: Your bot token from @BotFather
- `PORT`: Usually `10000` for Render

### Fix 3: Application Entry Point
Use this command in Render for the startup command:
```bash
python run_diagnostics.py && python f1_bot.py
```

### Fix 4: Network Issues
If API calls fail:
- Check Render's network estrictions
- Try different API endpoints
- Verify outbound HTTPS access

## 📊 Interpreting Diagnostic Results

### ✅ Success Indicators
- "✅ Bot setup completed successfully"
- "✅ Webhook set successfully"
- "✅ API data received successfully"
- No ERROR entries in log

### ❌ Failure Indicators
- "❌ No bot token available"
- "❌ Failed to set webhook"
- "❌ API request failed"
- Network timeout errors

## 🔧 Advanced Troubleshooting

### Check Render Environment
```python
# Add this to test.py and run in Render
import os
print("Environment variables:", os.environ.keys())
print("RENDER_EXTERNAL_HOSTNAME:", os.getenv("RENDER_EXTERNAL_HOSTNAME"))
print("PORT:", os.getenv("PORT"))
```

### Test Telegram Connectivity
```python
# Test if bot token works
from telegram import Bot
bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
print("Bot info:", await bot.get_me())
```

### Test Webhook
```python
# Test webhook manually
import requests
response = requests.get(f"https://api.telegram.org/bot{token}/getWebhookInfo")
print(response.json())
```

## 🚀 Deployment Checklist

Before deploying to Render:

- [ ] Set `TELEGRAM_BOT_TOKEN` in Render dashboard
- [ ] Set `PORT=10000` in Render dashboard
- [ ] Upload all files including diagnostic scripts
- [ ] Use startup command: `python run_diagnostics.py && python f1_bot.py`
- [ ] Check Render logs after deployment
- [ ] Send `/start` to test bot functionality
- [ ] Check `bot_diagnostics.log` for detailed information

## 📞 Getting Help

If diagnostics don't resolve the issue:

1. **Share your `bot_diagnostics.log`**
2. **Share Render deployment logs**
3. **Describe what happens when you test the bot**
4. **Check if other Telegram bots work on the same Render account**

The diagnostic logs will show exactly where the communication is failing.