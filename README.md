# Newsbridge
(Note: This app is still under active development. Expect serious bugs.)

Are you a fan of daily news briefings, but wish you had a wider selection of
sources? Say no more! Newsbridge is a simple app that allows you to add your
sources as RSS feeds, and then delivers the top stories rom all sources 
(**regardless of the source language**) on demand as a 5-6 minute audio 
briefing.

Video demo: https://www.youtube.com/watch?v=FGFq3OgrUZ4

## Security
**DON'T PUT ANY SENSITIVE INFO ON THE WEBSITE!!!** This project is by no means
made by professionals. There could be massive, MASSIVE security vulnerabilities.

Nothing is stopping you from using a bogus email address for the account, if 
that makes you more comfortable.

## Roadmap
- [ ] public hosting
- [ ] support for briefing in all Llama 3.1 languages.
- [ ] streams - 
  - [ ] play immediately as the news is summarized
  - [ ] print the text as the summary is generated (in case audio is unclear)
- [ ] audio controls
  - [ ] audio progress bar (for rewind / skip)
  - [ ] audio download button
  - [ ] caching user's last n briefings
  - [ ] speed controls for audio
- [ ] porting
  - [ ] electron app
  - [ ] docker container (for easy self-hosting)
  - [ ] android app
- [ ] Google OAuth integration
- [ ] optional ads (for funding, if demand is high)

## Usage
TODO: add `.env` instructions after service is decoupled from Google Cloud

TODO: add UI usage instructions

TODO: add supported languages

- Install Docker
- Install the [Nvidia Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) on your machine.
- Clone this repo and `cd` into it
- `make prod` (or `make dev` if you plan on developing)
  - to only start / stop a specific service (e.g. tts, llm, db), just append `service=<service>`
- Open http://localhost:3000 in your browser.

### Common issues
- `ERR_BLOCKED_BY_CLIENT` in development mode
  - Solution: Disable your adblocker

## Contributing
Please open a pull request first, then ask to be assigned to it. We don't want
to be stepping on each other's toes while the project is under heavy 
development.

These rules will become more comprehensive as the project grows.
