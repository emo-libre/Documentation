# K210 Protocol

How the ESP32 talks to the K210 AI chip, which drives the camera and the screen. For what each chip does, see the [hardware split](README.md#hardware-split-esp32-and-k210).

Source: `ghidraExtracted-elfPartition1.c`. See the [evidence legend](README.md#evidence-legend).

---

## UART link

### Tasks (Confirmed)

| Task | String address | Function | Purpose |
| --- | --- | --- | --- |
| `k210_uart_recv_task` | `0x3f40c4bf` | `FUN_401d8768` | ESP32 receives from K210 |
| `k210_uart_trans_task` | `0x3f40c4d3` | `FUN_401d9080` | ESP32 transmits to K210 |

### Buffer limits (Confirmed)

```c
"uart rx buffer length error(>128)"       // 0x3f4254b0
"uart tx buffer length error(>128 or 0)"  // 0x3f4254d2
```

These error strings suggest a 128-byte limit per packet. A 3072-byte driver buffer size was mentioned in earlier notes, but it isn't backed by any string (**Inferred**).

### Not confirmed

UART port number, TX/RX GPIO pins, baud rate, data bits, parity, stop bits and flow control aren't in the readable strings. They need to be read from board schematics, probed on hardware, or found in the `uart_param_config` / `uart_set_pin` calls. See [Unconfirmed: example configuration](#unconfirmed-example-configuration).

### Packet framing (Inferred)

The command codes below and the `k210_sum` NVS key suggest a binary frame around the payload, roughly:

```c
typedef struct {
    uint8_t  header;      // 0xAA or similar
    uint8_t  command;     // 0x02, 0x03, 0x12, 0x13, ...
    uint16_t length;      // payload length
    uint8_t  payload[];   // JSON or binary data
    uint8_t  checksum;
} k210_message_t;
```

Related strings (Confirmed): `"small pack error\r"` (`0x3f426c96`) and `"got SMALL_PACK_ACK!!!!!!!!!!\r"` (`0x3f426ce2`).

---

## JSON operations (ESP32 → K210)

All of these JSON strings are in the binary (**Confirmed**). Messages have this shape:

```json
{
  "operation": "<operation_type>",
  "content": "<optional_content>",
  "index": <optional_index>,
  "group_index": <optional_group_index>
}
```

### Summary

| Operation | Parameters | Purpose |
| --- | --- | --- |
| `slave_ready` | none | ESP32 is ready (startup) |
| `talk` | `content`, `group_index` (optional) | Text to display/speak |
| `talk_end` | none | End of a conversation |
| `take_photo` | none | Take a photo |
| `graffiti` | `content` | Show a drawing |
| `glasses` | `content` | Put on/remove glasses |
| `game_rps` | `index` (optional) | Rock-paper-scissors |
| `dance_both` | `index` | Synchronized dance (face + body) |
| `choose_master` | none | Pick the master EMO (multi-EMO) |
| `sync_step` | `index` | Sync movement with other EMOs |
| `exchange_info` | `content` | Exchange info between EMOs |
| `sync_theme` | `index` | Sync theme/appearance |

### Variants and string addresses

| JSON | Address | Notes |
| --- | --- | --- |
| `{"operation": "slave_ready"}` | `0x3f42fae4` | Startup |
| `{"operation": "talk"}` | `0x3f42fb01` | |
| `{"operation": "talk", "content": "%s"}` | `0x3f42fc00` | |
| `{"operation": "talk", "group_index": 1, "content": "%s"}` | `0x3f42ffe2`, `0x3f4300a2` | Group talk |
| `{"operation": "talk", "group_index": -1, "content": "%s"}` | `0x3f430035` | Group talk |
| `{"operation": "talk_end"}` | `0x3f42fba7` | |
| `{"operation": "take_photo"}` | `0x3f42fb50` | |
| `{"operation": "graffiti", "content": "EMO1Graffiti"}` | `0x3f42fb6c` | Also `EMO2Graffiti` |
| `{"operation": "glasses", "content": "remove"}` | `0x3f42fbc1` | Also `EMO1_glasses_give`, `EMO2_glasses_take` |
| `{"operation": "game_rps"}` | `0x3f42fb36` | |
| `{"operation": "game_rps", "index": %d}` | `0x3f42fd42` | 0 = rock, 1 = paper, 2 = scissors (**Inferred**) |
| `{"operation": "dance_both", "index": %d}` | `0x3f42fe2b` | Index = dance number |
| `{"operation": "choose_master"}` | `0x3f42ff75` | |
| `{"operation": "sync_step", "index": %d}` | `0x3f42ff94` | |
| `{"operation": "exchange_info", "content": "%s"}` | `0x3f4301fa` | |
| `{"operation": "sync_theme", "index": %d}` | `0x430159` (as recorded) | |

Send path: `FUN_401f8d0c` formats and sends the JSON, using `FUN_40106784` (sprintf-like).

### Content strings (Confirmed)

- Greetings: `"hello, i am emo %s, what's your name?"`, `"nice to meet you too."`, `"hello, emo %s, i am emo %s, nice to meet you."`
- Games: `"yes, let's play."`, `"i win."`, `"you win."`, `"let's play again."`, `"no, the game is over, and i'm the winner."`
- Dance: `"sure, let's do it."`, `"ok, let the party begin."`, `"ok, let's dance together."`, `"ok, d j turn it up."`, `"we did great, let's take a break."`, `"i can really dance."`
- Photo: `"you look great, can i take a photo?"`
- Idle chat between EMOs: `"S: hey emo %s, i am wandering around."` (`0x3f4302bc`), `"M: hey emo %s, what are you doing?"` (`0x3f430299`)

### Example flows (Inferred ordering)

```
Conversation:   talk{"hello"} → talk_end
Photo:          talk{"you look great, can i take a photo?"} → take_photo → talk_end
RPS:            talk{"let's play rock paper scissors"} → game_rps{index:1} → talk{"i win!"} → talk_end
Dance:          talk{"let's dance together"} → dance_both{index:1} → talk{"we did great!"} → talk_end
                (K210 plays the face animation while the ESP32 drives the servos)
Multi-EMO:      choose_master → exchange_info{"hello, i am emo A"} → talk{group_index:1,…} → sync_step{index:5} → talk_end
```

### Message priority and error handling (Inferred)

Earlier notes ranked the operations like this, with no code evidence:

1. System (highest): `slave_ready`, `screen_info`
2. Interactive: `talk` with content, `take_photo`, `game_rps`
3. Animation: `dance_both`, `graffiti`, `glasses`
4. Coordination (low): `sync_step`, `sync_theme`, `exchange_info`
5. Termination (always last): `talk_end`

They also said the firmware checks for invalid JSON, missing fields, invalid index values and UART transmission failures, and that message timing matters for multi-EMO synchronization.

---

## Other keys and responses

| Key | Direction | Address | Purpose |
| --- | --- | --- | --- |
| `face_req` | ESP32 → K210 | `0x3f4113dd` | Face recognition request |
| `photo_req` | ESP32 → K210 | | Photo request |
| `customize_req` | ESP32 → K210 | | Customization request |
| `face_rsp` | K210 → ESP32 | `0x3f412382` | Face recognition result |
| `faces` | K210 → ESP32 | `0x3f4123f8` | Several faces |
| `anim_rsp` | K210 → ESP32 | `0x3f412379` | Animation status |
| `eye_rsp` | K210 → ESP32 | `0x3f411e12` | Eye response |

### Command codes (Confirmed log strings)

| Code | Log string | Meaning (Inferred) |
| --- | --- | --- |
| `0x02` | `"got face cmd"` | Single face |
| `0x03` | `"got faces cmd"` | Multiple faces |
| `0x12` | `"got face cmd 0x12"` | Face recognition/registration |
| `0x13` | `"got faces cmd 0x13"` | Face query/management |
| | `"got faces end"` | End of face list |

### Object recognition and OTA (Confirmed)

```c
"EMO_SEND_YOLO_CLASS %d, x=%d, y=%d!!!\r\n"   // 0x3f426cba
"SEND_RUN_OTA %d\r\n"                         // 0x3f426ca8
```

---

## Face recognition

### Response layout (Inferred from log strings)

The ESP32 logs these fields from a K210 face result (Confirmed strings, see [Strings and addresses](strings_and_addresses.md#face-coordinate-tracking)):
`coordinate_data1->face.x/.y/.width/.height/.id/.name`, `face_center_x1`, `face_center_y1`.

A plausible struct (types are **Inferred**):

```c
typedef struct {
    int16_t  x;          // face center X
    int16_t  y;          // face center Y
    uint16_t width;      // bounding box width
    uint16_t height;     // bounding box height
    uint8_t  id;         // face ID
    char     name[32];   // face name
} face_response_t;
```

A JSON form like `{"face_rsp": {"x":120,"y":80,"width":60,"height":80,"id":1,"name":"John"}}` and a `face_req` with `"command": "register|query|delete"` have been suggested, but the exact JSON field names are **Inferred**. The full examples from earlier notes (all **Inferred**):

```json
{"face_req": {"command": "register|query|delete", "face_id": 0, "name": "John"}}

{"faces": [
  {"id": 1, "name": "John", "x": 120, "y": 80},
  {"id": 2, "name": "Jane", "x": 200, "y": 90}
]}

{"anim_rsp": {"type": "face_animation", "file": "/test/animation_name.avi", "loop": true, "duration": 1000}}
```

### Flows

```
Register: ESP32 → K210 register_face
          K210 captures + processes the face → face_rsp with new id
          ESP32 saves NVS "faceinfo_%d" (save_custom_face_info_to_nvs)
          plays /spiffs/avi/reg_face_success.avi

Query:    ESP32 → K210 query_face → face_rsp → ESP32 looks up the name in NVS
          unknown face → doesnt_know_face

Detect:   K210 processes the camera continuously → face_rsp when a face is seen
          ESP32 logs the coordinates and turns towards the face
```

App-side face events: `app_face_in`, `app_face_out`, `app_face_delete`.

---

## Screen info

- NVS key `screen_info` (`0x3f40f512`)
- `send_screen_info` (`0x3f4129d3`), log `"send screen info"`
- `save_screen_info_to_nvs` (`0x3f435b0d`)

---

## K210 firmware update and files

```c
"k210_update_queue failed, %ld"
"k210_update_receive 2047, restart!!!"
"err k210_update_receive = %d"
"k210_update_receive1 = %d"
"k210 ota error, download this file again"

"esp32_read_k210_sdcard_file"
"esp32_read_k210_json_file_to_buf"
"esp32_read_k210_sd_file_to_buf"
```

The K210 OTA file format is documented in [How to decompile](/DecompileFWs.md#k210-ota-file-format).

## NVS keys

| Key | Purpose |
| --- | --- |
| `k210_kpu` | K210 KPU config (`update_k210_kpu_info_to_nvs`) |
| `k210_sum` | K210 checksum |
| `screen_info` | Screen configuration |
| `faceinfo_%d` | Registered face data |
| `show_index` | Current show index |

---

## Unconfirmed: example configuration

None of these values come from the firmware. They're common defaults for testing on hardware.

```c
uart_config_t uart_config = {
    .baud_rate = 115200,                 // unconfirmed (115200 / 921600 are common)
    .data_bits = UART_DATA_8_BITS,
    .parity    = UART_PARITY_DISABLE,
    .stop_bits = UART_STOP_BITS_1,
    .flow_ctrl = UART_HW_FLOWCTRL_DISABLE
};
uart_driver_install(UART_NUM_2, 3072, 3072, 0, NULL, 0);    // port + sizes unconfirmed
uart_param_config(UART_NUM_2, &uart_config);
uart_set_pin(UART_NUM_2, 17 /* TX */, 16 /* RX */,           // pins unconfirmed
             UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
```

Example wiring (unconfirmed):

| ESP32 pin | Function | K210 pin |
| --- | --- | --- |
| GPIO 16 | UART RX | K210 TX |
| GPIO 17 | UART TX | K210 RX |
| GND | Ground | GND |

Both chips use 3.3 V logic, so they can be connected directly without a level shifter.

To sniff the link, connect a USB-serial adapter's RX to the ESP32 TX line (and GND), then try `screen /dev/ttyUSB0 115200` or `minicom -D /dev/ttyUSB0 -b 115200`.

To send a test command from the ESP32 side (port unconfirmed):

```c
const char *command = "test_command\r\n";
uart_write_bytes(UART_NUM_2, command, strlen(command));

uint8_t data[128];
int len = uart_read_bytes(UART_NUM_2, data, sizeof(data), 100 / portTICK_PERIOD_MS);
```

Troubleshooting:
- **No communication**: check that TX→RX and RX→TX are crossed, both sides use the same baud rate, and the K210 is powered and initialized. Look for the buffer length errors above.
- **Garbled data**: try other baud rates (115200 / 921600 are common). Add 4.7 kΩ pull-ups on RX/TX against noise and keep the cables short (<30 cm).
- **Buffer overflows**: increase the driver buffers, e.g. `uart_driver_install(UART_NUM_2, 4096, 4096, 0, NULL, 0);`.
