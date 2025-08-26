#!/usr/bin/env python3
"""
Enhanced Launcher for Email Verification Service
Beautiful splash screen with modern UI launch
"""

import sys
import os
from datetime import datetime

def print_banner():
    print("=" * 50)
    print("📧 EMAIL VERIFICATION SERVICE LAUNCHER")
    print("=" * 50)
    print(f"🕒 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎨 Launching with modern UI...")

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

def launch_with_splash():
    """Launch with beautiful splash screen"""
    try:
        print("🎨 Starting with splash screen...")
        from splash import show_splash_and_launch
        show_splash_and_launch()
    except ImportError as e:
        print(f"⚠️ Splash screen not available: {e}")
        print("🚀 Starting GUI directly...")
        launch_gui_direct()
    except Exception as e:
        print(f"❌ Error with splash screen: {e}")
        print("🚀 Starting GUI directly...")
        launch_gui_direct()

def launch_gui_direct():
    """Launch the GUI application directly"""
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
    
    # Ask user for launch preference
    try:
        choice = input("\nLaunch options:\n1. Modern UI with splash screen (recommended)\n2. Direct launch\n\nChoose (1/2) or press Enter for default: ").strip()
        
        if choice == "2":
            launch_gui_direct()
        else:
            launch_with_splash()
            
    except KeyboardInterrupt:
        print("\n\n👋 Launcher interrupted by user.")
        sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Launcher interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
