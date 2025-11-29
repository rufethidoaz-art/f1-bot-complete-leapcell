# Railway Testing & Validation Guide

This guide helps you test and validate your F1 Telegram Bot deployment on Railway to ensure everything works correctly before switching from Leapcell.

## 🧪 Pre-Deployment Testing

### 1. Local Testing

Before deploying to Railway, test your updated configuration locally:

#### Docker Build Test
```bash
# Test Docker build with Railway configuration
docker build -t f1-bot-railway .

# Run container locally
docker run -p 8080:8080 -e TELEGRAM_BOT_TOKEN=your_test_token f1-bot-railway

# Test health endpoints
curl http://localhost:8080/health
curl http://localhost:8080/status
```

#### Playwright Testing
```bash
# Test Playwright installation
docker exec -it container_name playwright install chromium

# Test browser functionality
docker exec -it container_name python -c "
from optimized_scraper import get_optimized_live_timing
import asyncio
data = asyncio.run(get_optimized_live_timing())
print('Playwright test:', 'Success' if data else 'Failed')
"
```

### 2. Configuration Validation

Use this script to validate your Railway configuration:

```python
#!/usr/bin/env python3
"""
Railway Deployment Validation Script
Validates configuration for Railway deployment.
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def validate_railway_config():
    """Validate Railway-specific configuration"""
    print("🔍 Validating Railway Configuration...")
    
    errors = []
    warnings = []
    info = []
    
    # Check railway.toml
    if Path('railway.toml').exists():
        info.append("✅ railway.toml found")
        try:
            with open('railway.toml', 'r') as f:
                content = f.read()
                if 'startCommand' in content and 'gunicorn' in content:
                    info.append("✅ Railway start command configured")
                else:
                    errors.append("❌ Invalid start command in railway.toml")
        except Exception as e:
            errors.append(f"❌ Error reading railway.toml: {e}")
    else:
        errors.append("❌ railway.toml not found")
    
    # Check Dockerfile for Railway optimizations
    if Path('Dockerfile').exists():
        with open('Dockerfile', 'r') as f:
            dockerfile_content = f.read()
            
        railway_checks = {
            'ENV PIP_NO_CACHE_DIR=1': 'PIP cache disabled',
            'ENV PIP_DISABLE_PIP_VERSION_CHECK=1': 'PIP version check disabled',
            'xvfb': 'Xvfb for headless browser',
            'HEALTHCHECK': 'Health check configured',
            'USER app': 'Non-root user'
        }
        
        for check, description in railway_checks.items():
            if check in dockerfile_content:
                info.append(f"✅ {description}")
            else:
                warnings.append(f"⚠️ Missing: {description}")
    
    # Check environment variables
    required_env_vars = ['TELEGRAM_BOT_TOKEN', 'PORT']
    for var in required_env_vars:
        if os.getenv(var):
            info.append(f"✅ Environment variable set: {var}")
        else:
            warnings.append(f"⚠️ Environment variable not set: {var}")
    
    # Validate requirements for Railway
    if Path('requirements.txt').exists():
        with open('requirements.txt', 'r') as f:
            requirements = f.read()
            
        railway_packages = [
            'playwright',
            'flask',
            'gunicorn',
            'python-telegram-bot'
        ]
        
        for package in railway_packages:
            if package in requirements:
                info.append(f"✅ Required package: {package}")
            else:
                errors.append(f"❌ Missing package: {package}")
    
    # Docker build test
    try:
        print("\n🐳 Testing Docker build...")
        result = subprocess.run([
            'docker', 'build', '-t', 'f1-bot-railway', '.'
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            info.append("✅ Docker build successful")
            # Clean up
            subprocess.run(['docker', 'rmi', 'f1-bot-railway'], capture_output=True)
        else:
            errors.append(f"❌ Docker build failed: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        warnings.append("⚠️ Docker build timeout")
    except FileNotFoundError:
        warnings.append("⚠️ Docker not installed (skipping build test)")
    except Exception as e:
        warnings.append(f"⚠️ Docker test error: {e}")
    
    # Generate report
    print("\n" + "="*60)
    print("RAILWAY DEPLOYMENT VALIDATION REPORT")
    print("="*60)
    
    print(f"\nSUMMARY:")
    print(f"Info: {len(info)}")
    print(f"Warnings: {len(warnings)}")
    print(f"Errors: {len(errors)}")
    
    if info:
        print(f"\nINFO:")
        for msg in info:
            print(f"  {msg}")
    
    if warnings:
        print(f"\nWARNINGS:")
        for msg in warnings:
            print(f"  {msg}")
    
    if errors:
        print(f"\nERRORS:")
        for msg in errors:
            print(f"  {msg}")
    
    # Recommendations
    print(f"\nRECOMMENDATIONS:")
    if errors:
        print("  🚨 Fix all errors before deployment")
        print("  ⚠️ Address warnings for optimal performance")
    elif warnings:
        print("  ⚠️ Address warnings for optimal performance")
        print("  ✅ All critical components configured")
    else:
        print("  ✅ All validations passed!")
        print("  🚀 Ready for Railway deployment")
    
    return len(errors) == 0

if __name__ == "__main__":
    success = validate_railway_config()
    sys.exit(0 if success else 1)
```

Save this as `validate_railway_deployment.py` and run:
```bash
python validate_railway_deployment.py
```

## 🚀 Post-Deployment Testing

### 1. Railway Dashboard Verification

After deploying to Railway, verify these in the dashboard:

#### Build Status
- ✅ **Build completed successfully**
- ✅ **No build errors or warnings**
- ✅ **Playwright installation successful**
- ✅ **Container started without issues**

#### Service Status
- ✅ **Service is healthy**
- ✅ **Health checks passing**
- ✅ **No restarts or crashes**
- ✅ **Resource usage within limits**

### 2. Endpoint Testing

Test these endpoints after deployment:

#### Health Check
```bash
curl https://your-service.up.railway.app/health
```
Expected response:
```json
{
  "status": "healthy",
  "service": "F1 Telegram Bot Railway Deployment",
  "timestamp": "2024-01-01T00:00:00.000Z"
}
```

#### Bot Status
```bash
curl https://your-service.up.railway.app/status
```
Expected response:
```json
{
  "status": "running",
  "bot_running": true,
  "scrapers_available": {
    "optimized": true,
    "fallback": true
  },
  "timestamp": "2024-01-01T00:00:00.000Z",
  "features": [
    "live_timing",
    "standings",
    "race_schedule",
    "weather_forecast",
    "stream_management"
  ]
}
```

#### Service Info
```bash
curl https://your-service.up.railway.app/
```
Expected response:
```json
{
  "status": "F1 Telegram Bot (Railway) is running!",
  "version": "1.0.0-railway",
  "deployment": "Railway",
  "bot_running": true,
  "features": {
    "containerized": true,
    "webhook_mode": true,
    "optimized_scraping": true,
    "enhanced_error_handling": true
  }
}
```

### 3. Telegram Bot Testing

#### Basic Commands Test
Test these commands with your bot:

1. **Start Command**
   ```
   /start
   ```
   Expected: Welcome message with menu

2. **Standings**
   ```
   /standings
   ```
   Expected: Current driver standings

3. **Constructor Standings**
   ```
   /constructors
   ```
   Expected: Current constructor standings

4. **Next Race**
   ```
   /nextrace
   ```
   Expected: Next race schedule with weather

5. **Last Race**
   ```
   /lastrace
   ```
   Expected: Last race results

#### Live Timing Test (During F1 Session)
If there's an active F1 session:

1. **Live Timing Command**
   ```
   /live
   ```
   Expected: Live timing data with positions

2. **Auto-update Test**
   - Send `/live` command
   - Wait 30 seconds
   - Verify message updates automatically
   - Check logs for successful updates

#### Stream Management Test
1. **List Streams**
   ```
   /streams
   ```
   Expected: Available stream links

2. **Add Stream**
   ```
   /addstream Test | https://example.com/stream.m3u8
   ```
   Expected: Stream added confirmation

3. **Play Stream**
   ```
   /playstream 1
   ```
   Expected: Stream link

### 4. Performance Testing

#### Response Time Test
```bash
# Test response times
time curl -s https://your-service.up.railway.app/health
time curl -s https://your-service.up.railway.app/status
```
Expected: Response times under 2 seconds

#### Concurrent Request Test
```bash
# Test multiple concurrent requests
for i in {1..5}; do
  curl -s https://your-service.up.railway.app/health &
done
wait
```
Expected: All requests complete successfully

#### Memory Usage Check
Monitor in Railway dashboard:
- Memory usage should be under 512MB
- No memory leaks over time
- Stable memory usage during bot commands

### 5. Error Handling Test

#### Invalid Command Test
```
/invalidcommand
```
Expected: "Unknown command" error message

#### API Failure Test
- Simulate API unavailability
- Check if bot handles gracefully with fallback messages

#### Playwright Error Test
- Test during non-F1 periods
- Verify fallback mechanisms work
- Check error messages are user-friendly

## 📊 Monitoring Setup

### Railway Monitoring

Set up monitoring in Railway dashboard:

1. **Enable Alerts**
   - Go to **Settings → Alerts**
   - Set up email notifications for:
     - Service downtime
     - High resource usage
     - Build failures

2. **Monitor Metrics**
   - **CPU Usage**: Should be under 50%
   - **Memory Usage**: Should be under 512MB
   - **Monthly Credits**: Track usage vs $5 free credit
   - **Request Rate**: Monitor traffic patterns

### Log Monitoring

Check Railway logs for:

```bash
# Application startup
2024-01-01 00:00:00 INFO Starting F1 Bot in production mode...
2024-01-01 00:00:00 INFO ✅ Bot setup completed successfully!

# Bot initialization
2024-01-01 00:00:00 INFO 🤖 Bot is ready and waiting for webhook updates...

# Playwright operations
2024-01-01 00:00:00 INFO Playwright browser initialized successfully

# Error tracking
2024-01-01 00:00:00 ERROR [Error details] - Should be minimal
```

### Health Check Monitoring

Set up external health monitoring:

```bash
# Using curl with monitoring
while true; do
  if curl -f https://your-service.up.railway.app/health > /dev/null 2>&1; then
    echo "$(date): Service healthy"
  else
    echo "$(date): Service unhealthy!" | mail -s "Service Alert" your-email@example.com
  fi
  sleep 60
done
```

## 🔄 Migration Validation

### Before Switching Webhook

Ensure these are working on Railway:

- [ ] All basic commands respond correctly
- [ ] Live timing works during F1 sessions
- [ ] Health checks pass consistently
- [ ] No errors in logs for 24 hours
- [ ] Performance is acceptable
- [ ] Playwright scraper works properly

### Webhook Switch Process

1. **Backup Current Setup**
   - Document current Leapcell webhook URL
   - Export user data (`user_streams.json`)
   - Take screenshots of working bot

2. **Update Telegram Webhook**
   ```bash
   # Get new Railway webhook URL
   NEW_WEBHOOK="https://your-service.up.railway.app/webhook"
   
   # Update webhook using Bot API
   curl -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/setWebhook" \
     -d "url=$NEW_WEBHOOK"
   ```

3. **Verify Webhook Update**
   ```bash
   curl "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getWebhookInfo"
   ```
   Should show:
   ```json
   {
     "url": "https://your-service.up.railway.app/webhook",
     "has_custom_certificate": false,
     "pending_update_count": 0,
     "last_error_date": 0,
     "max_connections": 40,
     "ip_address": "railway.app"
   }
   ```

4. **Test Live Bot**
   - Send commands to bot
   - Verify responses come from Railway
   - Check Railway logs for webhook requests

### Post-Migration Monitoring

Monitor for 1 week after migration:

- [ ] Bot responds to all commands
- [ ] No missed webhook requests
- [ ] Performance is stable
- [ ] No data loss
- [ ] Users report no issues

## 📞 Emergency Rollback Plan

If issues arise after migration:

### Immediate Rollback
1. **Revert Webhook**
   ```bash
   curl -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/setWebhook" \
     -d "url=https://your-leapcell-url/webhook"
   ```

2. **Verify Rollback**
   - Test bot commands
   - Confirm responses from original service
   - Check logs for successful fallback

### Investigation
1. **Compare Performance**
   - Response times
   - Error rates
   - Resource usage

2. **Identify Issues**
   - Check Railway logs
   - Compare with Leapcell logs
   - Test individual components

3. **Decision Point**
   - Choose better platform based on data
   - Document lessons learned
   - Plan final migration if Railway works better

---

This comprehensive testing guide ensures your F1 Telegram Bot migration to Railway is successful and reliable! 🧪✅