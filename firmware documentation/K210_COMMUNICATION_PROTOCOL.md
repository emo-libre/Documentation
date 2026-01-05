# K210 Communication Protocol - ESP32 to K210

## Hardware Architecture

Based on the decompiled firmware analysis, the EMO robot has the following architecture:

Confirmation status:
- Confirmed: K210 task names, face_req/face_rsp strings, SPIFFS file paths, K210 OTA/error strings.
- Not confirmed: UART port number, baud rate, GPIO pin mapping.

### ESP32 Controls:
- **4 Servos** (2 legs with 2 servos each: leg + foot)
- **2 Blue LEDs** (headphone LEDs - left and right)
- **1 ToF Sensor** (Time-of-Flight distance sensor)
- **4 Foot Sensors** (falling/surface detection sensors)
- **4 Microphones** (microphone array)
- **3 Touch Sensors** (bottom and sides)
- **UART Communication** to K210

### K210 (Kendryte K210 AI Chip) Controls:
- **1 Camera** (face recognition, image processing)
- **1 Screen/Display** (face animations, UI)
- **Face Recognition** (AI processing)
- **Image Processing**

## Communication Protocol

### UART Configuration
```c
// From firmware analysis
// UART port, baud rate, and framing are not confirmed in the decompiled strings.
// Use board-level schematics or runtime configuration to verify.
UART: Not confirmed
Baud Rate: Not confirmed
Data Bits: Not confirmed
Parity: Not confirmed
Stop Bits: Not confirmed
```

### Task Names Found
```c
"k210_uart_recv_task"   // ESP32 receives data from K210
"k210_uart_trans_task"  // ESP32 transmits data to K210
```

## Command Structure

### Face Commands (ESP32 → K210)

#### Command 0x02 - Face Command
```
Log: "got face cmd"
Purpose: Single face operation
```

#### Command 0x03 - Faces Command
```
Log: "got faces cmd"
Purpose: Multiple faces operation
```

#### Command 0x12 - Face Command Extended
```
Log: "got face cmd 0x12"
Purpose: Face recognition/registration command
```

#### Command 0x13 - Faces Command Extended
```
Log: "got faces cmd 0x13"
Purpose: Face query/management command
```

### Response Structure (K210 → ESP32)

#### face_rsp - Face Response
```c
// Used for face recognition results
// Contains face coordinates and ID
typedef struct {
    int16_t x;          // Face center X coordinate
    int16_t y;          // Face center Y coordinate
    uint16_t width;     // Face bounding box width
    uint16_t height;    // Face bounding box height
    uint8_t id;         // Face ID (0-255)
    char name[32];      // Face name
} face_response_t;
```

### Screen/Display Commands

#### screen_info
```c
// Send screen information to K210
"send screen info"
```

#### Animation Files (Stored in SPIFFS)
```
/spiffs/avi/face_id.avi
/spiffs/avi/reg_face_success.avi
/spiffs/json/profile.json
```

## Face Recognition Flow

### 1. Register Face
```
ESP32 → K210: "register_face" command
K210: Captures image, processes face
K210 → ESP32: face_rsp with new face_id
ESP32: Saves to NVS as "faceinfo_%d"
ESP32: Plays "/spiffs/avi/reg_face_success.avi"
```

### 2. Query Face
```
ESP32 → K210: "query_face" command
K210: Searches for known faces
K210 → ESP32: face_rsp with face data
ESP32: Retrieves name from NVS
```

### 3. Face Detection
```
K210: Continuously processes camera
K210 → ESP32: face_rsp when face detected
ESP32: Logs coordinates:
  - "coordinate_data1->face.x = %d"
  - "coordinate_data1->face.y = %d"
  - "coordinate_data1->face.width = %d"
  - "coordinate_data1->face.height = %d"
  - "coordinate_data1->face.id = %d"
  - "coordinate_data1->face.name = %s"
  - "face_center_x1 = %d"
  - "face_center_y1 = %d"
```

### 4. Face Operations
```c
"app_face_in"      // Face entered view
"app_face_out"     // Face left view
"app_face_delete"  // Delete face from database
```

## K210 Update/OTA

### K210 Firmware Update
```c
"k210_update_queue failed, %ld"
"k210_update_receive 2047, restart!!!"
"err k210_update_receive = %d"
"k210_update_receive1 = %d"
"k210 ota error, download this file again"
```

### K210 File Operations
```c
"esp32_read_k210_sdcard_file"
"esp32_read_k210_json_file_to_buf"
"esp32_read_k210_sd_file_to_buf"
```

## NVS Storage Keys

### K210 Related
```c
"k210_kpu"          // K210 KPU (Knowledge Processing Unit) config
"k210_sum"          // K210 checksum
"screen_info"       // Screen configuration
"faceinfo_%d"       // Face data (where %d is face ID 0-N)
```

### Storage Functions
```c
save_custom_face_info_to_nvs()
update_k210_kpu_info_to_nvs()
save_screen_info_to_nvs()
```

## JSON Protocol

### Face Request/Response
```json
{
  "face_req": {
    "command": "register|query|delete",
    "face_id": 0,
    "name": "John"
  }
}
```

```json
{
  "face_rsp": {
    "x": 120,
    "y": 80,
    "width": 60,
    "height": 80,
    "id": 1,
    "name": "John"
  }
}
```

### Faces Query
```json
{
  "faces": [
    {
      "id": 1,
      "name": "John",
      "x": 120,
      "y": 80
    },
    {
      "id": 2,
      "name": "Jane",
      "x": 200,
      "y": 90
    }
  ]
}
```

## Animation Protocol

### Display Animation Command
The ESP32 sends animation commands to K210 to display on the screen.

**Format**: JSON over UART

```json
{
  "anim_rsp": {
    "type": "face_animation",
    "file": "/test/animation_name.avi",
    "loop": true,
    "duration": 1000
  }
}
```

### Animation Types Found
```
"blink_come_back1"
"mood_sad"
"image_react_high"
"image_look_up"
"image_search"
"doesnt_know_face"
"reg_face_success"
```

## Correct API Implementation

Based on this analysis, the animation API should work as follows:

### ESP32 Role
1. **Receives JSON commands** via HTTP API (from external source)
2. **Controls servos** directly (foot/leg animations)
3. **Controls LEDs** directly (headphone LEDs)
4. **Forwards face animations** to K210 via UART
5. **Receives face recognition data** from K210

### K210 Role
1. **Processes camera** for face recognition
2. **Displays animations** on screen
3. **Sends face data** back to ESP32
4. **Executes display commands** from ESP32

## Updated Architecture

```
External API (HTTP/WiFi)
         ↓
    ESP32 Firmware
    ├─→ Servo Control (direct)
    ├─→ LED Control (direct)
    ├─→ Sensor Reading (direct)
    └─→ UART → K210
              ├─→ Screen/Display
              ├─→ Camera
              └─→ Face Recognition
              
K210 → UART → ESP32 (face detection results)
```

## Example Communication Flow

### Display Face Animation
```
1. HTTP API → ESP32: 
   POST /api/face
   {
     "name": "happy",
     "type": "happy",
     "frames": [...]
   }

2. ESP32 → K210 (UART):
   {
     "anim_rsp": {
       "type": "happy",
       "file": "/test/happy.avi"
     }
   }

3. K210: Displays animation on screen
```

### Combined Animation (Face + Foot + LED)
```
1. HTTP API → ESP32:
   POST /api/animate
   {
     "face": {...},    // Forward to K210
     "foot": {...},    // Execute on ESP32
     "led": {...}      // Execute on ESP32
   }

2. ESP32:
   - Sends face animation to K210 via UART
   - Controls servos directly
   - Controls LEDs directly
```

## Implementation Notes

1. **Face animations are NOT LED matrix** - they are displayed on the K210's screen
2. **ESP32 acts as a bridge** - receives HTTP commands, forwards display commands to K210
3. **K210 is the display controller** - handles all screen rendering
4. **Servo and LED control stays on ESP32** - direct hardware control
5. **Face recognition data flows back** - K210 sends detected faces to ESP32

## UART Message Format (Estimated)

Based on the command codes found:

```c
typedef struct {
    uint8_t header;      // 0xAA or similar
    uint8_t command;     // 0x02, 0x03, 0x12, 0x13, etc.
    uint16_t length;     // Payload length
    uint8_t payload[];   // JSON or binary data
    uint8_t checksum;    // "k210_sum"
} k210_message_t;
```

## Next Steps

1. Update the animation API to forward face animations to K210 via UART
2. Implement UART communication protocol
3. Keep servo and LED control on ESP32
4. Parse face recognition responses from K210
5. Test with actual hardware

---

**Key Finding**: The screen is controlled by the K210, not the ESP32. Face animations must be sent to the K210 via UART, not displayed on an LED matrix.
