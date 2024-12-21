"""Developer credit component with clickable link."""
import tkinter as tk
import webbrowser
from utils.config import COLORS, FONTS

class DeveloperCredit(tk.Frame):
    """A component that displays developer credit with a clickable link."""
    
    def __init__(self, parent):
        super().__init__(parent, bg=COLORS['background'])
        self.create_credit()
        
    def create_credit(self):
        """Create the developer credit label with link."""
        credit_label = tk.Label(
            self,
            text="DEVELOPED BY MITHUNCY",
            font=FONTS['credits'],
            bg=COLORS['background'],
            fg=COLORS['text'],
            cursor="hand2"
        )
        credit_label.pack(pady=(0, 5))
        credit_label.bind('<Button-1>', self._open_developer_link)
        
    def _open_developer_link(self, _):
        """Open the developer's GitHub profile."""
        webbrowser.open('https://github.com/Mithuncydev')