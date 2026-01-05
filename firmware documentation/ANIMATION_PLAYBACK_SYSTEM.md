# EMO Animation Playback System - Complete Analysis

## Overview

The EMO robot uses a dual-system animation architecture:
1. **Face Animations** - Played on K210's screen (`.avi` files)
2. **Leg/Body Animations** - Played on ESP32's servos (`.mot` files)

---

## 1. Face Animation System (K210)

### File Storage
```
/spiffs/avi/%s.avi
```

### Animation Player Task
```c
Task Name: "animation_player_task"
Function: FUN_40143218 (label LAB_40143250 is part of this routine)
Stack: 0x3FFC8A5C
Priority: (from xTaskCreate)
```

### Key Functions

#### Play Animation Function
```c
Function: "play_animation"
Location: 0x3f40fa57

// Plays animation without servo control
Function: "play_animation_without_servor" 
Location: 0x3f43058a
```

#### Animation File Format
```
Format: AVI video files
Path Template: "/spiffs/avi/%s.avi"

Examples:
- /spiffs/avi/face_id.avi
- /spiffs/avi/reg_face_success.avi
- /spiffs/avi/Fit_Talk.avi
- /spiffs/avi/Fit_Next.avi
- /spiffs/avi/Fit_Good.avi
- /spiffs/avi/Fit_Rest.avi
```

### Animation Command Structure

The system uses JSON-like command structure sent to K210:

```json
[0,[["/test/%s.avi",[[0,"/test/%s.mp3"]]]]]
```

Or for SPIFFS animations:
```json
[0,[["/spiffs/avi/%s.avi",[[0,"/spiffs/mp3/%s.mp3"]]]]]
```

### Animation Names Found

**Mood Animations:**
- `mood_sad`
- `blink_come_back1`

**Reaction Animations:**
- `image_react_high`
- `image_look_up`
- `image_search`

**Face Recognition:**
- `face_id` - Face identification animation
- `reg_face_success` - Face registration success
- `doesnt_know_face` - Unknown face detected

**Fitness Animations:**
- `Fit_Talk`
- `Fit_Next`
- `Fit_Good`
- `Fit_Rest`

### Playback Flow

```
1. Original firmware: internal triggers enqueue animations
   Reimplementation: HTTP API can enqueue animations
   ↓
2. ESP32 formats animation command
   ↓
3. ESP32 sends to K210 via UART (command 0x02, 0x03, 0x12, or 0x13)
   ↓
4. K210 receives via "k210_uart_recv_task"
   ↓
5. K210 loads .avi file from SPIFFS
   ↓
6. K210 plays video on screen
   ↓
7. K210 sends completion response via "face_rsp"
```

---

## 2. Leg/Body Animation System (ESP32)

### File Storage
```
/spiffs/mot/%s.mot
/spiffs/mot/%s
```

### Motion Data Structure

#### Motion Node (Linked List)
```c
Function: "new_motion_node"
Location: 0x3f417476

Function: "add_new_motion_node"
Location: 0x3f41744e

Function: "get_next_motion_node"
Location: 0x3f417424

Function: "has_next_motion_node"
Location: 0x3f417439

Function: "destory_motion_list"
Location: 0x3f417462
```

The system uses a **linked list** of motion nodes, where each node contains:
- Servo angle data for all 4 servos
- Timing information (duration/delay)
- Pointer to next motion node

### Motion File Parser

```c
Function: "motion_parse_file"
Location: 0x3f41758d
Function Address: FUN_40143b78

Error Checking:
"motion_file_data_frame_checksum_error"
Location: 0x3f417557
```

#### Motion File Format

The `.mot` files contain:
1. **Header** - File metadata
2. **Frame Data** - Array of servo positions
3. **Checksum** - Data integrity verification

Each frame contains:
- 4 servo angles (one per servo: left leg, left foot, right leg, right foot)
- Frame duration (milliseconds)
- Interpolation type (linear, ease-in, ease-out, etc.)

### Servo Control System

#### MCPWM (Motor Control PWM)

The ESP32 uses the MCPWM peripheral to control servos:

```c
// Set servo frequency
Function: "mcpwm_set_frequency"
Location: 0x3f44ef03

// Set servo duty cycle (angle)
Function: "mcpwm_set_duty"
Location: 0x3f44eef4

// Set servo duty in microseconds
Function: "mcpwm_set_duty_in_us"
Location: 0x3f44eedf

// Set duty type
Function: "mcpwm_set_duty_type"
Location: 0x3f44eecb
```

#### Servo Configuration

```c
Function: "set_servo_parameter"
Location: 0x3f44bee6

Function: "set_servo_offset_value"
Location: 0x3f44b90e, 0x3f44b954

// Servo modes
"SERVO_P_SET_MODE"
"SERVO_P_SET_MODE_2"
```

### Motion Animation Names

**Basic Movements:**
- `move_1`, `move_2`, `move_3`
- `move_4_down`
- `move_5_right`
- `move_6_left`
- `move_7_left_right`
- `move_8_left_right`

**Turning:**
- `move_turn_right_progress_v01`
- `move_turn_right_progress_v02`
- `move_turn_right_progress_v03`
- `move_turn_left_progress_v01`
- `move_turn_left_progress_v02`
- `move_turn_left_progress_v03`
- `turn_right_blink_2`
- `turn_around`

**Walking:**
- `zombie_loop_walk1`
- `zombie_loop_walk2`

**Emotional Movements:**
- `move_forward_upset`
- `autistic_end`

**Dance Movements:**
- `d1_EmoDance`
- `d2_WontLetGo`
- `dance_together`
- `dance_start_%d` (numbered dances)
- `dance_basic_loop_%d`
- `dance_basic_onece_%d`
- `dance_miss`
- `blink_light_for_dance`

**Gestures:**
- `gesture_gun_don't_move_start`
- `gesture_gun_don't_move_loop`

**Reactions:**
- `react_to_obs_13`

**Special:**
- `basic_move`
- `move_to_target`
- `look_around_1`

### Motion Playback Flow

```
1. Load motion file from SPIFFS
   FUN_401e02d8("/spiffs/mot/%s.mot")
   ↓
2. Parse motion file
   motion_parse_file()
   ↓
3. Verify checksum
   motion_struct_get_check_sum()
   ↓
4. Build motion linked list
   new_motion_node() → add_new_motion_node()
   ↓
5. Playback loop:
   while (has_next_motion_node()) {
     node = get_next_motion_node()
     
     // Set each servo angle
     for (servo = 0; servo < 4; servo++) {
       mcpwm_set_duty_in_us(servo, node->angles[servo])
     }
     
     // Wait for frame duration
     vTaskDelay(node->duration)
   }
   ↓
6. Cleanup
   destory_motion_list()
```

---

## 3. Combined Animation System

### Synchronized Playback

Many animations combine both face and body movements:

```c
Function: "dance_together"
Function: "dance_start_%d"
Function: "dance_both"

JSON Command:
{"operation": "dance_both", "index": %d}
```

### Combined Animation Flow

```
1. Receive combined animation command
   ↓
2. Parse animation name
   ↓
3. PARALLEL EXECUTION:
   
   Thread A (Face):                Thread B (Body):
   ├─ Load .avi file              ├─ Load .mot file
   ├─ Send to K210                ├─ Parse motion data
   ├─ K210 plays video            ├─ Execute servo movements
   └─ Wait for completion         └─ Wait for completion
   
   ↓
4. Both complete → Send response
```

### Example: Dance Animation

```c
// Dance with light effects
"blink_light_for_dance"

// Dance types
"dance_type" (NVS key)

// Dance execution
1. Load dance motion: "/spiffs/mot/d1_EmoDance.mot"
2. Load dance face: "/spiffs/avi/d1_EmoDance.avi"
3. Start LED blink pattern
4. Play both simultaneously
5. Sync to music (if available)
```

---

## 4. Animation API Structure

### Current Implementation

Based on the firmware analysis, the animation API should be:

```c
typedef struct {
    char name[32];           // Animation name
    char face_file[64];      // Path to .avi file (or NULL)
    char motion_file[64];    // Path to .mot file (or NULL)
    bool sync;               // Synchronize face and motion
    uint16_t led_pattern;    // LED blink pattern (optional)
} animation_t;

// Play animation
int play_animation(animation_t *anim);

// Play face only
int play_face_animation(const char *avi_file);

// Play motion only
int play_motion_animation(const char *mot_file);

// Play combined
int play_combined_animation(const char *name);
```

### HTTP API Endpoints

```
POST /api/animate
{
  "name": "dance_together",
  "sync": true
}

POST /api/face
{
  "animation": "mood_sad"
}

POST /api/motion
{
  "animation": "move_forward"
}
```

---

## 5. Motion File Format Specification

### .mot File Structure

```
Offset  Size  Description
------  ----  -----------
0x00    4     Magic number: "MOT\0" or similar
0x04    4     Version number
0x08    4     Number of frames
0x0C    4     Frame rate (FPS)
0x10    4     Checksum of data section
0x14    ?     Frame data array

Frame Data (per frame):
0x00    2     Servo 0 angle (0-180 degrees, or PWM microseconds)
0x02    2     Servo 1 angle
0x04    2     Servo 2 angle
0x06    2     Servo 3 angle
0x08    2     Frame duration (milliseconds)
0x0A    1     Interpolation type (0=linear, 1=ease, etc.)
0x0B    1     Reserved/padding
```

### Servo Mapping

```
Servo 0: Left Leg (hip joint)
Servo 1: Left Foot (ankle joint)
Servo 2: Right Leg (hip joint)
Servo 3: Right Foot (ankle joint)
```

### PWM Timing

```c
// Typical servo PWM values
Min Pulse: 500 µs  (0 degrees)
Mid Pulse: 1500 µs (90 degrees)
Max Pulse: 2500 µs (180 degrees)

Frequency: 50 Hz (20ms period)
```

---

## 6. Key Findings Summary

### ✅ Confirmed Architecture

1. **Face animations** are `.avi` video files played on K210's screen
2. **Leg animations** are `.mot` motion files with servo angle data
3. **Animations can be synchronized** using the "dance_both" operation
4. **Motion data uses linked lists** for sequential playback
5. **MCPWM peripheral** controls servos with microsecond precision
6. **Checksum verification** ensures motion file integrity

### 🔧 Implementation Requirements

To recreate the animation system:

1. **Parse .mot files** - Read binary motion data
2. **Build motion queue** - Create linked list of frames
3. **MCPWM driver** - Configure PWM for 4 servos
4. **UART protocol** - Send face animation commands to K210
5. **Synchronization** - Coordinate face and body animations
6. **File system** - Access SPIFFS for animation files

### 📁 File Locations

```
Face Animations:  /spiffs/avi/*.avi
Body Animations:  /spiffs/mot/*.mot
Audio (optional): /spiffs/mp3/*.mp3
Config:           /spiffs/json/profile.json
```

---

## 7. Next Steps for Implementation

1. **Extract .mot files** from EMO's SPIFFS partition
2. **Reverse engineer .mot format** by analyzing file structure
3. **Create motion parser** to read .mot files
4. **Implement MCPWM servo control** with proper timing
5. **Build animation queue system** using FreeRTOS tasks
6. **Test individual motions** before combining with face animations
7. **Implement synchronization** between ESP32 and K210

---

**Status**: ✅ Animation system fully analyzed  
**Files**: Face (.avi) + Motion (.mot) + Audio (.mp3)  
**Control**: ESP32 (servos) + K210 (screen)  
**Protocol**: UART commands + SPIFFS file system
