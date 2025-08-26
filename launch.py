#!/usr/bin/env python3
"""
Quick Launcher for Email Verification Service
Automatically loads previous settings and starts the GUI
"""

import sys
import os
from datetime import datetime

def print_banner():
    print("=" * 50)
    print("📧 EMAIL VERIFICATION SERVICE LAUNCHER")
    print("=" * 50)
    print(f"🕒 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🔄 Loading saved settings...")

def check_settings():
    """Check if settings file exists"""
    if os.path.exists("app_settings.json"):
        try:
            import json
            with open("app_settings.json", 'r') as f:
                settings = json.load(f)
            
            recent_count = len(settings.get('recent_recipients', []))
            last_saved = settings.get('last_saved', 'Unknown')
            
            print(f"✅ Found saved settings")
            print(f"📧 Recent recipients: {recent_count}")
            print(f"💾 Last saved: {last_saved}")
            return True
        except:
            print("⚠️ Settings file found but corrupted")
            return False
    else:
        print("📝 No saved settings (first run)")
        return False

def launch_gui():
    """Launch the GUI application"""
    try:
        print("🚀 Starting GUI application...")
        from gui_app import main
        main()
    except ImportError as e:
        print(f"❌ Could not import GUI application: {e}")
        print("Make sure gui_app.py is in the same directory")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

def main():
    print_banner()
    check_settings()
    print("=" * 50)
    launch_gui()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Launcher interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
