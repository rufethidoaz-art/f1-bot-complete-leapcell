#!/usr/bin/env python3
"""
Render-specific startup script for F1 Telegram Bot
Handles deployment-specific configuration and startup
"""

import os
import sys
import subprocess
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


def install_playwright():
    """Install playwright and its dependencies"""
    logger.info("🔧 Installing Playwright and browser dependencies...")

    try:
        # Install playwright
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "playwright"],
            check=True,
            capture_output=True,
        )
        logger.info("✅ Playwright installed successfully")

        # Install browsers
        subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"],
            check=True,
            capture_output=True,
        )
        logger.info("✅ Chromium browser installed successfully")

        return True

    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Playwright installation failed: {e}")
        logger.warning(
            "Continuing without Playwright - live timing will use fallback APIs"
        )
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error during Playwright installation: {e}")
        return False


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
        logger.warning(
            "⚠️ RENDER_EXTERNAL_HOSTNAME not found - will be set after deployment"
        )

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
            "streams.txt",
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
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Working directory: {os.getcwd()}")

    # Install Playwright if needed
    playwright_available = install_playwright()

    # Setup Render environment
    if not setup_render_environment():
        logger.error("❌ Environment setup failed!")
        sys.exit(1)

    # Run diagnostics
    if not run_diagnostics():
        logger.error("❌ Diagnostics failed!")
        sys.exit(1)

    logger.info("✅ Setup and diagnostics completed successfully!")

    if playwright_available:
        logger.info("✅ Playwright available - enhanced live timing enabled")
    else:
        logger.warning("⚠️ Playwright not available - using fallback APIs")

    # Import and start the main bot
    try:
        from f1_bot import app

        # Get port from environment
        port = int(os.getenv("PORT", 10000))

        logger.info(f"🌐 Starting Flask server on port {port}")

        # Start the server
        app.run(host="0.0.0.0", port=port, debug=False, threaded=True)

    except Exception as e:
        logger.error(f"❌ Failed to start bot: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
