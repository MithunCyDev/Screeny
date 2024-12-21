"""Main recorder class that coordinates video and audio recording."""
import threading
import os
from recorder.video_recorder import VideoRecorder
from recorder.audio_recorder import AudioRecorder
from utils.video_processor import combine_audio_video
from utils.config import DEFAULT_SAVE_DIR

class ScreenRecorder:
    """Main recorder class that coordinates video and audio recording."""
    
    def __init__(self):
        self.video_recorder = VideoRecorder()
        self.audio_recorder = AudioRecorder()
        self.video_thread = None
        self.audio_thread = None
        self.temp_video = None
        self.temp_audio = None
        self.recording_region = None
        
    def start_recording(self, width, height, region=None):
        """Start both video and audio recording."""
        if self.video_recorder.recording or self.audio_recorder.recording:
            return
            
        # Store recording region
        self.recording_region = region
            
        # Ensure save directory exists
        os.makedirs(DEFAULT_SAVE_DIR, exist_ok=True)
        
        # Start recorders and get temporary file paths
        self.temp_video = self.video_recorder.start(width, height, region)
        self.temp_audio = self.audio_recorder.start()
        
        # Create and start recording threads
        self.video_thread = threading.Thread(
            target=self._record_video_thread,
            args=(width, height),
            daemon=True
        )
        self.audio_thread = threading.Thread(
            target=self.audio_recorder.record_audio,
            daemon=True
        )
        
        self.video_thread.start()
        self.audio_thread.start()
        
    def _record_video_thread(self, width, height):
        """Video recording thread function."""
        try:
            # Use region dimensions if available
            if self.recording_region:
                width = self.recording_region[2]
                height = self.recording_region[3]
                
            writer = self.video_recorder.get_writer(width, height)
            while self.video_recorder.recording:
                self.video_recorder.record_frame(width, height, writer)
            writer.release()
        except Exception as e:
            print(f"Error in video recording thread: {e}")
            self.video_recorder.recording = False
        
    def stop_recording(self):
        """Stop recording and combine video and audio."""
        if not (self.video_recorder.recording or self.audio_recorder.recording):
            return None
            
        # Stop recorders
        self.video_recorder.stop()
        self.audio_recorder.stop()
        
        # Wait for threads to finish with timeout
        if self.video_thread and self.video_thread.is_alive():
            self.video_thread.join(timeout=2.0)
        if self.audio_thread and self.audio_thread.is_alive():
            self.audio_thread.join(timeout=2.0)
        
        try:
            # Combine video and audio
            output_path = combine_audio_video(self.temp_video, self.temp_audio)
            
            # Clean up temporary files
            for temp_file in [self.temp_video, self.temp_audio]:
                if temp_file and os.path.exists(temp_file):
                    try:
                        os.remove(temp_file)
                    except:
                        pass
            
            return output_path
            
        except Exception as e:
            # Clean up on error
            for temp_file in [self.temp_video, self.temp_audio]:
                if temp_file and os.path.exists(temp_file):
                    try:
                        os.remove(temp_file)
                    except:
                        pass
            raise e