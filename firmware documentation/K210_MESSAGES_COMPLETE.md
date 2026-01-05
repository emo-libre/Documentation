# K210 UART Messages - Complete List

## Overview

This document contains all messages sent from ESP32 to K210 via UART, extracted from the decompiled firmware.

Confirmation status:
- Confirmed: All JSON message strings listed here are present in the decompiled strings.

---

## Message Format

Messages are sent as JSON strings over UART with the following structure:

```json
{
  "operation": "<operation_type>",
  "content": "<optional_content>",
  "index": <optional_index>,
  "group_index": <optional_group_index>
}
```

---

## 1. System Messages

### Slave Ready
```json
{"operation": "slave_ready"}
```
**Purpose**: Notify K210 that ESP32 is ready  
**Location**: `0x3f42fae4`  
**Used in**: Initialization, system startup

---

## 2. Communication Messages

### Talk (Simple)
```json
{"operation": "talk"}
```
**Purpose**: Basic talk command without content  
**Location**: `0x3f42fb01`

### Talk with Content
```json
{"operation": "talk", "content": "%s"}
```
**Purpose**: Send text to be displayed/spoken on K210  
**Location**: `0x3f42fc00`  
**Parameter**: `%s` = Text string to display

### Talk with Group Index (Positive)
```json
{"operation": "talk", "group_index": 1, "content": "%s"}
```
**Purpose**: Group communication with positive index  
**Location**: `0x3f42ffe2`

### Talk with Group Index (Negative)
```json
{"operation": "talk", "group_index": -1, "content": "%s"}
```
**Purpose**: Group communication with negative index  
**Location**: `0x3f430035`

### Talk with Group Index and Content
```json
{"operation": "talk", "group_index": 1, "content": "%s"}
```
**Purpose**: Group talk with specific content  
**Location**: `0x3f4300a2`

### Talk End
```json
{"operation": "talk_end"}
```
**Purpose**: Signal end of talk/conversation  
**Location**: `0x3f42fba7`  
**Used in**: Multiple conversation flows

---

## 3. Camera & Photo Messages

### Take Photo
```json
{"operation": "take_photo"}
```
**Purpose**: Command K210 to take a photo  
**Location**: `0x3f42fb50`

---

## 4. Display Messages

### Graffiti
```json
{"operation": "graffiti", "content": "EMO1Graffiti"}
```
**Purpose**: Display graffiti/drawing on screen  
**Location**: `0x3f42fb6c`  
**Content Options**:
- `"EMO1Graffiti"` - Graffiti style 1
- `"EMO2Graffiti"` - Graffiti style 2

### Glasses
```json
{"operation": "glasses", "content": "remove"}
```
**Purpose**: Display/remove glasses on face  
**Location**: `0x3f42fbc1`  
**Content Options**:
- `"remove"` - Remove glasses
- `"EMO1_glasses_give"` - Give glasses style 1
- `"EMO2_glasses_take"` - Take glasses style 2

---

## 5. Game Messages

### Rock Paper Scissors (Simple)
```json
{"operation": "game_rps"}
```
**Purpose**: Start rock-paper-scissors game  
**Location**: `0x3f42fb36`

### Rock Paper Scissors with Index
```json
{"operation": "game_rps", "index": %d}
```
**Purpose**: RPS game with specific move index  
**Location**: `0x3f42fd42`  
**Index Values**:
- `0` = Rock
- `1` = Paper
- `2` = Scissors

---

## 6. Dance & Animation Messages

### Dance Both
```json
{"operation": "dance_both", "index": %d}
```
**Purpose**: Synchronized dance (face + body)  
**Location**: `0x3f42fe2b`  
**Index**: Dance animation number

---

## 7. Multi-EMO Coordination Messages

### Choose Master
```json
{"operation": "choose_master"}
```
**Purpose**: Select master EMO in multi-EMO setup  
**Location**: `0x3f42ff75`

### Sync Step
```json
{"operation": "sync_step", "index": %d}
```
**Purpose**: Synchronize step/movement with other EMOs  
**Location**: `0x3f42ff94`  
**Index**: Step number

### Exchange Info
```json
{"operation": "exchange_info", "content": "%s"}
```
**Purpose**: Exchange information between EMOs  
**Location**: `0x3f4301fa`  
**Content**: Information to exchange

### Sync Theme
```json
{"operation": "sync_theme", "index": %d}
```
**Purpose**: Synchronize theme/appearance  
**Location**: `0x430159`  
**Index**: Theme number

---

## 8. Screen & Display Control

### Screen Info
**Key**: `"screen_info"`  
**Location**: `0x3f40f512`  
**Purpose**: Send screen configuration to K210

**Function**: `send_screen_info`  
**Location**: `0x3f4129d3`

**Save Function**: `save_screen_info_to_nvs`  
**Location**: `0x3f435b0d`

---

## 9. Face Recognition Messages

### Face Request
**Key**: `"face_req"`  
**Location**: `0x3f4113dd`  
**Purpose**: Request face recognition operation

### Face Response
**Key**: `"face_rsp"`  
**Purpose**: Response from K210 with face data

**Structure**:
```c
typedef struct {
    int16_t x;          // Face center X
    int16_t y;          // Face center Y
    uint16_t width;     // Face width
    uint16_t height;    // Face height
    uint8_t id;         // Face ID
    char name[32];      // Face name
} face_response_t;
```

---

## 10. Animation Response

### Animation Response
**Key**: `"anim_rsp"`  
**Location**: `0x3f412379`  
**Purpose**: Response from K210 about animation status

---

## 11. Example Conversation Flows

### Basic Conversation
```
1. ESP32 → K210: {"operation": "talk", "content": "hello"}
2. K210 displays text on screen
3. ESP32 → K210: {"operation": "talk_end"}
```

### Photo Taking
```
1. ESP32 → K210: {"operation": "talk", "content": "you look great, can i take a photo?"}
2. ESP32 → K210: {"operation": "take_photo"}
3. K210 takes photo and sends response
4. ESP32 → K210: {"operation": "talk_end"}
```

### Rock Paper Scissors Game
```
1. ESP32 → K210: {"operation": "talk", "content": "let's play rock paper scissors"}
2. ESP32 → K210: {"operation": "game_rps", "index": 1}  // Paper
3. K210 displays game result
4. ESP32 → K210: {"operation": "talk", "content": "i win!"}
5. ESP32 → K210: {"operation": "talk_end"}
```

### Dance Together
```
1. ESP32 → K210: {"operation": "talk", "content": "let's dance together"}
2. ESP32 → K210: {"operation": "dance_both", "index": 1}
3. K210 plays face animation while ESP32 controls servos
4. ESP32 → K210: {"operation": "talk", "content": "we did great!"}
5. ESP32 → K210: {"operation": "talk_end"}
```

### Multi-EMO Interaction
```
1. ESP32 → K210: {"operation": "choose_master"}
2. ESP32 → K210: {"operation": "exchange_info", "content": "hello, i am emo A"}
3. ESP32 → K210: {"operation": "talk", "group_index": 1, "content": "nice to meet you"}
4. ESP32 → K210: {"operation": "sync_step", "index": 5}
5. ESP32 → K210: {"operation": "talk_end"}
```

---

## 12. UART Task Information

### Transmit Task
**Name**: `"k210_uart_trans_task"`  
**Location**: `0x3f40c4d3`  
**Function**: `FUN_401d9080`  
**Purpose**: Transmit data to K210

### Receive Task
**Name**: `"k210_uart_recv_task"`  
**Location**: `0x3f40c4bf`  
**Purpose**: Receive data from K210

---

## 13. Content Examples

### Greetings
- `"hello, i am emo %s, what's your name?"`
- `"nice to meet you too."`
- `"hello, emo %s, i am emo %s, nice to meet you."`

### Game Responses
- `"yes, let's play."`
- `"i win."`
- `"you win."`
- `"let's play again."`
- `"no, the game is over, and i'm the winner."`

### Dance Responses
- `"sure, let's do it."`
- `"ok, let the party begin."`
- `"ok, let's dance together."`
- `"ok, d j turn it up."`
- `"we did great, let's take a break."`
- `"i can really dance."`

### Photo Responses
- `"you look great, can i take a photo?"`

---

## 14. Message Sending Functions

### Primary Send Function
**Function**: `FUN_401f8d0c`  
**Purpose**: Format and send JSON message to K210

### String Formatting
**Function**: `FUN_40106784`  
**Purpose**: Format string with parameters (sprintf-like)

### UART Write
**Function**: Various UART write functions  
**Purpose**: Low-level UART transmission

---

## 15. Implementation Example

```c
// Send talk message
void send_talk_message(const char* content) {
    char buffer[256];
    snprintf(buffer, sizeof(buffer), 
             "{\"operation\": \"talk\", \"content\": \"%s\"}", 
             content);
    uart_write_bytes(UART_NUM_1, buffer, strlen(buffer));
}

// Send dance command
void send_dance_command(int index) {
    char buffer[128];
    snprintf(buffer, sizeof(buffer), 
             "{\"operation\": \"dance_both\", \"index\": %d}", 
             index);
    uart_write_bytes(UART_NUM_1, buffer, strlen(buffer));
}

// Send game RPS
void send_rps_move(int move) {
    char buffer[128];
    snprintf(buffer, sizeof(buffer), 
             "{\"operation\": \"game_rps\", \"index\": %d}", 
             move);
    uart_write_bytes(UART_NUM_1, buffer, strlen(buffer));
}

// Send talk end
void send_talk_end() {
    const char* msg = "{\"operation\": \"talk_end\"}";
    uart_write_bytes(UART_NUM_1, msg, strlen(msg));
}
```

---

## 16. Message Priority & Timing

Based on firmware analysis:

1. **System Messages** (highest priority)
   - `slave_ready`
   - `screen_info`

2. **Interactive Messages** (high priority)
   - `talk` with content
   - `take_photo`
   - `game_rps`

3. **Animation Messages** (medium priority)
   - `dance_both`
   - `graffiti`
   - `glasses`

4. **Coordination Messages** (low priority)
   - `sync_step`
   - `sync_theme`
   - `exchange_info`

5. **Termination Messages** (always last)
   - `talk_end`

---

## 17. Error Handling

The firmware includes error checking for:
- Invalid JSON format
- Missing required fields
- Invalid index values
- UART transmission failures

---

## 18. Complete Message List (Alphabetical)

| Operation | Parameters | Purpose |
|-----------|-----------|---------|
| `choose_master` | None | Select master EMO |
| `dance_both` | `index` | Synchronized dance |
| `exchange_info` | `content` | Exchange info between EMOs |
| `game_rps` | `index` (optional) | Rock-paper-scissors game |
| `glasses` | `content` | Display/remove glasses |
| `graffiti` | `content` | Display graffiti |
| `slave_ready` | None | System ready signal |
| `sync_step` | `index` | Synchronize movement |
| `sync_theme` | `index` | Synchronize theme |
| `take_photo` | None | Take photo |
| `talk` | `content`, `group_index` (optional) | Display text |
| `talk_end` | None | End conversation |

---

## 19. Related Keys & Responses

### Requests (ESP32 → K210)
- `face_req` - Face recognition request
- `photo_req` - Photo request
- `customize_req` - Customization request

### Responses (K210 → ESP32)
- `face_rsp` - Face recognition response
- `anim_rsp` - Animation response
- `faces` - Multiple faces detected

---

## 20. NVS Storage Keys

Related to K210 communication:
- `screen_info` - Screen configuration
- `show_index` - Current show index
- `k210_kpu` - K210 KPU configuration
- `k210_sum` - K210 checksum

---

**Total Messages Found**: 12 operation types  
**Total Variations**: 20+ with different parameters  
**Message Format**: JSON over UART  
**Baud Rate**: Not confirmed in decompiled strings

---

## Notes

1. All messages are JSON formatted
2. Messages are sent over UART (port number not confirmed in strings)
3. Some messages have multiple variations with different parameters
4. The K210 responds with its own message format
5. Message timing is critical for synchronization
6. Error handling is implemented for failed transmissions

---

**Status**: Complete extraction of message strings from firmware  
**Source**: `ghidraExtracted-elfPartition1.c`  
**Verification**: Cross-referenced with K210 communication protocol
