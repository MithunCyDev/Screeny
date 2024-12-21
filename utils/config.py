"""Configuration settings for the screen recorder application."""
import os

# Available recording resolutions
RESOLUTIONS = [
    "800x400",
    "1024x576",
    "1280x720",
    "1920x1080"
]

# Default directory for saving recordings
DEFAULT_SAVE_DIR = os.path.join(os.path.expanduser("~"), "Videos")

# Recording settings
FRAME_RATE = 20
AUDIO_SAMPLE_RATE = 44100
AUDIO_CHANNELS = 2

# UI Colors
COLORS = {
    'background': "#10233f",
    'developerText': "#213c63",
    'text': "#ebece4",
    'title': "#0093ab",
    'start_button': "#076271", 
    'stop_button': "#ff2828",   
    'region_button': "#173663", 
    'selection_border': "#00a2bd",
    'hover': {
        'start': "#004955",    
        'stop': "#dc0000",     
        'region': "#173663",    
    }
}

# UI Font settings
FONTS = {
    'title': ("Helvetica", 26, "bold"),
    'normal': ("Helvetica", 12, "bold"),
    'small': ("Helvetica", 10),
    'credits': ("Helvetica", 8, "normal")
}