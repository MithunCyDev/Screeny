"""Button icons using Unicode symbols for a modern look."""
from dataclasses import dataclass

@dataclass
class ButtonIcon:
    """Represents a button icon with symbol and padding."""
    symbol: str
    padding: int = 5

class Icons:
    """Collection of button icons using Unicode symbols."""
    RECORD = ButtonIcon("⏺")
    STOP = ButtonIcon("⏹")
    REGION = ButtonIcon("⊡")
    
    # Alternative symbols if needed:
    # RECORD = ButtonIcon("●")
    # STOP = ButtonIcon("■")
    # REGION = ButtonIcon("▣")