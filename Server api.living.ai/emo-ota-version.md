# /emo/ota/version

## Description:
Check for new firmware.  

### Sample Request:
**URL:** GET /emo/ota/version?type=1&version_num=42 HTTP/1.0  
- Parameter *type* = always 1 (firmware 3.x)
- Parameter *version_num* = current firmware version (firmware 3.x)  

**Headers:**  
- *Authorization*  
    JWT Token, for example "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NDA5OTg4MDAsInN1YiI6ImFhYmJjY2RkZWVmZiIsIm5iZiI6MTY0MDk5MTYwMCwiaWF0IjoxNjQwOTkxNjAwfQ.PEmljG3s2k5DqvvAOJZ3-lT5jSPtYGI0GuzSqQe-QCA"  

### Sample Response:
{"version-name":"1.4.0","version-num":21}
firmware 3.x: {"version-name":"1.1.1","version-num":1}
