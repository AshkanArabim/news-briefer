from abc import ABC, abstractmethod
import ollama
import subprocess
import time
import google.generativeai as genai


class AbstractModel(ABC):
    @abstractmethod
    def generate(self, prompt: str):
        """
        Generates a streaming response for the given prompt.
        """
        pass


class Llama(AbstractModel):
    def __init__(self, llama_name: str):
        # start the ollama server in the background
        print("Waiting for Ollama server to start")
        subprocess.Popen(
            ["ollama", "serve"],
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(0.5)  # ugly hack.

        # download the model if it's not here
        print("Downloading if", llama_name, "not already downloaded...", flush=True)
        ollama.pull(llama_name)

        self.model_name = llama_name

    def generate(self, prompt: str):
        stream = ollama.generate(model=self.model_name, prompt=prompt, stream=True)
        for chunk in stream:
            yield chunk["response"]


class Gemini2(AbstractModel):
    def __init__(self, model_name: str, api_key: str):
        # src: copied code from Google's AI studio
        genai.configure(api_key=api_key)

        # Create the model
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config,
        )

    def generate(self, prompt: str):
        # src: https://github.com/google-gemini/generative-ai-python/blob/main/docs/api/google/generativeai/GenerativeModel.md#generate_content
        stream = self.model.generate_content(prompt, stream=True)
        for chunk in stream:
            yield chunk.text
