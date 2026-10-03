# Reimplementation Notes

> **Not part of the original firmware.** This page collects design notes for a clean-room ESP32 firmware written during the analysis. The REST API, structs, task priorities and build setup below are proposals. None of them exist in EMO's firmware, and the code they refer to (`main/`, `docu/`) is not in this repository. For what the original firmware does, see the [Firmware](README.md) pages.

---

## Target platform

- ESP-IDF v5.5.1. The original firmware was built on an older IDF (v3.3–v4.0 estimated, see [Libraries](libraries.md#15-library-version-summary)).
- Proposed layout: `main/` (firmware source), `main/include/` (public APIs: servo, face, audio, sensors, WiFi, OTA), `extracted_animations/` (output of [Extraction](extraction.md)), `emo_esp32_firmware splitted/` (original partitions).

### Build and flash

```bash
idf.py menuconfig
idf.py build
idf.py -p /dev/ttyUSB0 flash
idf.py -p /dev/ttyUSB0 monitor
```

## Libraries

Must have: ESP-IDF (with FreeRTOS), ESP-ADF (audio), cJSON, mbedTLS. Optional: ESP-NOW (peer-to-peer between EMOs), BLE Mesh, HTTP server.

```bash
git clone --recursive https://github.com/espressif/esp-idf.git
cd esp-idf && ./install.sh
git clone --recursive https://github.com/espressif/esp-adf.git
export ADF_PATH=$PWD/esp-adf
. $HOME/esp/esp-idf/export.sh
```

Licensing: ESP-IDF and mbedTLS are Apache 2.0, Bluedroid is Apache 2.0 with some proprietary parts, FreeRTOS and cJSON are MIT, and LwIP is BSD. ESP-ADF was noted as Espressif proprietary (requires a license); check its current license before shipping.

## Proposed tasks

| Task | Priority | Purpose |
| --- | --- | --- |
| audio_task | 6 | I2S audio (16 kHz, 16-bit, mono) |
| servo_task | 5 | Servo loop, 50 Hz |
| face_task | 5 | Face/eye animations via the K210 |
| sensor_task | 4 | Touch, foot, IMU |
| wifi_task | 3 | WiFi and API server |

System states: `INIT → IDLE → ACTIVE ↔ SLEEP`, with `ACTIVE → OTA` and `INIT → ERROR`.

## Animation API

### C API

```c
typedef struct {
    char     name[32];
    char     face_file[64];     // .avi path or NULL
    char     motion_file[64];   // .mot path or NULL
    bool     sync;              // synchronize face and motion
    uint16_t led_pattern;       // optional
} animation_t;

int  play_animation(animation_t *anim);
int  play_face_animation(const char *avi_file);
int  play_motion_animation(const char *mot_file);
int  play_combined_animation(const char *name);
void stop_animation(void);
void pause_animation(void);
void resume_animation(void);
bool is_animation_playing(void);
const char *get_current_animation(void);
```

### Queue

```c
typedef struct {
    char    *animation_name;
    uint8_t  priority;          // 0 critical … 4 background
    uint32_t timestamp;
    bool     interruptible;
    void   (*callback)(void);
} animation_queue_item_t;

void queue_animation(const char *name, uint8_t priority);
void priority_queue_animation(const char *name, uint8_t priority);  // insert at front
void clear_animation_queue(void);
uint8_t get_queue_length(void);
```

Suggested limits: queue up to 10 items, queued items expire after 30 s. The priority levels follow the [observed interrupt behavior](animation_system.md#5-termination-and-priorities-inferred).

### REST API

Base URL `http://<ESP32_IP>`. The HTTP server starts after DHCP.

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/` | API documentation page |
| POST | `/api/animate` | Combined face + foot + LED |
| POST | `/api/face` | Face animation only (forwarded to the K210) |
| POST | `/api/foot` | Foot/servo animation only |
| POST | `/api/led` | LED animation only |
| POST | `/api/stop` | Stop all animations |
| GET | `/api/status` | Playback status |

```json
{
  "name": "blink",
  "type": "blink",
  "loop": true,
  "loop_count": 0,
  "frames": [ { "duration": 100, "pixels": [[0,1,1,0]] } ]
}
```

`/api/animate` takes `{"face": {...}, "foot": {...}, "led": {...}}`. The ESP32 forwards `face` to the K210 over UART and plays `foot` and `led` itself.

Other request examples:

```
POST /api/animate   {"name": "dance_together", "sync": true}
POST /api/face      {"animation": "mood_sad"}
POST /api/motion    {"animation": "move_forward"}
```

Example flow for a face animation: `POST /api/face {"name": "happy", "type": "happy", "frames": [...]}` → the ESP32 sends `{"anim_rsp": {"type": "happy", "file": "/test/happy.avi"}}` to the K210 over UART → the K210 shows it on the screen.

Quick start: call `emo_wifi_save_credentials("SSID", "password")`, flash, read the IP from the serial log, then run `curl http://<ESP32_IP>/` and `curl -X POST http://<ESP32_IP>/api/stop`.

### K210 send helpers

```c
void send_talk_message(const char *content) {
    char buf[256];
    snprintf(buf, sizeof(buf), "{\"operation\": \"talk\", \"content\": \"%s\"}", content);
    uart_write_bytes(K210_UART, buf, strlen(buf));
}

void send_dance_command(int index) {
    char buf[128];
    snprintf(buf, sizeof(buf), "{\"operation\": \"dance_both\", \"index\": %d}", index);
    uart_write_bytes(K210_UART, buf, strlen(buf));
}

void send_rps_move(int move) {
    char buf[128];
    snprintf(buf, sizeof(buf), "{\"operation\": \"game_rps\", \"index\": %d}", move);
    uart_write_bytes(K210_UART, buf, strlen(buf));
}

void send_talk_end(void) {
    const char *msg = "{\"operation\": \"talk_end\"}";
    uart_write_bytes(K210_UART, msg, strlen(msg));
}
```

See [K210 protocol](k210_protocol.md) for the full message list. The UART port and pins are unconfirmed.

### `.mot` parser

A starting point based on the [guessed 12-byte frame layout](animation_system.md#mot-format-inferred). Adjust `frame_size` once the format is confirmed:

```python
import struct

def parse_mot_file(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()

    frames = []
    frame_size = 12  # adjust based on analysis

    for i in range(0, len(data), frame_size):
        frame_data = data[i:i+frame_size]
        servos = struct.unpack('<4H', frame_data[0:8])
        duration = struct.unpack('<H', frame_data[8:10])[0]
        frames.append({'servos': servos, 'duration': duration})

    return frames
```

## Implementation phases

1. **Hardware abstraction**: GPIO, touch (3 pads), foot sensors, IMU (roll/pitch), I2S in/out. Map pins first (see [Strings and addresses: address ranges](strings_and_addresses.md#16-function-address-ranges)).
2. **Motion**: old and new servo types, per-servo control and parameters, `.mot` parser plus playback with interpolation.
3. **K210 link**: UART protocol, face animation commands, face recognition responses, face data in NVS.
4. **Audio**: microphone (I2S reader), speaker (I2S writer), volume in NVS, MP3 playback from SPIFFS, Bluetooth speaker.
5. **Behavior**: one FreeRTOS task per subsystem, animation queue with priorities, idle state machine ([Idle behavior](idle_behavior.md)), touch/voice/face reactions.

Test each subsystem on its own, and test motions alone before syncing them with face animations.

## Status (as last recorded)

- Done: project structure, core API definitions, NVS, WiFi, I2S framework, touch, servo framework, OTA (HTTPS with rollback).
- In progress: servo protocol, LED driver (PWM), animation playback integration, audio file playback, face recognition.
- Planned: IMU driver, camera, Bluetooth speaker, web config UI, full `.mot` parsing.

## Troubleshooting

- Servo not responding: check the servo pins, power, and protocol/baud rate.
- No audio: check the I2S pins and volume.
- Touch not working: calibrate the thresholds.
