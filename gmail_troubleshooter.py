#!/usr/bin/env python3
"""
Gmail Authentication Troubleshooter
Helps diagnose and fix Gmail authentication issues
"""

import smtplib
import os
from dotenv import load_dotenv
import sys

def print_header():
    print("=" * 60)
    print("🔐 GMAIL AUTHENTICATION TROUBLESHOOTER")
    print("=" * 60)

def check_environment():
    """Check environment configuration"""
    print("\n🔍 Checking environment configuration...")
    
    load_dotenv()
    email = os.getenv('SENDER_EMAIL')
    password = os.getenv('SENDER_PASSWORD')
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', 587))
    
    print(f"📧 Email: {email}")
    print(f"🔑 Password: {'*' * len(password) if password else 'NOT SET'}")
    print(f"🌐 SMTP Server: {smtp_server}")
    print(f"🔌 SMTP Port: {smtp_port}")
    
    if not email or not password:
        print("❌ Email or password not configured!")
        return None, None, None, None
    
    return email, password, smtp_server, smtp_port

def check_password_format(password):
    """Check if password looks like an App Password"""
    print("\n🔍 Checking password format...")
    
    if not password:
        print("❌ No password set")
        return False
    
    # Remove spaces for checking
    clean_password = password.replace(' ', '')
    
    if len(clean_password) == 16 and clean_password.isalnum():
        print("✅ Password format looks like Gmail App Password")
        return True
    elif len(password) < 16 and any(c in password for c in "!@#$%^&*()-_+="):
        print("⚠️  Password looks like regular Gmail password")
        print("   Gmail requires App Passwords for third-party apps")
        return False
    else:
        print("⚠️  Password format unclear - may need App Password")
        return False

def test_smtp_connection(email, password, smtp_server, smtp_port):
    """Test SMTP connection and authentication"""
    print("\n🔍 Testing SMTP connection...")
    
    try:
        print(f"📡 Connecting to {smtp_server}:{smtp_port}...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        print("✅ Connected to SMTP server")
        
        print("🔐 Starting TLS encryption...")
        server.starttls()
        print("✅ TLS encryption started")
        
        print("🔑 Attempting authentication...")
        server.login(email, password)
        print("✅ Authentication successful!")
        
        server.quit()
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print("\n💡 This usually means:")
        print("   1. You're using regular password instead of App Password")
        print("   2. 2-Factor Authentication is not enabled")
        print("   3. App Password is incorrect")
        return False
        
    except smtplib.SMTPConnectError as e:
        print(f"❌ Connection failed: {e}")
        print("\n💡 This usually means:")
        print("   1. Internet connection issues")
        print("   2. Firewall blocking SMTP")
        print("   3. Wrong SMTP server/port")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def provide_solutions():
    """Provide step-by-step solutions"""
    print("\n" + "=" * 60)
    print("🛠️  SOLUTION STEPS")
    print("=" * 60)
    
    print("\n🔐 STEP 1: Enable 2-Factor Authentication")
    print("   1. Go to: https://myaccount.google.com/security")
    print("   2. Click '2-Step Verification'")
    print("   3. Follow setup instructions")
    
    print("\n🔑 STEP 2: Generate App Password")
    print("   1. Go to: https://myaccount.google.com/security")
    print("   2. Click 'App passwords' (under 2-Step Verification)")
    print("   3. Select 'Mail' as app")
    print("   4. Select 'Windows Computer' as device")
    print("   5. Click 'Generate'")
    print("   6. Copy the 16-character password")
    
    print("\n📝 STEP 3: Update Configuration")
    print("   1. Open the .env file")
    print("   2. Replace SENDER_PASSWORD with the App Password")
    print("   3. Format: SENDER_PASSWORD=abcd efgh ijkl mnop")
    print("   4. Save the file")
    
    print("\n🧪 STEP 4: Test Again")
    print("   1. Run this troubleshooter again")
    print("   2. Or test with your main application")

def main():
    print_header()
    
    # Check environment
    email, password, smtp_server, smtp_port = check_environment()
    if not all([email, password, smtp_server, smtp_port]):
        print("\n❌ Configuration incomplete. Please check your .env file.")
        return
    
    # Check password format
    is_app_password = check_password_format(password)
    
    # Test connection
    connection_ok = test_smtp_connection(email, password, smtp_server, smtp_port)
    
    # Summary and solutions
    print("\n" + "=" * 60)
    print("📋 DIAGNOSIS SUMMARY")
    print("=" * 60)
    
    if connection_ok:
        print("✅ All tests passed! Your Gmail configuration is working.")
        print("📧 You should now be able to send emails successfully.")
    else:
        print("❌ Authentication issues detected.")
        if not is_app_password:
            print("🔑 Main issue: You need to use a Gmail App Password")
        provide_solutions()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTroubleshooting interrupted by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
