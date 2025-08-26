import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from email_service import EmailVerificationService
import os
import json
from datetime import datetime

class EmailVerificationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Verification Service")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Settings file for persistent storage
        self.settings_file = "app_settings.json"
        
        # Initialize email service
        self.email_service = EmailVerificationService()
        
        # Load saved settings
        self.load_settings()
        
        # Create main container
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Email Verification Service", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Configuration Section
        config_frame = ttk.LabelFrame(main_frame, text="Email Configuration", padding="10")
        config_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        config_frame.columnconfigure(1, weight=1)
        
        # Sender Email
        ttk.Label(config_frame, text="Sender Email:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.sender_email_var = tk.StringVar(value=self.email_service.sender_email or "")
        self.sender_email_entry = ttk.Entry(config_frame, textvariable=self.sender_email_var, width=40)
        self.sender_email_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2)
        
        # Sender Password
        ttk.Label(config_frame, text="App Password:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.sender_password_var = tk.StringVar(value=self.email_service.sender_password or "")
        self.sender_password_entry = ttk.Entry(config_frame, textvariable=self.sender_password_var, 
                                             show="*", width=40)
        self.sender_password_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2)
        
        # Update config button
        ttk.Button(config_frame, text="Update Configuration", 
                  command=self.update_config).grid(row=2, column=1, sticky=tk.E, pady=(10, 0))
        
        # Send Email Section
        send_frame = ttk.LabelFrame(main_frame, text="Send Verification Email", padding="10")
        send_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        send_frame.columnconfigure(1, weight=1)
        
        # Recipient Email
        ttk.Label(send_frame, text="Recipient Email:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.recipient_email_var = tk.StringVar()
        
        # Create combobox for recipient email with history
        self.recipient_email_combo = ttk.Combobox(send_frame, textvariable=self.recipient_email_var, width=37)
        self.recipient_email_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2)
        
        # Load recent recipients
        self.load_recent_recipients()
        
        # Custom Message
        ttk.Label(send_frame, text="Custom Message:").grid(row=1, column=0, sticky=(tk.W, tk.N), pady=2)
        self.custom_message_text = scrolledtext.ScrolledText(send_frame, height=3, width=40)
        self.custom_message_text.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2)
        
        # Load last custom message if available
        if hasattr(self, 'last_custom_message') and self.last_custom_message:
            self.custom_message_text.insert(1.0, self.last_custom_message)
        
        # Send button and clear recipients button
        button_frame = ttk.Frame(send_frame)
        button_frame.grid(row=3, column=1, sticky=tk.E, pady=(10, 0))
        
        self.send_button = ttk.Button(button_frame, text="Send Verification Email", 
                                     command=self.send_email_threaded)
        self.send_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        ttk.Button(button_frame, text="Clear Recent", 
                  command=self.clear_recent_recipients).pack(side=tk.RIGHT)
        
        # Verify Code Section
        verify_frame = ttk.LabelFrame(main_frame, text="Verify Code", padding="10")
        verify_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        verify_frame.columnconfigure(1, weight=1)
        
        # Email for verification
        ttk.Label(verify_frame, text="Email:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.verify_email_var = tk.StringVar()
        self.verify_email_entry = ttk.Entry(verify_frame, textvariable=self.verify_email_var, width=40)
        self.verify_email_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2)
        
        # Verification code
        ttk.Label(verify_frame, text="Verification Code:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.verify_code_var = tk.StringVar()
        self.verify_code_entry = ttk.Entry(verify_frame, textvariable=self.verify_code_var, width=20)
        self.verify_code_entry.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Verify button
        ttk.Button(verify_frame, text="Verify Code", 
                  command=self.verify_code).grid(row=2, column=1, sticky=tk.E, pady=(10, 0))
        
        # Log Section
        log_frame = ttk.LabelFrame(main_frame, text="Activity Log", padding="10")
        log_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Log text area
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Clear log button
        ttk.Button(log_frame, text="Clear Log", 
                  command=self.clear_log).grid(row=1, column=0, sticky=tk.E, pady=(10, 0))
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Bind Enter key events
        self.recipient_email_combo.bind('<Return>', lambda e: self.send_email_threaded())
        self.verify_code_entry.bind('<Return>', lambda e: self.verify_code())
        
        # Bind window close event to save settings
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Log startup messages now that log_text is available
        self.log_message("Email Verification Service started")
        
        if self.settings_loaded:
            self.log_message("✅ Settings loaded successfully")
            if self.recent_recipients:
                self.log_message(f"📧 Found {len(self.recent_recipients)} recent recipients")
        else:
            if hasattr(self, 'load_error'):
                self.log_message(f"⚠️ Could not load settings: {self.load_error}")
            else:
                self.log_message("📝 Using default settings (first run)")
        
        self.log_message("Ready to send verification emails!")
    
    def load_settings(self):
        """Load saved settings from file"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    
                self.recent_recipients = settings.get('recent_recipients', [])
                self.last_custom_message = settings.get('last_custom_message', '')
                self.window_geometry = settings.get('window_geometry', '800x600')
                
                # Apply window geometry
                if self.window_geometry:
                    self.root.geometry(self.window_geometry)
                    
                self.settings_loaded = True
            else:
                # Initialize default settings
                self.recent_recipients = []
                self.last_custom_message = ''
                self.window_geometry = '800x600'
                self.settings_loaded = False
                
        except Exception as e:
            self.recent_recipients = []
            self.last_custom_message = ''
            self.window_geometry = '800x600'
            self.settings_loaded = False
            self.load_error = str(e)
    
    def save_settings(self):
        """Save current settings to file"""
        try:
            settings = {
                'recent_recipients': self.recent_recipients[:10],  # Keep only last 10
                'last_custom_message': self.custom_message_text.get(1.0, tk.END).strip(),
                'window_geometry': self.root.geometry(),
                'last_saved': datetime.now().isoformat()
            }
            
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
                
            self.log_message("💾 Settings saved successfully")
            
        except Exception as e:
            self.log_message(f"⚠️ Could not save settings: {e}")
    
    def load_recent_recipients(self):
        """Load recent recipients into combobox"""
        if hasattr(self, 'recent_recipients') and self.recent_recipients:
            self.recipient_email_combo['values'] = self.recent_recipients
            # Set the most recent email as default
            if self.recent_recipients:
                self.recipient_email_var.set(self.recent_recipients[0])
    
    def add_recent_recipient(self, email):
        """Add email to recent recipients list"""
        if not hasattr(self, 'recent_recipients'):
            self.recent_recipients = []
            
        # Remove if already exists
        if email in self.recent_recipients:
            self.recent_recipients.remove(email)
        
        # Add to beginning
        self.recent_recipients.insert(0, email)
        
        # Keep only last 10
        self.recent_recipients = self.recent_recipients[:10]
        
        # Update combobox
        self.recipient_email_combo['values'] = self.recent_recipients
    
    def clear_recent_recipients(self):
        """Clear recent recipients list"""
        result = messagebox.askyesno("Clear Recent Recipients", 
                                   "Are you sure you want to clear all recent recipients?")
        if result:
            self.recent_recipients = []
            self.recipient_email_combo['values'] = []
            self.recipient_email_var.set("")
            self.save_settings()
            self.log_message("🗑️ Recent recipients cleared")

    def on_closing(self):
        """Handle window closing event"""
        self.save_settings()
        self.log_message("👋 Goodbye! Settings saved.")
        self.root.destroy()

    def log_message(self, message):
        """Add message to log with timestamp"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_log(self):
        """Clear the log text area"""
        self.log_text.delete(1.0, tk.END)
    
    def update_config(self):
        """Update email service configuration"""
        try:
            self.email_service.sender_email = self.sender_email_var.get()
            self.email_service.sender_password = self.sender_password_var.get()
            
            # Save to .env file
            env_content = f"""# Email Configuration
SENDER_EMAIL={self.sender_email_var.get()}
SENDER_PASSWORD={self.sender_password_var.get()}
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# App Configuration
APP_NAME=Email Verification Service"""
            
            with open('.env', 'w') as f:
                f.write(env_content)
            
            self.log_message("✅ Configuration updated successfully")
            self.status_var.set("Configuration updated")
            messagebox.showinfo("Success", "Configuration updated successfully!")
            
        except Exception as e:
            self.log_message(f"❌ Failed to update configuration: {str(e)}")
            messagebox.showerror("Error", f"Failed to update configuration: {str(e)}")
    
    def send_email_threaded(self):
        """Send email in a separate thread to prevent UI freezing"""
        def send_email():
            try:
                recipient = self.recipient_email_var.get().strip()
                custom_message = self.custom_message_text.get(1.0, tk.END).strip()
                
                if not recipient:
                    messagebox.showerror("Error", "Please enter recipient email")
                    return
                
                if not self.email_service.sender_email or not self.email_service.sender_password:
                    messagebox.showerror("Error", "Please configure sender email and password")
                    return
                
                self.send_button.config(state='disabled')
                self.status_var.set("Sending email...")
                self.log_message(f"📤 Sending verification email to {recipient}")
                
                success, code = self.email_service.send_verification_email(recipient, custom_message)
                
                if success:
                    # Save recipient to recent list
                    self.add_recent_recipient(recipient)
                    self.save_settings()  # Auto-save after successful send
                    
                    self.log_message(f"✅ Email sent successfully to {recipient}")
                    self.log_message(f"🔢 Verification code: {code}")
                    self.log_message(f"💾 Saved {recipient} to recent recipients")
                    self.verify_email_var.set(recipient)  # Auto-fill verification email
                    self.status_var.set("Email sent successfully")
                    messagebox.showinfo("Success", f"Verification email sent to {recipient}\nCode: {code}")
                else:
                    self.log_message(f"❌ Failed to send email to {recipient}")
                    self.status_var.set("Failed to send email")
                    messagebox.showerror("Error", "Failed to send email. Check your configuration.")
                
            except Exception as e:
                self.log_message(f"❌ Error: {str(e)}")
                self.status_var.set("Error occurred")
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
            
            finally:
                self.send_button.config(state='normal')
        
        threading.Thread(target=send_email, daemon=True).start()
    
    def verify_code(self):
        """Verify the entered code"""
        try:
            email = self.verify_email_var.get().strip()
            code = self.verify_code_var.get().strip()
            
            if not email or not code:
                messagebox.showerror("Error", "Please enter both email and verification code")
                return
            
            self.log_message(f"🔍 Verifying code for {email}")
            is_valid, message = self.email_service.verify_code(email, code)
            
            if is_valid:
                self.log_message(f"✅ {message}")
                self.status_var.set("Verification successful")
                messagebox.showinfo("Success", message)
                # Clear fields after successful verification
                self.verify_email_var.set("")
                self.verify_code_var.set("")
            else:
                self.log_message(f"❌ {message}")
                self.status_var.set("Verification failed")
                messagebox.showerror("Verification Failed", message)
                
        except Exception as e:
            self.log_message(f"❌ Error during verification: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    root = tk.Tk()
    app = EmailVerificationGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
