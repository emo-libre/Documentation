# /emo/speech/tts

## Description:
Emo uses this request to speak custom text, Text to Speech engine, Parameters are URL-Encoded.
- Parameter *q* = Text to speak
- Parameter *l* = Requested Language

### Sample Request:
**URL:** GET /emo/speech/tts?q=i%27m%20sorry,%20but%20what%27s%20your%20name.&l=en

**Headers:** 
- *Content-Type*  
    Allways "application/x-www-form-urlencoded"

### Sample Response:
{
    "code": 200,
    "errmessage": "ok",
    "url": "http://eu-api.living.ai/tts/dl/202601038954171416958627a7df284.93976064"
}
prioer to firmware 3.0.0: {"code":200,"errmessage":"ok","url":"http://tts.living.ai/download/1640995200.wav?token=e8bbc12570c382ae0d70b9d66b76b380618d3f4f87e6594bd89a44f95140438f"}
