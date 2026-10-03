# /emo/notice/latest

## Description:
Check for latest notices.

### Sample Request:
**URL:** GET /emo/notice/latest HTTP/1.0  

**Headers:**  
- *Authorization*  
    JWT Token, for example "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NDA5OTg4MDAsInN1YiI6ImFhYmJjY2RkZWVmZiIsIm5iZiI6MTY0MDk5MTYwMCwiaWF0IjoxNjQwOTkxNjAwfQ.PEmljG3s2k5DqvvAOJZ3-lT5jSPtYGI0GuzSqQe-QCA"  

Firmware 3.x: the notice list can be empty: {"code":200,"errmessage":"ok","notice":{}}

### Sample Response:
{"code":200,"errmessage":"ok","notice":{"0":{"id":3,"message":"it's good to see you"}}}
