import smtplib
import random
import string
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

class EmailVerificationService:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.app_name = os.getenv('APP_NAME', 'Email Verification Service')
        
        # Store verification codes with expiration times
        self.verification_codes = {}
    
    def generate_verification_code(self):
        """Generate a 6-digit verification code"""
        return ''.join(random.choices(string.digits, k=6))
    
    def create_email_content(self, recipient_email, verification_code):
        """Create the email content with the verification code"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 20px;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .header {{
                    text-align: center;
                    margin-bottom: 30px;
                }}
                .code-box {{
                    background-color: #f8f9fa;
                    border: 2px dashed #007bff;
                    border-radius: 8px;
                    padding: 20px;
                    text-align: center;
                    margin: 20px 0;
                }}
                .verification-code {{
                    font-size: 32px;
                    font-weight: bold;
                    color: #007bff;
                    letter-spacing: 5px;
                    margin: 10px 0;
                }}
                .footer {{
                    margin-top: 30px;
                    text-align: center;
                    color: #666;
                    font-size: 14px;
                }}
                .warning {{
                    background-color: #fff3cd;
                    border: 1px solid #ffeaa7;
                    color: #856404;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1 style="color: #333;">Email Verification</h1>
                    <h2 style="color: #666;">{self.app_name}</h2>
                </div>
                
                <p>Hello,</p>
                <p>You have requested email verification. Please use the following 6-digit code to complete your verification:</p>
                
                <div class="code-box">
                    <p style="margin: 0; color: #333;">Your verification code is:</p>
                    <div class="verification-code">{verification_code}</div>
                </div>
                
                <div class="warning">
                    <strong>⚠️ Important:</strong> This code will expire in 10 minutes for security reasons.
                </div>
                
                <p>If you didn't request this verification, please ignore this email.</p>
                
                <div class="footer">
                    <p>This is an automated message from {self.app_name}</p>
                    <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Email Verification - {self.app_name}
        
        Hello,
        
        You have requested email verification. Please use the following 6-digit code to complete your verification:
        
        Verification Code: {verification_code}
        
        ⚠️ Important: This code will expire in 10 minutes for security reasons.
        
        If you didn't request this verification, please ignore this email.
        
        This is an automated message from {self.app_name}
        Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        return html_content, text_content
    
    def send_verification_email(self, recipient_email, custom_message=""):
        """Send verification email to the recipient"""
        try:
            # Generate verification code
            verification_code = self.generate_verification_code()
            
            # Store code with expiration time (10 minutes)
            expiration_time = datetime.now() + timedelta(minutes=10)
            self.verification_codes[recipient_email] = {
                'code': verification_code,
                'expires_at': expiration_time
            }
            
            # Create email content
            html_content, text_content = self.create_email_content(recipient_email, verification_code)
            
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = f"Email Verification Code - {self.app_name}"
            message["From"] = self.sender_email
            message["To"] = recipient_email
            
            # Add custom message if provided
            if custom_message:
                text_content = f"{custom_message}\n\n{text_content}"
                html_content = html_content.replace(
                    "<p>Hello,</p>", 
                    f"<p>Hello,</p><p>{custom_message}</p>"
                )
            
            # Create text and HTML parts
            text_part = MIMEText(text_content, "plain")
            html_part = MIMEText(html_content, "html")
            
            # Add parts to message
            message.attach(text_part)
            message.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            print(f"✅ Verification email sent successfully to {recipient_email}")
            print(f"📧 Verification code: {verification_code}")
            print(f"⏰ Code expires at: {expiration_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            return True, verification_code
            
        except Exception as e:
            print(f"❌ Failed to send email: {str(e)}")
            return False, None
    
    def verify_code(self, email, entered_code):
        """Verify if the entered code is correct and not expired"""
        if email not in self.verification_codes:
            return False, "No verification code found for this email"
        
        stored_data = self.verification_codes[email]
        
        # Check if code is expired
        if datetime.now() > stored_data['expires_at']:
            del self.verification_codes[email]
            return False, "Verification code has expired"
        
        # Check if code matches
        if stored_data['code'] == entered_code:
            del self.verification_codes[email]
            return True, "Verification successful"
        else:
            return False, "Invalid verification code"
    
    def cleanup_expired_codes(self):
        """Remove expired verification codes"""
        current_time = datetime.now()
        expired_emails = [
            email for email, data in self.verification_codes.items()
            if current_time > data['expires_at']
        ]
        
        for email in expired_emails:
            del self.verification_codes[email]
        
        if expired_emails:
            print(f"🧹 Cleaned up {len(expired_emails)} expired codes")

if __name__ == "__main__":
    # Example usage
    service = EmailVerificationService()
    
    # Test sending an email
    recipient = input("Enter recipient email: ")
    custom_msg = input("Enter custom message (optional): ")
    
    success, code = service.send_verification_email(recipient, custom_msg)
    
    if success:
        # Test verification
        while True:
            entered_code = input("Enter the verification code you received: ")
            is_valid, message = service.verify_code(recipient, entered_code)
            print(f"Result: {message}")
            
            if is_valid:
                break
            else:
                retry = input("Try again? (y/n): ")
                if retry.lower() != 'y':
                    break
