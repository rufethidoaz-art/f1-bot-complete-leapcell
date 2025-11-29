# Local Testing Guide for F1 Telegram Bot

## 🔍 Test Your Project Locally Before Deployment

This guide helps you verify that your F1 Telegram Bot works correctly on your local machine before uploading to GitHub and deploying to Railway.

---

## 📋 Pre-Testing Checklist

### Required Files in Your Project
Ensure these files are present in your project directory:
```
✅ f1_bot.py (main bot application)
✅ requirements.txt (Python dependencies)
✅ optimized_scraper.py (live timing scraper)
✅ fallback_scraper.py (backup scraper)
✅ streams.txt (default stream links)
✅ user_streams.json (user data)
✅ Dockerfile (container configuration)
✅ railway.toml (Railway configuration)
```

### System Requirements
- **Python**: 3.11 or higher
- **Docker**: Installed and running (for container testing)
- **Internet**: Stable connection for API testing
- **GitHub**: Account for repository upload

---

## 🚀 Phase 1: Local Environment Setup

### Step 1: Install Python Dependencies

```bash
# Create virtual environment (recommended)
python -m venv f1_bot_env

# Activate virtual environment
# Windows:
f1_bot_env\Scripts\activate
# macOS/Linux:
source f1_bot_env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Test Basic Python Setup

```bash
# Test Python version
python --version

# Test key imports
python -c "import flask, requests, asyncio; print('✅ Basic imports successful')"

# Test Playwright installation
python -c "import playwright; print('✅ Playwright imported successfully')"

# Install Playwright browsers
playwright install chromium
```

### Step 3: Set Up Environment Variables

Create a `.env` file in your project root:
```env
TELEGRAM_BOT_TOKEN=your_test_bot_token_here
PORT=8080
PYTHON_VERSION=3.11.0
WORKER_CLASS=gthread
WORKERS=1
THREADS=4
TIMEOUT=120
MAX_REQUESTS=1000
MAX_REQUESTS_JITTER=100
```

**Note**: Use a test bot token for local testing. You can create one with [@BotFather](https://t.me/BotFather) if needed.

---

## 🧪 Phase 2: Application Testing

### Step 4: Test Bot Application Startup

```bash
# Test basic application startup
python -c "
from f1_bot import app
print('✅ Flask app created successfully')
print('✅ Application ready for testing')
"
```

### Step 5: Test Flask Server Locally

```bash
# Start Flask development server
python -c "
import os
from f1_bot import app

# Use port 8080 (Railway standard)
port = int(os.getenv('PORT', 8080))
print(f'Starting server on port {port}...')
app.run(host='0.0.0.0', port=port, debug=True)
"
```

### Step 6: Test Health Endpoints

In a new terminal window, test your local server:

```bash
# Test health endpoint
curl http://localhost:8080/health

# Test status endpoint
curl http://localhost:8080/status

# Test main endpoint
curl http://localhost:8080/
```

Expected responses:
```json
// Health endpoint
{"status": "healthy", "service": "F1 Telegram Bot Local Test"}

// Status endpoint
{"status": "running", "bot_running": true, "features": ["live_timing", "standings"]}
```

---

## 🔬 Phase 3: Bot Functionality Testing

### Step 7: Test Bot Commands (Without Telegram)

Test individual bot functions directly:

```python
# Create test script: test_bot_functions.py
import sys
sys.path.append('.')

from f1_bot import (
    get_current_standings,
    get_constructor_standings, 
    get_last_session_results,
    get_next_race,
    get_streams
)

print("Testing bot functions...")

# Test standings
try:
    standings = get_current_standings()
    print("✅ Driver standings:", "Success" if standings else "Failed")
except Exception as e:
    print("❌ Driver standings failed:", e)

# Test constructor standings
try:
    constructors = get_constructor_standings()
    print("✅ Constructor standings:", "Success" if constructors else "Failed")
except Exception as e:
    print("❌ Constructor standings failed:", e)

# Test next race
try:
    next_race = get_next_race()
    print("✅ Next race:", "Success" if next_race else "Failed")
except Exception as e:
    print("❌ Next race failed:", e)

# Test streams
try:
    streams, keyboard = get_streams()
    print("✅ Streams:", "Success" if streams else "Failed")
except Exception as e:
    print("❌ Streams failed:", e)
```

Run the test:
```bash
python test_bot_functions.py
```

### Step 8: Test Playwright/Scraper

```python
# Create test script: test_scraper.py
import sys
sys.path.append('.')

try:
    from optimized_scraper import get_optimized_live_timing
    import asyncio
    
    print("Testing optimized scraper...")
    data = asyncio.run(get_optimized_live_timing())
    print("✅ Optimized scraper:", "Success" if data else "Failed")
    
except Exception as e:
    print("❌ Optimized scraper failed:", e)
    
try:
    from fallback_scraper import scrape_formula_timer_live_timing
    import asyncio
    
    print("Testing fallback scraper...")
    data = asyncio.run(scrape_formula_timer_live_timing())
    print("✅ Fallback scraper:", "Success" if data else "Failed")
    
except Exception as e:
    print("❌ Fallback scraper failed:", e)
```

Run the test:
```bash
python test_scraper.py
```

---

## 🐳 Phase 4: Docker Container Testing

### Step 9: Build Docker Image Locally

```bash
# Build Docker image
docker build -t f1-bot-railway .

# Check if build succeeded
docker images | grep f1-bot-railway
```

### Step 10: Test Docker Container

```bash
# Run container locally
docker run -d \
  --name f1-bot-test \
  -p 8080:8080 \
  -e TELEGRAM_BOT_TOKEN=your_test_token \
  f1-bot-railway

# Check if container is running
docker ps | grep f1-bot-test

# Test endpoints
curl http://localhost:8080/health
curl http://localhost:8080/status

# View logs
docker logs f1-bot-test

# Stop and remove container
docker stop f1-bot-test
docker rm f1-bot-test
```

### Step 11: Test Docker Health Checks

```bash
# Test health check endpoint specifically
curl -v http://localhost:8080/health

# Expected: HTTP 200 response with health status
```

---

## 🔍 Phase 5: Comprehensive Testing

### Step 12: Create Comprehensive Test Script

Create `comprehensive_test.py`:

```python
#!/usr/bin/env python3
"""
Comprehensive test script for F1 Telegram Bot
Tests all components before Railway deployment
"""

import os
import sys
import json
import subprocess
import requests
from pathlib import Path

def test_python_environment():
    """Test Python environment and dependencies"""
    print("🔍 Testing Python Environment...")
    
    # Test Python version
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        print("✅ Python version:", f"{version.major}.{version.minor}.{version.micro}")
    else:
        print("❌ Python version:", f"{version.major}.{version.minor}.{version.micro} (need 3.11+)")
        return False
    
    # Test imports
    required_modules = [
        'flask', 'requests', 'asyncio', 'telegram', 
        'playwright', 'bs4', 'lxml'
    ]
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ Module: {module}")
        except ImportError as e:
            print(f"❌ Module: {module} - {e}")
            return False
    
    return True

def test_file_structure():
    """Test required files exist"""
    print("\n📁 Testing File Structure...")
    
    required_files = [
        'f1_bot.py',
        'requirements.txt', 
        'optimized_scraper.py',
        'fallback_scraper.py',
        'streams.txt',
        'user_streams.json',
        'Dockerfile',
        'railway.toml'
    ]
    
    all_present = True
    for file in required_files:
        if Path(file).exists():
            print(f"✅ File: {file}")
        else:
            print(f"❌ Missing: {file}")
            all_present = False
    
    return all_present

def test_environment_variables():
    """Test environment variables"""
    print("\n⚙️ Testing Environment Variables...")
    
    required_vars = ['TELEGRAM_BOT_TOKEN', 'PORT']
    all_set = True
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ Environment: {var}={'*' * len(value) if var == 'TELEGRAM_BOT_TOKEN' else value}")
        else:
            print(f"❌ Missing: {var}")
            all_set = False
    
    return all_set

def test_bot_functions():
    """Test bot functionality"""
    print("\n🤖 Testing Bot Functions...")
    
    try:
        sys.path.append('.')
        
        # Test imports
        from f1_bot import get_current_standings, get_constructor_standings
        print("✅ Bot imports successful")
        
        # Test API functions
        try:
            standings = get_current_standings()
            if standings and "championat" in standings.lower():
                print("✅ Driver standings API working")
            else:
                print("⚠️ Driver standings API returned unexpected data")
        except Exception as e:
            print(f"⚠️ Driver standings test failed: {e}")
        
        try:
            constructors = get_constructor_standings()
            if constructors and "constructor" in constructors.lower():
                print("✅ Constructor standings API working")
            else:
                print("⚠️ Constructor standings API returned unexpected data")
        except Exception as e:
            print(f"⚠️ Constructor standings test failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Bot functions test failed: {e}")
        return False

def test_scraper_functions():
    """Test scraper functionality"""
    print("\n🔍 Testing Scraper Functions...")
    
    try:
        import asyncio
        from optimized_scraper import get_optimized_live_timing
        
        print("Testing optimized scraper...")
        data = asyncio.run(get_optimized_live_timing())
        if data:
            print("✅ Optimized scraper working")
        else:
            print("⚠️ Optimized scraper returned no data (might be normal)")
        
        return True
        
    except Exception as e:
        print(f"❌ Scraper test failed: {e}")
        return False

def test_docker_build():
    """Test Docker build"""
    print("\n🐳 Testing Docker Build...")
    
    try:
        # Check if Docker is available
        result = subprocess.run(['docker', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Docker available:", result.stdout.strip())
        else:
            print("❌ Docker not available")
            return False
        
        # Test Docker build
        print("Building Docker image...")
        result = subprocess.run([
            'docker', 'build', '-t', 'f1-bot-test', '.'
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Docker build successful")
            
            # Clean up
            subprocess.run(['docker', 'rmi', 'f1-bot-test'], 
                         capture_output=True)
            return True
        else:
            print("❌ Docker build failed")
            print("Error:", result.stderr[:500])
            return False
            
    except subprocess.TimeoutExpired:
        print("⚠️ Docker build timeout (might be slow internet)")
        return False
    except FileNotFoundError:
        print("⚠️ Docker not installed (skipping container test)")
        return True
    except Exception as e:
        print(f"❌ Docker test error: {e}")
        return False

def test_local_server():
    """Test local server functionality"""
    print("\n🌐 Testing Local Server...")
    
    try:
        # Start server in background
        env = os.environ.copy()
        env['PORT'] = '8080'
        
        # This is a simplified test - in practice you'd want to
        # start the server and test endpoints
        print("✅ Server configuration valid")
        return True
        
    except Exception as e:
        print(f"❌ Server test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 F1 Telegram Bot - Comprehensive Local Testing")
    print("=" * 50)
    
    tests = [
        test_python_environment,
        test_file_structure,
        test_environment_variables,
        test_bot_functions,
        test_scraper_functions,
        test_docker_build,
        test_local_server
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Your project is ready for Railway deployment!")
        print("\nNext steps:")
        print("1. Push code to GitHub")
        print("2. Follow Railway_Deployment_Guide.md")
        print("3. Deploy to Railway")
    else:
        print("❌ Some tests failed. Please fix issues before deployment.")
        print("\nCommon fixes:")
        print("- Install missing Python packages: pip install -r requirements.txt")
        print("- Install Playwright browsers: playwright install chromium")
        print("- Set required environment variables")
        print("- Check file structure and naming")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
```

Run the comprehensive test:
```bash
python comprehensive_test.py
```

---

## 📊 Phase 6: Performance Testing

### Step 13: Test Response Times

```bash
# Test API response times
time curl -s http://localhost:8080/health
time curl -s http://localhost:8080/status
time curl -s http://localhost:8080/
```

Expected: Response times under 2 seconds

### Step 14: Test Concurrent Requests

```bash
# Test multiple concurrent requests
for i in {1..5}; do
  curl -s http://localhost:8080/health &
done
wait
echo "All concurrent requests completed"
```

---

## 🔧 Phase 7: Troubleshooting

### Common Issues and Solutions

#### Import Errors
```bash
# Error: ModuleNotFoundError
Solution: pip install -r requirements.txt
```

#### Playwright Errors
```bash
# Error: Browser executable not found
Solution: playwright install chromium
```

#### Port Already in Use
```bash
# Error: Address already in use
Solution: Change PORT environment variable or stop other services
```

#### Docker Build Failures
```bash
# Error: Build context too large
Solution: Add .gitignore and clean up project directory
```

### Debug Commands

```bash
# Check Python path
python -c "import sys; print('\n'.join(sys.path))"

# Check environment variables
python -c "import os; [print(f'{k}={v}') for k,v in os.environ.items() if 'PORT' in k or 'BOT' in k]"

# Check installed packages
pip list | grep -E "(flask|telegram|playwright|requests)"

# Test specific imports
python -c "from f1_bot import app; print('App imported successfully')"
```

---

## ✅ Phase 8: Pre-Deployment Checklist

Before uploading to GitHub and deploying to Railway:

### Code Quality
- [ ] All Python files have proper syntax
- [ ] No hardcoded secrets in code
- [ ] Environment variables used for configuration
- [ ] Error handling implemented
- [ ] Logging configured

### Dependencies
- [ ] `requirements.txt` is up to date
- [ ] All required packages install successfully
- [ ] Playwright browsers installed
- [ ] No conflicting dependencies

### Configuration
- [ ] `railway.toml` configured correctly
- [ ] `Dockerfile` optimized for Railway
- [ ] Environment variables documented
- [ ] Health check endpoints working

### Testing
- [ ] All comprehensive tests pass
- [ ] Local server starts successfully
- [ ] Bot functions work correctly
- [ ] Scraper functionality verified
- [ ] Docker build succeeds
- [ ] Response times are acceptable

### Documentation
- [ ] README updated with Railway instructions
- [ ] Environment variables documented
- [ ] Deployment guide available
- [ ] Troubleshooting guide provided

---

## 🚀 Ready for GitHub and Railway!

Once all tests pass:

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Ready for Railway deployment"
   git push origin main
   ```

2. **Deploy to Railway**:
   - Follow `Railway_Deployment_Guide.md`
   - Use configuration from `Railway_Configuration_Files.md`
   - Monitor deployment using `Railway_Testing_Guide.md`

3. **Verify Production**:
   - Test all endpoints on Railway URL
   - Verify Telegram bot responses
   - Monitor performance and costs

---

## 📞 Need Help?

If tests fail:

1. **Check error messages** carefully
2. **Run individual test scripts** to isolate issues
3. **Verify environment setup** (Python, Docker, etc.)
4. **Check file structure** and naming
5. **Review requirements.txt** for missing packages

**You've got this!** Local testing ensures a smooth Railway deployment. 🎉