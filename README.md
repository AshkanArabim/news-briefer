# Newsbridge
(Note: This app is still under active development. Expect serious bugs.)

Are you a fan of daily news briefings, but wish you had a wider selection of
sources? Say no more! Newsbridge is a simple app that allows you to add your
sources as RSS feeds, and then delivers the top stories rom all sources 
(**regardless of the source language**) on demand as a 5-6 minute audio 
briefing.

## Roadmap
- [ ] public hosting
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
- Install Docker
- Install the [Nvidia Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) on your machine.
- Clone this repo and `cd` into it
- `docker build --no-cache` - Just to make sure we're not using outdated images
- `docker compose up -d`
- Open http://localhost:3000 in your browser.

## Contributing
Please open a pull request first, then ask to be assigned to it. We don't want
to be stepping on each other's toes while the project is under heavy 
development.

These rules will become more comprehensive as the project grows.
