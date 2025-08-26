# Email Verification Service

A Python application that sends verification emails with 6-digit codes. Perfect for email confirmation, two-factor authentication, or any verification workflow.

## 🚀 Features

- **Send Verification Emails**: Send professional-looking emails with 6-digit verification codes
- **HTML & Text Format**: Beautiful HTML emails with fallback text version
- **Code Expiration**: Verification codes expire after 10 minutes for security
- **Multiple Interfaces**: Both GUI and command-line interfaces available
- **Code Verification**: Built-in verification system to validate codes
- **Automatic Cleanup**: Expired codes are automatically cleaned up
- **Customizable Messages**: Add custom messages to verification emails
- **Gmail Integration**: Pre-configured for Gmail SMTP (easily adaptable for other providers)

## 📋 Requirements

- Python 3.6+
- Gmail account with App Password enabled
- Internet connection for sending emails

## ⚙️ Setup

### 1. Install Dependencies

Run the setup script:
```bash
setup.bat
```

Or manually install:
```bash
pip install python-dotenv
```

### 2. Configure Gmail App Password

1. Go to your Google Account settings
2. Enable 2-Factor Authentication
3. Generate an App Password:
   - Go to Security → 2-Step Verification → App Passwords
   - Select "Mail" and generate a password
   - Use this password (not your regular Gmail password)

### 3. Configure Email Settings

Edit the `.env` file or configure through the application:
```
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
APP_NAME=Email Verification Service
```

## 🖥️ Usage

### GUI Version (Recommended)

```bash
python gui_app.py
```

Features:
- User-friendly interface
- Real-time logging
- Configuration management
- Email sending and verification

### Command Line Version

```bash
python cli_app.py
```

Features:
- Interactive menu system
- Step-by-step guidance
- Full functionality in terminal

### Direct Integration

```python
from email_service import EmailVerificationService

# Initialize service
service = EmailVerificationService()

# Send verification email
success, code = service.send_verification_email(
    "user@example.com", 
    "Welcome! Please verify your email."
)

# Verify code
is_valid, message = service.verify_code("user@example.com", "123456")
```

## 📧 Email Features

### Professional Design
- Clean, modern HTML layout
- Responsive design
- Clear code presentation
- Security warnings
- Branding customization

### Security Features
- 6-digit random codes
- 10-minute expiration
- Automatic cleanup
- Secure code generation

### Customization
- Custom messages
- App name configuration
- SMTP server flexibility
- Message templates

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SENDER_EMAIL` | Your Gmail address | Required |
| `SENDER_PASSWORD` | Gmail App Password | Required |
| `SMTP_SERVER` | SMTP server address | smtp.gmail.com |
| `SMTP_PORT` | SMTP port number | 587 |
| `APP_NAME` | Application name in emails | Email Verification Service |

### SMTP Providers

#### Gmail (Default)
```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

#### Outlook/Hotmail
```
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
```

#### Yahoo
```
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
```

## 📁 File Structure

```
Auto Email/
├── email_service.py      # Core email service class
├── gui_app.py           # GUI application
├── cli_app.py           # Command-line application
├── setup.bat            # Windows setup script
├── requirements.txt     # Python dependencies
├── .env                # Configuration file
└── README.md           # This file
```

## 🛠️ Core Components

### EmailVerificationService Class

Main methods:
- `send_verification_email(recipient, custom_message="")`: Send verification email
- `verify_code(email, code)`: Verify entered code
- `generate_verification_code()`: Generate 6-digit code
- `cleanup_expired_codes()`: Remove expired codes

### GUI Features
- Configuration management
- Email sending interface
- Code verification
- Activity logging
- Status updates

### CLI Features
- Interactive menu system
- Step-by-step workflows
- Configuration wizard
- Real-time feedback

## 🔒 Security Considerations

1. **App Passwords**: Use Gmail App Passwords, not regular passwords
2. **Environment Variables**: Store credentials in `.env` file
3. **Code Expiration**: Codes expire automatically after 10 minutes
4. **Secure Generation**: Uses cryptographically secure random generation
5. **No Storage**: Codes are stored in memory only (not persistent)

## 🎨 Customization

### Email Template
Modify the `create_email_content()` method in `email_service.py` to customize:
- HTML styling
- Email layout
- Colors and fonts
- Company branding

### Code Length
Change the code generation in `generate_verification_code()`:
```python
def generate_verification_code(self, length=6):
    return ''.join(random.choices(string.digits, k=length))
```

### Expiration Time
Modify expiration time in `send_verification_email()`:
```python
expiration_time = datetime.now() + timedelta(minutes=15)  # 15 minutes
```

## 🐛 Troubleshooting

### Common Issues

1. **"Authentication failed"**
   - Ensure 2FA is enabled on Gmail
   - Use App Password, not regular password
   - Check email and password are correct

2. **"Connection refused"**
   - Check internet connection
   - Verify SMTP server settings
   - Check firewall/antivirus blocking

3. **"Import 'dotenv' could not be resolved"**
   - Run: `pip install python-dotenv`
   - Or use the setup.bat script

4. **"No module named 'email_service'"**
   - Ensure all files are in the same directory
   - Run from the correct directory

### Debug Mode
Add debug output to `email_service.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📝 Examples

### Basic Usage
```python
service = EmailVerificationService()
success, code = service.send_verification_email("user@example.com")
if success:
    print(f"Code sent: {code}")
```

### With Custom Message
```python
custom_msg = "Welcome to our service! Please verify your email to continue."
success, code = service.send_verification_email("user@example.com", custom_msg)
```

### Verification Workflow
```python
# Send code
service.send_verification_email("user@example.com")

# User enters code
user_code = input("Enter verification code: ")

# Verify
is_valid, message = service.verify_code("user@example.com", user_code)
print(message)
```

## 🤝 Contributing

Feel free to:
- Report bugs
- Suggest features
- Submit improvements
- Add new email providers
- Enhance the UI/UX

## 📄 License

This project is open source and available under the MIT License.

## 🙋‍♂️ Support

If you encounter any issues:
1. Check the troubleshooting section
2. Verify your configuration
3. Test with a simple email first
4. Check Gmail security settings

---

**Happy coding! 📧✨**
