"""Component to display rendering progress with a modern design."""
import tkinter as tk
from tkinter import ttk
from utils.config import COLORS, FONTS

class RenderingProgress:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Processing Recording")
        
        # Configure window position (center of the screen)
        window_width = 400
        window_height = 120
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        # Configure window appearance
        self.window.configure(bg=COLORS['background'])
        self.window.attributes('-topmost', True)
        self.window.overrideredirect(True)  # Remove window decorations
        self.window.resizable(False, False)
        
        # Create main frame with border
        main_frame = tk.Frame(
            self.window,
            bg=COLORS['background'],
            highlightbackground=COLORS['text'],
            highlightthickness=1,
            bd=0
        )
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)
        
        # Status message
        self.status_label = tk.Label(
            main_frame,
            text="Processing...",
            font=FONTS['normal'],
            bg=COLORS['background'],
            fg=COLORS['text']
        )
        self.status_label.pack(pady=(15, 10))
        
        # Progress bar style
        style = ttk.Style()
        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor=COLORS['background'],
            background=COLORS['start_button'],
            darkcolor=COLORS['start_button'],
            lightcolor=COLORS['start_button'],
            bordercolor=COLORS['background']
        )
        
        # Progress bar
        self.progress = ttk.Progressbar(
            main_frame,
            style="Custom.Horizontal.TProgressbar",
            length=350,
            mode='indeterminate'
        )
        self.progress.pack(pady=(0, 15), padx=20)
        
        # Start progress animation
        self.progress.start(15)
        
    def update_status(self, message):
        """Update the status message."""
        try:
            self.status_label.config(text=message)
            self.window.update()
        except tk.TclError:
            pass
        
    def finish(self):
        """Clean up and close the progress window."""
        try:
            self.progress.stop()
            self.window.destroy()
        except tk.TclError:
            pass