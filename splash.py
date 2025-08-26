import tkinter as tk
from tkinter import ttk
import time
import threading

class SplashScreen:
    def __init__(self, main_app_callback):
        self.main_app_callback = main_app_callback
        self.splash = tk.Toplevel()
        self.splash.title("")
        self.splash.geometry("500x300")
        self.splash.resizable(False, False)
        self.splash.configure(bg='#2C3E50')
        
        # Remove window decorations
        self.splash.overrideredirect(True)
        
        # Center the splash screen
        self.center_window()
        
        # Create gradient-like effect
        self.create_splash_content()
        
        # Start loading animation
        self.start_loading()
    
    def center_window(self):
        """Center the splash screen on the screen"""
        self.splash.update_idletasks()
        width = self.splash.winfo_width()
        height = self.splash.winfo_height()
        x = (self.splash.winfo_screenwidth() // 2) - (width // 2)
        y = (self.splash.winfo_screenheight() // 2) - (height // 2)
        self.splash.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_splash_content(self):
        """Create the splash screen content"""
        # Top gradient bar
        gradient_frame = tk.Frame(self.splash, bg='#3498DB', height=10)
        gradient_frame.pack(fill=tk.X)
        
        # Main content frame
        content_frame = tk.Frame(self.splash, bg='#2C3E50')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # App icon (using emoji)
        icon_label = tk.Label(content_frame, text="📧",
                             font=('Segoe UI', 48),
                             bg='#2C3E50', fg='#3498DB')
        icon_label.pack(pady=(20, 10))
        
        # App title
        title_label = tk.Label(content_frame, text="Email Verification Service",
                              font=('Segoe UI', 20, 'bold'),
                              bg='#2C3E50', fg='#ECF0F1')
        title_label.pack(pady=(0, 5))
        
        # Version
        version_label = tk.Label(content_frame, text="Version 2.0 - Modern Edition",
                                font=('Segoe UI', 12),
                                bg='#2C3E50', fg='#95A5A6')
        version_label.pack(pady=(0, 20))
        
        # Loading label
        self.loading_label = tk.Label(content_frame, text="Loading...",
                                     font=('Segoe UI', 11),
                                     bg='#2C3E50', fg='#3498DB')
        self.loading_label.pack(pady=(10, 0))
        
        # Progress bar
        self.progress = ttk.Progressbar(content_frame, mode='indeterminate',
                                       length=300, style='Modern.Horizontal.TProgressbar')
        self.progress.pack(pady=(10, 20))
        
        # Copyright
        copyright_label = tk.Label(content_frame, text="© 2025 Email Verification Service",
                                  font=('Segoe UI', 9),
                                  bg='#2C3E50', fg='#7F8C8D')
        copyright_label.pack(side=tk.BOTTOM)
    
    def start_loading(self):
        """Start the loading animation"""
        # Configure progress bar style
        style = ttk.Style()
        style.configure('Modern.Horizontal.TProgressbar',
                       background='#3498DB',
                       troughcolor='#34495E',
                       borderwidth=0,
                       lightcolor='#3498DB',
                       darkcolor='#3498DB')
        
        self.progress.start(10)
        
        # Simulate loading process
        self.loading_steps = [
            "Initializing components...",
            "Loading configuration...",
            "Setting up email service...",
            "Preparing modern UI...",
            "Finalizing setup...",
            "Ready to launch!"
        ]
        
        self.current_step = 0
        self.update_loading_text()
    
    def update_loading_text(self):
        """Update loading text with animation"""
        if self.current_step < len(self.loading_steps):
            self.loading_label.config(text=self.loading_steps[self.current_step])
            self.current_step += 1
            self.splash.after(800, self.update_loading_text)
        else:
            self.finish_loading()
    
    def finish_loading(self):
        """Finish loading and launch main app"""
        self.progress.stop()
        self.loading_label.config(text="Launching application...")
        
        # Wait a moment then launch main app
        self.splash.after(1000, self.launch_main_app)
    
    def launch_main_app(self):
        """Launch the main application"""
        self.splash.destroy()
        self.main_app_callback()

def show_splash_and_launch():
    """Show splash screen then launch main app"""
    def launch_main():
        from gui_app import main
        main()
    
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    splash = SplashScreen(launch_main)
    root.mainloop()

if __name__ == "__main__":
    show_splash_and_launch()
