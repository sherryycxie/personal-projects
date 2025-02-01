import openai
import os
from pydub import AudioSegment

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def convert_to_wav(audio_path):
    """Convert audio file to WAV format if needed."""
    if audio_path.endswith('.wav'):
        return audio_path
    
    audio = AudioSegment.from_file(audio_path)
    wav_path = audio_path.rsplit('.', 1)[0] + '.wav'
    audio.export(wav_path, format='wav')
    return wav_path

def transcribe_audio(audio_path):
    """Transcribe audio file using OpenAI Whisper API."""
    try:
        # Convert to WAV if needed
        wav_path = convert_to_wav(audio_path)
        
        # Open the audio file and send it to OpenAI Whisper API
        with open(wav_path, "rb") as audio_file:
            response = openai.audio.transcriptions.create(model="whisper-1", file=audio_file)
        
        # Extract text from the response
        text = response.text

        # Clean up temporary WAV file if it was converted
        if wav_path != audio_path:
            os.remove(wav_path)
        
        return text
    
    except Exception as e:
        raise Exception(f"Error processing audio: {str(e)}")
