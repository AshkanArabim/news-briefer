#!/bin/bash

# src: https://stackoverflow.com/a/78501628/14751074

# Start Ollama in the background.
/bin/ollama serve &
# Record Process ID.
pid=$!

# Pause for Ollama to start.
sleep 5

echo "🔴 Retrieving model '${MODEL_NAME}'..."
ollama pull ${MODEL_NAME}
echo "🟢 Done!"

# Wait for Ollama process to finish.
wait $pid
