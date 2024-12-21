"""Floating control window with recording timer."""
import tkinter as tk
from datetime import datetime, timedelta
from utils.config import COLORS, FONTS

class FloatingControls:
    def __init__(self, stop_callback):
        self.window = None
        self.timer_label = None
        self.start_time = None
        self.stop_callback = stop_callback
        self._drag_data = {"x": 0, "y": 0}
        self._is_destroyed = False
        
    def show(self):
        """Create and show the floating control window."""
        if self.window and self.window.winfo_exists():
            return
            
        self._is_destroyed = False
        self.window = tk.Toplevel()
        
        # Configure window
        self.window.title("Recording Controls")
        self.window.attributes('-topmost', True)
        self.window.overrideredirect(True)
        self.window.configure(bg=COLORS['background'])
        
        # Position window in top-right corner
        window_width = 200
        window_height = 100
        screen_width = self.window.winfo_screenwidth()
        x = screen_width - window_width - 20
        self.window.geometry(f"{window_width}x{window_height}+{x}+20")
        
        # Create main frame with border
        main_frame = tk.Frame(
            self.window,
            bg=COLORS['background'],
            highlightbackground=COLORS['text'],
            highlightthickness=1,
            bd=0
        )
        main_frame.pack(expand=True, fill='both')
        
        # Title bar for dragging
        title_bar = tk.Frame(
            main_frame,
            bg=COLORS['background'],
            height=25,
            cursor="fleur"
        )
        title_bar.pack(fill='x')
        title_bar.bind('<Button-1>', self.start_drag)
        title_bar.bind('<B1-Motion>', self.drag)
        
        # Timer label
        self.timer_label = tk.Label(
            main_frame,
            text="00:00:00",
            font=FONTS['normal'],
            bg=COLORS['background'],
            fg=COLORS['text']
        )
        self.timer_label.pack(pady=5)
        
        # Stop button
        stop_button = tk.Button(
            main_frame,
            text="Stop Recording",
            command=self._on_stop,
            bg=COLORS['stop_button'],
            fg="white",
            font=FONTS['normal'],
            relief=tk.FLAT,
            cursor="hand2",
            activebackground=COLORS['hover']['stop'],
            activeforeground="white"
        )
        stop_button.pack(pady=5)
        
        # Start timer
        self.start_time = datetime.now()
        self.update_timer()
        
    def start_drag(self, event):
        """Start window drag."""
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
        
    def drag(self, event):
        """Handle window dragging."""
        if self.window:
            x = self.window.winfo_x() + (event.x - self._drag_data["x"])
            y = self.window.winfo_y() + (event.y - self._drag_data["y"])
            self.window.geometry(f"+{x}+{y}")
        
    def update_timer(self):
        """Update the recording timer."""
        if not self._is_destroyed and self.window and self.window.winfo_exists():
            try:
                elapsed = datetime.now() - self.start_time
                elapsed = timedelta(seconds=int(elapsed.total_seconds()))
                self.timer_label.config(text=str(elapsed))
                self.window.after(1000, self.update_timer)
            except tk.TclError:
                pass
                
    def _on_stop(self):
        """Handle stop button click."""
        if not self._is_destroyed:
            self._is_destroyed = True
            if self.window and self.window.winfo_exists():
                self.window.destroy()
            if self.stop_callback:
                self.stop_callback()
        
    def hide(self):
        """Hide the floating controls."""
        self._is_destroyed = True
        if self.window and self.window.winfo_exists():
            try:
                self.window.destroy()
            except tk.TclError:
                pass
        self.window = None