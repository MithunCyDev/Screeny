"""Styled button components with hover effects and modern design."""
import tkinter as tk
from utils.config import COLORS, FONTS
from gui.components.icons import Icons

class StyledButton(tk.Button):
    """A custom styled button with icons and hover effects."""
    
    def __init__(self, master, **kwargs):
        # Extract custom properties
        button_type = kwargs.pop('button_type', 'default')
        
        # Set icon based on button type
        icon = self._get_icon(button_type)
        if icon:
            text = kwargs.get('text', '')
            kwargs['text'] = f"{icon.symbol} {text}"
        
        # Set default styles based on button type
        if button_type == 'start':
            bg_color = COLORS['start_button']
            hover_color = COLORS['hover']['start']
            kwargs['width'] = 13
            kwargs['height'] = 1
        elif button_type == 'stop':
            bg_color = COLORS['stop_button']
            hover_color = COLORS['hover']['stop']
            kwargs['width'] = 13
            kwargs['height'] = 1
        else:  # region
            bg_color = COLORS['region_button']
            hover_color = COLORS['hover']['region']
            
        # Configure base button properties
        super().__init__(
            master,
            bg=bg_color,
            fg='white',
            font=FONTS['normal'],
            relief=tk.FLAT,
            cursor='hand2',
            activebackground=hover_color,
            activeforeground='white',
            borderwidth=0,
            padx=20 if icon else 10,  # Adjust padding based on icon presence
            pady=10,
            **kwargs
        )
        
        # Store colors for state management
        self._normal_bg = bg_color
        self._hover_bg = hover_color
        
        # Add hover effects
        self.bind('<Enter>', self._on_hover)
        self.bind('<Leave>', self._on_leave)
        
        # Add click effect
        self.bind('<Button-1>', self._on_click)
        self.bind('<ButtonRelease-1>', self._on_release)
        
    def _get_icon(self, button_type):
        """Get the appropriate icon for the button type."""
        if button_type == 'start':
            return Icons.RECORD
        elif button_type == 'stop':
            return Icons.STOP
        elif button_type == 'region':
            return Icons.REGION
        return None
        
    def _on_hover(self, event):
        """Handle mouse hover."""
        if self['state'] != 'disabled':
            self.configure(bg=self._hover_bg)
            
    def _on_leave(self, event):
        """Handle mouse leave."""
        if self['state'] != 'disabled':
            self.configure(bg=self._normal_bg)
            
    def _on_click(self, event):
        """Handle mouse click."""
        if self['state'] != 'disabled':
            self.configure(relief=tk.SUNKEN)
            
    def _on_release(self, event):
        """Handle mouse release."""
        if self['state'] != 'disabled':
            self.configure(relief=tk.FLAT)
            self._on_hover(event)