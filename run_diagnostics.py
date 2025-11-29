#!/usr/bin/env python3
"""
Run diagnostics and start the F1 Telegram Bot
This script should be used for testing in Render before full deployment
"""

import os
import sys
import subprocess
import time


def run_diagnostics():
    """Run diagnostic tests"""
    print("🔍 Running diagnostic tests...")

    try:
        # Run the diagnostic test script
        result = subprocess.run(
            [sys.executable, "diagnostic_test.py"],
            capture_output=True,
            text=True,
            timeout=60,
        )

        print("Diagnostic output:")
        print(result.stdout)

        if result.stderr:
            print("Errors:")
            print(result.stderr)

        return result.returncode == 0

    except subprocess.TimeoutExpired:
        print("❌ Diagnostics timed out")
        return False
    except Exception as e:
        print(f"❌ Diagnostics failed: {e}")
        return False


def check_diagnostics_log():
    """Check the diagnostics log for issues"""
    print("\n📋 Checking diagnostics log...")

    try:
        if os.path.exists("bot_diagnostics.log"):
            with open("bot_diagnostics.log", "r") as f:
                lines = f.readlines()

            # Show last 20 lines
            print("Last 20 lines of diagnostics:")
            for line in lines[-20:]:
                print(line.strip())

            # Check for critical errors
            error_lines = [line for line in lines if "ERROR" in line]
            if error_lines:
                print(f"\n❌ Found {len(error_lines)} errors in diagnostics")
                for error in error_lines[-5:]:  # Show last 5 errors
                    print(error.strip())
                return False
            else:
                print("\n✅ No critical errors found")
                return True
        else:
            print("❌ No diagnostics log found")
            return False

    except Exception as e:
        print(f"❌ Error reading diagnostics log: {e}")
        return False


def main():
    """Main function"""
    print("🚀 F1 Telegram Bot - Diagnostic & Startup Script")
    print("=" * 60)

    # Run diagnostics
    diagnostics_passed = run_diagnostics()

    # Check log file
    log_ok = check_diagnostics_log()

    print("\n" + "=" * 60)
    print("📊 DIAGNOSTIC SUMMARY")
    print("=" * 60)
    print(f"Diagnostics Test: {'✅ PASSED' if diagnostics_passed else '❌ FAILED'}")
    print(f"Log Analysis: {'✅ PASSED' if log_ok else '❌ FAILED'}")

    if diagnostics_passed and log_ok:
        print("\n🎉 All diagnostics passed! Bot should work correctly.")
        print("\nNext steps for Render deployment:")
        print("1. Set TELEGRAM_BOT_TOKEN environment variable")
        print("2. Set PORT environment variable (usually 10000)")
        print("3. Deploy to Render")
        print("4. Check bot_diagnostics.log after deployment")
        print("5. Test your bot with /start command")
    else:
        print("\n❌ Some diagnostics failed. Check the output above.")
        print("\nCommon issues and fixes:")
        print("- Missing TELEGRAM_BOT_TOKEN: Set it in Render environment variables")
        print("- API connectivity issues: Check network/firewall settings")
        print("- Import errors: Check requirements.txt and Python version")
        print("- Webhook errors: Check RENDER_EXTERNAL_HOSTNAME is set")

    return diagnostics_passed and log_ok


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
