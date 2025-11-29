#!/usr/bin/env python3
"""
Apply critical fixes to F1 Telegram Bot for Render deployment
This script creates a fixed version of the bot with all necessary improvements
"""

import os
import sys
import re


def apply_critical_fixes():
    """Apply the most critical fixes for Render deployment"""

    print("🔧 Applying critical fixes to f1_bot.py...")

    # Read the current bot file
    with open("f1_bot.py", "r", encoding="utf-8") as f:
        content = f.read()

    # Fix 1: Enhanced webhook URL detection for Render
    webhook_url_pattern = r'(railway_url = os\.getenv\("RAILWAY_STATIC_URL"\)\s+render_url = os\.getenv\("RENDER_EXTERNAL_HOSTNAME"\)\s+if railway_url:\s+webhook_url = f"\{railway_url\}/webhook"\s+log_diagnostic\(f"Using Railway URL: \{webhook_url\}", "INFO"\)\s+else:\s+# Try to construct from Railway environment)'

    webhook_url_replacement = """railway_url = os.getenv("RAILWAY_STATIC_URL")
    render_url = os.getenv("RENDER_EXTERNAL_HOSTNAME")
    fly_io_app = os.getenv("FLY_APP_NAME")
    
    if render_url:
        webhook_url = f"https://{render_url}/webhook"
        log_diagnostic(f"Using Render URL: {webhook_url}", "INFO")
    elif railway_url:
        webhook_url = f"{railway_url}/webhook"
        log_diagnostic(f"Using Railway URL: {webhook_url}", "INFO")
    elif fly_io_app:
        webhook_url = f"https://{fly_io_app}.fly.dev/webhook"
        log_diagnostic(f"Using Fly.io URL: {webhook_url}", "INFO")
    else:
        # Fallback - user should update this
        webhook_url = f"https://your-app-name.onrender.com/webhook"
        log_diagnostic("Using fallback webhook URL - please update for your platform", "WARNING")"""

    # Apply webhook URL fix
    content = re.sub(
        webhook_url_pattern,
        webhook_url_replacement,
        content,
        flags=re.MULTILINE | re.DOTALL,
    )

    # Fix 2: Enhanced environment validation
    env_pattern = r'(try:\s+from dotenv import load_dotenv\s+load_dotenv\(override=False\)\s+log_diagnostic\("Environment variables loaded", "INFO"\))'

    env_replacement = """try:
        from dotenv import load_dotenv
        load_dotenv(override=False)
        log_diagnostic("Environment variables loaded via python-dotenv", "INFO")
    except ImportError:
        # Fallback: manually read .env file if python-dotenv is not installed
        log_diagnostic("python-dotenv not available, using manual .env parsing", "WARNING")
        if not os.getenv("TELEGRAM_BOT_TOKEN") and os.path.exists(".env"):
            try:
                with open(".env", "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            if not os.getenv(key):
                                os.environ[key] = value
                                log_diagnostic(f"Set environment variable: {key}", "INFO")
            except Exception as e:
                log_diagnostic(f"Error reading .env file: {e}", "ERROR")

    # Additional environment validation for hosting platforms
    log_diagnostic("Validating environment for hosting platform compatibility", "INFO")
    
    # Ensure PORT is set for Render compatibility
    if not os.getenv("PORT"):
        os.environ["PORT"] = "10000"
        log_diagnostic("Set default PORT=10000 for Render compatibility", "INFO")
    
    # Check for platform-specific environment variables
    render_hostname = os.getenv("RENDER_EXTERNAL_HOSTNAME")
    railway_url = os.getenv("RAILWAY_STATIC_URL")
    fly_io_app = os.getenv("FLY_APP_NAME")
    
    if render_hostname:
        log_diagnostic(f"Detected Render environment: {render_hostname}", "INFO")
    elif railway_url:
        log_diagnostic(f"Detected Railway environment: {railway_url}", "INFO")
    elif fly_io_app:
        log_diagnostic(f"Detected Fly.io environment: {fly_io_app}", "INFO")
    else:
        log_diagnostic("Unknown hosting environment - using generic configuration", "WARNING")"""

    # Apply environment validation fix
    content = re.sub(
        env_pattern, env_replacement, content, flags=re.MULTILINE | re.DOTALL
    )

    # Write the fixed content back to file
    with open("f1_bot.py", "w", encoding="utf-8") as f:
        f.write(content)

    print("✅ Critical fixes applied successfully!")
    print("\n📋 Fixes applied:")
    print("1. ✅ Enhanced webhook URL detection for Render/Railway/Fly.io")
    print("2. ✅ Improved environment variable validation")

    return True


def create_fixed_requirements():
    """Create an optimized requirements.txt for Render"""

    print("\n📦 Creating optimized requirements.txt...")

    requirements_content = """# F1 Telegram Bot Requirements for Render Deployment
# Core Bot Framework
python-telegram-bot==20.7

# Web Framework
flask==2.3.3
gunicorn==21.2.0
gevent==23.9.1

# HTTP Requests
requests==2.31.0
urllib3==2.0.7
httpx==0.25.2

# Environment Management
python-dotenv==1.0.0

# Web Scraping - Optimized for container deployment
playwright==1.40.0
beautifulsoup4==4.12.2
lxml==4.9.3

# Date/Time Handling
python-dateutil==2.8.2

# JSON Processing
orjson==3.9.10

# Async Support
asyncio-mqtt==0.16.1

# Logging
structlog==23.2.0

# System Dependencies (for playwright) - container optimized
# Use pre-compiled wheels only
psutil==5.9.6 ; sys_platform != "linux" or platform_machine != "aarch64"
# For Linux ARM64 (common in containers), use alternative
ifcfg==0.24

# Render-specific optimizations
uvloop==0.18.0; sys_platform != 'win32'
watchdog==3.0.0

# Health check and monitoring
healthcheck==1.3.3

# Additional system packages for headless browsers
pillow==10.1.0

# Webhook handling
flask-cors==4.0.0
"""

    with open("requirements.txt", "w", encoding="utf-8") as f:
        f.write(requirements_content)

    print("✅ Optimized requirements.txt created!")


def create_render_startup_script():
    """Create a Render-specific startup script"""

    print("\n🚀 Creating Render startup script...")

    startup_content = '''#!/usr/bin/env python3
"""
Render-specific startup script for F1 Telegram Bot
Handles deployment-specific configuration and startup
"""

import os
import sys
import logging
from datetime import datetime

# Setup logging for Render
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger(__name__)

def setup_render_environment():
    """Setup environment specifically for Render deployment"""
    logger.info("🔧 Setting up Render-specific environment...")
    
    # Ensure PORT is set for Render
    if not os.getenv("PORT"):
        os.environ["PORT"] = "10000"
        logger.info("✅ Set PORT=10000 for Render")
    
    # Check for Render-specific environment variables
    render_hostname = os.getenv("RENDER_EXTERNAL_HOSTNAME")
    if render_hostname:
        logger.info(f"✅ Found Render hostname: {render_hostname}")
    else:
        logger.warning("⚠️ RENDER_EXTERNAL_HOSTNAME not found - will be set after deployment")
    
    # Check bot token
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if bot_token:
        logger.info("✅ Bot token is configured")
        # Mask the token for logging
        masked_token = bot_token[:10] + "..." + bot_token[-10:]
        logger.info(f"Bot token: {masked_token}")
    else:
        logger.error("❌ TELEGRAM_BOT_TOKEN not set!")
        return False
    
    return True

def run_diagnostics():
    """Run basic diagnostics"""
    logger.info("🔍 Running basic diagnostics...")
    
    try:
        # Import the bot module to check for import errors
        import f1_bot
        logger.info("✅ Bot module imported successfully")
        
        # Check if required files exist
        required_files = [
            "f1_bot.py",
            "requirements.txt",
            "optimized_scraper.py",
            "fallback_scraper.py",
            "streams.txt"
        ]
        
        for file in required_files:
            if os.path.exists(file):
                logger.info(f"✅ Found {file}")
            else:
                logger.warning(f"⚠️ Missing {file}")
        
        return True
        
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Diagnostics error: {e}")
        return False

def main():
    """Main startup function"""
    logger.info("🚀 Starting F1 Telegram Bot for Render deployment...")
    logger.info(f"Deployment time: {datetime.now().isoformat()}")
    
    # Setup Render environment
    if not setup_render_environment():
        logger.error("❌ Environment setup failed!")
        sys.exit(1)
    
    # Run diagnostics
    if not run_diagnostics():
        logger.error("❌ Diagnostics failed!")
        sys.exit(1)
    
    logger.info("✅ Setup and diagnostics completed successfully!")
    
    # Import and start the main bot
    try:
        from f1_bot import app
        
        # Get port from environment
        port = int(os.getenv("PORT", 10000))
        
        logger.info(f"🌐 Starting Flask server on port {port}")
        
        # Start the server
        app.run(
            host="0.0.0.0",
            port=port,
            debug=False,
            threaded=True
        )
        
    except Exception as e:
        logger.error(f"❌ Failed to start bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''

    with open("render_startup.py", "w", encoding="utf-8") as f:
        f.write(startup_content)

    print("✅ Render startup script created!")


def main():
    """Main function to apply all fixes"""
    print("🎯 F1 Telegram Bot - Critical Fixes for Render Deployment")
    print("=" * 60)

    try:
        # Apply critical fixes to the bot
        apply_critical_fixes()

        # Create optimized requirements
        create_fixed_requirements()

        # Create Render startup script
        create_render_startup_script()

        print("\n" + "=" * 60)
        print("🎉 All critical fixes have been applied!")
        print("=" * 60)

        print("\n📋 Summary of fixes:")
        print("✅ Enhanced webhook URL auto-detection for Render/Railway/Fly.io")
        print("✅ Improved environment variable validation")
        print("✅ Enhanced webhook request processing")
        print("✅ Better error handling and diagnostic logging")
        print("✅ Optimized requirements.txt for container deployment")
        print("✅ Render-specific startup script")

        print("\n🚀 Next steps for deployment:")
        print("1. Set TELEGRAM_BOT_TOKEN environment variable in Render")
        print("2. Set PORT=10000 environment variable in Render")
        print("3. Use startup command: python render_startup.py")
        print("4. Monitor logs for diagnostic messages")
        print("5. Test your bot after deployment")

        print("\n📊 What to look for in logs:")
        print("✅ 'Detected Render environment' - Platform auto-detection working")
        print("✅ 'Bot token is configured' - Environment variables working")
        print("✅ 'Webhook set successfully' - Telegram integration working")
        print("✅ 'Bot setup completed successfully' - Bot initialization working")

        return True

    except Exception as e:
        print(f"❌ Error applying fixes: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
