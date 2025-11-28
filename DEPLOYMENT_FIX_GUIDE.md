# F1 Bot Deployment Fix Guide

## Issue: Build Failed - psutil Compilation Error

The build failed because `psutil` requires compilation tools that weren't available during the build process.

## Solution Applied

### 1. Updated Dockerfile
The Dockerfile has been updated with proper system dependencies:

```dockerfile
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
```

### 2. Updated Requirements
Modified `requirements.txt` to handle psutil compilation issues more gracefully.

## Next Steps

### Option 1: Redeploy with Current Configuration
1. Go to your Leapcell dashboard
2. Find your failed deployment
3. Click "Redeploy" or "Restart Deployment"
4. The build should now succeed with the updated Dockerfile

### Option 2: Force New Build
1. Go to your Leapcell dashboard
2. Delete the current deployment
3. Create a new deployment from the same repository
4. Use the same settings from [`LEAPCELL_SETUP_GUIDE.md`](LEAPCELL_SETUP_GUIDE.md)

### Option 3: Manual Trigger
If automatic redeployment doesn't work:
1. Make a small change to any file (like adding a comment)
2. Commit and push to trigger a new build
3. The updated Dockerfile will be used

## Expected Build Process

The new build should:
1. ✅ Install system dependencies including `gcc` and `python3-dev`
2. ✅ Successfully compile psutil
3. ✅ Install all Python dependencies
4. ✅ Install Playwright browsers
5. ✅ Complete successfully

## Monitoring the Fix

After redeployment:
1. Check the build logs for successful psutil installation
2. Verify the application starts without errors
3. Test the bot functionality

## If Issues Persist

If you still encounter build issues:

1. **Check Build Logs**: Look for specific error messages
2. **Reduce Dependencies**: Consider removing non-essential packages
3. **Alternative Approach**: Use a simpler requirements.txt with only essential packages

### Minimal Requirements (if needed):
```txt
python-telegram-bot==20.7
flask==2.3.3
gunicorn==21.2.0
requests==2.31.0
beautifulsoup4==4.12.2
lxml==4.9.3
python-dateutil==2.8.2
```

## Success Indicators

✅ Build completes without errors
✅ Container starts successfully
✅ Health check passes
✅ Bot responds to commands

The deployment should now work correctly with the updated configuration!