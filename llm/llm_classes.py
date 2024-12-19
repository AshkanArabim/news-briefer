from abc import ABC, abstractmethod
import ollama
import subprocess
import time


# TODO: model superclass for consistency
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
        time.sleep(0.5) # ugly hack. 
        
        # download the model if it's not here
        print("Downloading if", llama_name, "not already downloaded...", flush=True)
        ollama.pull(llama_name)

        self.model_name = llama_name

    def generate(self, prompt: str):
        stream = ollama.generate(model=self.model_name, prompt=prompt, stream=True)
        for chunk in stream:
            yield chunk["response"]


class Gemini2(AbstractModel):
    def __init__(self, api_key: str):
        # TODO:
        pass

    def generate(self, prompt: str):
        # TODO:
        pass
