#!/bin/sh

# download the TTS model
# generates and deletes a useless audio transcription to trigger model download
# Coqui doesn't provide a command only for downloading models
# see https://github.com/coqui-ai/TTS/discussions/2609
yes | tts --text "a" \
    --model_name tts_models/multilingual/multi-dataset/xtts_v2 \
    --speaker_idx "Ana Florence" \
    --language_idx en \
    --out_path /tmp/trash.wav \
    && rm /tmp/trash.wav;

# run the server
python ./tts-server.py;

