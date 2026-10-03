# Server

Server-URL: api.living.ai

## Known main entry points:
- /time
    - Description: Emo request the currnet unixtime in utc
    - don't need any auth from server side
- /token/
    - Description: Emo authenticate against the server
    - send his mac as part of the path
    - emo sends only a Secret as header with the request
- /emo/
    - Main api for emo
    - emo sends a Secret and Authorization as headers with every request
    - query id is not required to come from official servers for emo to process the request.
    - result code in query resuslt is not required to come from official servers for emo to process the request.

## Requests from Emo:
All requests from emo to this server are made over https, but without any checks of the certificate. With every request emo sends the following http header:
- *Secret*  
    Contains a string that change every second. the string is 22 characters long and can contains the characters a-z, A-Z, 0-9, -_  
    Differs on every request, the derivation is still unknown.

Since firmware 3.x (esp=3.2.0, ver=42) the JWT from /token/ additionally contains the claims *version* (firmware ver, "42") and *name* (esp firmware, "3.2.0"). Observed validity (*expire_in*) varies, e.g. 7548 and 13727 seconds.

## Endpoints seen with firmware 3.2.0 (ver 42)
| Endpoint | Method | Doc |
|---|---|---|
| /time | GET | [time.md](time.md) |
| /token/\<mac> | GET | [token.md](token.md) |
| /emo/ota/version | GET | [emo-ota-version.md](emo-ota-version.md) |
| /emo/notice/latest | GET | [emo-notice-latest.md](emo-notice-latest.md) |
| /emo/permission | GET | [emo-permission.md](emo-permission.md) |
| /emo/server/alt | GET | [emo-server-alt.md](emo-server-alt.md) |
| /emo/report/info | POST | [emo-report-info.md](emo-report-info.md) |
| /emo/weather/forecast | GET | [emo-weather-forecast.md](emo-weather-forecast.md) |
| /emo/speech/tts | GET | [emo-speech-tts.md](emo-speech-tts.md) |
| /emo/chat/start | GET | [emo-chat-start.md](emo-chat-start.md) |
| /emo/voice/detectintent | POST | [emo-voice-detectintent.md](emo-voice-detectintent.md) |
