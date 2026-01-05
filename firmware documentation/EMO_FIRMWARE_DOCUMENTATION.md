# EMO Firmware Documentation (Consolidated)

## Scope

This document consolidates the firmware analysis and reimplementation notes in this repository. It covers architecture, hardware interfaces, animation systems, K210 communication, API usage, extraction workflow, and known status.

## Table of Contents

- [Project Overview](#project-overview)
- [Repository Layout](#repository-layout)
- [Build and Flash (ESP-IDF v5.5.1)](#build-and-flash-esp-idf-v551)
- [Hardware Architecture](#hardware-architecture)
  - [Responsibilities](#responsibilities)
  - [UART Connection (ESP32 to K210)](#uart-connection-esp32-to-k210)
- [System Architecture](#system-architecture)
  - [Core Tasks](#core-tasks)
  - [State Machine (High Level)](#state-machine-high-level)
- [Libraries and Frameworks (Original Firmware)](#libraries-and-frameworks-original-firmware)
- [Subsystems](#subsystems)
  - [Servo System](#servo-system)
  - [Sensor System](#sensor-system)
  - [Audio System](#audio-system)
  - [Face and Eye System](#face-and-eye-system)
  - [WiFi and OTA](#wifi-and-ota)
  - [Storage](#storage)
- [Firmware Analysis Highlights (Original Binary)](#firmware-analysis-highlights-original-binary)
  - [Servo and Motion (Analysis)](#servo-and-motion-analysis)
  - [Face and Eye (Analysis)](#face-and-eye-analysis)
  - [Audio (Analysis)](#audio-analysis)
- [Animation System (Dual Path)](#animation-system-dual-path)
  - [Face Animations (K210)](#face-animations-k210)
  - [Motion Animations (ESP32)](#motion-animations-esp32)
  - [LED Animations (ESP32)](#led-animations-esp32)
  - [Playback Flow](#playback-flow)
- [Animation Workflow and State Machine](#animation-workflow-and-state-machine)
- [Animation REST API](#animation-rest-api)
  - [Quick Start](#quick-start)
  - [Endpoints](#endpoints)
  - [Common JSON Structure](#common-json-structure)
- [K210 Communication](#k210-communication)
  - [UART JSON Message Format](#uart-json-message-format)
  - [Common Operations](#common-operations)
  - [Face Recognition Messages](#face-recognition-messages)
  - [Face Response Structure](#face-response-structure)
  - [Face Recognition Flow](#face-recognition-flow)
- [Idle Behavior System](#idle-behavior-system)
- [Animation Triggers and Termination](#animation-triggers-and-termination)
  - [Triggers](#triggers)
  - [Termination](#termination)
- [Extraction Workflow](#extraction-workflow)
- [Troubleshooting](#troubleshooting)
- [Development Status](#development-status)
- [References (Original Documents)](#references-original-documents)

## Project Overview

- Clean-room reimplementation of EMO pet firmware using ESP-IDF v5.5.1
- Reverse-engineered behavior, animation, and communication protocols based on firmware analysis
- Dual-processor design: ESP32 handles motion, sensors, audio, WiFi, OTA; K210 handles camera and display

## Repository Layout

- `main/` - ESP32 firmware source (clean-room implementation)
- `main/include/` - public APIs (servo, face, audio, sensors, WiFi, OTA)
- `docu/` - consolidated documentation output (this file)
- `extracted_animations/` - extracted SPIFFS content (avi/mot/mp3/json)
- `emo_esp32_firmware splitted/` - original firmware partitions and storage
- `extract_spiffs.py` - SPIFFS extraction tool (recommended)
- `analyze_mot_files.py` - MOT motion file analyzer

## Build and Flash (ESP-IDF v5.5.1)

1. Install ESP-IDF v5.5.1 and set up environment.
2. Build and flash:

```bash
idf.py menuconfig
idf.py build
idf.py -p /dev/ttyUSB0 flash
idf.py -p /dev/ttyUSB0 monitor
```

## Hardware Architecture

### Responsibilities

- ESP32:
  - 4 servos (legs and feet)
  - 2 headphone LEDs (left/right)
  - ToF sensor
  - 4 foot sensors
  - 4 microphones
  - 3 touch sensors
  - WiFi and OTA
  - UART link to K210
- K210:
  - Camera
  - Screen/display for face animations
  - Face recognition and image processing

### UART Connection (ESP32 to K210)

- UART port: Not confirmed in decompiled strings
- Baud rate and framing: Not confirmed in decompiled strings
- ESP32 pins: Not confirmed in decompiled strings (board-specific)

## System Architecture

### Core Tasks

| Task | Priority | Purpose |
| --- | --- | --- |
| audio_task | 6 | Audio processing (I2S) |
| servo_task | 5 | Servo control loop (50Hz) |
| face_task | 5 | Face and eye animations |
| sensor_task | 4 | Touch, foot, IMU monitoring |
| wifi_task | 3 | WiFi management and API server |

### State Machine (High Level)

```
INIT -> IDLE -> ACTIVE <-> SLEEP
  |                 |
  |                 +-> OTA
  +-> ERROR
```

## Libraries and Frameworks (Original Firmware)

- ESP-IDF core (original binary shows ESP-IDF component paths; exact version not confirmed; this reimplementation targets v5.5.1).
- FreeRTOS for tasks, queues, event groups, timers, and IPC.
- NVS for configuration (WiFi, volume, face data), SPIFFS for assets, VFS as the unified file layer.
- WiFi stack for station/AP mode, scanning, and power management.
- ESP Audio Development Framework (ADF) usage for I2S stream reader/writer and audio status pipeline.
- System services: esp_timer, watchdog, brownout detection, RNG, reset reasons.

## Subsystems

### Servo System

- 4 servos: left leg, left foot, right leg, right foot
- UART-based servo communication
- Supports old and new servo hardware
- Animation playback integrates with motion (.mot) data

### Sensor System

- Touch sensors (up to 10 pads)
- Foot sensor for surface detection
- IMU framework (I2C-ready)
- Event callbacks for touch and motion

### Audio System

- I2S input/output (16kHz, 16-bit, mono)
- Volume persistence via NVS
- Playback and recording framework
- Audio output integrated with animation system

### Face and Eye System

- Face animations and effects displayed on K210 screen
- Eye modes: white on/off, clear, laser, custom
- Face recognition integration with K210
- Face data stored in NVS (faceinfo_%d)

### WiFi and OTA

- Station mode, credential storage in NVS
- HTTP API server starts after DHCP
- HTTPS OTA support with rollback

### Storage

- NVS for configuration and face data
- SPIFFS for animation assets

## Firmware Analysis Highlights (Original Binary)

### Servo and Motion (Analysis)

- Servo type detection strings: `AA_this is old servo` and `AA_this is new servo`.
- Init and mode strings: `set servos`, `set new servos`, `SERVO_P_SET_MODE`, `SERVO_P_SET_MODE_2`.
- Update logging: left/right legs and feet update done/fail messages.
- Read result strings: `servo_read_success` and multiple `servo_read_fail` variants.
- Motion parsing error string: `motion_file_data_frame_checksum_error`.
- Face-only playback string: `play_animation_without_servor`.

### Face and Eye (Analysis)

- Eye modes and operations: `white_eye_on`, `white_eye_off`, `clear_eye`, `set_eye`, `new_eye`, `laser_eye`.
- Customization strings: `eyes_stickers_set`, `eyes_stickers_clear`, `eyes_color_change1`.
- Face commands: `face_req`, `face_rsp`, `faces`, `register_face`, `query_face`.
- Face assets and storage: `/spiffs/avi/face_id.avi`, `/spiffs/avi/reg_face_success.avi`, `faceinfo_%d`.

### Audio (Analysis)

- ESP ADF strings: `I2S_STREAM`, `I2S_READER`, `I2S_WRITER`.
- Audio status strings: `AUDIO_STATUS_FINISHED`, `AUDIO_STATUS_ERROR`, `AUDIO_STATUS_AUX_IN`.
- Volume strings: `volume_mute`, `volume_low`, `volume_med`, `volume_high`, `volume_set_*`.

## Animation System (Dual Path)

### Face Animations (K210)

- File path: `/spiffs/avi/%s.avi`
- Played on K210 display
- Triggered by ESP32 via UART commands
- Example files: `face_id.avi`, `reg_face_success.avi`, `Fit_Talk.avi`

### Motion Animations (ESP32)

- File path: `/spiffs/mot/%s.mot`
- Custom motion file format with frames:
  - 4 servo angles (2 bytes each)
  - duration (2 bytes)
  - flags (2 bytes)

### LED Animations (ESP32)

- Headphone RGB LEDs (left/right)
- GPIO-driven (PWM not yet implemented)

### Playback Flow

```
Original firmware: internal triggers -> animation queue -> playback task
Reimplementation: HTTP API -> JSON parser -> animation queue -> playback task
  |                                        |
  |                                        +-> Face (K210)
  +-> Servo (ESP32)                        +-> LED (ESP32)
```

## Animation Workflow and State Machine

- Animation task: `animation_player_task` manages the queue and playback.
- Entry points: `play_animation` (face + body) and `play_animation_without_servor` (face-only).
- Combines sequential, parallel, conditional, and looped animation sequences.
- Priority interrupts:
  - Critical (cliff/fall) stops immediately.
  - High (user interaction/voice) stops at next frame.
  - Medium (face/gesture) completes current, clears queue.
  - Low (idle) completes queued animations.

State machine (simplified):

```
IDLE -> QUEUED -> PLAYING -> COMPLETE
          |         |-> PAUSED
          |         |-> INTERRUPTED
          |         -> ERROR
```

## Animation REST API

Base URL: `http://<ESP32_IP>`

Note: This API is part of the clean-room reimplementation and is not present in the decompiled firmware.

### Quick Start

1. Save WiFi credentials:

```c
emo_wifi_save_credentials("YourWiFiSSID", "YourPassword");
```

2. Build and flash the firmware.
3. Watch serial logs for the IP address.
4. Test the API:

```bash
curl http://<ESP32_IP>/
curl -X POST http://<ESP32_IP>/api/stop
```

### Endpoints

- `GET /` - API documentation page
- `POST /api/animate` - Combined face + foot + LED
- `POST /api/face` - Face animation only
- `POST /api/foot` - Foot animation only
- `POST /api/led` - LED animation only
- `POST /api/stop` - Stop all animations
- `GET /api/status` - Playback status

### Common JSON Structure

```json
{
  "name": "blink",
  "type": "blink",
  "loop": true,
  "loop_count": 0,
  "frames": [
    { "duration": 100, "pixels": [[0,1,1,0]] }
  ]
}
```

## K210 Communication

### UART JSON Message Format

```json
{
  "operation": "talk",
  "content": "hello",
  "index": 1,
  "group_index": 0
}
```

### Common Operations

- `slave_ready`
- `talk` / `talk_end`
- `take_photo`
- `game_rps`
- `dance_both`
- `choose_master`
- `sync_step`
- `exchange_info`
- `sync_theme`
- `graffiti`
- `glasses`
- `screen_info`

### Face Recognition Messages

- `face_req` - request operation (register/query/delete)
- `face_rsp` - response with coordinates and id
- `anim_rsp` - animation status response

### Face Response Structure

```c
typedef struct {
    int16_t x;
    int16_t y;
    uint16_t width;
    uint16_t height;
    uint8_t id;
    char name[32];
} face_response_t;
```

### Face Recognition Flow

1. ESP32 sends `register_face` or `query_face` to K210.
2. K210 returns `face_rsp` with id and coordinates.
3. ESP32 stores name in NVS (`faceinfo_%d`).
4. K210 plays success or info animation on screen.

Additional UART notes:
- Tasks: `k210_uart_recv_task`, `k210_uart_trans_task`.
- RX/TX buffers are 3072 bytes; firmware logs errors when payloads exceed expected limits.

## Idle Behavior System

The behavior task manages autonomous actions when idle.

Idle progression (timeouts not confirmed in decompiled strings):
- Short idle: vigilant mode
- Medium idle: explore and free-play
- Long idle: sleep mode

Categories:
- Look around
- Explore play
- Explore movement (turn, forward, back away, up/down)
- Free play actions
- Vigilant (keep_vigilant1)
- Sleep entry, loop, breath, yawn, wake-up animations

## Animation Triggers and Termination

### Triggers

- Sensors: shake, foot contact, cliff detection, obstacle detection
- Touch: petting
- IMU: look down
- Vision: face detection, gesture recognition, image recognition
- Time: idle timeout, reminders, sleep
- External (inferred): app command, voice command, button

### Termination

- Natural completion
- Priority interrupt (critical events stop current animation)
- Timeout guard
- Servo error / communication error

## Extraction Workflow

Note: Extraction steps and partition offsets come from the partition table and scripts, not from decompiled strings.

### Quick Steps

```bash
python extract_spiffs.py
python analyze_mot_files.py extracted_animations/mot/
```

Expected output structure:

```
extracted_animations/
  avi/   # face animations
  mot/   # motion data
  mp3/   # audio
  json/  # configuration
  filenames.txt
```

Typical counts after extraction:
- AVI: ~20-30 files
- MOT: ~30-40 files
- MP3: ~5-10 files
- JSON: ~2-5 files

SPIFFS partition details:
- Offset: 0xa20000
- Size: 1,048,576 bytes (1MB)
- Page size: 256 bytes
- Block size: 4096 bytes

Optional mkspiffs command:

```bash
mkspiffs -u extracted_animations -p 256 -b 4096 -s 1048576 "emo_esp32_firmware splitted/storage.bin"
```

Fallback extraction tool:

```bash
python extract_animations.py
```

## Troubleshooting

- Servo not responding: verify UART pins, power, baud rate
- No audio output: verify I2S pins and volume
- Touch sensors not working: calibrate and check thresholds
- No extraction results: confirm `storage.bin` path and use mkspiffs

## Development Status

Completed:
- Project structure and build setup
- Core API definitions
- NVS storage
- WiFi connectivity
- I2S audio framework
- Touch sensor support
- Servo control framework
- OTA update system

In progress:
- Servo protocol details
- LED matrix driver
- Animation playback system integration
- Audio file playback
- Face recognition integration

Planned:
- IMU driver
- Camera integration
- Bluetooth speaker mode
- Web configuration UI
- Full animation extraction and parsing

## References (Original Documents)

- `README_EMO.md`
- `PROJECT_SUMMARY.md`
- `API_DOCUMENTATION.md`
- `ANIMATION_API_SUMMARY.md`
- `ANIMATION_PLAYBACK_SYSTEM.md`
- `ANIMATION_WORKFLOW_COMPLETE.md`
- `IDLE_BEHAVIOR_SYSTEM.md`
- `K210_COMMUNICATION_PROTOCOL.md`
- `K210_MESSAGES_COMPLETE.md`
- `K210_UART_GPIO_PINS.md`
- `ANIMATION_EXTRACTION_README.md`
- `EXTRACTION_GUIDE.md`
- `EXTRACTION_SUMMARY.md`
- `FIRMWARE_ANALYSIS_REPORT.md`
- `FUNCTION_MAPPING_GUIDE.md`
- `LIBRARIES_AND_FRAMEWORKS.md`
