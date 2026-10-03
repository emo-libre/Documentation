# /time

## Description:
Emo request this to get the current time and date as a unixtimestamp.
- Parameter *tz* = Timezone for offset

### Sample Request:
**URL:** GET /time?tz=Europe/Berlin HTTP/1.0  
**Headers:**  
- *Secret*  
    Is empty on time requets

Firmware 3.x also seen: the response contains only *time* (no *offset*): {"time":1640995200}

### Sample Response:
{"time":1640995200,"offset":7200}