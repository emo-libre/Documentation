# /emo/voice/detectintent

## Description:
Used to parse speech and get intent.
- Parameter *locale* = Configured City
- Parameter *timezone* = Timezone
- Parameter *languagecode* = Language, "en" (firmware 3.x: "en-c")
- Parameter *lon* = unused?! ("0.00000")
- Parameter *lat* = unused?! ("0.00000")
- Parameter *alwaysReply* = 0 or 1 (seems to be in the app settings)
- Parameter *index* = request counter, echoed in the response, not monotonic across reboots (firmware 3.x)
- Parameter *source* = always 0 (firmware 3.x)
- Parameter *role* = "chatgpt" only when in ChatGPT conversation mode, see [/emo/chat/start](emo-chat-start.md) (firmware 3.x)
- Body is the recorded audio, see below.

### Body (audio)
Not JSON. Sent with *Transfer-Encoding: chunked* (firmware 3.x).
Layout: `0x22 | PCM | 0x22`. The leading and trailing 0x22 (`"`) are framing bytes, so length = 2 + 2 * samples.
- Firmware 3.x: PCM signed 16-bit little-endian, mono, 16000 Hz (confirmed by listening)
- ChatGPT mode turns are capped at 48128 samples (~3.0 s), normal ones are shorter
- Old firmware: 8000 Hz, 1 channel, 32bit unsigned big endian (unverified)

### Sample Request:
**URL:** POST /emo/voice/detectintent?locale=Bonn&timezone=Europe/Berlin&lon=0.00000&lat=0.00000&languagecode=en-c&alwaysReply=1&index=3&source=0 HTTP/1.1

**Headers:** 
- *Content-Type*  
    Allways "application/octet-stream"
- *Content-Length* or *Transfer-Encoding: chunked*
- *Authorization*  
    JWT Token, for example "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NDA5OTg4MDAsInN1YiI6ImFhYmJjY2RkZWVmZiIsIm5iZiI6MTY0MDk5MTYwMCwiaWF0IjoxNjQwOTkxNjAwfQ.PEmljG3s2k5DqvvAOJZ3-lT5jSPtYGI0GuzSqQe-QCA"  

### Sample Response:
{"queryId":"d3bebf60-87e1-4367-a1b7-b939-89f67c5a491b","queryResult":{"resultCode":"4a05af1c-4101-4da0-9eca-b939-f822a1668b34","queryText":"shut down","intent":{"name":"power_off","confidence":1},"rec_behavior":"power_off","behavior_paras":{}},"languageCode":"en"}

Firmware 3.x also adds `"index"` (echo of the request index) at the top level.

### Response fields
- *intent.confidence* is a number or a string ("0.9928"), both occur
- *behavior_paras* is `[]` or `{}` when empty
- *rec_behavior* selects the behavior emo executes and *behavior_paras* holds its parameters. All behaviors and their parameters are documented in the [Behaviors](/Behaviors) folder, one page per behavior.
