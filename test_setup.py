#!/usr/bin/env python3
"""
Test script for Email Verification Service
Run this to verify your setup is working correctly
"""

import sys
import os
from email_service import EmailVerificationService

def test_service_initialization():
    """Test if the service can be initialized"""
    print("🧪 Testing service initialization...")
    try:
        service = EmailVerificationService()
        print("✅ Service initialized successfully")
        return service
    except Exception as e:
        print(f"❌ Service initialization failed: {e}")
        return None

def test_code_generation(service):
    """Test code generation"""
    print("\n🧪 Testing code generation...")
    try:
        code = service.generate_verification_code()
        if len(code) == 6 and code.isdigit():
            print(f"✅ Code generation working: {code}")
            return True
        else:
            print(f"❌ Invalid code generated: {code}")
            return False
    except Exception as e:
        print(f"❌ Code generation failed: {e}")
        return False

def test_configuration(service):
    """Test configuration"""
    print("\n🧪 Testing configuration...")
    
    config_items = [
        ("SMTP Server", service.smtp_server),
        ("SMTP Port", service.smtp_port),
        ("App Name", service.app_name),
        ("Sender Email", service.sender_email),
        ("Sender Password", "***" if service.sender_password else None)
    ]
    
    all_good = True
    for name, value in config_items:
        if value:
            print(f"✅ {name}: {value}")
        else:
            print(f"⚠️  {name}: Not configured")
            if name in ["Sender Email", "Sender Password"]:
                all_good = False
    
    return all_good

def run_tests():
    """Run all tests"""
    print("=" * 50)
    print("📧 EMAIL VERIFICATION SERVICE - TEST SUITE")
    print("=" * 50)
    
    # Test 1: Service initialization
    service = test_service_initialization()
    if not service:
        print("\n❌ Cannot continue tests - service initialization failed")
        return False
    
    # Test 2: Code generation
    if not test_code_generation(service):
        print("\n❌ Code generation test failed")
        return False
    
    # Test 3: Configuration
    config_ok = test_configuration(service)
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    if config_ok:
        print("✅ All tests passed! Your setup is ready to use.")
        print("\nNext steps:")
        print("1. Run 'python gui_app.py' for the GUI version")
        print("2. Run 'python cli_app.py' for the CLI version")
        print("3. Configure your email settings if not done already")
    else:
        print("⚠️  Tests passed but configuration needed:")
        print("1. Set up your Gmail App Password")
        print("2. Configure SENDER_EMAIL and SENDER_PASSWORD in .env")
        print("3. Run the test again")
    
    return True

if __name__ == "__main__":
    try:
        run_tests()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error during testing: {e}")
        sys.exit(1)
