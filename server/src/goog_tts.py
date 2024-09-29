import os
import io
import json
from dotenv import load_dotenv
import google.cloud.texttospeech as tts
from pydub import AudioSegment
from pydub.playback import play

load_dotenv()

API_KEY = json.loads(os.environ.get("TTS_API_KEY"))

def text_to_audio_stream(voice_name: str, text: str):
    # Derive the language code from the voice name
    language_code = "-".join(voice_name.split("-")[:2])

    # Initialize the client
    client = tts.TextToSpeechClient()
    
    # Set up the input text
    text_input = tts.SynthesisInput(text=text)

    # Define the voice parameters
    voice_params = tts.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )

    # Configure audio encoding as MP3 for streaming
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.MP3)

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=text_input,
        voice=voice_params,
        audio_config=audio_config,
    )
    
    # Save the audio to a temporary file
    temp_audio_file = "/tmp/temp_audio.mp3"
    with open(temp_audio_file, "wb") as out:
        out.write(response.audio_content)
    
    return temp_audio_file
