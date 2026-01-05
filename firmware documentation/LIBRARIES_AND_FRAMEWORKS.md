# EMO Firmware - Libraries and Frameworks Analysis

## Overview
This document identifies all libraries, frameworks, and components used in the EMO pet firmware based on analysis of the decompiled code.

---

## Core Framework: ESP-IDF (Espressif IoT Development Framework)

### Version Information
- **Development Path**: `/home/zht/esp/idf/`
- **Developer**: zht (username found in paths)
- **Platform**: ESP32
- **Framework**: ESP-IDF (Espressif's official development framework)

### ESP-IDF Version Indicators
The decompiled strings confirm ESP-IDF component paths, but the exact version is not embedded. API names suggest a pre-v5 IDF, but the version cannot be confirmed from strings alone.

---

## 1. ESP-IDF Core Components

### 1.1 ESP32 Hardware Components
```
Location: /home/zht/esp/idf/components/esp32/

Components:
- cpu_start.c          - CPU initialization and startup
- clk.c                - Clock configuration
- crosscore_int.c      - Cross-core interrupts
- intr_alloc.c         - Interrupt allocation
- dport_access.c       - DPORT register access
- brownout.c           - Brownout detection
- task_wdt.c           - Task watchdog timer
- spiram_psram.c       - PSRAM support
- hw_random.c          - Hardware random number generator
- reset_reason.c       - Reset reason detection
- esp_timer_esp32.c    - ESP32 timer implementation
```

**Key Functions Found**:
- `esp_task_wdt_init()` - Watchdog timer initialization
- `esp_task_wdt_add()` - Add task to watchdog
- `esp_clk_init()` - Clock initialization
- `esp_crosscore_int_init()` - Cross-core interrupt init
- `esp_intr_alloc()` - Interrupt allocation
- `esp_brownout_init()` - Brownout detector init
- `esp_fill_random()` - Hardware RNG

### 1.2 ESP Common Components
```
Location: /home/zht/esp/idf/components/esp_common/

Components:
- esp_timer.c          - High-resolution timer
- ipc.c                - Inter-processor communication
```

**Key Functions**:
- `esp_timer_create()` - Create timer
- `esp_timer_start_once()` - One-shot timer
- `esp_timer_start_periodic()` - Periodic timer
- `esp_ipc_init()` - IPC initialization

### 1.3 FreeRTOS (Real-Time Operating System)
```
Location: /home/zht/esp/idf/components/freertos/

Components:
- queue.c              - Queue management
- portmux.c            - Port mutex implementation
- event_groups.c       - Event group synchronization
- tasks.c              - Task management
- timers.c             - Software timers
```

**Usage**: Core RTOS for multitasking, task scheduling, and synchronization.

**Key APIs**:
- `xTaskCreate()` - Create tasks
- `xQueueCreate()` - Create queues
- `xEventGroupCreate()` - Create event groups
- `xTimerCreate()` - Create software timers

---

## 2. Storage & File System Components

### 2.1 NVS (Non-Volatile Storage)
```
Location: /home/zht/esp/idf/components/nvs_flash/

Components:
- nvs_api.cpp          - NVS API implementation
- nvs_storage.cpp      - Storage backend
- nvs_page.cpp         - Page management
- nvs_pagemanager.cpp  - Page manager
- nvs_item_hash_list.cpp - Hash list for items
```

**Purpose**: Key-value storage in flash memory for configuration data.

**Error Codes Found**:
- `ESP_ERR_NVS_NOT_INITIALIZED`
- `ESP_ERR_NVS_NOT_FOUND`
- `ESP_ERR_NVS_TYPE_MISMATCH`
- `ESP_ERR_NVS_READ_ONLY`
- `ESP_ERR_NVS_NOT_ENOUGH_SPACE`
- `ESP_ERR_NVS_INVALID_NAME`
- `ESP_ERR_NVS_INVALID_HANDLE`
- `ESP_ERR_NVS_REMOVE_FAILED`
- `ESP_ERR_NVS_KEY_TOO_LONG`
- `ESP_ERR_NVS_INVALID_STATE`
- `ESP_ERR_NVS_INVALID_LENGTH`
- `ESP_ERR_NVS_NO_FREE_PAGES`
- `ESP_ERR_NVS_VALUE_TOO_LONG`
- `ESP_ERR_NVS_PART_NOT_FOUND`
- `ESP_ERR_NVS_NEW_VERSION_FOUND`
- `ESP_ERR_NVS_XTS_ENCR_FAILED`
- `ESP_ERR_NVS_XTS_DECR_FAILED`
- `ESP_ERR_NVS_XTS_CFG_FAILED`
- `ESP_ERR_NVS_XTS_CFG_NOT_FOUND`
- `ESP_ERR_NVS_ENCR_NOT_SUPPORTED`
- `ESP_ERR_NVS_KEYS_NOT_INITIALIZED`
- `ESP_ERR_NVS_CORRUPT_KEY_PART`
- `ESP_ERR_NVS_CONTENT_DIFFERS`

**Usage in EMO**:
- Face recognition data storage
- Volume settings
- Microphone configuration
- WiFi credentials
- User preferences

### 2.2 SPIFFS (SPI Flash File System)
```
File Paths Found:
- /spiffs/avi/face_id.avi
- /spiffs/avi/reg_face_success.avi
- /spiffs/json/profile.json
```

**Purpose**: File system for storing animation files, audio files, and configuration JSON files.

### 2.3 VFS (Virtual File System)
```
Location: /home/zht/esp/idf/components/vfs/

Components:
- vfs.c                - VFS core
- vfs_uart.c           - UART VFS implementation
```

**Purpose**: Unified file system interface for SPIFFS, SD cards, etc.

---

## 3. Networking Components

### 3.1 WiFi Stack
```
Location: /home/zht/esp/idf/components/esp32/ (WiFi driver)

Key Strings:
- "esp_wifi_init()"
- "esp_wifi_set_config()"
- "esp_wifi_set_storage()"
- "esp_wifi_scan_get_ap_records()"
```

**Error Codes**:
- `ESP_ERR_WIFI_NOT_INIT`
- `ESP_ERR_WIFI_NOT_STARTED`
- `ESP_ERR_WIFI_NOT_STOPPED`
- `ESP_ERR_WIFI_IF`
- `ESP_ERR_WIFI_MODE`
- `ESP_ERR_WIFI_STATE`
- `ESP_ERR_WIFI_CONN`
- `ESP_ERR_WIFI_NVS`
- `ESP_ERR_WIFI_MAC`
- `ESP_ERR_WIFI_SSID`
- `ESP_ERR_WIFI_PASSWORD`
- `ESP_ERR_WIFI_TIMEOUT`
- `ESP_ERR_WIFI_WAKE_FAIL`
- `ESP_ERR_WIFI_WOULD_BLOCK`
- `ESP_ERR_WIFI_NOT_CONNECT`
- `ESP_ERR_WIFI_POST`
- `ESP_ERR_WIFI_INIT_STATE`
- `ESP_ERR_WIFI_STOP_STATE`
- `ESP_ERR_WIFI_REGISTRAR`
- `ESP_ERR_WIFI_WPS_TYPE`
- `ESP_ERR_WIFI_WPS_SM`

**Features**:
- Station mode (client)
- AP mode (access point)
- WiFi scanning
- WPS support
- Power save modes

### 3.2 TCP/IP Adapter
```
Location: /home/zht/esp/idf/components/tcpip_adapter/

Purpose: Network interface abstraction layer
```

**Error Codes**:
- `ESP_ERR_TCPIP_ADAPTER_INVALID_PARAMS`
- `ESP_ERR_TCPIP_ADAPTER_IF_NOT_READY`
- `ESP_ERR_TCPIP_ADAPTER_DHCPC_START_FAILED`
- `ESP_ERR_TCPIP_ADAPTER_DHCP_ALREADY_STARTED`
- `ESP_ERR_TCPIP_ADAPTER_DHCP_ALREADY_STOPPED`
- `ESP_ERR_TCPIP_ADAPTER_NO_MEM`
- `ESP_ERR_TCPIP_ADAPTER_DHCP_NOT_STOPPED`

### 3.3 LwIP (Lightweight IP)
```
References Found:
- "data_to_lwip"
- "rx_data_to_lwip"
- lwip component paths
```

**Purpose**: TCP/IP stack implementation for ESP32.

**Features**:
- TCP/UDP protocols
- DHCP client/server
- DNS client
- ICMP (ping)
- Raw sockets

### 3.4 ESP-NOW
```
Error Codes:
- ESP_ERR_ESPNOW_NOT_INIT
- ESP_ERR_ESPNOW_ARG
- ESP_ERR_ESPNOW_NO_MEM
- ESP_ERR_ESPNOW_FULL
- ESP_ERR_ESPNOW_NOT_FOUND
- ESP_ERR_ESPNOW_INTERNAL
- ESP_ERR_ESPNOW_EXIST
- ESP_ERR_ESPNOW_IF
```

**Purpose**: Connectionless WiFi communication protocol.

### 3.5 ESP Mesh
```
Error Codes:
- ESP_ERR_MESH_WIFI_NOT_START
- ESP_ERR_MESH_NOT_INIT
- ESP_ERR_MESH_NOT_CONFIG
- ESP_ERR_MESH_NOT_START
- ESP_ERR_MESH_NOT_SUPPORT
- ESP_ERR_MESH_NOT_ALLOWED
- ESP_ERR_MESH_NO_MEMORY
- ESP_ERR_MESH_ARGUMENT
- ESP_ERR_MESH_EXCEED_MTU
- ESP_ERR_MESH_TIMEOUT
- ESP_ERR_MESH_DISCONNECTED
- ESP_ERR_MESH_QUEUE_FAIL
- ESP_ERR_MESH_QUEUE_FULL
- ESP_ERR_MESH_NO_PARENT_FOUND
- ESP_ERR_MESH_NO_ROUTE_FOUND
- ESP_ERR_MESH_OPTION_NULL
- ESP_ERR_MESH_OPTION_UNKNOWN
- ESP_ERR_MESH_XON_NO_WINDOW
- ESP_ERR_MESH_INTERFACE
- ESP_ERR_MESH_DISCARD_DUPLICATE
- ESP_ERR_MESH_DISCARD
- ESP_ERR_MESH_VOTING
```

**Purpose**: WiFi mesh networking (may not be actively used).

---

## 4. Bluetooth Components

### 4.1 Bluetooth Controller
```
Location: /home/zht/esp/idf/components/bt/controller/
```

**Purpose**: Low-level Bluetooth controller driver.

### 4.2 Bluedroid Stack
```
Location: /home/zht/esp/idf/components/bt/host/bluedroid/

Components Found:
- btc/              - Bluetooth Common layer
- bta/              - Bluetooth Application layer
- stack/            - Bluetooth stack
- api/              - API layer
- hci/              - Host Controller Interface
```

**Purpose**: Full Bluetooth Classic and BLE stack.

**Features**:
- Bluetooth Classic (SPP, A2DP, AVRCP)
- Bluetooth Low Energy (BLE)
- GATT server/client
- GAP (Generic Access Profile)

### 4.3 BLE Mesh
```
Location: /home/zht/esp/idf/components/bt/esp_ble_mesh/

Components:
- mesh_core/        - Core mesh functionality
- mesh_server/      - Mesh server models
```

**Purpose**: BLE Mesh networking support.

### 4.4 Bluetooth OSI (Operating System Interface)
```
Location: /home/zht/esp/idf/components/bt/common/osi/

Components:
- list.c            - Linked list implementation
- hash_map.c        - Hash map data structure
- fixed_queue.c     - Fixed-size queue
- config.c          - Configuration management
- alarm.c           - Alarm/timer functionality
- thread.c          - Thread management
- mutex.c           - Mutex implementation
- future.c          - Future/promise pattern
```

**Purpose**: OS abstraction layer for Bluetooth stack.

### 4.5 Bluetooth Audio (A2DP)
```
References:
- "Advanced Audio"
- "Advanced Audio Sink"
- "EMO_SPEAKER_%02X%02X"
```

**Purpose**: Bluetooth speaker functionality using A2DP profile.

---

## 5. Security & Encryption

### 5.1 mbedTLS
```
Error Codes:
- ESP_ERR_MBEDTLS_CERT_PARTLY_OK
- ESP_ERR_MBEDTLS_CTR_DRBG_SEED_FAILED
- ESP_ERR_MBEDTLS_SSL_SET_HOSTNAME_FAILED
- ESP_ERR_MBEDTLS_SSL_CONFIG_DEFAULTS_FAILED
- ESP_ERR_MBEDTLS_SSL_CONF_ALPN_PROTOCOLS_FAILED
- ESP_ERR_MBEDTLS_X509_CRT_PARSE_FAILED
- ESP_ERR_MBEDTLS_SSL_CONF_OWN_CERT_FAILED
- ESP_ERR_MBEDTLS_SSL_SETUP_FAILED
- ESP_ERR_MBEDTLS_SSL_WRITE_FAILED
- ESP_ERR_MBEDTLS_PK_PARSE_KEY_FAILED
- ESP_ERR_MBEDTLS_SSL_HANDSHAKE_FAILED
- ESP_ERR_MBEDTLS_SSL_CONF_PSK_FAILED
```

**Purpose**: TLS/SSL encryption library for secure communications.

**Features**:
- TLS 1.2 support
- X.509 certificate handling
- RSA, ECC cryptography
- AES encryption
- SHA hashing

### 5.2 ESP-TLS
```
Error Codes:
- ESP_ERR_ESP_TLS_CANNOT_RESOLVE_HOSTNAME
- ESP_ERR_ESP_TLS_CANNOT_CREATE_SOCKET
- ESP_ERR_ESP_TLS_UNSUPPORTED_PROTOCOL_FAMILY
- ESP_ERR_ESP_TLS_FAILED_CONNECT_TO_HOST
- ESP_ERR_ESP_TLS_SOCKET_SETOPT_FAILED
- ESP_ERR_ESP_TLS_CONNECTION_TIMEOUT
```

**Purpose**: ESP-IDF wrapper for mbedTLS.

### 5.3 WPA Supplicant
```
Location: /home/zht/esp/idf/components/wpa_supplicant/
```

**Purpose**: WiFi security (WPA/WPA2) implementation.

---

## 6. HTTP & Web Components

### 6.1 HTTP Client
```
Error Codes:
- ESP_ERR_HTTP_MAX_REDIRECT
- ESP_ERR_HTTP_CONNECT
- ESP_ERR_HTTP_WRITE_DATA
- ESP_ERR_HTTP_FETCH_HEADER
- ESP_ERR_HTTP_INVALID_TRANSPORT
- ESP_ERR_HTTP_CONNECTING
- ESP_ERR_HTTP_EAGAIN
```

**HTTP Requests Found**:
```c
"GET /emo/ota/version HTTP/1.1\r\nHost: %s\r\n"
"GET /emo/ota/res/%d HTTP/1.1\r\nHost: %s\r\n"
"GET /emo/ota/allres/%d HTTP/1.1\r\nHost: %s\r\n"
"GET /emo/ota/version?type=%d&version_num=%d HTTP/1.1"
"GET /emo/permission HTTP/1.1\r\nHost: %s\r\n"
"POST /emo/ai/draw/txttoimg?%s HTTP/1.1"
```

**Purpose**: HTTP client for OTA updates and API communication.

### 6.2 HTTP Server (HTTPD)
```
Error Codes:
- ESP_ERR_HTTPD_HANDLERS_FULL
- ESP_ERR_HTTPD_HANDLER_EXISTS
- ESP_ERR_HTTPD_INVALID_REQ
- ESP_ERR_HTTPD_RESULT_TRUNC
- ESP_ERR_HTTPD_RESP_HDR
- ESP_ERR_HTTPD_RESP_SEND
- ESP_ERR_HTTPD_ALLOC_MEM
- ESP_ERR_HTTPD_TASK
```

**Purpose**: HTTP server for web interface (if used).

### 6.3 HTTPS OTA
```
Error Codes:
- ESP_ERR_HTTPS_OTA_IN_PROGRESS
```

**Purpose**: Secure OTA updates over HTTPS.

---

## 7. OTA (Over-The-Air Update) System

### 7.1 ESP OTA Component
```
Location: /home/zht/esp/idf/components/app_update/

Functions Found:
- esp_ota_ops
- esp_ota_get_next_update_partition()
- esp_ota_get_running_partition()
- esp_ota_write()
- get_ota_partition_count()
- esp_ota_init()
```

**Error Codes**:
- `ESP_ERR_OTA_PARTITION_CONFLICT`
- `ESP_ERR_OTA_SELECT_INFO_INVALID`
- `ESP_ERR_OTA_VALIDATE_FAILED`
- `ESP_ERR_OTA_SMALL_SEC_VER`
- `ESP_ERR_OTA_ROLLBACK_FAILED`
- `ESP_ERR_OTA_ROLLBACK_INVALID_STATE`

**OTA Strings Found**:
```
"OTA_F"                    - OTA flag
"OTA_E"                    - OTA end
"OTA_start"                - OTA start
"OTA TEST FINISH !!!"      - OTA test complete
"get ota err = %d"         - OTA error
">>> OTA SUCCESS <<<"      - OTA success
"OTA fail ERR CEDE is %d"  - OTA failure
"get in ota"               - Enter OTA mode
"USE_OTA_SERVER"           - OTA server flag
```

**Purpose**: Firmware update over WiFi.

---

## 8. Audio Framework

### 8.1 ESP Audio ADF (Audio Development Framework)
```
Paths Found:
/workshop/audio/esp-audio-app/components/

Components:
- players/              - Audio player implementations
- esp_audio/            - ESP Audio core
- audio_stream/         - Audio streaming
- audio_pipeline/       - Audio pipeline
```

**Key Strings**:
```
"ESP_AUDIO"                    - ESP Audio framework
"AUDIO_STREAM"                 - Audio stream component
"I2S_STREAM"                   - I2S audio stream
"I2S_WRITER"                   - I2S output
"I2S_READER"                   - I2S input
"CreateI2sStreamReader"        - Create I2S reader
"CreateI2sStreamWriter"        - Create I2S writer
"AudioStreamI2sGet"            - Get I2S stream
```

**Error Codes**:
```
"AUDIO_ERR_UNKNOWN"
"CODEC"
"STREAM_I2S_READ_ERROR"
"STREAM_I2S_WRITE_ERROR"
"SOFTCODEC_INTI_ERROR"
"SOFTCODEC_ENCODE_DECODE_ERROR"
"PLAYER_NO_AUDIO_AVAILABLE"
```

**Purpose**: Complete audio framework for playback, recording, and processing.

### 8.2 Audio Functions
```
Functions:
- mediaSetVolumeByCtrl()
- mediaGetVolumeByCtrl()
- mediaCtrlQueryCodecLibByCtrl()
- audioAddUriByCtrl()
- addCodecLibByCtrl()
- mediaStopToneByCtrl()
- mediaSamplingSetup()
- setAudioDownloaderParam()
```

---

## 9. JSON Parsing

### 9.1 cJSON Library
```
References:
- "cjson_hooks==NULL!!!"
- "json_deal"
- "deal_ble_json_task"
- "application/json"
- "esp32_read_k210_json_file_to_buf"
```

**Purpose**: JSON parsing and generation for API communication and configuration.

**Usage**:
- Parsing server responses
- Configuration file reading
- BLE data exchange
- Profile management

---

## 10. Driver Components

### 10.1 SPI Flash
```
Location: /home/zht/esp/idf/components/spi_flash/

Components:
- partition.c          - Partition management
- cache_utils.c        - Cache utilities
- flash_ops.c          - Flash operations
```

**Error Codes**:
- `ESP_ERR_FLASH_OP_FAIL`
- `ESP_ERR_FLASH_OP_TIMEOUT`
- `ESP_ERR_FLASH_NOT_INITIALISED`
- `ESP_ERR_FLASH_UNSUPPORTED_HOST`
- `ESP_ERR_FLASH_UNSUPPORTED_CHIP`
- `ESP_ERR_FLASH_PROTECTED`

### 10.2 GPIO Driver
```
Location: /home/zht/esp/idf/components/driver/gpio.c

Functions:
- gpio_config()
- gpio_set_level()
- gpio_get_level()
- gpio_set_pull_mode()
- gpio_intr_disable()
```

### 10.3 UART Driver
```
Location: /home/zht/esp/idf/components/driver/uart.c
```

### 10.4 SPI Driver
```
Location: /home/zht/esp/idf/components/driver/spi_common.c
```

### 10.5 I2S Driver
```
Functions:
- i2s_read()
- i2s_write()
- i2s_set_sample_rates()
- i2s_driver_install()
```

**Purpose**: Audio input/output via I2S interface.

### 10.6 Touch Sensor Driver
```
Location: /home/zht/esp/idf/components/driver/rtc_module.c

Functions:
- touch_pad_init()
- touch_pad_config()
- touch_pad_read()
- touch_pad_read_filtered()
- touch_pad_filter_start()
- touch_pad_set_voltage()
- touch_pad_set_thresh()
- touch_pad_set_fsm_mode()
- touch_pad_set_trigger_mode()
- touch_pad_set_group_mask()
- touch_pad_clear_group_mask()
```

### 10.7 DAC Driver
```
Functions:
- dac_output_enable()
- dac_output_disable()
- dac_pad_get_io_num()
```

**Purpose**: Digital-to-Analog conversion for audio output.

---

## 11. System Components

### 11.1 Heap Memory Management
```
Location: /home/zht/esp/idf/components/heap/

Components:
- heap_caps_init.c     - Heap capabilities initialization
- heap_caps.c          - Heap capabilities API
```

**Purpose**: Dynamic memory allocation with capability-based allocation.

### 11.2 Bootloader Support
```
Location: /home/zht/esp/idf/components/bootloader_support/
```

**Purpose**: Bootloader utilities and partition management.

### 11.3 SoC (System on Chip)
```
Location: /home/zht/esp/idf/components/soc/

Components:
- esp32/rtc_time.c     - RTC time management
- src/memory_layout.c  - Memory layout configuration
```

### 11.4 eFuse
```
Location: /home/zht/esp/idf/components/efuse/

Error Codes:
- ESP_ERR_EFUSE
- ESP_OK_EFUSE_CNT
- ESP_ERR_EFUSE_CNT_IS_FULL
- ESP_ERR_EFUSE_REPEATED_PROG
```

**Purpose**: One-time programmable memory for device configuration.

### 11.5 Newlib
```
Location: /home/zht/esp/idf/components/newlib/

Components:
- locks.c              - Thread-safe locks for newlib
```

**Purpose**: Standard C library implementation.

### 11.6 Pthread
```
Location: /home/zht/esp/idf/components/pthread/

Components:
- pthread.c            - POSIX threads implementation
- pthread_local_storage.c - Thread-local storage
```

**Purpose**: POSIX threads API on top of FreeRTOS.

### 11.7 ESP ADC Calibration
```
Location: /home/zht/esp/idf/components/esp_adc_cal/
```

**Purpose**: ADC calibration for accurate analog readings.

### 11.8 ESP Ringbuf
```
Location: /home/zht/esp/idf/components/esp_ringbuf/
```

**Purpose**: Ring buffer implementation for data streaming.

---

## 12. Additional Libraries

### 12.1 ULP (Ultra Low Power) Coprocessor
```
Error Codes:
- ESP_ERR_ULP_SIZE_TOO_BIG
- ESP_ERR_ULP_INVALID_LOAD_ADDR
- ESP_ERR_ULP_DUPLICATE_LABEL
- ESP_ERR_ULP_UNDEFINED_LABEL
- ESP_ERR_ULP_BRANCH_OUT_OF_RANGE
```

**Purpose**: Ultra-low-power coprocessor for sensor reading during deep sleep.

### 12.2 Ping
```
Error Codes:
- ESP_ERR_PING_INVALID_PARAMS
- ESP_ERR_PING_NO_MEM
```

**Purpose**: ICMP ping utility.

### 12.3 Image Processing
```
Error Codes:
- ESP_ERR_IMAGE_FLASH_FAIL
- ESP_ERR_IMAGE_INVALID
```

**Purpose**: Image validation and processing.

### 12.4 Coding
```
Error Code:
- ESP_ERR_CODING
```

**Purpose**: Data encoding/decoding utilities.

---

## 13. Custom/Third-Party Components

### 13.1 K210 Integration
```
References:
- "k210 ota error, download this file again"
- "esp32_read_k210_json_file_to_buf"
```

**Purpose**: Integration with Kendryte K210 AI chip (likely for face recognition).

### 13.2 Profile Management
```
File: /spiffs/json/profile.json
```

**Purpose**: User profile and configuration management.

---

## 14. Development Tools & Paths

### Development Environment
```
Base Path: /home/zht/esp/idf/
Developer: zht
Project Path: /home/zht/zht/master/esp-alexa/
Audio Path: /workshop/audio/esp-audio-app/
```

### Project Name
The internal project name appears to be **"esp-alexa"**, suggesting the firmware may have been based on or inspired by Alexa integration code.

---

## 15. Library Version Summary

| Library/Framework | Version Estimate | Purpose |
|------------------|------------------|---------|
| ESP-IDF | v3.3 - v4.0 | Core framework |
| FreeRTOS | v10.x | RTOS |
| LwIP | v2.x | TCP/IP stack |
| mbedTLS | v2.16+ | TLS/SSL |
| Bluedroid | ESP32 version | Bluetooth stack |
| ESP Audio ADF | v1.x - v2.x | Audio framework |
| cJSON | Latest | JSON parsing |
| SPIFFS | ESP-IDF version | File system |

---

## 16. Key Dependencies Graph

```
EMO Firmware
├── ESP-IDF (Core Framework)
│   ├── FreeRTOS (RTOS)
│   ├── LwIP (TCP/IP)
│   ├── mbedTLS (Security)
│   ├── WiFi Stack
│   ├── Bluetooth Stack (Bluedroid)
│   │   ├── BLE
│   │   ├── Classic Bluetooth
│   │   └── A2DP (Audio)
│   ├── Drivers
│   │   ├── GPIO
│   │   ├── I2S
│   │   ├── SPI
│   │   ├── UART
│   │   ├── Touch Sensor
│   │   └── DAC
│   └── Storage
│       ├── NVS
│       ├── SPIFFS
│       └── SPI Flash
├── ESP Audio ADF
│   ├── Audio Pipeline
│   ├── I2S Stream
│   ├── Codec Support
│   └── Audio Player
├── cJSON (JSON Parser)
├── HTTP Client
├── OTA System
└── Custom Components
    ├── K210 Integration
    ├── Face Recognition
    ├── Servo Control
    └── Animation Engine
```

---

## 17. Compilation & Build System

### Build System
- **CMake** (ESP-IDF v4.x) or **Make** (ESP-IDF v3.x)
- Component-based build system
- Kconfig for configuration

### Configuration Files
- `sdkconfig` - Main configuration
- `CMakeLists.txt` - Build configuration
- Component-specific configs

---

## 18. Notable Features Enabled

Based on error codes and function references:

✅ **WiFi**
- Station mode
- AP mode  
- WiFi scanning
- Power save modes

✅ **Bluetooth**
- BLE
- Classic Bluetooth
- A2DP (Audio streaming)
- BLE Mesh (available but may not be used)

✅ **Security**
- TLS/SSL (mbedTLS)
- WPA/WPA2
- Secure boot (eFuse)
- Flash encryption (possible)

✅ **Storage**
- NVS (configuration)
- SPIFFS (files)
- OTA partitions

✅ **Audio**
- I2S input (microphone)
- I2S output (speaker)
- DAC output
- Audio framework (ADF)
- Bluetooth audio (A2DP)

✅ **Networking**
- HTTP/HTTPS client
- OTA updates
- JSON API communication
- TCP/UDP sockets

✅ **Sensors**
- Touch sensors (10 pads)
- GPIO
- ADC
- IMU (external, via I2C/SPI)

---

## 19. Licensing Considerations

### Open Source Components
- **ESP-IDF**: Apache License 2.0
- **FreeRTOS**: MIT License
- **LwIP**: BSD License
- **mbedTLS**: Apache License 2.0
- **cJSON**: MIT License

### Proprietary Components
- **ESP Audio ADF**: Espressif proprietary (requires license)
- **Bluedroid**: Apache License 2.0 (with some proprietary parts)

---

## 20. Recommendations for Reimplementation

### Must-Have Libraries
1. **ESP-IDF** (latest stable version)
2. **FreeRTOS** (included in ESP-IDF)
3. **ESP Audio ADF** (for audio features)
4. **cJSON** (for JSON parsing)
5. **mbedTLS** (for security)

### Optional Libraries
1. **ESP-NOW** (if peer-to-peer communication needed)
2. **BLE Mesh** (if mesh networking needed)
3. **HTTP Server** (if web interface needed)

### Development Setup
```bash
# Install ESP-IDF
git clone --recursive https://github.com/espressif/esp-idf.git
cd esp-idf
./install.sh

# Install ESP-ADF
git clone --recursive https://github.com/espressif/esp-adf.git
export ADF_PATH=$PWD/esp-adf

# Set up environment
. $HOME/esp/esp-idf/export.sh
```

---

## Conclusion

The EMO firmware is built on a solid foundation of industry-standard libraries and frameworks:

- **Core**: ESP-IDF with FreeRTOS
- **Networking**: LwIP, WiFi, Bluetooth (Bluedroid)
- **Security**: mbedTLS, WPA Supplicant
- **Audio**: ESP Audio ADF with I2S
- **Storage**: NVS, SPIFFS
- **Parsing**: cJSON
- **Updates**: OTA system

All major components are well-documented and actively maintained by Espressif, making reimplementation straightforward with proper licensing and attribution.
