FROM ollama/ollama:latest

# # ./llm/entrypoint.sh:/entrypoint.sh # dev
COPY ./entrypoint.sh /

# overriding the deafult `ollama` entrypoint
ENTRYPOINT [ "/bin/bash", "/entrypoint.sh" ]
