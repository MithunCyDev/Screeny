"""Main application window module."""
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess
from datetime import datetime
import shutil

from recorder.screen_recorder import ScreenRecorder
from gui.components.screen_selector import ScreenSelector
from gui.components.recording_border import RecordingBorder
from gui.components.floating_controls import FloatingControls
from gui.components.developer_credit import DeveloperCredit
from gui.components.rendering_progress import RenderingProgress
from gui.components.control_buttons import ControlButtons
from utils.config import COLORS, FONTS
from utils.icon_manager import IconManager

class RecorderApp:
    """Main application window class."""
    
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_components()
        self.setup_ui()
        
    def setup_window(self):
        """Configure the main window."""
        self.root.title("Screen Recorder")
        self.root.geometry("600x350")
        self.root.configure(bg=COLORS['background'])
        
          # Load application icon
        IconManager.load_app_icon(self.root)
        
    def setup_components(self):
        """Initialize application components."""
        self.recorder = ScreenRecorder()
        self.screen_selector = ScreenSelector()
        self.recording_border = RecordingBorder()
        self.recording_region = None
        self.floating_controls = None
        
    def setup_ui(self):
        """Set up the user interface."""
        # Main frame
        main_frame = tk.Frame(self.root, bg=COLORS['background'])
        main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        # Developer credit with 50% opacity
        developer_credit = DeveloperCredit(main_frame)
        developer_credit.pack(pady=(0, 5))
        developer_credit_label = developer_credit.winfo_children()[0]
        developer_credit_label.configure(fg=COLORS['developerText'], bg=COLORS['background'])
        developer_credit_label.bind("<Map>", lambda e: developer_credit_label.tk.call(
            "tk", "scaling", 0.5))
        
        # Title
        title = tk.Label(
            main_frame,
            text="Screeny",
            font=FONTS['title'],
            bg=COLORS['background'],
            fg=COLORS['title']
        )
        title.pack(pady=15)
        
        # Control buttons
        self.control_buttons = ControlButtons(
            main_frame,
            on_region_select=self.select_region,
            on_start=self.start_recording,
            on_stop=self.stop_recording
        )
        self.control_buttons.pack()
        
        # Status label
        self.status_label = tk.Label(
            main_frame,
            text="Ready to record",
            font=FONTS['small'],
            bg=COLORS['background'],
            fg=COLORS['text']
        )
        self.status_label.pack(pady=10)
        
    def select_region(self):
        """Handle region selection."""
        self.root.iconify()
        self.screen_selector.show_selection_window()
        self.recording_region = self.screen_selector.get_coordinates()
        self.root.deiconify()
        
        if self.recording_region:
            x, y, width, height = self.recording_region
            self.status_label.config(text=f"Selected region: {width}×{height}")
            
    def start_recording(self):
        """Start screen recording."""
        try:
            # Get recording dimensions
            if not self.recording_region:
                screen_width = self.root.winfo_screenwidth()
                screen_height = self.root.winfo_screenheight()
                width, height = screen_width, screen_height
                region = None
            else:
                width = self.recording_region[2]
                height = self.recording_region[3]
                region = self.recording_region
            
            # Show recording border if region is selected
            if region:
                self.recording_border.show_border(*region)
            
            # Start recording with region
            self.recorder.start_recording(width, height, region)
            
            # Update UI state
            self.root.iconify()
            self.control_buttons.update_button_states(recording=True)
            self.status_label.config(text="Recording...")
            
            # Show floating controls
            self.floating_controls = FloatingControls(self.stop_recording)
            self.floating_controls.show()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.recording_border.hide_border()
            
    def stop_recording(self):
        """Stop recording and save the file."""
        try:
            # Hide recording border first
            if hasattr(self, 'recording_border'):
                self.recording_border.hide_border()
            
            # Hide floating controls
            if hasattr(self, 'floating_controls') and self.floating_controls:
                self.floating_controls.hide()
                self.floating_controls = None
            
            # Show rendering progress
            progress = RenderingProgress(self.root)
            progress.update_status("Processing recording...")
            
            # Stop recording and get output path
            output_path = self.recorder.stop_recording()
            if not output_path:
                progress.finish()
                return
            
            # Restore main window
            self.root.deiconify()
            self.root.update()
            
            # Reset UI state
            self.control_buttons.update_button_states(recording=False)
            
            # Show save dialog
            progress.update_status("Saving recording...")
            initial_dir = os.path.dirname(output_path)
            file_path = filedialog.asksaveasfilename(
                defaultextension=".mp4",
                filetypes=[("MP4 files", "*.mp4")],
                initialdir=initial_dir,
                initialfile=f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4",
                parent=self.root
            )
            
            if file_path:
                shutil.move(output_path, file_path)
                save_dir = os.path.dirname(file_path)
                
                # Update status and show message
                self.status_label.config(text=f"Recording saved to: {file_path}")
                progress.finish()
                messagebox.showinfo(
                    "Success",
                    f"Recording saved to:\n{file_path}",
                    parent=self.root
                )
                
                # Open save directory
                if os.path.exists(save_dir):
                    if os.name == 'nt':
                        os.startfile(save_dir)
                    else:
                        subprocess.run(['xdg-open', save_dir])
            else:
                if os.path.exists(output_path):
                    os.remove(output_path)
                self.status_label.config(text="Recording discarded")
                progress.finish()
                
        except Exception as e:
            print(f"Error in stop_recording: {str(e)}")
            try:
                messagebox.showerror("Error", str(e), parent=self.root)
            except:
                pass