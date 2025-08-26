#!/usr/bin/env python3
"""
Simple Email Verification CLI
A command-line interface for sending verification emails with 6-digit codes
"""

import sys
import os
from email_service import EmailVerificationService

def print_banner():
    """Print application banner"""
    print("=" * 60)
    print("📧 EMAIL VERIFICATION SERVICE")
    print("=" * 60)
    print("Send verification emails with 6-digit codes")
    print("=" * 60)

def configure_email():
    """Configure email settings"""
    print("\n🔧 EMAIL CONFIGURATION")
    print("-" * 30)
    
    sender_email = input("Enter sender email: ").strip()
    sender_password = input("Enter app password (hidden): ").strip()
    
    # Save to .env file
    env_content = f"""# Email Configuration
SENDER_EMAIL={sender_email}
SENDER_PASSWORD={sender_password}
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# App Configuration
APP_NAME=Email Verification Service"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Configuration saved successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to save configuration: {e}")
        return False

def send_verification_email(service):
    """Send verification email"""
    print("\n📤 SEND VERIFICATION EMAIL")
    print("-" * 35)
    
    recipient = input("Enter recipient email: ").strip()
    if not recipient:
        print("❌ Recipient email is required!")
        return None
    
    print("\nEnter custom message (press Enter twice to finish):")
    custom_message_lines = []
    while True:
        line = input()
        if line == "":
            break
        custom_message_lines.append(line)
    
    custom_message = "\n".join(custom_message_lines)
    
    print("\n🚀 Sending email...")
    success, code = service.send_verification_email(recipient, custom_message)
    
    if success:
        print(f"✅ Email sent successfully!")
        print(f"📧 Recipient: {recipient}")
        print(f"🔢 Verification code: {code}")
        return recipient
    else:
        print("❌ Failed to send email!")
        return None

def verify_code(service):
    """Verify a code"""
    print("\n🔍 VERIFY CODE")
    print("-" * 20)
    
    email = input("Enter email: ").strip()
    code = input("Enter 6-digit code: ").strip()
    
    if not email or not code:
        print("❌ Both email and code are required!")
        return
    
    is_valid, message = service.verify_code(email, code)
    
    if is_valid:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")

def show_menu():
    """Show main menu"""
    print("\n" + "=" * 40)
    print("MAIN MENU")
    print("=" * 40)
    print("1. Configure Email Settings")
    print("2. Send Verification Email")
    print("3. Verify Code")
    print("4. Cleanup Expired Codes")
    print("5. Show Current Configuration")
    print("6. Exit")
    print("=" * 40)

def show_configuration(service):
    """Show current configuration"""
    print("\n📋 CURRENT CONFIGURATION")
    print("-" * 30)
    print(f"Sender Email: {service.sender_email or 'Not configured'}")
    print(f"SMTP Server: {service.smtp_server}")
    print(f"SMTP Port: {service.smtp_port}")
    print(f"App Name: {service.app_name}")
    print(f"Active Codes: {len(service.verification_codes)}")

def main():
    """Main application function"""
    print_banner()
    
    # Initialize service
    try:
        service = EmailVerificationService()
    except Exception as e:
        print(f"❌ Failed to initialize service: {e}")
        sys.exit(1)
    
    # Check if configuration exists
    if not service.sender_email or not service.sender_password:
        print("\n⚠️  Email configuration not found!")
        print("Please configure your email settings first.")
        if not configure_email():
            sys.exit(1)
        # Reload service with new configuration
        service = EmailVerificationService()
    
    last_recipient = None
    
    while True:
        show_menu()
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            configure_email()
            # Reload service with new configuration
            service = EmailVerificationService()
            
        elif choice == '2':
            if not service.sender_email or not service.sender_password:
                print("❌ Please configure email settings first!")
                continue
            last_recipient = send_verification_email(service)
            
        elif choice == '3':
            if last_recipient:
                print(f"\n💡 Tip: Last email sent to: {last_recipient}")
            verify_code(service)
            
        elif choice == '4':
            service.cleanup_expired_codes()
            
        elif choice == '5':
            show_configuration(service)
            
        elif choice == '6':
            print("\n👋 Thank you for using Email Verification Service!")
            print("Goodbye!")
            break
            
        else:
            print("❌ Invalid choice! Please enter 1-6.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Application interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
