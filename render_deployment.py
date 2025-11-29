#!/usr/bin/env python3
"""
Render-specific deployment script for F1 Telegram Bot
Implements fixes for common Render deployment issues
"""

import os
import sys
import logging
from flask import Flask, request, jsonify
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
        logger.warning("⚠️ RENDER_EXTERNAL_HOSTNAME not found")

    # Check bot token
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if bot_token:
        logger.info("✅ Bot token is configured")
    else:
        logger.error("❌ TELEGRAM_BOT_TOKEN not set!")
        return False

    return True


def create_render_app():
    """Create Flask app optimized for Render"""
    app = Flask(__name__)

    @app.route("/")
    def health_check():
        """Render health check endpoint"""
        return {
            "status": "healthy",
            "service": "F1 Telegram Bot - Render Deployment",
            "timestamp": datetime.now().isoformat(),
            "platform": "Render",
            "environment": {
                "port": os.getenv("PORT"),
                "hostname": os.getenv("RENDER_EXTERNAL_HOSTNAME"),
                "bot_token_set": bool(os.getenv("TELEGRAM_BOT_TOKEN")),
            },
        }

    @app.route("/health")
    def simple_health():
        """Simple health check for Render"""
        return "OK", 200

    @app.route("/webhook", methods=["POST"])
    def webhook():
        """Webhook endpoint"""
        logger.info(f"Webhook called with {request.method} method")
        return jsonify({"status": "received"}), 200

    return app


def main():
    """Main deployment function"""
    logger.info("🚀 Starting F1 Telegram Bot for Render deployment...")

    # Setup Render environment
    if not setup_render_environment():
        logger.error("❌ Environment setup failed!")
        sys.exit(1)

    # Create Flask app
    app = create_render_app()

    # Get port from environment
    port = int(os.getenv("PORT", 10000))

    logger.info(f"🌐 Starting Flask server on port {port}")

    # Start the server
    try:
        app.run(host="0.0.0.0", port=port, debug=False, threaded=True)
    except Exception as e:
        logger.error(f"❌ Server failed to start: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
