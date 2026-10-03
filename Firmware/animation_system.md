# Animation System

How EMO plays animations: what triggers them, how face and body playback are combined, and what stops them. For idle and sleep animations, see [Idle behavior](idle_behavior.md). For the per-animation pages from the app's Theater, see [/Animations](/Animations).

Source: `ghidraExtracted-elfPartition1.c`. See the [evidence legend](README.md#evidence-legend).

---

## 1. Two playback paths

| | Face | Body |
| --- | --- | --- |
| Files | `/spiffs/avi/%s.avi` | `/spiffs/mot/%s.mot` (also `/spiffs/mot/%s`) |
| Played by | K210 screen | ESP32 servos |
| Audio | `/spiffs/mp3/%s.mp3` (optional) | |

All three paths are Confirmed strings. Earlier notes claimed that AVI files live in K210 flash as 320x240 MJPEG at 15–30 FPS. The path is in ESP32 SPIFFS, and the video format is **Inferred** (check against the [extracted files](extraction.md)). Earlier notes also gave the MP3 files as 16 kHz or 44.1 kHz at 128 kbps (**Inferred**).

The headphone LEDs are driven by the ESP32 as well, e.g. `blink_light_for_dance`.

### Core functions (Confirmed)

| Name | Address | Notes |
| --- | --- | --- |
| `animation_player_task` | `0x3f417389` | Task; function `FUN_40143218` (label `LAB_40143250` is inside it). Earlier notes recorded stack `0x3FFC8A5C` and priority "High" (not verified) |
| `animation_player` | `0x3f41739f` | Queue and execution |
| `play_animation` | `0x3f40fa57` | Face + body |
| `play_animation_without_servor` | `0x3f43058a` | Face only, no servo movement |

### Face command to the K210 (Confirmed strings)

```json
[0,[["/spiffs/avi/%s.avi",[[0,"/spiffs/mp3/%s.mp3"]]]]]
[0,[["/test/%s.avi",[[0,"/test/%s.mp3"]]]]]
```

Each entry pairs a video with an audio track. How these strings are framed on the UART is covered in [K210 protocol](k210_protocol.md).

### Face playback flow (Inferred)

```
1. Trigger enqueues an animation
2. ESP32 formats the command and sends it over UART (command codes 0x02/0x03/0x12/0x13)
3. K210 (k210_uart_recv_task on the ESP32 side) loads the .avi and plays it
4. K210 reports back (anim_rsp / face_rsp)
```

---

## 2. Motion (`.mot`) playback

### Motion list (Confirmed)

| Function | Address |
| --- | --- |
| `new_motion_node` | `0x3f417476` |
| `add_new_motion_node` | `0x3f41744e` |
| `get_next_motion_node` | `0x3f417424` |
| `has_next_motion_node` | `0x3f417439` |
| `destory_motion_list` | `0x3f417462` |
| `motion_parse_file` | `0x3f41758d` (function `FUN_40143b78`) |
| `motion_struct_get_check_sum` | |
| `"motion_file_data_frame_checksum_error"` | `0x3f417557` |

A `.mot` file is parsed into a **linked list** of frames, each holding the 4 servo positions and a duration. A checksum is verified per frame.

### Playback loop (Inferred)

```c
load("/spiffs/mot/%s.mot");            // FUN_401e02d8
motion_parse_file();                   // + motion_struct_get_check_sum()
while (has_next_motion_node()) {
    node = get_next_motion_node();
    for (servo = 0; servo < 4; servo++)
        mcpwm_set_duty_in_us(servo, node->angles[servo]);
    vTaskDelay(node->duration);
}
destory_motion_list();
```

### `.mot` format (Inferred)

The checksum string is the only Confirmed fact about the format. This layout is the current best guess and needs checking with [`analyze_mot_files.py`](scripts/analyze_mot_files.py):

```
Header (unverified): magic, version, frame count, frame rate, checksum (4 bytes each?)

Frame, 12 bytes:
0x00  2  Servo 0: left leg  (hip)
0x02  2  Servo 1: left foot (ankle)
0x04  2  Servo 2: right leg (hip)
0x06  2  Servo 3: right foot (ankle)
0x08  2  Duration (ms)
0x0A  2  Flags / interpolation type
```

Values are either PWM pulse width (500–2500 µs, 1500 = center, 50 Hz) or angles (0–180°). Earlier notes also described a 12-servo frame. EMO has 4 servos, so that version was dropped.

### Servo control

Confirmed strings show both MCPWM and a servo command/parameter protocol. How the servos are actually driven is still **unresolved**: PWM via MCPWM, a serial servo bus, or both for the "old" and "new" servo types.

- MCPWM: `mcpwm_set_frequency` (`0x3f44ef03`), `mcpwm_set_duty` (`0x3f44eef4`), `mcpwm_set_duty_in_us` (`0x3f44eedf`), `mcpwm_set_duty_type` (`0x3f44eecb`)
- Config: `set_servo_parameter` (`0x3f44bee6`), `set_servo_offset_value` (`0x3f44b90e`, `0x3f44b954`), `SERVO_P_SET_MODE`, `SERVO_P_SET_MODE_2`
- All other servo strings (old/new type, update done/fail, read fail): see [Strings and addresses](strings_and_addresses.md#1-motorservo-control-functions)

---

## 3. Animation names

Names found as strings in the binary. Many map to app animations documented in [/Animations](/Animations).

**Face (`.avi`)**
- Moods: `mood_sad`, `mood_happy`, `mood_angry`, `blink_come_back1`
- Reactions: `image_react_high` (`0x3f42cb3d`), `image_look_up`, `image_search`
- Face recognition: `face_id`, `reg_face_success`, `doesnt_know_face`
- Fitness: `Fit_Talk`, `Fit_Next`, `Fit_Good`, `Fit_Rest`

**Motion (`.mot`)**
- Basic: `basic_move`, `move_1`, `move_2`, `move_3`, `move_4_down`, `move_5_right`, `move_6_left`, `move_7_left_right`, `move_8_left_right`, `move_to_target`
- Turning: `move_turn_left_progress_v01`–`v03`, `move_turn_right_progress_v01`–`v03`, `turn_around`, `turn_right_blink_2`
- Walking: `zombie_loop_walk1`, `zombie_loop_walk2`
- Emotional: `move_forward_upset`, `autistic_end`
- Dance: `d1_EmoDance`, `d2_WontLetGo`, `dance_together`, `dance_start_%d`, `dance_basic_loop_%d`, `dance_basic_onece_%d`, `dance_miss`, `blink_light_for_dance`
- Gestures: `gesture_gun_don't_move_start`, `gesture_gun_don't_move_loop`, `Group_photo_gesture_1`–`6`
- Look around: `look_around_1`, … (see [Idle behavior](idle_behavior.md#3-exploration-behaviors))

**Reactions (triggered, see §4)**
- `shake_loop_1`–`5`, `shake_end_1`–`8`
- `react_put_down_1` (`0x3f42a22f`), `react_put_down_2` (`0x3f42a240`)
- `cliff_react_left_2` (`0x3f42a30f`), `cliff_react_left_3` (`0x3f42a322`), `cliff_react_right_2` (`0x3f42a335`), `cliff_react_right_3` (`0x3f42a349`)
- `react_to_obs_1`–`13`, `react_back_1`–`8`
- `react_look_down_1_1`–`1_4`, `react_look_down_2_1`–`2_4`
- `react_depressed` (`0x3f42a2f4`), `react_to_gesture` (`0x3f42b7ed`)
- `reminder_eat` (`0x3f42b038`), `reminder_sleep` (`0x3f42b045`)

### Naming convention

`<category>_<action>_<variation>`, e.g. `explore_play1`, `react_back_5`, `sleep_loop_2`. Categories: `explore_`, `react_`, `sleep_`, `shake_`, `cliff_`, `free_play_`, `look_around_`, `move_`, `dance_`.

---

## 4. Triggers

The animation names and state strings are Confirmed. Which sensor drives which reaction, and the thresholds, are **Inferred**.

| Trigger | Source | State string | Animations |
| --- | --- | --- | --- |
| Shaking | IMU | `"Shaked"` (`0x3f435d7d`) | random `shake_loop_X` while shaking, then a random `shake_end_X` |
| Put down / picked up | Foot sensors | | `react_put_down_1/2` |
| Cliff edge | ToF / foot sensors | | `cliff_react_left_X` / `cliff_react_right_X` |
| Obstacle | ToF | `"obstacle_detected"` (`0x3f431813`) | `react_to_obs_X` → `react_back_X` → turn away |
| Petting | Head touch | `"Petting"` (`0x3f435d75`) | happy reactions, purring sounds, eye animations |
| Looking down | IMU pitch (`roll = %d, pitch = %d`) | | `react_look_down_X_Y` |
| No interaction for a long time | Timer | | `react_depressed` (threshold unknown; "30 min" is a guess) |
| Face seen | K210 | | turn to face, greeting (see [K210 face flows](k210_protocol.md#flows)) |
| Gesture | K210 | | `react_to_gesture` |
| Object recognized | K210 (YOLO) | | `image_react_high` |
| Reminders | Clock | | `reminder_eat`, `reminder_sleep` |
| Idle / sleep | Timer | | see [Idle behavior](idle_behavior.md) |
| Voice, app, schedule | Cloud intent / app | | see [/Intents](/Intents) and [/Behaviors](/Behaviors) |
| Button press | Physical button | | mode-specific (**Inferred**, no string found) |

### Example sequences (Inferred)

```
Shake:     IMU shake → state "Shaked" → shake_loop_X (1–5, may switch while shaking)
           → shaking stops → shake_end_X (1–8) → idle

Obstacle:  ToF obstacle → state "obstacle_detected" → stop moving → react_to_obs_X (1–13)
           → react_back_X (1–8) → turn left/right → resume exploring

Face:      K210 sees a face → sends position → ESP32 computes the turn angle
           → interrupts a low-priority animation → turns → greeting (face + body)
           → keeps tracking; face lost → idle
```

### Combining animations

- **Sequential**: one after another, e.g. `shake_loop_X` then `shake_end_X`.
- **Parallel**: face (K210) + body (ESP32) + audio at the same time. Dances (`dance_both` with `dance_together` / `dance_start_%d`) also run the LED pattern (`blink_light_for_dance`). The NVS key `dance_type` stores the dance choice.
- **Looped**: repeat while a condition holds, e.g. while shaking.

---

## 5. Termination and priorities (Inferred)

The servo result strings are Confirmed. The priority scheme is a model of observed behavior, not something found in code.

**Normal completion**: the last frame is reached. Per-servo results are logged:
`"Left  legs servo update done"` / `"... fail"`, same for left foot, right legs, right foot (see [Strings and addresses](strings_and_addresses.md#servo-update-functions)).

**Error**: a servo update fails or a file fails its checksum → stop and log.

**Interrupt**: a more important event replaces the current animation:

| Priority | Value | Examples | Behavior |
| --- | --- | --- | --- |
| Critical | 0 | Falling, cliff edge | Stop immediately, can't be interrupted |
| High | 1 | Voice/app command, petting | Stop at the next frame, clear the queue; interrupts Medium, Low and Background |
| Medium | 2 | Face or gesture seen | Finish the current animation, drop the queue |
| Low | 3 | Idle, explore | Can be interrupted by anything |
| Background | 4 | Ambient movements | Can be interrupted by anything |

Animations with the same priority are played first come, first served. The earlier notes disagreed on Low: one said it "completes all queued animations", the other that it "can be interrupted by all".

A timeout guard, a queue limit (~10) and queue expiry (~30 s) were suggested but have no evidence.

### State model

```
IDLE → QUEUED → PLAYING → COMPLETE
                   ├→ INTERRUPTED (higher priority)
                   ├→ PAUSED
                   └→ ERROR (servo / file failure)
```

---

## 6. Counts (as recorded, Inferred)

These numbers come from earlier notes and were never measured. For a recount of the idle and sleep animations from the strings, see [Idle behavior: counts](idle_behavior.md#9-counts).

| Trigger | Animations | Interruptible |
| --- | --- | --- |
| Shake | 13 (5 loops + 8 ends) | Yes |
| Obstacle | 13 reactions + 8 backs | Yes |
| Cliff | 4 (left/right × 2) | No |
| Put down | 2 | Yes |
| Look down | 8 | Yes |
| Gesture | 1 (multiple gestures) | Yes |
| Sleep | 23 (entry/loop/wake) | Wake only |
| Idle | 83+ | Yes |

Other figures from the same notes: 200+ unique animations, 15+ categories, 5 priority levels, max queue length 10, average animation 2–5 s, servo update rate 50 Hz, face animation 15–30 FPS.
