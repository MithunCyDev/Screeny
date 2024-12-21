"""Recording border display component."""
import tkinter as tk
from utils.config import COLORS

class RecordingBorder:
    """Shows a border around the recording area."""
    
    def __init__(self):
        self.border_windows = []
        
    def show_border(self, x, y, width, height):
        """Show border around recording area."""
        self.hide_border()  # Clean up any existing windows
        
        # Create windows for each border edge
        positions = [
            (x, y, width, 2),                    # Top
            (x, y + height - 2, width, 2),       # Bottom
            (x, y, 2, height),                   # Left
            (x + width - 2, y, 2, height)        # Right
        ]
        
        for pos in positions:
            try:
                window = tk.Toplevel()
                window.overrideredirect(True)
                window.attributes('-topmost', True, '-alpha', 0.8)
                window.geometry(f"{pos[2]}x{pos[3]}+{pos[0]}+{pos[1]}")
                
                frame = tk.Frame(window, bg=COLORS['selection_border'])
                frame.pack(fill='both', expand=True)
                
                self.border_windows.append(window)
            except tk.TclError:
                continue  # Skip if window creation fails
        
    def hide_border(self):
        """Hide the recording border."""
        for window in self.border_windows[:]:  # Create a copy of the list
            try:
                if window.winfo_exists():
                    window.destroy()
            except:
                pass  # Ignore any destroy errors
        self.border_windows.clear()