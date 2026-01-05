# EMO Pet Firmware Analysis Report

## Executive Summary
This document provides a comprehensive analysis of the decompiled EMO pet firmware (ESP32-based) extracted from `ghidraExtracted-elfPartition1.c`. The firmware contains extensive functionality for motor control, face/eye animations, audio processing, GPIO management, microphone input, and touch sensors.

---

## 1. Motor Movement & Servo Control

### Key Findings
The firmware implements a sophisticated servo control system for EMO's movement and animations.

### Servo Management Functions
- **Servo Types**: Distinguishes between "old servo" and "new servo" hardware
  - References: `s_AA_this_is_old_servo_3f412869` (line 3f412869)
  - References: `s_AA_this_is_new_servo_3f412893` (line 3f412893)

### Servo Control Operations
- **Servo initialization and configuration**:
  - `set_servos...` (3f42f602)
  - `set_new_servos...` (3f42f582)
  - `SERVO_P_SET_MODE` (3f42f611)
  - `SERVO_P_SET_MODE_2` (3f42f623)

- **Servo reading and testing**:
  - `reading_servos!` (3f42f746)
  - `reading_servos!\nnew servo test` (3f42f694)
  - `SERVO_TEST` (3f42ccd8) - referenced 8 times throughout code

- **Servo updates by body part**:
  - Left legs: `Left_legs_servo_update_done` (3f44baf0), `Left_legs_servo_update_fail` (3f44bb0e)
  - Left foot: `Left_foot_servo_update_done` (3f44bb36), `Left_foot_servo_update_fail` (3f44bb54)
  - Right legs: `Right_legs_servo_update_done` (3f44bb7d), `Right_legs_servo_update_fail` (3f44bb9b)
  - Right foot: `Right_foot_servo_update_done` (3f44bbc4), `Right_foot_servos_update_fail` (3f44bbe2)

### Servo Parameters
- **Parameter management**:
  - `set_servo_parameter_%d_%02x_%d` (3f44be64)
  - `read_servo_parameter` (3f44befa)
  - `read_new_servo_parameter` (3f44beb9)
  - `change_servo_ratio` (3f44bf1d)
  - `change_new_servo_ratio` (3f44bea2)

- **Servo control modes**:
  - `servo_stop_1` (3f44c0db)
  - `servo_stop_2` (3f44c193)
  - `emo_servo_tight = %d` (3f42c607)

### Animation System
- **Animation playback**:
  - `play_animation_without_servor` (3f43058a)
  - Animation tables likely stored as static arrays (referenced but not directly visible in strings)

### Servo I/O
- **GPIO control for servos**:
  - `get_in_servo_io = %d` (3f44bdd1)
  - `servo_option_cmd %s addr %02x data %d` (3f44bd24)

### Error Handling
- Multiple servo read failure messages:
  - `servo_read_fail %d` (3f44bd5f)
  - `servo_read_fail2 %d` (3f44bd74)
  - `servo_read_fail3 %d` (3f44bd8a)
  - `servo_read_fail4 %d` (3f44bda0)
  - `servo_read_success` (3f44bd4b)

---

## 2. Face & Eye Animations

### Display System
The firmware implements a comprehensive face animation system with LED matrix control.

### Eye Animation Types
- **White eye modes**:
  - `white_eye_on` (3f411a97) - with preference theme support
  - `white_eye_off` (3f411ad7) - with preference theme support
  - `white_eye` (3f412173) - base white eye mode
  - `white_emo_eyes_change_1BW` (3f42b662)
  - `white_emo_eyes_change_2WB` (3f42b67c)

- **Eye operations**:
  - `clear_eye` (3f411dcc) - clear/reset eye display
  - `set_eye` (3f411e05) - set specific eye pattern
  - `new_eye` (3f412502) - new eye animation system
  - `laser_eye` (3f40fa75) - special laser eye effect
  - `laser_eye_2` (3f42b8fb) - alternate laser effect

### Eye Stickers & Customization
- `eyes_stickers_set` (3f42a610)
- `eyes_stickers_clear` (3f42b714)
- `eyes_color_change1` (3f42b6e0)
- `eyes_setting_in` (3f42b6f3)
- `eyes_setting_out` (3f42b703)

### Face Recognition & Management
- **Face operations**:
  - `face_req` (3f4113dd) - face request command
  - `face_rsp` (3f412382) - face response (referenced 7 times)
  - `faces` (3f4123f8) - multiple faces management
  - `register_face` (3f42e56a)
  - `query_face` (3f42e5a8)
  - `doesnt_know_face` (3f42e5c8)
  - `reg_face_success` (3f42b0f4)

- **Face commands**:
  - `got face cmd` (3f4163f3)
  - `got faces cmd` (3f41642d)
  - `got face cmd 0x12` (3f41643c)
  - `got faces cmd 0x13` (3f41644f)
  - `got faces end` (3f416463)

### Face Data Structure
- **Coordinate tracking**:
  - `coordinate_data1->face.x = %d` (3f42ca44)
  - `coordinate_data1->face.y = %d` (3f42ca64)
  - `coordinate_data1->face.width = %d` (3f42ca84)
  - `coordinate_data1->face.height = %d` (3f42caa8)
  - `coordinate_data1->face.id = %d` (3f42cacd)
  - `coordinate_data1->face.name = %s` (3f42caee)
  - `face_center_x1 = %d` (3f42cb11)
  - `face_center_y1 = %d` (3f42cb27)

### Face Storage
- **File paths**:
  - `/spiffs/avi/face_id.avi` (3f42cba8)
  - `/spiffs/avi/reg_face_success.avi` (3f42cbc0)
  - `faceinfo_%d` (3f43572e) - NVS storage key
  - `save_custom_face_info_to_nvs` (3f4358a5)

### App Integration
- `app_face_in` (3f42b69f)
- `app_face_out` (3f42b6ab)
- `app_face_delete` (3f42b6b8)

### Display Scanning
- `display_scan_result` (3f41243f)

### Pixel Management
- `pixels: %d` (3f435526)
- Multiple references to width, height, and pixel counting for frame buffers

---

## 3. Speaker & Audio System

### Audio Framework
The firmware uses the **ESP Audio Development Framework (ADF)** extensively.

### Audio Status Management
- **Status types**:
  - `AUDIO_STATUS_UNKNOWN` (3f427e51)
  - `AUDIO_STATUS_FINISHED 0` (3f427e7e)
  - `AUDIO_STATUS 0` (3f427e99)
  - `AUDIO_STATUS_ERROR` (3f427eab)
  - `AUDIO_STATUS_AUX_IN` (3f427ec1)
  - `audio_status_task` (3f427f20)
  - `setting audio status %d` (3f426f81)

### Volume Control
- **Volume settings**:
  - `volume` (3f40f756) - referenced 8 times
  - `volume_mute` (3f411561) - with preference theme
  - `volume_low` (3f41159f) - with preference theme
  - `volume_med` (3f4115db) - with preference theme
  - `volume_high` (3f411617) - with preference theme
  - `volume_set_mute` (3f42a57d)
  - `volume_set` (3f42a58d)
  - `volume_set_down` (3f42a598)
  - `volume_set_mid` (3f42a5a8)
  - `save_volume_info_to_nvs` (3f435972)

### I2S Audio Streaming
- **I2S components**:
  - `I2S_STREAM` (3f4453e8) - referenced 20 times
  - `i2s_type_%d` (3f44542c)
  - `I2S_WRITER` (3f44577c) - referenced 16 times
  - `I2S_READER` (3f445944) - referenced 4 times
  - `CreateI2sStreamReader` (3f445b34)
  - `CreateI2sStreamWriter` (3f445b4c)
  - `i2s_read` (3f44f698)
  - `i2sMonoFix` (3f445b64)
  - `i2sDacDataScale` (3f445b70)

### I2S Configuration
- `I2S_DAC_PDM_only_support_on_I2S0` (3f44f5f8)
- `I2S DAC built-in only support on I2S0` (3f44f5d2)

### Audio Playback
- **Audio items**:
  - `audio_items` (3f40f809)
  - `audio_left_01` (3f42a3cb)
  - `audio_left_02` (3f42a3d9)
  - `audio_right_01` (3f42a3e7)
  - `audio_right_02` (3f42a3f6)
  - `audio_mid_01` (3f42a391)
  - `audio_mid_02` (3f42a39e)
  - `audio_bounce_01` (3f42a3ab)
  - `audio_bounce_02` (3f42a3bb)
  - `rest_loop_01` (referenced in PTR table)

### Sound Effects
- `loud_sound1` (3f42cbe1)
- `loud_sound2` (3f42cbed)
- `sounds guud.` (3f42f916)

### DAC (Digital-to-Analog Converter)
- `DAC channel error` (3f426956)
- `dac_output_disable` (3f426973)
- `dac_output_enable` (3f426986)
- `dac_pad_get_io_num` (3f426998)

### Bluetooth Speaker
- **BT speaker functions**:
  - `EMO_SPEAKER_%02X%02X` (3f419865) - device name format
  - `bt_speaker_connect_to_last_device` (3f417264)
  - `speaker_connecting` (3f4314c3)
  - `speaker_con_fail` (3f4314d6)
  - `speaker_con_succ` (3f4314e7)
  - `set bt volume %d` (3f41686d)
  - `audio full` (3f416b31)
  - `emo_system->emo_speaker_running = 1` (3f416e30)
  - `speaker_role` (3f412154)

### Audio Scheduling
- `schedule_sound` (3f412126)

### ESP Audio Platform
- `ESP_AUDIO` (3f44302c) - referenced 3 times
- `AUDIO_STREAM` (3f447ff0) - referenced 19 times
- Multiple references to ESP Audio workshop paths

### Audio Errors
- `AUDIO_ERR_UNKNOWN` (3f448248)
- `STREAM_I2S_READ_ERROR` (3f448364)
- `STREAM_I2S_WRITE_ERROR` (3f44837c)
- `SOFTCODEC_INTI_ERROR` (3f448584)
- `SOFTCODEC_ENCODE_DECODE_ERROR` (3f44859c)
- `PLAYER_NO_AUDIO_AVAILABLE` (3f4485dc)

### Advanced Audio
- `Advanced Audio` (3f41d3b7)
- `Advanced Audio Sink` (3f420e40)

---

## 4. GPIO Configuration

### GPIO Functions
- **Core GPIO operations**:
  - `gpio_config` (3f42611e) - referenced 5 times
  - `gpio_set_level` (3f42619e) - referenced 2 times
  - `gpio_get_level` (implied by usage patterns)
  - `gpio_set_pull_mode` (referenced in PTR table)
  - `gpio_intr_disable` (3f4261ad)
  - `psram_gpio_config` (3f4025d6) - PSRAM GPIO configuration

### GPIO Usage
The GPIO system is used extensively for:
- Servo control signals
- Sensor inputs (foot sensors, touch sensors)
- LED matrix control
- Audio I/O
- General peripheral control

### Error Messages
- Various "Cannot use SET_PERI_REG_BITS" and "Cannot use CLEAR_PERI_REG_MASK" warnings
- Indicates direct register manipulation with safety checks

---

## 5. Microphone System

### Microphone Configuration
- **Microphone management**:
  - `mic` (3f41404d) - referenced 6 times
  - `my mic` (3f414042)
  - `you mic` (3f414049)
  - `open_mic` (3f42db50) - referenced 5 times
  - `mic_num` (3f42f532) - referenced 3 times
  - `set mic num %d` (3f42f53a)

### Audio Input
- **I2S microphone input**:
  - `I2S_READER` (3f445944) - handles microphone data
  - `i2s_read` (3f44f698) - reads audio data from microphone
  - `CreateI2sStreamReader` (3f445b34) - creates microphone input stream

### MIC Computation
- `MIC computation for BIP Failed(res=%d)` (3f404b0c)
- `MIC mismatch for the Bcast Mgmt frame(res=%d)` (3f404b58)
- These appear to be related to WiFi security (MIC = Message Integrity Check)

### Voice Processing
- `chatgpt_hear` (referenced in PTR table) - likely voice command processing

---

## 6. Touch Sensors

### Touch Pad System
The firmware implements a comprehensive capacitive touch sensor system.

### Touch Pad Functions
- **Initialization**:
  - `touch_pad_io_init` (3f426b24)
  - `touch_pad_config` (3f426a7b) - referenced 3 times

- **Reading**:
  - `touch_pad_read` (3f426a6c) - referenced 4 times
  - `touch_pad_read_filtered` (3f426a54) - referenced 5 times

- **Filter management**:
  - `touch_pad_filter_start` (3f426a3d) - referenced 3 times
  - `Touch_pad_filter_period_error` (3f4267f8)
  - `Touch_pad_filter_not_initialized` (3f4267d7)

### Touch Pad Configuration
- **Voltage settings**:
  - `touch_pad_set_voltage` (3f426b4d) - referenced 4 times
  - `touch_refh_error` (3f42667f)
  - `touch_refl_error` (3f426690)
  - `touch_atten_error` (3f4266a1)

- **Mode settings**:
  - `touch_pad_set_fsm_mode` (3f426b0d)
  - `touch_pad_set_cnt_mode` (3f426b36) - referenced 3 times
  - `touch_pad_set_trigger_mode` (3f426add)
  - `touch_pad_set_trigger_source` (3f426ac0)

- **Threshold**:
  - `touch_pad_set_thresh` (3f426af8)

### Touch Pad Grouping
- **Group mask operations**:
  - `touch_pad_set_group_mask` (3f426aa7) - referenced 4 times
  - `touch_pad_clear_group_mask` (3f426a8c) - referenced 4 times
  - `touch_set1_bitmask_error` (3f426751)
  - `touch_set2_bitmask_error` (3f42676a)
  - `touch_work_en_bitmask_error` (referenced)

### Touch Pad Parameters
- `touch_slope_error` (3f4266b3)
- `touch_opt_error` (3f4266c5)
- `touch_IO_error` (3f4266d5)
- `touch_fsm_mode_error` (3f426708)
- `touch_trigger_mode_error` (3f42671d)
- `touch_trigger_source_error` (3f426736)

### Touch Pad Errors
- `Touch_pad_not_initialized` (3f42679f) - referenced 6 times
- `Touch_Pad Num Err` (3f4267b9) - referenced 5 times
- `touch_value` (3f4267cb)

### RTC Module Integration
- Touch sensors are controlled via the RTC (Real-Time Clock) module
- Reference: `RTC_MODULE` (3f4264c1) - used extensively with touch functions

---

## 7. Task Architecture

### FreeRTOS Tasks
The firmware uses FreeRTOS for multitasking. Key tasks identified:

- **Audio task**: `audio_status_task` (3f427f20)
- **Sensor tasks**: Likely for reading touch, foot sensors, IMU
- **Motion task**: Servo control and animation playback
- **Communication tasks**: WiFi, Bluetooth
- **Face recognition task**: Camera and face processing

### Task Creation
Multiple references to `xTaskCreate` throughout the code indicate task-based architecture.

---

## 8. Storage & Configuration

### NVS (Non-Volatile Storage)
- `save_volume_info_to_nvs` (3f435972)
- `save_custom_face_info_to_nvs` (3f4358a5)
- `faceinfo_%d` (3f43572e) - face data storage keys
- `mic_num` (3f42f532) - microphone configuration storage

### SPIFFS File System
- `/spiffs/avi/face_id.avi` (3f42cba8)
- `/spiffs/avi/reg_face_success.avi` (3f42cbc0)
- Animation and face data stored in SPIFFS

### Preference Themes
Multiple "preference theme" strings indicate user-configurable settings:
- Volume preferences
- Eye animation preferences
- Behavior preferences

---

## 9. Communication Systems

### WiFi
- Standard ESP32 WiFi functionality
- `esp_wifi` references throughout
- Network interface configuration

### Bluetooth
- Bluetooth speaker functionality
- `EMO_SPEAKER_%02X%02X` device naming
- BT connection management

### OTA (Over-The-Air Updates)
- Multiple OTA references
- Firmware update capability
- `OTA_F` string reference

---

## 10. Sensor Systems

### Foot Sensors
- `read_foot_sensor 0` (3f41287f)
- Used for detecting when EMO is picked up or on a surface

### IMU (Inertial Measurement Unit)
- `roll = %d, pitch = %d` (3f42c5ef)
- Orientation and motion detection

### Camera
- Face recognition functionality
- Coordinate tracking for detected faces

---

## 11. Code Organization

### File Structure
The decompiled code shows references to development paths:
- `/home/zht/zht/master/esp-alexa/...`
- `/workshop/audio/esp-audio-app/components/...`
- Indicates original development environment

### Libraries Used
- **ESP-IDF**: Core ESP32 framework
- **ESP Audio ADF**: Audio Development Framework
- **FreeRTOS**: Real-time operating system
- **LVGL or similar**: Likely for display management
- **OpenSSL**: For secure communications

---

## 12. Key Function Addresses

### Critical Functions (Examples)
- Servo control: Functions around 0x40258000 - 0x4025A000
- Touch sensors: Functions around 0x401D7000 - 0x401D8000
- Audio: Functions around 0x40246000 - 0x40252000
- Face recognition: Functions around 0x401E5000 - 0x401ED000
- GPIO: Functions around 0x401D5000 - 0x401D6000

---

## 13. Recommendations for Reimplementation

### Phase 1: Core Systems
1. **GPIO & Hardware Abstraction**
   - Implement GPIO control for servos, sensors, LEDs
   - Create HAL for touch sensors
   - Set up I2S for audio I/O

2. **Sensor Reading**
   - Touch pad driver (10 pads based on error messages)
   - Foot sensor reading
   - IMU integration (roll/pitch tracking)

### Phase 2: Motion Control
1. **Servo System**
   - Support for both "old" and "new" servo types
   - Individual servo control (left/right legs, left/right feet)
   - Servo parameter reading/writing
   - Animation playback system

2. **Movement Tables**
   - Create animation data structures
   - Implement interpolation for smooth motion

### Phase 3: Display & Face System
1. **LED Matrix Control**
   - Eye animation rendering
   - Face pattern display
   - Sticker/customization system

2. **Face Recognition**
   - Camera integration
   - Face detection and tracking
   - Face storage in NVS

### Phase 4: Audio System
1. **I2S Audio**
   - Microphone input (I2S_READER)
   - Speaker output (I2S_WRITER)
   - Volume control

2. **Audio Playback**
   - Sound effect management
   - Audio file playback from SPIFFS
   - Bluetooth speaker mode

### Phase 5: High-Level Behavior
1. **Task Management**
   - Create FreeRTOS tasks for each subsystem
   - Implement inter-task communication

2. **User Interaction**
   - Touch sensor event handling
   - Voice command processing
   - Face recognition responses

---

## 14. Hardware Configuration Summary

Based on the firmware analysis:

### Servos
- **4 servo groups**: Left leg, Right leg, Left foot, Right foot
- **Two servo types**: Old and new hardware versions
- **Communication**: Likely serial or PWM-based

### Touch Sensors
- **10 touch pads** (based on error checking)
- **Capacitive sensing** via ESP32 RTC module
- **Filtering support** for noise reduction

### Audio
- **I2S interface** for both input and output
- **DAC support** for analog audio output
- **Microphone**: I2S PDM or standard I2S
- **Speaker**: I2S DAC or external codec

### Display
- **LED matrix** for eyes/face
- **Pixel-based rendering**
- **Frame buffer management**

### Sensors
- **Foot sensors**: At least 1 (possibly 2)
- **IMU**: Roll and pitch sensing
- **Camera**: For face recognition

### Storage
- **NVS**: Configuration and face data
- **SPIFFS**: Animation files, audio files

---

## 15. Next Steps for Development

1. **Extract Animation Data**
   - Search for large static arrays in the binary
   - These likely contain servo position tables

2. **Map GPIO Pins**
   - Identify which GPIO pins control which hardware
   - Create pin definition header file

3. **Implement HAL**
   - Hardware Abstraction Layer for each subsystem
   - Allows for easier testing and modification

4. **Create Test Programs**
   - Individual tests for each subsystem
   - Verify hardware functionality

5. **Build Behavior Engine**
   - State machine for EMO's behaviors
   - Event-driven architecture

---

## Conclusion

The EMO firmware is a sophisticated embedded system with:
- **Multi-servo motion control** with animation playback
- **Advanced face recognition** and display system
- **Full audio pipeline** (microphone, processing, speaker)
- **Touch sensor interface** for user interaction
- **Wireless connectivity** (WiFi, Bluetooth)
- **OTA update capability**

The code is well-structured with clear separation of concerns, extensive error handling, and modular design. A clean-room reimplementation should focus on recreating the functionality rather than copying the exact implementation.

---

## File References

**Primary Analysis File**: `ghidraExtracted-elfPartition1.c` (82.5 MB, ~79 MB)
**Secondary File**: `emo_esp32_firmware.bin.c` (16 MB, heavily stripped)

**Report Generated**: 2025-01-05
**Analysis Tool**: Ghidra decompilation + manual code review
