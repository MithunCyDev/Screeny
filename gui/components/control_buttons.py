"""Control buttons component for the screen recorder."""
import tkinter as tk
from gui.components.styled_buttons import StyledButton

class ControlButtons(tk.Frame):
    """Component containing the main control buttons."""
    
    def __init__(self, parent, on_region_select, on_start, on_stop):
        super().__init__(parent, bg=parent['bg'])
        self.on_region_select = on_region_select
        self.on_start = on_start
        self.on_stop = on_stop
        self.setup_buttons()
        
    def setup_buttons(self):
        """Set up the control buttons."""
        # Region selection button
        self.region_button = StyledButton(
            self,
            text="Select Region",
            command=self.on_region_select,
            button_type='region'
        )
        self.region_button.pack(pady=10)
        
        # Recording controls frame
        buttons_frame = tk.Frame(self, bg=self['bg'])
        buttons_frame.pack(pady=20)
        
        # Start button
        self.start_button = StyledButton(
            buttons_frame,
            text="Start Recording",
            command=self.on_start,
            button_type='start'
        )
        self.start_button.pack(side=tk.LEFT, padx=10)
        
        # Stop button
        self.stop_button = StyledButton(
            buttons_frame,
            text="Stop Recording",
            command=self.on_stop,
            button_type='stop',
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=10)
        
    def update_button_states(self, recording=False):
        """Update button states based on recording status."""
        if recording:
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.region_button.config(state=tk.DISABLED)
        else:
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.region_button.config(state=tk.NORMAL)