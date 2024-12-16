import os
import aiohttp


async def text_to_audio(text: str, language: str): # lang is the two-letter language code
    TTS_SERVER = os.environ.get("TTS_SERVER")
    
    # print("== generating audio for for:", text, flush=True) # DEBUG
    
    url = f'http://{TTS_SERVER}/api/tts'
    params = {
        'text': text,
        'languagecode': language
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status != 200:
                raise Exception(f"Error: {response.status}, {await response.text()}")
            return await response.read()  # raw wav audio
    