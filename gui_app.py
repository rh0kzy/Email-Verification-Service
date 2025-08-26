import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, font
import threading
from email_service import EmailVerificationService
import os
import json
from datetime import datetime

class EmailVerificationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("📧 Email Verification Service")
        self.root.geometry("900x700")
        
        # Modern color scheme
        self.colors = {
            'primary': '#2E86C1',      # Modern blue
            'secondary': '#F39C12',     # Orange accent
            'success': '#27AE60',       # Green
            'danger': '#E74C3C',        # Red
            'warning': '#F1C40F',       # Yellow
            'light': '#ECF0F1',         # Light gray
            'dark': '#2C3E50',          # Dark blue-gray
            'white': '#FFFFFF',
            'gradient_start': '#667eea',
            'gradient_end': '#764ba2'
        }
        
        # Configure modern styling
        self.setup_modern_style()
        
        # Settings file for persistent storage
        self.settings_file = "app_settings.json"
        
        # Initialize email service
        self.email_service = EmailVerificationService()
        
        # Load saved settings
        self.load_settings()
        
        # Initialize variables
        self.initialize_variables()
        
        # Create modern UI
        self.create_modern_ui()
    
    def initialize_variables(self):
        """Initialize all tkinter variables"""
        self.sender_email_var = tk.StringVar(value=self.email_service.sender_email or "")
        self.sender_password_var = tk.StringVar(value=self.email_service.sender_password or "")
        self.recipient_email_var = tk.StringVar()
        self.verify_email_var = tk.StringVar()
        self.verify_code_var = tk.StringVar()
        
        # Create modern UI
        self.create_modern_ui()
    
    def setup_modern_style(self):
        """Setup modern styling for the application"""
        style = ttk.Style()
        
        # Configure modern theme
        style.theme_use('clam')
        
        # Custom styles for modern look
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 24, 'bold'),
                       foreground=self.colors['dark'],
                       background=self.colors['white'])
        
        style.configure('Subtitle.TLabel',
                       font=('Segoe UI', 12),
                       foreground=self.colors['primary'],
                       background=self.colors['white'])
        
        style.configure('Modern.TFrame',
                       background=self.colors['white'],
                       relief='flat',
                       borderwidth=0)
        
        style.configure('Card.TFrame',
                       background=self.colors['white'],
                       relief='solid',
                       borderwidth=1)
        
        style.configure('Primary.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       foreground=self.colors['white'],
                       background=self.colors['primary'],
                       borderwidth=0,
                       focuscolor='none')
        
        style.map('Primary.TButton',
                 background=[('active', '#2471A3'),
                           ('pressed', '#1B4F72')])
        
        style.configure('Success.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       foreground=self.colors['white'],
                       background=self.colors['success'],
                       borderwidth=0,
                       focuscolor='none')
        
        style.configure('Warning.TButton',
                       font=('Segoe UI', 9),
                       foreground=self.colors['dark'],
                       background=self.colors['warning'],
                       borderwidth=0,
                       focuscolor='none')
        
        style.configure('Modern.TEntry',
                       font=('Segoe UI', 10),
                       borderwidth=2,
                       relief='solid',
                       focuscolor=self.colors['primary'])
        
        style.configure('Modern.TCombobox',
                       font=('Segoe UI', 10),
                       borderwidth=2,
                       relief='solid')
        
        style.configure('Modern.TLabelFrame',
                       font=('Segoe UI', 11, 'bold'),
                       foreground=self.colors['dark'],
                       background=self.colors['white'],
                       borderwidth=2,
                       relief='solid')
        
        style.configure('Modern.TLabelFrame.Label',
                       font=('Segoe UI', 11, 'bold'),
                       foreground=self.colors['primary'],
                       background=self.colors['white'])
    
    def create_modern_ui(self):
        """Create the modern UI layout"""
        # Set window background
        self.root.configure(bg=self.colors['light'])
        
        # Create main container with padding
        self.main_container = tk.Frame(self.root, bg=self.colors['light'])
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create header section
        self.create_header()
        
        # Create content area with cards
        self.create_content_area()
        
        # Create footer
        self.create_footer()
        
        # Apply final touches
        self.apply_modern_touches()
    
    def create_header(self):
        """Create modern header section"""
        header_frame = tk.Frame(self.main_container, bg=self.colors['white'], relief='solid', bd=1)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Add gradient-like effect with multiple frames
        gradient_frame = tk.Frame(header_frame, height=5, bg=self.colors['primary'])
        gradient_frame.pack(fill=tk.X)
        
        content_frame = tk.Frame(header_frame, bg=self.colors['white'])
        content_frame.pack(fill=tk.X, padx=30, pady=20)
        
        # App title with emoji
        title_label = tk.Label(content_frame, 
                              text="📧 Email Verification Service",
                              font=('Segoe UI', 28, 'bold'),
                              fg=self.colors['dark'],
                              bg=self.colors['white'])
        title_label.pack()
        
        # Subtitle
        subtitle_label = tk.Label(content_frame,
                                 text="Send beautiful verification emails with 6-digit codes",
                                 font=('Segoe UI', 12),
                                 fg=self.colors['primary'],
                                 bg=self.colors['white'])
        subtitle_label.pack(pady=(5, 0))
    
    def create_content_area(self):
        """Create content area with modern cards"""
        content_frame = tk.Frame(self.main_container, bg=self.colors['light'])
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left column
        left_column = tk.Frame(content_frame, bg=self.colors['light'])
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Right column  
        right_column = tk.Frame(content_frame, bg=self.colors['light'])
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Create cards
        self.create_config_card(left_column)
        self.create_send_card(left_column)
        self.create_verify_card(right_column)
        self.create_log_card(right_column)
    
    def create_config_card(self, parent):
        """Create email configuration card"""
        card = self.create_card(parent, "⚙️ Email Configuration", self.colors['primary'])
        
        # Email input
        self.create_modern_input(card, "📧 Sender Email:", self.sender_email_var, 
                               "Enter your Gmail address")
        
        # Password input
        self.create_modern_input(card, "🔑 App Password:", self.sender_password_var, 
                               "Enter Gmail App Password", show="*")
        
        # Update button
        btn_frame = tk.Frame(card, bg=self.colors['white'])
        btn_frame.pack(fill=tk.X, pady=(15, 0))
        
        update_btn = tk.Button(btn_frame, text="💾 Update Configuration",
                              command=self.update_config,
                              bg=self.colors['success'],
                              fg=self.colors['white'],
                              font=('Segoe UI', 10, 'bold'),
                              relief='flat',
                              padx=20, pady=8,
                              cursor='hand2')
        update_btn.pack(side=tk.RIGHT)
        
        # Hover effects
        self.add_hover_effect(update_btn, self.colors['success'], '#229954')
    
    def create_send_card(self, parent):
        """Create send email card"""
        card = self.create_card(parent, "📤 Send Verification Email", self.colors['secondary'])
        
        # Recipient email with history
        recipient_frame = tk.Frame(card, bg=self.colors['white'])
        recipient_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(recipient_frame, text="📧 Recipient Email:",
                font=('Segoe UI', 10, 'bold'),
                fg=self.colors['dark'],
                bg=self.colors['white']).pack(anchor='w')
        
        self.recipient_email_combo = ttk.Combobox(recipient_frame, 
                                                 textvariable=self.recipient_email_var,
                                                 style='Modern.TCombobox',
                                                 font=('Segoe UI', 11))
        self.recipient_email_combo.pack(fill=tk.X, pady=(5, 0))
        
        # Load recent recipients
        self.load_recent_recipients()
        
        # Custom message
        msg_frame = tk.Frame(card, bg=self.colors['white'])
        msg_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        tk.Label(msg_frame, text="💬 Custom Message:",
                font=('Segoe UI', 10, 'bold'),
                fg=self.colors['dark'],
                bg=self.colors['white']).pack(anchor='w')
        
        # Custom message text area with modern styling
        text_frame = tk.Frame(msg_frame, bg=self.colors['white'], relief='solid', bd=2)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        self.custom_message_text = tk.Text(text_frame, height=3,
                                          font=('Segoe UI', 10),
                                          bg=self.colors['white'],
                                          fg=self.colors['dark'],
                                          relief='flat',
                                          wrap=tk.WORD,
                                          padx=10, pady=8)
        self.custom_message_text.pack(fill=tk.BOTH, expand=True)
        
        # Load last custom message
        if hasattr(self, 'last_custom_message') and self.last_custom_message:
            self.custom_message_text.insert(1.0, self.last_custom_message)
        
        # Buttons
        btn_frame = tk.Frame(card, bg=self.colors['white'])
        btn_frame.pack(fill=tk.X, pady=(15, 0))
        
        # Clear recent button
        clear_btn = tk.Button(btn_frame, text="🗑️ Clear Recent",
                             command=self.clear_recent_recipients,
                             bg=self.colors['light'],
                             fg=self.colors['dark'],
                             font=('Segoe UI', 9),
                             relief='flat',
                             padx=15, pady=6,
                             cursor='hand2')
        clear_btn.pack(side=tk.LEFT)
        
        # Send button
        self.send_button = tk.Button(btn_frame, text="🚀 Send Verification Email",
                                    command=self.send_email_threaded,
                                    bg=self.colors['primary'],
                                    fg=self.colors['white'],
                                    font=('Segoe UI', 11, 'bold'),
                                    relief='flat',
                                    padx=25, pady=10,
                                    cursor='hand2')
        self.send_button.pack(side=tk.RIGHT)
        
        # Hover effects
        self.add_hover_effect(clear_btn, self.colors['light'], '#D5DBDB')
        self.add_hover_effect(self.send_button, self.colors['primary'], '#2471A3')
    
    def create_verify_card(self, parent):
        """Create verification card"""
        card = self.create_card(parent, "🔍 Verify Code", self.colors['success'])
        
        # Email input
        self.create_modern_input(card, "📧 Email:", self.verify_email_var, 
                               "Enter email to verify")
        
        # Code input
        self.create_modern_input(card, "🔢 Verification Code:", self.verify_code_var, 
                               "Enter 6-digit code")
        
        # Verify button
        btn_frame = tk.Frame(card, bg=self.colors['white'])
        btn_frame.pack(fill=tk.X, pady=(15, 0))
        
        verify_btn = tk.Button(btn_frame, text="✅ Verify Code",
                              command=self.verify_code,
                              bg=self.colors['success'],
                              fg=self.colors['white'],
                              font=('Segoe UI', 11, 'bold'),
                              relief='flat',
                              padx=25, pady=10,
                              cursor='hand2')
        verify_btn.pack(side=tk.RIGHT)
        
        self.add_hover_effect(verify_btn, self.colors['success'], '#229954')
    
    def create_log_card(self, parent):
        """Create activity log card"""
        card = self.create_card(parent, "📋 Activity Log", self.colors['dark'])
        
        # Log text area with modern styling
        log_frame = tk.Frame(card, bg=self.colors['white'], relief='solid', bd=2)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.log_text = tk.Text(log_frame, height=12,
                               font=('Consolas', 9),
                               bg='#2C3E50',
                               fg='#ECF0F1',
                               relief='flat',
                               wrap=tk.WORD,
                               padx=15, pady=10)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(log_frame, command=self.log_text.yview,
                                bg=self.colors['dark'],
                                troughcolor=self.colors['light'])
        self.log_text.config(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Clear log button
        clear_log_btn = tk.Button(card, text="🧹 Clear Log",
                                 command=self.clear_log,
                                 bg=self.colors['warning'],
                                 fg=self.colors['dark'],
                                 font=('Segoe UI', 9),
                                 relief='flat',
                                 padx=15, pady=6,
                                 cursor='hand2')
        clear_log_btn.pack(side=tk.RIGHT)
        
        self.add_hover_effect(clear_log_btn, self.colors['warning'], '#F4D03F')
    
    def create_footer(self):
        """Create modern footer with status"""
        footer_frame = tk.Frame(self.main_container, bg=self.colors['white'], relief='solid', bd=1)
        footer_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Status bar
        status_frame = tk.Frame(footer_frame, bg=self.colors['white'])
        status_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Status indicator
        self.status_indicator = tk.Label(status_frame, text="🟢", 
                                        font=('Segoe UI', 12),
                                        bg=self.colors['white'])
        self.status_indicator.pack(side=tk.LEFT)
        
        # Status text
        self.status_var = tk.StringVar(value="Ready to send emails")
        status_label = tk.Label(status_frame, textvariable=self.status_var,
                               font=('Segoe UI', 10),
                               fg=self.colors['dark'],
                               bg=self.colors['white'])
        status_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # App info
        info_label = tk.Label(status_frame, text="📧 Email Verification Service v2.0",
                             font=('Segoe UI', 9),
                             fg=self.colors['primary'],
                             bg=self.colors['white'])
        info_label.pack(side=tk.RIGHT)
    
    def create_card(self, parent, title, accent_color):
        """Create a modern card with shadow effect"""
        # Card container with shadow effect
        card_container = tk.Frame(parent, bg=self.colors['light'])
        card_container.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Shadow frame
        shadow_frame = tk.Frame(card_container, bg='#BDC3C7', height=5)
        shadow_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Main card
        card = tk.Frame(card_container, bg=self.colors['white'], relief='solid', bd=1)
        card.pack(fill=tk.BOTH, expand=True)
        
        # Card header with accent color
        header_frame = tk.Frame(card, bg=accent_color, height=8)
        header_frame.pack(fill=tk.X)
        
        # Title
        title_frame = tk.Frame(card, bg=self.colors['white'])
        title_frame.pack(fill=tk.X, padx=20, pady=(15, 15))
        
        title_label = tk.Label(title_frame, text=title,
                              font=('Segoe UI', 14, 'bold'),
                              fg=self.colors['dark'],
                              bg=self.colors['white'])
        title_label.pack(anchor='w')
        
        # Content area
        content_frame = tk.Frame(card, bg=self.colors['white'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        return content_frame
    
    def create_modern_input(self, parent, label_text, var, placeholder="", show=None):
        """Create a modern input field"""
        input_frame = tk.Frame(parent, bg=self.colors['white'])
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Label
        label = tk.Label(input_frame, text=label_text,
                        font=('Segoe UI', 10, 'bold'),
                        fg=self.colors['dark'],
                        bg=self.colors['white'])
        label.pack(anchor='w')
        
        # Input field with modern styling
        entry_frame = tk.Frame(input_frame, bg=self.colors['white'], relief='solid', bd=2)
        entry_frame.pack(fill=tk.X, pady=(5, 0))
        
        entry = tk.Entry(entry_frame, textvariable=var,
                        font=('Segoe UI', 11),
                        bg=self.colors['white'],
                        fg=self.colors['dark'],
                        relief='flat',
                        show=show,
                        insertbackground=self.colors['primary'])
        entry.pack(fill=tk.X, padx=10, pady=8)
        
        # Placeholder effect
        if placeholder:
            self.add_placeholder_effect(entry, placeholder)
        
        return entry
    
    def add_placeholder_effect(self, entry, placeholder_text):
        """Add placeholder effect to entry"""
        def on_focus_in(event):
            if entry.get() == placeholder_text:
                entry.delete(0, tk.END)
                entry.config(fg=self.colors['dark'])
        
        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, placeholder_text)
                entry.config(fg='#95A5A6')
        
        entry.insert(0, placeholder_text)
        entry.config(fg='#95A5A6')
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)
    
    def add_hover_effect(self, widget, normal_color, hover_color):
        """Add hover effect to buttons"""
        def on_enter(event):
            widget.config(bg=hover_color)
        
        def on_leave(event):
            widget.config(bg=normal_color)
        
        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)
    
    def apply_modern_touches(self):
        """Apply final modern touches"""
        # Bind events
        self.recipient_email_combo.bind('<Return>', lambda e: self.send_email_threaded())
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Log startup messages
        self.log_startup_messages()
    
    def log_startup_messages(self):
        """Log startup messages now that log_text is available"""
        self.log_message("🚀 Email Verification Service started")
        
        if self.settings_loaded:
            self.log_message("✅ Settings loaded successfully")
            if self.recent_recipients:
                self.log_message(f"📧 Found {len(self.recent_recipients)} recent recipients")
        else:
            if hasattr(self, 'load_error'):
                self.log_message(f"⚠️ Could not load settings: {self.load_error}")
            else:
                self.log_message("📝 Using default settings (first run)")
        
        self.log_message("🎨 Modern UI loaded successfully")
        self.log_message("Ready to send beautiful verification emails!")

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
        """Add message to log with timestamp and color coding"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Color code messages based on content
        if "✅" in message or "Success" in message:
            color = "#27AE60"  # Green
        elif "❌" in message or "Failed" in message or "Error" in message:
            color = "#E74C3C"  # Red
        elif "⚠️" in message or "Warning" in message:
            color = "#F39C12"  # Orange
        elif "📧" in message or "Email" in message:
            color = "#3498DB"  # Blue
        elif "🔢" in message or "Code" in message:
            color = "#9B59B6"  # Purple
        elif "💾" in message or "Saved" in message:
            color = "#16A085"  # Teal
        else:
            color = "#ECF0F1"  # Light gray
        
        # Configure text tags for colors
        self.log_text.tag_configure("colored", foreground=color)
        
        # Insert colored message
        self.log_text.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.log_text.insert(tk.END, f"{message}\n", "colored")
        self.log_text.see(tk.END)
        
        # Update status indicator based on message
        if "✅" in message or "Success" in message:
            self.status_indicator.config(text="🟢")
            self.status_var.set("Operation successful")
        elif "❌" in message or "Failed" in message:
            self.status_indicator.config(text="🔴")
            self.status_var.set("Operation failed")
        elif "📤" in message or "Sending" in message:
            self.status_indicator.config(text="🟡")
            self.status_var.set("Sending email...")
        
        self.root.update_idletasks()
    
    def clear_log(self):
        """Clear the log text area with confirmation"""
        result = messagebox.askyesno("Clear Log", "Are you sure you want to clear the activity log?")
        if result:
            self.log_text.delete(1.0, tk.END)
            self.log_message("🧹 Activity log cleared")
            self.status_indicator.config(text="🟢")
            self.status_var.set("Log cleared")
    
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
