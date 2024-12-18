# Newsbridge
(Note: This app is still under active development. Expect serious bugs.)

Are you a fan of daily news briefings, but wish you had a wider selection of
sources? Say no more! Newsbridge is a simple app that allows you to add your
sources as RSS feeds, and then delivers the top stories rom all sources 
(**regardless of the source language**) on demand as a 5-6 minute audio 
briefing.

Mix sources from French, Hindi, Italian, etc., it doesn't matter.
Everything is translated to your language before audio is played.

**Note:** Source languages are limited by the chosen LLM (Llama 3.2 by default)
and target languages (in which you'll hear the audio) are languages supported
by both the LLM and the TSS (XTTS v2 in this case).
See below for details. 

You COULD go beyond the officially supported languages,
but you may get a garbage output.

**Try it yourself:** http://news.ashkan.zone

**Video demo:**

[![image](https://github.com/user-attachments/assets/ee8288b9-fd88-4901-ac7b-60b2c1a92ce7)](https://youtu.be/OtwY-ry_MwY)

## Security
**DON'T PUT ANY SENSITIVE INFO ON THE WEBSITE!!!** This project is by no means
made by professionals. There could be massive, MASSIVE security vulnerabilities.

Nothing is stopping you from using a bogus email address for the account, if 
that makes you more comfortable.

## Supported languages
Input languages / languages of your sources (([source](https://ollama.com/library/llama3.2))):

Note that even though Llama 3.3 doesn't expand this list, it performs much 
better on the "unsupported" languages, such as Persian.
- English
- German
- French
- Italian
- Portuguese
- Hindi
- Spanish
- Thai

Output languages / language of the output audio (union of [Llama 3.2 languages](https://ollama.com/library/llama3.2) and [XTTS v2 languages](https://coqui-tts.readthedocs.io/en/latest/models/xtts.html#languages)):
- English
- German
- French
- Italian
- Portuguese
- Hindi
- Spanish

## Roadmap
- [x] public hosting
- [ ] support for popular LLM and TTS APIs (e.g. if someone wants to use GPT-4o and ElevenLabs)
- [ ] streams - 
  - [x] play immediately as the news is summarized
  - [ ] print the text as the summary is generated (in case audio is unclear)
- [ ] audio controls
  - [ ] audio progress bar (for rewind / skip)
  - [ ] audio download button
  - [ ] caching user's last n briefings
  - [ ] speed controls for audio
- [ ] porting
  - [ ] electron app
  - [x] docker container (for easy self-hosting)
  - [ ] android app
- [ ] optional ads (for funding, if demand is high)

## Usage (the UI)
Refer to the demo video above.

## Usage (for self-hosting)
- Install Docker
- Install the [Nvidia Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) on your machine.
- Clone this repo and `cd` into it
- `make prod` (or `make dev` if you plan on developing)
  - to detach and get your terminal back, add `detached=-d`
  - to only start / stop a specific service (e.g. tts, llm, db), just append `service=<service>`
- Open http://localhost:3000 in your browser.
- To stop the app, run `make down` (or `docker compose down`)

### Configuration
All user configuration (stuff like ports, models, etc.) is found under `.env.prod`. The goal is to keep this setup so configuration is simple.

For more information on configuring each part of the system, refer to the `README.md` file under each component's directory.

### Updating
Simply run `git pull` in the project directory periodically, and restart the service.

### Hardware Requirements
- Min 6GB RAM (~5.2GB from testing)
- Min 6GB VRAM (~4.2GB from testing)
  - NVIDIA GPUs recommended. The system has not beed tested on AMD GPUs. (Please make a PR if you manage to get it working on AMD / other GPU brands)
  - Larger LLMs (e.g. Llama 3.1 70b) and TTS models will require more VRAM.

### Common issues
- `ERR_BLOCKED_BY_CLIENT` in development mode
  - Solution: Disable your adblocker
- No audio after clicking on "Feed"
  - Make sure you've added valid RSS sources.
  - Click "Home" and "Feed" again.

## Contributing
Please refer to [CONTRIBUTING.md](CONTRIBUTING.md)
