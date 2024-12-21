"""Icon management utilities."""
import os
import tkinter as tk
from PIL import Image, ImageTk

class IconManager:
    """Manages application icons and their loading."""
    
    @staticmethod
    def load_app_icon(window):
        """Load and set the application icon."""
        try:
            icon_path = os.path.join('assets', 'icons', 'icon.ico')
            if os.path.exists(icon_path):
                window.iconbitmap(icon_path)
            return True
        except Exception as e:
            print(f"Failed to load application icon: {e}")
            return False