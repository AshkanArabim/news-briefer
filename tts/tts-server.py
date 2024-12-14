from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import torch
from TTS.api import TTS
import uvicorn
import io
import os
import numpy as np
from scipy.io.wavfile import write


# implementation sources:
# basic coqui inference: https://docs.coqui.ai/en/latest/inference.html
# full API: https://github.com/coqui-ai/TTS/blob/dev/TTS/api.py
# basic fastapi server: https://fastapi.tiangolo.com/
# sample audio source: LJSpeech dataset
    # https://synesthesiam.github.io/opentts/#coqui-tts_en_en_ljspeech


app = FastAPI()
device = "cuda" if torch.cuda.is_available() else "cpu"
api = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2").to(device)


@app.get("/api/tts")
def text_to_wav_audio(text: str, languagecode: str):
    wav_arr = api.tts(
        text=text,
        speaker="Ana Florence",
        language=languagecode
    )
    
    # implementation of this section pulled from here:
    # https://github.com/idiap/coqui-ai-TTS/blob/dev/TTS/utils/audio/numpy_transforms.py#L434
    wav_arr = np.asarray(wav_arr)
    wav_norm = wav_arr * (32767 / max(0.01, np.max(np.abs(wav_arr))))
    sample_rate = 22050

    wav_io = io.BytesIO()
    wav_norm = wav_norm.astype(np.int16)
    write(wav_io, sample_rate, wav_norm)
    
    return StreamingResponse(wav_io, media_type="audio/wav")

if __name__=="__main__":
    port = os.environ.get("TTS_PORT")
    assert port is not None, "TTS_PORT in tts-server is not set!"
    port = int(port)
    
    is_dev = os.environ.get("IS_DEV", "false").lower() == "true"
    
    uvicorn.run(__name__ + ":app",host='0.0.0.0', port=port, reload=is_dev)
