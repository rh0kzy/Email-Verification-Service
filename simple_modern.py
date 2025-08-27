import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
from email_service import EmailVerificationService
import os
import json
from datetime import datetime

class SimpleModernGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("📧 Email Verification Service - Modern")
        self.root.geometry("1000x650")
        
        # Modern dark theme colors
        self.bg_color = '#2b2b3d'
        self.card_color = '#3a3a52'
        self.accent_color = '#ff6b6b'
        self.text_color = '#ffffff'
        self.secondary_text = '#b0b0b0'
        
        self.root.configure(bg=self.bg_color)
        
        # Settings
        self.settings_file = "app_settings.json"
        self.email_service = EmailVerificationService()
        self.load_settings()
        
        # Setup styles
        self.setup_styles()
        
        # Create UI
        self.create_ui()
        
        # Bind events
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Show startup messages
        self.show_startup_messages()
    
    def setup_styles(self):
        """Setup modern ttk styles"""
        style = ttk.Style()
        
        # Modern button style
        style.configure('Modern.TButton',
                       background=self.accent_color,
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 10, 'bold'))
        
        style.map('Modern.TButton',
                 background=[('active', '#ff5252')])
        
        # Modern entry style
        style.configure('Modern.TEntry',
                       fieldbackground=self.card_color,
                       foreground=self.text_color,
                       borderwidth=1,
                       insertcolor=self.text_color)
        
        # Modern combobox style
        style.configure('Modern.TCombobox',
                       fieldbackground=self.card_color,
                       foreground=self.text_color,
                       borderwidth=1)
    
    def create_ui(self):
        """Create the user interface"""
        # Header
        header_frame = tk.Frame(self.root, bg='#1a1a2e', height=70)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        
        # Title
        tk.Label(header_frame, text="📧 Email Verification Service", 
                font=('Segoe UI', 18, 'bold'), bg='#1a1a2e', fg=self.text_color).pack(side=tk.LEFT, pady=20)
        
        # Time
        self.time_var = tk.StringVar()
        tk.Label(header_frame, textvariable=self.time_var, 
                font=('Segoe UI', 10), bg='#1a1a2e', fg=self.secondary_text).pack(side=tk.RIGHT, pady=20)
        self.update_time()
        
        # Main content area
        content_frame = tk.Frame(self.root, bg=self.bg_color)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left panel
        left_frame = tk.Frame(content_frame, bg=self.card_color, relief='solid', bd=1)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Right panel
        right_frame = tk.Frame(content_frame, bg=self.card_color, relief='solid', bd=1)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Create sections
        self.create_config_section(left_frame)
        self.create_send_section(left_frame)
        self.create_verify_section(right_frame)
        self.create_log_section(right_frame)
        self.create_status_bar()
    
    def create_config_section(self, parent):
        """Create configuration section"""
        # Header
        tk.Label(parent, text="⚙️ Email Configuration", 
                font=('Segoe UI', 12, 'bold'), bg=self.card_color, fg=self.accent_color).pack(pady=(15, 10))
        
        config_frame = tk.Frame(parent, bg=self.card_color)
        config_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Sender Email
        tk.Label(config_frame, text="📧 Sender Email:", 
                font=('Segoe UI', 10), bg=self.card_color, fg=self.text_color).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.sender_email_var = tk.StringVar(value=self.email_service.sender_email or "")
        self.sender_email_entry = ttk.Entry(config_frame, textvariable=self.sender_email_var, 
                                           style='Modern.TEntry', width=35)
        self.sender_email_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # Sender Password
        tk.Label(config_frame, text="🔑 App Password:", 
                font=('Segoe UI', 10), bg=self.card_color, fg=self.text_color).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.sender_password_var = tk.StringVar(value=self.email_service.sender_password or "")
        self.sender_password_entry = ttk.Entry(config_frame, textvariable=self.sender_password_var,
                                              show="*", style='Modern.TEntry', width=35)
        self.sender_password_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # Update button
        ttk.Button(config_frame, text="💾 Update Config", 
                  style='Modern.TButton',
                  command=self.update_config).grid(row=2, column=1, sticky=tk.E, pady=(15, 0))
        
        config_frame.columnconfigure(1, weight=1)
    
    def create_send_section(self, parent):
        """Create send email section"""
        # Header
        tk.Label(parent, text="📤 Send Verification Email", 
                font=('Segoe UI', 12, 'bold'), bg=self.card_color, fg=self.accent_color).pack(pady=(20, 10))
        
        send_frame = tk.Frame(parent, bg=self.card_color)
        send_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Recipient Email
        tk.Label(send_frame, text="👤 Recipient Email:", 
                font=('Segoe UI', 10), bg=self.card_color, fg=self.text_color).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.recipient_email_var = tk.StringVar()
        self.recipient_email_combo = ttk.Combobox(send_frame, textvariable=self.recipient_email_var,
                                                 style='Modern.TCombobox', width=32)
        self.recipient_email_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        self.recipient_email_combo.bind('<Return>', lambda e: self.send_email_threaded())
        
        # Load recent recipients
        self.load_recent_recipients()
        
        # Custom Message
        tk.Label(send_frame, text="💬 Custom Message:", 
                font=('Segoe UI', 10), bg=self.card_color, fg=self.text_color).grid(row=1, column=0, sticky=(tk.W, tk.N), pady=(15, 5))
        
        self.custom_message_text = tk.Text(send_frame, height=4, width=35,
                                          bg='#2a2a3a', fg=self.text_color,
                                          insertbackground=self.text_color,
                                          font=('Segoe UI', 9), wrap=tk.WORD,
                                          relief='solid', bd=1)
        self.custom_message_text.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0), pady=(15, 5))
        
        # Load last custom message
        if hasattr(self, 'last_custom_message') and self.last_custom_message:
            self.custom_message_text.insert(1.0, self.last_custom_message)
        
        # Buttons
        button_frame = tk.Frame(send_frame, bg=self.card_color)
        button_frame.grid(row=2, column=1, sticky=tk.E, pady=(15, 0))
        
        ttk.Button(button_frame, text="🗑️ Clear Recent", 
                  style='Modern.TButton',
                  command=self.clear_recent_recipients).pack(side=tk.RIGHT, padx=(5, 0))
        
        self.send_button = ttk.Button(button_frame, text="🚀 Send Email", 
                                     style='Modern.TButton',
                                     command=self.send_email_threaded)
        self.send_button.pack(side=tk.RIGHT)
        
        send_frame.columnconfigure(1, weight=1)
        send_frame.rowconfigure(1, weight=1)
    
    def create_verify_section(self, parent):
        """Create verification section"""
        # Header
        tk.Label(parent, text="🔍 Verify Code", 
                font=('Segoe UI', 12, 'bold'), bg=self.card_color, fg=self.accent_color).pack(pady=(15, 10))
        
        verify_frame = tk.Frame(parent, bg=self.card_color)
        verify_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Email
        tk.Label(verify_frame, text="📧 Email:", 
                font=('Segoe UI', 10), bg=self.card_color, fg=self.text_color).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.verify_email_var = tk.StringVar()
        self.verify_email_entry = ttk.Entry(verify_frame, textvariable=self.verify_email_var,
                                           style='Modern.TEntry', width=30)
        self.verify_email_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        
        # Code
        tk.Label(verify_frame, text="🔢 Code:", 
                font=('Segoe UI', 10), bg=self.card_color, fg=self.text_color).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.verify_code_var = tk.StringVar()
        self.verify_code_entry = ttk.Entry(verify_frame, textvariable=self.verify_code_var,
                                          style='Modern.TEntry', width=15, font=('Consolas', 12))
        self.verify_code_entry.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        self.verify_code_entry.bind('<Return>', lambda e: self.verify_code())
        
        # Verify button
        ttk.Button(verify_frame, text="✅ Verify Code", 
                  style='Modern.TButton',
                  command=self.verify_code).grid(row=2, column=1, sticky=tk.E, pady=(15, 0))
        
        verify_frame.columnconfigure(1, weight=1)
    
    def create_log_section(self, parent):
        """Create log section"""
        # Header
        tk.Label(parent, text="📋 Activity Log", 
                font=('Segoe UI', 12, 'bold'), bg=self.card_color, fg=self.accent_color).pack(pady=(20, 10))
        
        log_frame = tk.Frame(parent, bg=self.card_color)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Log text with scrollbar
        self.log_text = scrolledtext.ScrolledText(log_frame, height=12, width=40,
                                                 bg='#2a2a3a', fg=self.text_color,
                                                 insertbackground=self.text_color,
                                                 font=('Consolas', 9), wrap=tk.WORD,
                                                 relief='solid', bd=1, state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Clear button
        ttk.Button(log_frame, text="🗑️ Clear Log", 
                  style='Modern.TButton',
                  command=self.clear_log).pack(anchor=tk.E)
    
    def create_status_bar(self):
        """Create status bar"""
        status_frame = tk.Frame(self.root, bg='#1a1a2e', height=35)
        status_frame.pack(fill=tk.X, padx=20, pady=(10, 20))
        status_frame.pack_propagate(False)
        
        self.status_var = tk.StringVar(value="🟢 Ready")
        tk.Label(status_frame, textvariable=self.status_var,
                bg='#1a1a2e', fg=self.secondary_text,
                font=('Segoe UI', 9)).pack(side=tk.LEFT, pady=8)
    
    def update_time(self):
        """Update time display"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_var.set(f"🕒 {current_time}")
        self.root.after(1000, self.update_time)
    
    def show_startup_messages(self):
        """Show startup messages"""
        self.log_message("🚀 Modern Email Verification Service started")
        if hasattr(self, 'settings_loaded') and self.settings_loaded:
            self.log_message("✅ Settings loaded successfully")
            if hasattr(self, 'recent_recipients') and self.recent_recipients:
                self.log_message(f"📧 Found {len(self.recent_recipients)} recent recipients")
        else:
            self.log_message("📝 Using default settings (first run)")
        self.log_message("💼 Ready to send verification emails!")
    
    def log_message(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.config(state=tk.DISABLED)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_log(self):
        """Clear log"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.log_message("🧹 Log cleared")
    
    # Include all the existing methods for settings, email sending, etc.
    def load_settings(self):
        """Load saved settings"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                self.recent_recipients = settings.get('recent_recipients', [])
                self.last_custom_message = settings.get('last_custom_message', '')
                self.settings_loaded = True
            else:
                self.recent_recipients = []
                self.last_custom_message = ''
                self.settings_loaded = False
        except Exception as e:
            self.recent_recipients = []
            self.last_custom_message = ''
            self.settings_loaded = False
    
    def save_settings(self):
        """Save settings"""
        try:
            settings = {
                'recent_recipients': self.recent_recipients[:10],
                'last_custom_message': self.custom_message_text.get(1.0, tk.END).strip(),
                'last_saved': datetime.now().isoformat()
            }
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
            self.log_message("💾 Settings saved")
        except Exception as e:
            self.log_message(f"⚠️ Could not save settings: {e}")
    
    def load_recent_recipients(self):
        """Load recent recipients"""
        if hasattr(self, 'recent_recipients') and self.recent_recipients:
            self.recipient_email_combo['values'] = self.recent_recipients
            if self.recent_recipients:
                self.recipient_email_var.set(self.recent_recipients[0])
    
    def add_recent_recipient(self, email):
        """Add recent recipient"""
        if not hasattr(self, 'recent_recipients'):
            self.recent_recipients = []
        if email in self.recent_recipients:
            self.recent_recipients.remove(email)
        self.recent_recipients.insert(0, email)
        self.recent_recipients = self.recent_recipients[:10]
        self.recipient_email_combo['values'] = self.recent_recipients
    
    def clear_recent_recipients(self):
        """Clear recent recipients"""
        if messagebox.askyesno("Clear Recent", "Clear all recent recipients?"):
            self.recent_recipients = []
            self.recipient_email_combo['values'] = []
            self.recipient_email_var.set("")
            self.save_settings()
            self.log_message("🗑️ Recent recipients cleared")
    
    def update_config(self):
        """Update configuration"""
        try:
            self.email_service.sender_email = self.sender_email_var.get()
            self.email_service.sender_password = self.sender_password_var.get()
            
            env_content = f"""# Email Configuration
SENDER_EMAIL={self.sender_email_var.get()}
SENDER_PASSWORD={self.sender_password_var.get()}
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# App Configuration
APP_NAME=Email Verification Service"""
            
            with open('.env', 'w') as f:
                f.write(env_content)
            
            self.log_message("✅ Configuration updated")
            self.status_var.set("🟢 Configuration updated")
            messagebox.showinfo("Success", "Configuration updated!")
        except Exception as e:
            self.log_message(f"❌ Failed to update config: {e}")
            messagebox.showerror("Error", f"Failed to update config: {e}")
    
    def send_email_threaded(self):
        """Send email in thread"""
        def send_email():
            try:
                recipient = self.recipient_email_var.get().strip()
                custom_message = self.custom_message_text.get(1.0, tk.END).strip()
                
                if not recipient:
                    messagebox.showerror("Error", "Please enter recipient email")
                    return
                
                if not self.email_service.sender_email or not self.email_service.sender_password:
                    messagebox.showerror("Error", "Please configure email settings")
                    return
                
                self.send_button.config(state='disabled')
                self.status_var.set("🚀 Sending email...")
                self.log_message(f"📤 Sending verification email to {recipient}")
                
                success, code = self.email_service.send_verification_email(recipient, custom_message)
                
                if success:
                    self.add_recent_recipient(recipient)
                    self.save_settings()
                    self.log_message(f"✅ Email sent to {recipient}")
                    self.log_message(f"🔢 Code: {code}")
                    self.verify_email_var.set(recipient)
                    self.status_var.set("🟢 Email sent successfully")
                    messagebox.showinfo("Success", f"Email sent to {recipient}\nCode: {code}")
                else:
                    self.log_message(f"❌ Failed to send email to {recipient}")
                    self.status_var.set("🔴 Failed to send email")
                    messagebox.showerror("Error", "Failed to send email")
            except Exception as e:
                self.log_message(f"❌ Error: {e}")
                self.status_var.set("🔴 Error occurred")
                messagebox.showerror("Error", f"Error: {e}")
            finally:
                self.send_button.config(state='normal')
        
        threading.Thread(target=send_email, daemon=True).start()
    
    def verify_code(self):
        """Verify code"""
        try:
            email = self.verify_email_var.get().strip()
            code = self.verify_code_var.get().strip()
            
            if not email or not code:
                messagebox.showerror("Error", "Please enter email and code")
                return
            
            self.log_message(f"🔍 Verifying code for {email}")
            is_valid, message = self.email_service.verify_code(email, code)
            
            if is_valid:
                self.log_message(f"✅ {message}")
                self.status_var.set("🟢 Verification successful")
                messagebox.showinfo("Success", message)
                self.verify_email_var.set("")
                self.verify_code_var.set("")
            else:
                self.log_message(f"❌ {message}")
                self.status_var.set("🔴 Verification failed")
                messagebox.showerror("Failed", message)
        except Exception as e:
            self.log_message(f"❌ Verification error: {e}")
            messagebox.showerror("Error", f"Error: {e}")
    
    def on_closing(self):
        """Handle window closing"""
        self.save_settings()
        self.log_message("👋 Goodbye!")
        self.root.destroy()

def main():
    root = tk.Tk()
    app = SimpleModernGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
