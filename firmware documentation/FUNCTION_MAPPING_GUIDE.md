# EMO Firmware Function Mapping Guide

## Purpose
This document provides specific function addresses, string references, and code citations from the decompiled firmware to help locate and understand each subsystem's implementation.

---

## 1. Motor/Servo Control Functions

### String References (Data Section)
```
Address         String                                  Usage
3f412869        "AA_this is old servo\n"               Servo type detection
3f412893        "AA_this is new servo\n"               Servo type detection
3f42c607        "emo_servo_tight = %d\r\n"             Servo tension parameter
3f42ccd8        "SERVO_TEST"                           Servo testing mode (8 refs)
3f42f582        "set new servos...\n"                  New servo initialization
3f42f602        "set servos...\n"                      Servo initialization
3f42f611        "SERVO_P_SET_MODE\r"                   Servo mode setting
3f42f623        "SERVO_P_SET_MODE_2\r"                 Alternate servo mode
3f42f694        "reading servos!\nnew servo test\n"    Servo read test
3f42f746        "reading servos!\n"                    Servo reading
3f43058a        "play_animation_without_servor"        Animation playback
```

### Servo Update Functions
```
Address         String                                  Body Part
3f44baf0        "Left  legs servo update done\n"       Left legs
3f44bb0e        "Left  legs servo update fail\n"       Left legs (error)
3f44bb36        "Left  foot servo update done\n"       Left foot
3f44bb54        "Left  foot servo update fail\n"       Left foot (error)
3f44bb7d        "Right legs servo update done\n"       Right legs
3f44bb9b        "Right legs servo update fail\n"       Right legs (error)
3f44bbc4        "Right foot servo update done\n"       Right foot
3f44bbe2        "Right foot servos update fail\n\n\n"  Right foot (error)
```

### Servo Parameter Functions
```
Address         String                                  Function
3f44be64        "set_servo_parameter %d %02x %d\r\n"   Set parameter
3f44befa        "read_servo_parameter"                 Read parameter
3f44beb9        "read_new_servo_parameter"             Read new servo param
3f44be85        "new_servo: start one %d %d\r\n"       Start new servo
3f44bea2        "change_new_servo_ratio"               Change servo ratio
3f44bf1d        "change_servo_ratio"                   Change servo ratio (old)
```

### Servo Control Functions
```
Address         String                                  Function
3f44c0db        "servo stop 1\r"                       Stop command 1
3f44c193        "servo stop 2\r"                       Stop command 2
3f44b8dc        "uninstall_servo_all 001\r"            Uninstall servos
3f44b8f5        "uninstall_servo_all 002\r"            Uninstall servos (alt)
3f44bacc        "Servo update...........\n\n"          Update start
```

### Servo I/O Functions
```
Address         String                                  Function
3f44bdd1        "get in servo io =  %d\r\n"            Get servo I/O state
3f44bd24        "servo option cmd %s addr %02x data %d\n" Servo command
3f44bd4b        "servo_read_success\r"                 Read success
3f44bd5f        "servo_read_fail %d\r\n"               Read fail 1
3f44bd74        "servo_read_fail2 %d\r\n"              Read fail 2
3f44bd8a        "servo_read_fail3 %d\r\n"              Read fail 3
3f44bda0        "servo_read_fail4 %d\r\n"              Read fail 4
```

### Key Function Addresses
```
Function                    Address         Description
FUN_40258d68               40258d68        Uninstall all servos
FUN_40258ec8               40258ec8        Set servo offset value
FUN_40258ef4               40258ef4        Set servo offset (alt)
FUN_40259410               40259410        Servo update main function
FUN_402597a0               402597a0        Servo option command handler
FUN_40259b84               40259b84        Get servo I/O
FUN_40259cbc               40259cbc        Read servo parameter
FUN_40259e00               40259e00        Set servo parameter
FUN_40259ef8               40259ef8        New servo start
FUN_4025a010               4025a010        New servo read parameter
FUN_4025a140               4025a140        Change servo ratio
FUN_4025cf6c               4025cf6c        Servo stop handler
```

---

## 2. Face/Eye Animation Functions

### Eye Mode Strings
```
Address         String                                  Mode
3f411a97        "white_eye_on"                         White eye on (7 refs)
3f411aa4        "preference theme white_eye_on!!..."   Preference setting
3f411ad7        "white_eye_off"                        White eye off (7 refs)
3f411ae5        "preference theme white_eye_off!!..."  Preference setting
3f411dcc        "clear_eye"                            Clear eye display (7 refs)
3f411dd6        "customize theme clear_eye!!..."       Customize theme
3f411e05        "set_eye"                              Set eye pattern (3 refs)
3f411e12        "eye_rsp"                              Eye response (5 refs)
3f412173        "white_eye"                            White eye mode (7 refs)
3f412502        "new_eye"                              New eye system (4 refs)
3f40fa75        "laser_eye"                            Laser eye effect (2 refs)
3f42b8fb        "laser_eye_2"                          Laser eye effect 2
```

### Eye Customization
```
Address         String                                  Function
3f42a610        "eyes_stickers_set"                    Set eye stickers (4 refs)
3f42b714        "eyes_stickers_clear"                  Clear stickers
3f42b6e0        "eyes_color_change1"                   Change eye color
3f42b6f3        "eyes_setting_in"                      Eye settings enter
3f42b703        "eyes_setting_out"                     Eye settings exit
3f42b662        "white_emo_eyes_change_1BW"            Eye change animation 1
3f42b67c        "white_emo_eyes_change_2WB"            Eye change animation 2
```

### Face Recognition Strings
```
Address         String                                  Function
3f4113dd        "face_req"                             Face request (4 refs)
3f412382        "face_rsp"                             Face response (7 refs)
3f4123f8        "faces"                                Multiple faces (4 refs)
3f42e56a        "register_face"                        Register new face
3f42e5a8        "query_face"                           Query face database
3f42e5c8        "doesnt_know_face"                     Unknown face
3f42b0f4        "reg_face_success"                     Registration success
```

### Face Command Strings
```
Address         String                                  Command
3f4163f3        "got face cmd\r"                       Face command received
3f41642d        "got faces cmd\r"                      Faces command received
3f41643c        "got face cmd 0x12\r"                  Face command 0x12
3f41644f        "got faces cmd 0x13\r"                 Faces command 0x13
3f416463        "got faces end\r"                      Faces command end
```

### Face Coordinate Tracking
```
Address         String                                  Data Field
3f42ca44        "coordinate_data1->face.x = %d\r\n"    Face X coordinate
3f42ca64        "coordinate_data1->face.y = %d\r\n"    Face Y coordinate
3f42ca84        "coordinate_data1->face.width = %d\r\n" Face width
3f42caa8        "coordinate_data1->face.height = %d\r\n" Face height
3f42cacd        "coordinate_data1->face.id = %d\r\n"   Face ID
3f42caee        "coordinate_data1->face.name = %s\r\n" Face name
3f42cb11        "face_center_x1 = %d\r\n"              Face center X
3f42cb27        "face_center_y1 = %d\r\n"              Face center Y
```

### Face Storage
```
Address         String                                  Path/Key
3f42cba8        "/spiffs/avi/face_id.avi"              Face ID video
3f42cbc0        "/spiffs/avi/reg_face_success.avi"     Success animation
3f43572e        "faceinfo_%d"                          NVS storage key
3f4358a5        "save_custom_face_info_to_nvs"         Save function
```

### App Face Integration
```
Address         String                                  Function
3f42b69f        "app_face_in"                          App face enter
3f42b6ab        "app_face_out"                         App face exit
3f42b6b8        "app_face_delete"                      Delete face from app
```

### Key Function Addresses
```
Function                    Address         Description
FUN_40123c00               40123c00        Face request handler
FUN_40124161               40124161        Eye mode handler (multiple modes)
FUN_40124cbe               40124cbe        Clear/set eye handler
FUN_40124f30               40124f30        Display scan result
FUN_401294d8               401294d8        New eye handler
FUN_4014120c               4014120c        Face command dispatcher
FUN_401e56b0               401e56b0        Eye stickers handler
FUN_401e7f88               401e7f88        Face registration success
FUN_401eda36               401eda36        Face coordinate logging
FUN_40201754               40201754        Face info handler
```

---

## 3. Audio/Speaker System Functions

### Audio Status Strings
```
Address         String                                  Status
3f427e51        " AUDIO_STATUS_UNKNOWN \r"             Unknown status
3f427e7e        " AUDIO_STATUS_FINISHED 0 \r"          Finished playing
3f427e99        " AUDIO_STATUS 0 \r"                   Status 0
3f427eab        " AUDIO_STATUS_ERROR \r"               Error status
3f427ec1        " AUDIO_STATUS_AUX_IN \r"              Aux input mode
3f427f20        "audio_status_task"                    Status task name
3f426f81        "setting audio status %d\r\n"          Status setter
```

### Volume Control Strings
```
Address         String                                  Function
3f40f756        "volume"                               Volume parameter (8 refs)
3f411561        "volume_mute"                          Mute mode (7 refs)
3f41156d        "preference theme volume_mute!!..."    Mute preference
3f41159f        "volume_low"                           Low volume (7 refs)
3f4115aa        "preference theme volume_low!!..."     Low preference
3f4115db        "volume_med"                           Medium volume (7 refs)
3f4115e6        "preference theme volume_med!!..."     Med preference
3f411617        "volume_high"                          High volume (7 refs)
3f411623        "preference theme volume_high!!..."    High preference
3f42a57d        "volume_set_mute"                      Set mute function
3f42a58d        "volume_set"                           Set volume function
3f42a598        "volume_set_down"                      Decrease volume
3f42a5a8        "volume_set_mid"                       Set medium volume
3f435972        "save_volume_info_to_nvs"              Save to NVS
```

### I2S Audio Strings
```
Address         String                                  Component
3f4453e8        "I2S_STREAM"                           I2S stream (20 refs)
3f44542c        "i2s_type_%d"                          I2S type (4 refs)
3f44577c        "I2S_WRITER"                           I2S writer (16 refs)
3f445944        "I2S_READER"                           I2S reader (4 refs)
3f445b34        "CreateI2sStreamReader"                Create reader (14 refs)
3f445b4c        "CreateI2sStreamWriter"                Create writer (14 refs)
3f44f698        "i2s_read"                             I2S read function (4 refs)
3f445b64        "i2sMonoFix"                           Mono fix function
3f445b70        "i2sDacDataScale"                      DAC scaling
3f44f5f8        "I2S DAC PDM only support on I2S0"     PDM limitation
```

### Audio Playback Strings
```
Address         String                                  Audio Item
3f40f809        "audio_items"                          Audio items list
3f42a3cb        "audio_left_01"                        Left audio 1
3f42a3d9        "audio_left_02"                        Left audio 2
3f42a3e7        "audio_right_01"                       Right audio 1
3f42a3f6        "audio_right_02"                       Right audio 2
3f42a391        "audio_mid_01"                         Mid audio 1
3f42a39e        "audio_mid_02"                         Mid audio 2
3f42a3ab        "audio_bounce_01"                      Bounce audio 1
3f42a3bb        "audio_bounce_02"                      Bounce audio 2
```

### Sound Effect Strings
```
Address         String                                  Sound
3f42cbe1        "loud_sound1"                          Loud sound 1
3f42cbed        "loud_sound2"                          Loud sound 2
3f42f916        "sounds guud."                         Sound good message
3f42f475        "Speaker!\n"                           Speaker message
```

### DAC Strings
```
Address         String                                  Function
3f426956        "DAC channel error"                    DAC error (4 refs)
3f426973        "dac_output_disable"                   Disable DAC
3f426986        "dac_output_enable"                    Enable DAC
3f426998        "dac_pad_get_io_num"                   Get DAC GPIO
```

### Bluetooth Speaker Strings
```
Address         String                                  Function
3f419865        "EMO_SPEAKER_%02X%02X"                 BT device name (8 refs)
3f417264        "bt_speaker_connect_to_last_device"    BT connect (6 refs)
3f4314c3        "speaker_connecting"                   Connecting status
3f4314d6        "speaker_con_fail"                     Connection failed
3f4314e7        "speaker_con_succ"                     Connection success
3f41686d        "set bt volume %d\r\n"                 Set BT volume
3f416b31        "audio full\r"                         Audio buffer full
3f416e30        "emo_system->emo_speaker_running = 1"  Speaker running flag
3f412154        "speaker_role"                         Speaker role (7 refs)
```

### ESP Audio Framework Strings
```
Address         String                                  Component
3f44302c        "ESP_AUDIO"                            ESP Audio (3 refs)
3f447ff0        "AUDIO_STREAM"                         Audio stream (19 refs)
3f448220        "AudioStreamI2sGet"                    Get I2S stream (4 refs)
3f448248        "AUDIO_ERR_UNKNOWN"                    Unknown error (11 refs)
3f448288        "CODEC"                                Codec component
3f448364        "STREAM_I2S_READ_ERROR"                I2S read error
3f44837c        "STREAM_I2S_WRITE_ERROR"               I2S write error
3f448584        "SOFTCODEC_INTI_ERROR"                 Codec init error
3f44859c        "SOFTCODEC_ENCODE_DECODE_ERROR"        Codec error
3f4485dc        "PLAYER_NO_AUDIO_AVAILABLE"            No audio available
```

### Key Function Addresses
```
Function                    Address         Description
FUN_40124161               40124161        Volume mode handler
FUN_401421e0               401421e0        Set BT volume
FUN_40142628               40142628        Audio full handler
FUN_40142538               40142538        BT speaker connect
FUN_40147d5c               40147d5c        EMO speaker name handler
FUN_401d83f8               401d83f8        DAC channel handler
FUN_401d8468               401d8468        DAC enable
FUN_401d8518               401d8518        DAC disable
FUN_401dad48               401dad48        Set audio status
FUN_401dfb38               401dfb38        Audio status handler
FUN_4024a344               4024a344        I2S stream handler
FUN_4024a900               4024a900        I2S writer/reader
FUN_4024afec               4024afec        Create I2S writer
FUN_4024b114               4024b114        Create I2S reader
FUN_40246a1c               40246a1c        ESP Audio handler
FUN_40251228               40251228        Audio error handler
FUN_4026a5b4               4026a5b4        I2S DAC/PDM config
FUN_4026af44               4026af44        I2S read function
```

---

## 4. GPIO Functions

### GPIO Control Strings
```
Address         String                                  Function
3f42611e        "gpio_config"                          GPIO config (5 refs)
3f42619e        "gpio_set_level"                       Set GPIO level (2 refs)
3f4261ad        "gpio_intr_disable"                    Disable interrupt
3f4025d6        "psram_gpio_config"                    PSRAM GPIO config
```

### Key Function Addresses
```
Function                    Address         Description
FUN_401d596c               401d596c        GPIO set level
FUN_401d5a5c               401d5a5c        GPIO set pull mode
FUN_401d5c08               401d5c08        GPIO config main
```

### GPIO Usage Patterns
Based on function calls:
- Servo control: Multiple GPIO pins for servo communication
- Touch sensors: GPIO pins connected to touch pads
- LEDs: GPIO pins for LED matrix control
- Sensors: GPIO pins for foot sensors and other inputs

---

## 5. Microphone System Functions

### Microphone Strings
```
Address         String                                  Function
3f41404d        "mic"                                  Microphone (6 refs)
3f414042        "my mic"                               My microphone
3f414049        "you mic"                              Your microphone
3f42db50        "open_mic"                             Open microphone (5 refs)
3f42f532        "mic_num"                              Mic number (3 refs)
3f42f53a        "set mic num %d\n"                     Set mic number
```

### MIC Security Strings (WiFi)
```
Address         String                                  Function
3f404b0c        "MIC computation for BIP Failed(res=%d)" MIC computation
3f404b58        "MIC mismatch for the Bcast Mgmt frame" MIC mismatch
```

### Key Function Addresses
```
Function                    Address         Description
FUN_40120fc8               40120fc8        Mic handler
FUN_40134718               40134718        You/my mic handler
FUN_401f1858               401f1858        Open mic handler
FUN_401f5028               401f5028        Set mic number
FUN_4020240c               4020240c        Mic number config
FUN_4024a900               4024a900        I2S reader (mic input)
FUN_4024b114               4024b114        Create I2S reader
FUN_4026af44               4026af44        I2S read (mic data)
```

---

## 6. Touch Sensor Functions

### Touch Pad Strings
```
Address         String                                  Function
3f42679f        "Touch pad not initialized"            Not init (6 refs)
3f4267b9        "Touch_Pad Num Err"                    Pad number error (5 refs)
3f4267cb        "touch_value"                          Touch value
3f4267d7        "Touch pad filter not initialized"     Filter not init
3f4267f8        "Touch pad filter period error"        Filter period error
3f426a3d        "touch_pad_filter_start"               Start filter (3 refs)
3f426a54        "touch_pad_read_filtered"              Read filtered (5 refs)
3f426a6c        "touch_pad_read"                       Read touch (4 refs)
3f426a7b        "touch_pad_config"                     Config touch (3 refs)
3f426a8c        "touch_pad_clear_group_mask"           Clear group (4 refs)
3f426aa7        "touch_pad_set_group_mask"             Set group (4 refs)
3f426ac0        "touch_pad_set_trigger_source"         Set trigger source
3f426add        "touch_pad_set_trigger_mode"           Set trigger mode
3f426af8        "touch_pad_set_thresh"                 Set threshold
3f426b0d        "touch_pad_set_fsm_mode"               Set FSM mode
3f426b24        "touch_pad_io_init"                    Init I/O
3f426b36        "touch_pad_set_cnt_mode"               Set count mode (3 refs)
3f426b4d        "touch_pad_set_voltage"                Set voltage (4 refs)
```

### Touch Error Strings
```
Address         String                                  Error Type
3f42667f        "touch refh error"                     Reference high error
3f426690        "touch refl error"                     Reference low error
3f4266a1        "touch atten error"                    Attenuation error
3f4266b3        "touch slope error"                    Slope error
3f4266c5        "touch opt error"                      Option error
3f4266d5        "touch IO error"                       I/O error
3f426708        "touch fsm mode error"                 FSM mode error
3f42671d        "touch trigger mode error"             Trigger mode error
3f426736        "touch trigger source error"           Trigger source error
3f426751        "touch set1 bitmask error"             Set1 bitmask error
3f42676a        "touch set2 bitmask error"             Set2 bitmask error
```

### Key Function Addresses
```
Function                    Address         Description
FUN_4008de74               4008de74        Touch pad read filtered
FUN_401d7214               401d7214        Touch pad set voltage
FUN_401d7310               401d7310        Touch pad set count mode
FUN_401d73dc               401d73dc        Touch pad I/O init
FUN_401d7474               401d7474        Touch pad set FSM mode
FUN_401d7560               401d7560        Touch pad set threshold
FUN_401d7608               401d7608        Touch pad set trigger mode
FUN_401d767c               401d767c        Touch pad set trigger source
FUN_401d76f0               401d76f0        Touch pad set group mask
FUN_401d7858               401d7858        Touch pad clear group mask
FUN_401d7b74               401d7b74        Touch pad config
FUN_401d7ce4               401d7ce4        Touch pad read
FUN_401d7dac               401d7dac        Touch pad filter start
```

### RTC Module Reference
```
Address         String                                  Module
3f4264c1        "RTC_MODULE"                           RTC module (used with touch)
3f4080f4        RTCCNTL (0x3FF48000)                   RTC control registers
```

---

## 7. Task Architecture

### Task Names
```
Address         String                                  Task
3f427f20        "audio_status_task"                    Audio status monitoring
```

### Task Creation Pattern
Look for `xTaskCreate` calls throughout the code. Key task creation areas:
- Audio tasks: Around 0x401D0000 - 0x401E0000
- Sensor tasks: Around 0x401D7000 - 0x401D8000
- Motion tasks: Around 0x40258000 - 0x4025A000

---

## 8. Storage & Configuration

### NVS Storage Keys
```
Address         String                                  Key
3f42f532        "mic_num"                              Microphone number
3f435972        "save_volume_info_to_nvs"              Volume settings
3f4358a5        "save_custom_face_info_to_nvs"         Face data
3f43572e        "faceinfo_%d"                          Face info (format string)
```

### SPIFFS Paths
```
Address         String                                  Path
3f42cba8        "/spiffs/avi/face_id.avi"              Face ID video
3f42cbc0        "/spiffs/avi/reg_face_success.avi"     Success animation
```

### Key Function Addresses
```
Function                    Address         Description
FUN_401d12b8               401d12b8        NVS read
FUN_401d12f8               401d12f8        NVS write
FUN_40201fa3               40201fa3        Save face info to NVS
FUN_4020200c               4020200c        Save volume info to NVS
FUN_40202503               40202503        Read mic num from NVS
```

---

## 9. Communication Systems

### WiFi Strings
```
Address         String                                  Function
3f40d7c0        "Network interface is not configured"  Network error
```

### Bluetooth Strings
```
Address         String                                  Function
3f419865        "EMO_SPEAKER_%02X%02X"                 BT device name
3f417264        "bt_speaker_connect_to_last_device"    BT connection
3f41d3b7        "Advanced Audio"                       Advanced audio profile
3f420e40        "Advanced Audio Sink"                  Audio sink profile
```

### OTA Strings
```
Address         String                                  Function
3f40c4a7        "OTA_F"                                OTA flag
```

---

## 10. Sensor Systems

### Foot Sensor Strings
```
Address         String                                  Function
3f41287f        "read_foot_sensor 0\r"                 Read foot sensor
```

### IMU Strings
```
Address         String                                  Function
3f42c5ef        "roll = %d, pitch = %d\r\n"            IMU orientation
```

---

## 11. Important Memory Addresses

### Hardware Registers
```
Address         Description
0x3FF48000      RTC Control (RTCCNTL)
0x3FF44000      GPIO registers (implied)
0x3FF4F000      I2S registers (implied)
```

### RAM Regions
```
Address Range           Description
0x3FFC0000-0x3FFC8000  Internal SRAM (data)
0x3FFB0000-0x3FFC0000  Internal SRAM (instruction)
0x3F400000-0x3F800000  External SPIRAM (if present)
```

### Flash Regions
```
Address Range           Description
0x3F400000-0x3F800000  Flash memory mapped region
0x400C0000-0x40400000  Instruction cache region
```

---

## 12. Development Environment Clues

### Source Paths Found
```
/home/zht/zht/master/esp-alexa/...
/workshop/audio/esp-audio-app/components/...
```

These indicate:
- Developer username: zht
- Project name: esp-alexa (likely EMO's internal name)
- ESP Audio ADF integration
- Linux development environment

---

## 13. Search Patterns for Further Analysis

### To Find Animation Tables
Search for:
- Large arrays of uint16_t or int16_t (servo angles)
- Arrays with regular patterns (animation frames)
- Data sections between 0x3F400000 - 0x3F450000

### To Find GPIO Pin Mappings
Search for:
- `gpio_set_level` calls with constant pin numbers
- `gpio_config` structures with pin definitions
- Pin number constants (0-39 for ESP32)

### To Find Task Priorities
Search for:
- `xTaskCreate` calls
- Priority values (typically 1-25)
- Stack sizes (typically 2048-8192 bytes)

---

## 14. Function Call Patterns

### Typical Servo Control Sequence
```
1. Check servo type (old/new)
2. Initialize servo parameters
3. Set servo mode
4. Read servo status
5. Update servo positions
6. Check for errors
```

### Typical Touch Sensor Sequence
```
1. Initialize touch pad I/O
2. Configure touch pad parameters
3. Set voltage and threshold
4. Start filter
5. Read filtered values
6. Process touch events
```

### Typical Audio Playback Sequence
```
1. Create I2S stream
2. Configure audio parameters
3. Set volume
4. Start playback
5. Monitor status
6. Handle errors
```

---

## 15. Cross-Reference Guide

### Servo ↔ GPIO
- Servo control uses GPIO for communication
- Look for `gpio_set_level` calls in servo functions
- Servo I/O functions reference GPIO pins

### Touch ↔ RTC
- Touch sensors controlled via RTC module
- All touch functions reference RTC registers
- Touch pad numbers map to RTC touch channels

### Audio ↔ I2S
- Audio input/output uses I2S peripheral
- I2S_READER for microphone
- I2S_WRITER for speaker
- DAC can be used for analog audio output

### Face ↔ Camera ↔ Storage
- Face recognition uses camera input
- Face data stored in NVS
- Face animations stored in SPIFFS
- Coordinate tracking for face position

---

## 16. Next Agent Instructions

### To Locate Specific Functionality:

1. **For Servo Control**:
   - Start at function addresses 0x40258000 - 0x4025A000
   - Search for strings starting with "servo"
   - Look for servo update functions by body part

2. **For Face/Eye Animations**:
   - Start at function addresses 0x40124000 - 0x40128000
   - Search for strings containing "eye", "face"
   - Check display-related functions around 0x401E5000

3. **For Audio**:
   - Start at function addresses 0x40246000 - 0x40252000
   - Search for "I2S", "audio", "volume"
   - Check I2S configuration around 0x4026A000

4. **For Touch Sensors**:
   - Start at function addresses 0x401D7000 - 0x401D8000
   - Search for "touch_pad"
   - All functions reference RTC module

5. **For GPIO**:
   - Start at function addresses 0x401D5000 - 0x401D6000
   - Search for "gpio_"
   - Look for pin number constants

### To Extract Animation Data:
1. Search for large static arrays in data sections
2. Look for patterns of int16_t values (servo angles typically -180 to +180)
3. Check addresses 0x3F400000 - 0x3F450000 for animation tables

### To Map Hardware Pins:
1. Find all `gpio_config` calls
2. Extract pin numbers from configuration structures
3. Cross-reference with servo, sensor, and LED functions

---

## Conclusion

This mapping guide provides specific addresses, strings, and function references to help locate and understand each subsystem in the EMO firmware. Use the string addresses as entry points to find related functions, and follow cross-references to understand how subsystems interact.

For detailed implementation analysis, examine the functions at the provided addresses in the decompiled code. The string references serve as landmarks to navigate the large codebase effectively.
