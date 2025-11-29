#!/usr/bin/env python3
"""
Diagnostic test script for F1 Telegram Bot
Tests all components and logs diagnostics to bot_diagnostics.log
"""

import os
import sys
import json
import logging
import requests
import asyncio
import threading
import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# Configure diagnostic logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - DIAGNOSTIC - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot_diagnostics.log", mode="a"),
        logging.StreamHandler(sys.stdout),
    ],
)

DIAGNOSTIC_LOGGER = logging.getLogger("diagnostics")


def log_diagnostic(message: str, level: str = "INFO"):
    """Log diagnostic information"""
    if level == "ERROR":
        DIAGNOSTIC_LOGGER.error(message)
    elif level == "WARNING":
        DIAGNOSTIC_LOGGER.warning(message)
    else:
        DIAGNOSTIC_LOGGER.info(message)


def test_environment():
    """Test deployment environment"""
    log_diagnostic("=" * 60, "INFO")
    log_diagnostic("F1 Telegram Bot - Diagnostic Test", "INFO")
    log_diagnostic("=" * 60, "INFO")

    log_diagnostic(f"Python version: {sys.version}", "INFO")
    log_diagnostic(f"Platform: {sys.platform}", "INFO")
    log_diagnostic(f"Working directory: {os.getcwd()}", "INFO")

    # Test environment variables
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    log_diagnostic(f"TELEGRAM_BOT_TOKEN set: {token is not None}", "INFO")

    port = os.getenv("PORT")
    log_diagnostic(f"PORT: {port}", "INFO")

    render_host = os.getenv("RENDER_EXTERNAL_HOSTNAME")
    log_diagnostic(f"RENDER_EXTERNAL_HOSTNAME: {render_host}", "INFO")

    railway_url = os.getenv("RAILWAY_STATIC_URL")
    log_diagnostic(f"RAILWAY_STATIC_URL: {railway_url}", "INFO")

    # Test write permissions
    try:
        with open("test_write.tmp", "w") as f:
            f.write("test")
        os.remove("test_write.tmp")
        log_diagnostic("Write permissions: Available", "INFO")
    except Exception as e:
        log_diagnostic(f"Write permissions: Denied - {e}", "WARNING")


def test_imports():
    """Test Python imports"""
    log_diagnostic("Testing imports...", "INFO")

    required_modules = [
        "flask",
        "requests",
        "asyncio",
        "telegram",
        "playwright",
        "bs4",
        "lxml",
        "dotenv",
    ]

    for module in required_modules:
        try:
            __import__(module)
            log_diagnostic(f"✅ {module}", "INFO")
        except ImportError as e:
            log_diagnostic(f"❌ {module}: {e}", "ERROR")


def test_api_connectivity():
    """Test API connectivity"""
    log_diagnostic("Testing API connectivity...", "INFO")

    apis = [
        "https://api.jolpi.ca/ergast/f1/current/driverStandings.json",
        "https://api.openf1.org/v1/sessions?year=2025",
        "https://api.open-meteo.com/v1/forecast?latitude=40.4093&longitude=49.8671&daily=temperature_2m_max&current_date=2025-01-01&end_date=2025-01-02",
    ]

    for api_url in apis:
        try:
            response = requests.get(api_url, timeout=10)
            status = (
                "✅" if response.status_code == 200 else f"❌ {response.status_code}"
            )
            log_diagnostic(f"{status} {api_url}", "INFO")
        except Exception as e:
            log_diagnostic(f"❌ {api_url}: {e}", "ERROR")


def test_flask_app():
    """Test Flask app"""
    log_diagnostic("Testing Flask app...", "INFO")

    try:
        # Import the Flask app
        sys.path.append(".")
        from f1_bot import app, home, health_check, bot_status

        log_diagnostic("✅ Flask app imported successfully", "INFO")

        # Test health endpoint
        with app.test_client() as client:
            response = client.get("/")
            log_diagnostic(f"✅ Health endpoint: {response.status_code}", "INFO")

            response = client.get("/health")
            log_diagnostic(f"✅ Health check: {response.status_code}", "INFO")

            response = client.get("/status")
            log_diagnostic(f"✅ Bot status: {response.status_code}", "INFO")

    except Exception as e:
        log_diagnostic(f"❌ Flask app test failed: {e}", "ERROR")


def test_telegram_bot():
    """Test Telegram bot setup"""
    log_diagnostic("Testing Telegram bot setup...", "INFO")

    try:
        from telegram.ext import Application

        token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not token:
            log_diagnostic("❌ No bot token available", "ERROR")
            return False

        # Test bot creation
        application = Application.builder().token(token).build()
        log_diagnostic("✅ Bot application created", "INFO")

        # Test webhook URL construction
        webhook_url = os.getenv("WEBHOOK_URL")
        render_url = os.getenv("RENDER_EXTERNAL_HOSTNAME")

        if render_url:
            webhook_url = f"https://{render_url}/webhook"
            log_diagnostic(f"✅ Using Render webhook URL: {webhook_url}", "INFO")
        elif os.getenv("RAILWAY_STATIC_URL"):
            webhook_url = f"{os.getenv('RAILWAY_STATIC_URL')}/webhook"
            log_diagnostic(f"✅ Using Railway webhook URL: {webhook_url}", "INFO")
        else:
            log_diagnostic("❌ No platform URL found", "WARNING")

        return True

    except Exception as e:
        log_diagnostic(f"❌ Telegram bot test failed: {e}", "ERROR")
        return False


def test_scraper_functions():
    """Test scraper functions"""
    log_diagnostic("Testing scraper functions...", "INFO")

    try:
        # Test OpenF1 API
        now = datetime.now(ZoneInfo("UTC"))
        current_year = now.year

        sessions_url = f"https://api.openf1.org/v1/sessions?year={current_year}"
        sessions_response = requests.get(sessions_url, timeout=10)

        if sessions_response.status_code == 200:
            sessions = sessions_response.json()
            log_diagnostic(f"✅ OpenF1 API: {len(sessions)} sessions", "INFO")
        else:
            log_diagnostic(f"❌ OpenF1 API: {sessions_response.status_code}", "ERROR")

    except Exception as e:
        log_diagnostic(f"❌ Scraper test failed: {e}", "ERROR")


def test_webhook_simulation():
    """Test webhook simulation"""
    log_diagnostic("Testing webhook simulation...", "INFO")

    try:
        from f1_bot import app

        # Simulate a Telegram webhook request
        webhook_data = {
            "update_id": 123456789,
            "message": {
                "message_id": 1,
                "from": {
                    "id": 123456789,
                    "is_bot": False,
                    "first_name": "Test",
                    "username": "testuser",
                },
                "chat": {
                    "id": 123456789,
                    "first_name": "Test",
                    "username": "testuser",
                    "type": "private",
                },
                "date": int(time.time()),
                "text": "/start",
            },
        }

        with app.test_client() as client:
            response = client.post("/webhook", json=webhook_data)
            log_diagnostic(f"✅ Webhook test: {response.status_code}", "INFO")

    except Exception as e:
        log_diagnostic(f"❌ Webhook simulation failed: {e}", "ERROR")


def run_comprehensive_test():
    """Run all diagnostic tests"""
    log_diagnostic("Starting comprehensive diagnostic test...", "INFO")

    test_environment()
    test_imports()
    test_api_connectivity()
    test_flask_app()
    test_telegram_bot()
    test_scraper_functions()
    test_webhook_simulation()

    log_diagnostic("=" * 60, "INFO")
    log_diagnostic("Diagnostic test completed!", "INFO")
    log_diagnostic("Check bot_diagnostics.log for detailed results", "INFO")
    log_diagnostic("=" * 60, "INFO")


if __name__ == "__main__":
    run_comprehensive_test()
