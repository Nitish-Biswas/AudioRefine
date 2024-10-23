from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import tempfile

class extracting_audio:
    
    def convert_stereo_to_mono(input_audio):
        try:
            print(input_audio)
            # Load the audio file
            audio = AudioSegment.from_wav(input_audio)
            
            # Convert to mono
            mono_audio = audio.set_channels(1)
            
            # Export the mono audio file
            temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            mono_audio.export(temp_audio.name, format="wav")
            
            return [True,temp_audio.name]
        
        except Exception as e:
            return [False,e]

    
    def extract_audio_from_video(video_file):
        try:
            video_clip = VideoFileClip(video_file)
            audio_clip = video_clip.audio
            temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            audio_clip.write_audiofile(temp_audio.name)
            print(temp_audio.name)
            return [True,temp_audio.name]
        except Exception as e:
            return [False,e]
