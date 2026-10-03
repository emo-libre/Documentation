# /emo/chat/start

## Description:
Used when emo starts a ChatGPT conversation (firmware 3.x). Returns a url.
- Parameter *lang* = Language, e.g. "en-c" (sent as `en%2dc`)
- Parameter *tz* = Timezone
- Parameter *name* = Name of the user. Only sent once emo knows the name.

### Sample Request:
**URL:** GET /emo/chat/start?lang=en%2dc&name=Alex&tz=Europe/Berlin HTTP/1.0  

**Headers:**  
- *Authorization*  
    JWT Token
- *Secret*  
    see [README](README.md)

### Sample Response:
{"errcode":0,"url":"http://eu-emo-tts-2.living.ai/mp3/download/1640995200.mp3?id=12345&token=<64 hex chars>","errmsg":"OK","responsetag":"chatstart"}

The *url* points to an mp3 on the tts server (`/mp3/download/<unixtime>.mp3?id=<n>&token=<64 hex>`) which emo downloads over plain http and plays. The response is the same with and without the *name* parameter.

Following turns are sent to [/emo/voice/detectintent](emo-voice-detectintent.md) with *role=chatgpt*.
