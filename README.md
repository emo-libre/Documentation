# Documentation
We keep documentation on our findings about EMO, the desktop robot by Living.AI. Most API findings are based on captured traffic of firmware 3.2.0 (ver 42) and older firmware 1.x; every page says which one it is about where it matters.

## Start here
- [How to capture](/HowToCapture.md) - How to capture, study, and analyze information sent to and from EMO.
- [How to decompile](/DecompileFWs.md) - How to decompile EMOs firmwares with Ghidra.
- [Our assumptions](/Assumptions.md) - Various assumptions we have made, aka educated guesses.

## Sections
- [api.living.ai Server](/Server%20api.living.ai) - The cloud API EMO talks to (https): time, token, status reports, weather, TTS, ChatGPT mode and speech intent detection. Has an endpoint index.
- [tts.living.ai Server](/Server%20tts.living.ai) - The old text-to-speech download server (potentially deprecated as of firmware 3.0.0, TTS is now served as mp3 from the eu-emo-tts hosts).
- [Intents](/Intents) - Intent responses that we have documented being sent to EMO.
- [Behaviors](/Behaviors) - Actions that EMO can do (the `rec_behavior` values of an intent response).
- [Animations](/Animations) - The animations EMO can play.
- [Bluetooth](/Bluetooth) - Bluetooth specific information.
- [Firmware](/Firmware) - Firmware versions, downloads, and firmware analysis (K210 protocol, animation system, idle behavior, libraries).
- [Hardware](/Hardware) - Any hardware information we find.
