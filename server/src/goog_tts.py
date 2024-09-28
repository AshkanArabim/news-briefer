import os
import json
from dotenv import load_dotenv
import google.cloud.texttospeech as tts

load_dotenv()

API_KEY = json.loads(os.environ.get("TTS_API_KEY"))

from google.cloud import texttospeech as tts

def text_to_audio_stream(voice_name: str, text: str):
    # Derive the language code from the voice name
    language_code = "-".join(voice_name.split("-")[:2])

    # Set up the input text
    text_input = tts.SynthesisInput(text=text)

    # Define the voice parameters
    voice_params = tts.VoiceSelectionParams(
        language_code=language_code, name= "en-US-Studio-O"
    )

    # Configure audio encoding as MP3 for streaming
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.MP3)

    # Initialize the client
    client = tts.TextToSpeechClient()

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=text_input,
        voice=voice_params,
        audio_config=audio_config,
    )

    # Return the audio content as a byte stream
    return response.audio_content
