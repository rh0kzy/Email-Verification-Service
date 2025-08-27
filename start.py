#!/usr/bin/env python3
"""
Email Verification Service - Quick Launcher
Start the modern email verification service
"""

import sys
import os

def main():
    print("🚀 Starting Email Verification Service...")
    print("📧 Modern UI Loading...")
    
    try:
        # Launch the modern UI directly
        from simple_modern import main as modern_main
        modern_main()
    except ImportError:
        print("❌ Could not find simple_modern.py")
        print("Please make sure all files are in the correct directory.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
