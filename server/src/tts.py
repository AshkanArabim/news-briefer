import os
import requests

def text_to_audio_file(language: str, text: str):
    TTS_SERVER = os.environ.get("TTS_SERVER")
    
    url = f'http://{TTS_SERVER}/api/tts'
    params = {
        'text': text,
        'speaker_id': 'p376',
        'style_wav': '',
        'language_id': language
    }
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code}, {response.text}")
    
    # Save the audio to a temporary file
    temp_audio_file = "/tmp/temp_audio.mp3"
    with open(temp_audio_file, "wb") as out:
        out.write(response.content)
    
    return temp_audio_file
