import os
import asyncio
from ollama import AsyncClient
from langcodes import Language


INSTRUCTIONS = """
I'm gonna give you a news story.

- Summarize it in <<LANGUAGE>>.
- Talk as if YOU are reporting the news on <<LANGUAGE>> TV. DON'T mention "The article ...".
- State the news agency (not the literal link) before you start summarizing. (e.g. This story is from ...)
- DO NOT use AI phrases or commentary.
- ONLY USE PARAGRAPH FORMATTING - no lists, bolding, or italics. ONLY PLAIN TEXT.
- Summarize the main points in ONLY 1-2 paragraphs. Be clear and informative.

Here's the story:
"""


LLM_SERVER = os.environ.get("LLM_SERVER")
if not LLM_SERVER:
    raise Exception("LLM_SERVER env var not set!")


client = AsyncClient(host=LLM_SERVER)


async def summarize_news(content: str, lang="en"):
    prompt = "\n".join([
        # converts language code to display name before replacing
        INSTRUCTIONS.replace("<<LANGUAGE>>", Language.get(lang).display_name()),
        '"""',
        content,
        '"""',
    ])
    
    generator = await client.generate(model="llama3.2", prompt=prompt, stream=True)
    async for chunk in generator:
        yield chunk
