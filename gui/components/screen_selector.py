"""Screen region selection with visual feedback."""
import tkinter as tk
from utils.config import COLORS, FONTS

class ScreenSelector:
    def __init__(self):
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.selection_window = None
        self.selection = None
        self.is_selecting = False
        self.dimensions_label = None
        
    def show_selection_window(self):
        """Show a fullscreen transparent window for region selection."""
        try:
            self.selection_window = tk.Toplevel()
            self.selection_window.attributes('-fullscreen', True, '-alpha', 0.3, '-topmost', True)
            self.selection_window.configure(bg='black')
            
            # Create canvas for drawing selection
            self.selection = tk.Canvas(
                self.selection_window,
                highlightthickness=0,
                bg='black'
            )
            self.selection.pack(fill='both', expand=True)
            
            # Create floating dimensions label
            self.dimensions_label = tk.Label(
                self.selection_window,
                font=FONTS['normal'],
                bg=COLORS['background'],
                fg='white',
                padx=10,
                pady=5
            )
            
            # Instructions
            self.selection.create_text(
                self.selection_window.winfo_screenwidth() // 2,
                50,
                text="Click and drag to select a region\nPress ESC to cancel, ENTER to confirm",
                fill='white',
                font=FONTS['normal'],
                justify=tk.CENTER
            )
            
            # Bind events
            self.selection.bind('<Button-1>', self._on_mouse_down)
            self.selection.bind('<B1-Motion>', self._on_mouse_drag)
            self.selection.bind('<ButtonRelease-1>', self._on_mouse_up)
            self.selection_window.bind('<Escape>', lambda e: self._cancel_selection())
            self.selection_window.bind('<Return>', lambda e: self._confirm_selection())
            
            # Grab focus
            self.selection_window.focus_force()
            
            self.selection_window.wait_window()
        except Exception as e:
            print(f"Error in screen selection: {e}")
            self._cancel_selection()
        
    def _on_mouse_down(self, event):
        """Handle mouse button press."""
        self.start_x = event.x
        self.start_y = event.y
        self.is_selecting = True
        self.selection.delete('all')  # Clear previous selection
        
        # Show instructions again
        self.selection.create_text(
            self.selection_window.winfo_screenwidth() // 2,
            50,
            text="Click and drag to select a region\nPress ESC to cancel, ENTER to confirm",
            fill='white',
            font=FONTS['normal'],
            justify=tk.CENTER
        )
        
    def _on_mouse_drag(self, event):
        """Handle mouse drag to draw selection rectangle."""
        if not self.is_selecting:
            return
            
        # Clear previous selection
        self.selection.delete('selection', 'dimensions')
        
        # Draw new selection rectangle
        x1, y1 = min(self.start_x, event.x), min(self.start_y, event.y)
        x2, y2 = max(self.start_x, event.x), max(self.start_y, event.y)
        
        # Draw selection rectangle
        self.selection.create_rectangle(
            x1, y1, x2, y2,
            outline=COLORS['selection_border'],
            width=2,
            tags='selection'
        )
        
        # Update dimensions label
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        self.dimensions_label.config(text=f"{width} × {height}")
        
        # Position dimensions label
        label_x = (x1 + x2) // 2
        label_y = y1 - 30 if y1 > 50 else y2 + 30
        self.dimensions_label.place(x=label_x, y=label_y, anchor='center')
        
    def _on_mouse_up(self, event):
        """Handle mouse button release."""
        if not self.is_selecting:
            return
            
        self.end_x = event.x
        self.end_y = event.y
        self.is_selecting = False
        
        # Add confirmation instructions
        self.selection.create_text(
            self.selection_window.winfo_screenwidth() // 2,
            self.selection_window.winfo_screenheight() - 50,
            text="Press ENTER to confirm selection or ESC to cancel",
            fill='white',
            font=FONTS['normal'],
            justify=tk.CENTER
        )
        
    def _confirm_selection(self, event=None):
        """Confirm the selection and close the window."""
        if self.start_x is not None and self.end_x is not None:
            self.selection_window.destroy()
        
    def _cancel_selection(self):
        """Cancel the selection process."""
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.is_selecting = False
        if self.selection_window:
            self.selection_window.destroy()
        
    def get_coordinates(self):
        """Return the selected region coordinates."""
        if not all([self.start_x, self.start_y, self.end_x, self.end_y]):
            return None
            
        # Ensure coordinates are positive
        x1, x2 = sorted([self.start_x, self.end_x])
        y1, y2 = sorted([self.start_y, self.end_y])
        
        # Calculate dimensions
        width = x2 - x1
        height = y2 - y1
        
        return (x1, y1, width, height) if width > 0 and height > 0 else None