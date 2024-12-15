# implementation reference: https://github.com/astral-sh/uv-docker-example

FROM ghcr.io/astral-sh/uv:python3.10-bookworm-slim

WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# copy rest of project source code
ADD . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []

# download the TTS model
# generates and deletes a useless audio transcription to trigger model download
# Coqui doesn't provide a command only for downloading models
# see https://github.com/coqui-ai/TTS/discussions/2609
RUN yes | tts --text "a" \
    --model_name tts_models/multilingual/multi-dataset/xtts_v2 \
    --speaker_idx "Ana Florence" \
    --language_idx en --out_path /tmp/trash.wav && rm /tmp/trash.wav

# run the app (fastapi by default)
CMD ["python", "./tts-server.py"]
