# /emo/speech/tts

## Description:
Emo uses this request to speak custom text, Text to Speech engine, Parameters are URL-Encoded.
- Parameter *q* = Text to speak
- Parameter *l* = Requested Language (firmware 3.x: "en-c", sent as `en%2dc` or `en-c`)
- The text is lower-cased by emo

### Sample Request:
**URL:** GET /emo/speech/tts?q=i%27m%20sorry,%20but%20what%27s%20your%20name.&l=en

**Headers:** 
- *Authorization*  
    JWT Token (firmware 3.x)
- *Content-Type*  
    Allways "application/x-www-form-urlencoded"

### Sample Response:
{
    "code": 200,
    "errmessage": "ok",
    "url": "http://eu-api.living.ai/tts/dl/202601038954171416958627a7df284.93976064"
}
firmware 3.2.0 returns an mp3 and not a wav: {"code":200,"errmessage":"ok","url":"http://eu-emo-tts-2.living.ai/mp3/download/1640995200.mp3?id=12345&token=<64 hex>"}

prior to firmware 3.0.0: {"code":200,"errmessage":"ok","url":"http://tts.living.ai/download/1640995200.wav?token=<64 hex>"}
