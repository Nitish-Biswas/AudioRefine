from google.cloud import speech, texttospeech
import tempfile
from pydub import AudioSegment
import subprocess
import os

class transforming:
    def transcribe_audio(audio_file_path):
        try:
            client = speech.SpeechClient()

            with open(audio_file_path, "rb") as audio_file:
                content = audio_file.read()

            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                language_code="en-US",  # Omitting sample_rate_hertz here
                enable_word_time_offsets=True,  # Enable word timestamps
                enable_automatic_punctuation=True
            )

            response = client.recognize(config=config, audio=audio)
            
            transcript = ""
            word_timings = []
                
            for result in response.results:
                for word_info in result.alternatives[0].words:
                    word_timings.append({
                        'word': word_info.word,
                        'start_time': word_info.start_time.total_seconds(),
                        'end_time': word_info.end_time.total_seconds()
                    })
                transcript += result.alternatives[0].transcript + " "
                    
            return [True, word_timings]
        except Exception as e:
            return [False, e]


    def generate_timed_speech(enhanced_segments):
        """Generate speech with specific timing for each segment."""
        try:
            segment_audios = []
            seg_record=[]
            client = texttospeech.TextToSpeechClient()
            
            for segment in enhanced_segments:
                if not segment['text']:
                    continue
                input_text = texttospeech.SynthesisInput(text=segment['text'])
                voice = texttospeech.VoiceSelectionParams(
                    language_code="en-US",
                    name="en-US-Journey-D"
                )
                
                # Calculate desired duration for this segment
                desired_duration = segment['timing']['end'] - segment['timing']['start']
                
                # First generate with normal rate to get base duration
                audio_config = texttospeech.AudioConfig(
                    audio_encoding=texttospeech.AudioEncoding.LINEAR16,
                    speaking_rate=1.0
                )
                
                response = client.synthesize_speech(
                    input=input_text,
                    voice=voice,
                    audio_config=audio_config
                )
                
                # Save temporary file to check duration
                temp_check = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
                with open(temp_check.name, "wb") as out:
                    out.write(response.audio_content)
                
                # Get duration of generated audio
                temp_audio = AudioSegment.from_file(temp_check.name)
                base_duration = len(temp_audio)/1000
                
                print(base_duration)
                
                # Calculate required speaking rate
                speaking_rate = base_duration / desired_duration
                
                # Clamp speaking rate to reasonable bounds (0.25x to 4x)
                speaking_rate = max(0.25, min(4.0, speaking_rate))
                
                temp_segment = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
                command = [
                    "ffmpeg","-y", "-i", temp_check.name, 
                    "-filter:a", f"atempo={speaking_rate}", 
                    "-vn", temp_segment.name
                ]
                subprocess.run(command)
                
                
                os.unlink(temp_check.name)
                audio123 = AudioSegment.from_file(temp_segment.name)
                current_duration123 = len(audio123)/1000
                
                
                segment_audios.append({
                    'path': temp_segment.name,
                    'timing': segment['timing'],
                    "text": segment['text'],
                    'base': base_duration,
                    "des":current_duration123,
                    # 'speaking_rate': speaking_rate
                })
                seg_record.append({
                    "text": segment['text'],
                    'base': base_duration,
                    "des":current_duration123,
                    'timing': segment['timing'],
                })
            
            return [True,segment_audios]
        except Exception as e:
        
            return [False,e]