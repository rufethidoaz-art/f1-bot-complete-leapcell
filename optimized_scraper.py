"""
Optimized scraper for F1 live timing data.
This is a placeholder implementation for Leapcell deployment.
"""

import asyncio
import logging
import requests
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

async def get_optimized_live_timing():
    """
    Get live timing data using optimized scraping.
    Returns None if not available or fallback to API.
    """
    try:
        # Try to get live timing from OpenF1 API first
        return await _get_openf1_timing()
    except Exception as e:
        logger.error(f"Optimized scraper failed: {e}")
        return None

async def _get_openf1_timing():
    """Get live timing from OpenF1 API"""
    try:
        # Get current active session
        now = datetime.now(ZoneInfo("UTC"))
        current_year = now.year
        
        # Check for active sessions
        sessions_url = f"https://api.openf1.org/v1/sessions?year={current_year}"
        sessions_response = requests.get(sessions_url, timeout=10)
        
        if sessions_response.status_code != 200:
            return None
            
        sessions = sessions_response.json()
        active_session = None
        
        for session in sessions:
            session_start = session.get("date_start")
            session_end = session.get("date_end")
            
            if session_start:
                start_dt = datetime.fromisoformat(session_start.replace('Z', '+00:00'))
                if start_dt.tzinfo is None:
                    start_dt = start_dt.replace(tzinfo=ZoneInfo("UTC"))
                
                # Check if session is active (within last 2 hours and next 4 hours)
                if (now - timedelta(hours=2)) <= start_dt <= (now + timedelta(hours=4)):
                    active_session = session
                    break
        
        if not active_session:
            return None
        
        session_key = active_session.get("session_key")
        if not session_key:
            return None
        
        # Get live timing data
        timing_url = f"https://api.openf1.org/v1/position?session_key={session_key}"
        timing_response = requests.get(timing_url, timeout=10)
        
        if timing_response.status_code != 200:
            return None
        
        timing_data = timing_response.json()
        if not timing_data:
            return None
        
        # Format data for Telegram
        return _format_openf1_data(timing_data, active_session)
        
    except Exception as e:
        logger.error(f"OpenF1 API failed: {e}")
        return None

def _format_openf1_data(timing_data, session_data):
    """Format OpenF1 timing data for Telegram display"""
    try:
        # Group positions by driver
        driver_positions = {}
        for entry in timing_data:
            driver_number = entry.get("driver_number")
            position = entry.get("position")
            date = entry.get("date")
            
            if driver_number and position and date:
                if driver_number not in driver_positions or date > driver_positions[driver_number]["date"]:
                    driver_positions[driver_number] = {
                        "position": position,
                        "date": date,
                        "current_lap": entry.get("current_lap", 0),
                        "gap_to_leader": entry.get("gap_to_leader", 0),
                        "status": entry.get("status", "")
                    }
        
        # Sort by position
        sorted_drivers = sorted(driver_positions.items(), key=lambda x: x[1]["position"])
        
        # Get session info
        session_name = session_data.get("meeting_name", "Unknown Session")
        session_type = session_data.get("session_type", "Session")
        
        return {
            "session": f"{session_name} - {session_type}",
            "timestamp": datetime.now().isoformat(),
            "drivers": sorted_drivers,
            "total_drivers": len(sorted_drivers)
        }
        
    except Exception as e:
        logger.error(f"Formatting failed: {e}")
        return None

def format_timing_data_for_telegram(data):
    """Format timing data for Telegram display"""
    if not data:
        return "❌ No live timing data available"
    
    try:
        message = f"🔴 *{data.get('session', 'Live Timing')}*\n\n"
        
        drivers = data.get("drivers", [])
        if not drivers:
            return message + "No drivers on track"
        
        for driver_num, driver_info in drivers[:20]:  # Show top 20
            position = driver_info.get("position", "?")
            current_lap = driver_info.get("current_lap", 0)
            gap = driver_info.get("gap_to_leader", 0)
            
            line = f"{position}. Driver {driver_num} (Lap {current_lap})"
            
            if position == 1:
                line += " 🏆"
            elif gap > 0:
                line += f" +{gap:.3f}s"
            
            message += line + "\n"
        
        message += f"\n📊 Updated: {datetime.now().strftime('%H:%M:%S')}"
        return message
        
    except Exception as e:
        logger.error(f"Telegram formatting failed: {e}")
        return "❌ Error formatting live timing data"

# Import required modules at the end to avoid circular imports
try:
    from datetime import datetime, timedelta
    from zoneinfo import ZoneInfo
except ImportError:
    # Fallback for older Python versions
    from datetime import datetime, timedelta
    try:
        from dateutil.tz import tzutc, gettz
        ZoneInfo = gettz  # Fallback to dateutil
    except ImportError:
        pass