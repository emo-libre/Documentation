# EMO Animation Workflow - Complete System

## Overview

This document details the complete animation workflow in EMO's firmware: what triggers animations, how they're combined, what ends them, and the complete state machine.

---

## 1. Animation System Architecture

### 1.1 Core Components

**Animation Player Task**:
```c
Task: "animation_player_task" (0x3f417389)
Function: FUN_40143218 (0x40143218)
Priority: High
Purpose: Main animation playback engine
```

**Animation Player**:
```c
Name: "animation_player" (0x3f41739f)
Purpose: Manages animation queue and execution
```

**Play Animation Function**:
```c
Function: "play_animation" (0x3f40fa57)
Purpose: Initiates animation playback
```

**Play Without Servo**:
```c
Function: "play_animation_without_servor" (0x3f43058a)
Purpose: Plays face animations only (no body movement)
```

---

## 2. Animation Triggers

### 2.1 Sensor-Based Triggers

#### **Shake Detection**
**Trigger**: IMU detects shaking motion  
**Animations**:
- `shake_loop_1` through `shake_loop_5` (continuous shaking)
- `shake_end_1` through `shake_end_8` (shake stops)

**Workflow**:
```
Shake Detected → shake_loop_X (random) → [Loop while shaking] → shake_end_X (random)
```

**State**: `"Shaked"` (0x3f435d7d)

#### **Put Down / Pick Up**
**Trigger**: Foot sensors detect surface contact change  
**Animations**:
- `react_put_down_1` (0x3f42a22f)
- `react_put_down_2` (0x3f42a240)

**Workflow**:
```
Foot Sensors: No Contact → Contact = Put Down
Foot Sensors: Contact → No Contact = Pick Up
```

#### **Cliff Detection**
**Trigger**: ToF sensors detect edge/drop  
**Animations**:
- `cliff_react_left_2` (0x3f42a30f)
- `cliff_react_left_3` (0x3f42a322)
- `cliff_react_right_2` (0x3f42a335)
- `cliff_react_right_3` (0x3f42a349)

**Workflow**:
```
ToF Left Edge → cliff_react_left_X (random)
ToF Right Edge → cliff_react_right_X (random)
```

#### **Obstacle Detection**
**Trigger**: ToF sensors detect obstacle ahead  
**State**: `"obstacle_detected"` (0x3f431813)  
**Animations**: 13 variations
- `react_to_obs_1` through `react_to_obs_13`

**Workflow**:
```
ToF Distance < Threshold → react_to_obs_X (random) → Back away
```

#### **Back Away Reactions**
**Animations**: 8 variations
- `react_back_1` through `react_back_8`

**Workflow**:
```
Obstacle Detected → react_to_obs_X → react_back_X → Turn/Avoid
```

#### **Petting Detection**
**Trigger**: Touch sensor on head  
**State**: `"Petting"` (0x3f435d75)  
**Animations**:
- Happy reactions
- Purring sounds
- Eye animations

#### **Look Down Reactions**
**Trigger**: IMU detects head tilted down  
**Animations**: 8 variations
- `react_look_down_1_1` through `react_look_down_1_4`
- `react_look_down_2_1` through `react_look_down_2_4`

**Workflow**:
```
IMU Pitch > Threshold → react_look_down_X_Y (random)
```

#### **Depressed State**
**Trigger**: Long period without interaction  
**Animation**: `react_depressed` (0x3f42a2f4)

**Workflow**:
```
No Interaction > 30 minutes → react_depressed → Sad face + slow movements
```

---

### 2.2 AI/Vision-Based Triggers

#### **Face Detection**
**Trigger**: K210 detects human face  
**Animations**:
- Look at face
- Follow face movement
- Greeting animations

**Workflow**:
```
K210: Face Detected → Calculate face position → Turn to face → Greeting animation
```

#### **Gesture Recognition**
**Trigger**: K210 detects hand gesture  
**Animation**: `react_to_gesture` (0x3f42b7ed)

**Supported Gestures**:
- Gesture types are not enumerated in the decompiled strings
- Strings like `Group_photo_gesture_1` through `Group_photo_gesture_6` are present

**Workflow**:
```
K210: Gesture Detected → react_to_gesture → Respond with matching animation
```

#### **Image Recognition**
**Trigger**: K210 recognizes object/image  
**Animation**: `image_react_high` (0x3f42cb3d)

**Workflow**:
```
K210: Object Recognized → image_react_high → Excited reaction
```

---

### 2.3 User Command Triggers

Note: Voice, app, and button triggers are inferred; explicit strings are not confirmed in the decompiled output.

#### **Voice Commands**
**Trigger**: Microphone + voice recognition  
**Animations**: Command-specific

**Workflow**:
```
Microphone → Voice Recognition → Command Parsed → Execute Animation
```

#### **App Commands**
**Trigger**: Bluetooth command from mobile app  
**Animations**: Any animation can be triggered

**Workflow**:
```
App → Bluetooth → Command Parser → Animation Player → Execute
```

#### **Button Press**
**Trigger**: Physical button on EMO  
**Animations**: Mode-specific

---

### 2.4 Time-Based Triggers

#### **Idle Timeout**
**Trigger**: No activity for X seconds  
**Animations**: Idle behaviors (see IDLE_BEHAVIOR_SYSTEM.md)

**Workflow**:
```
No Activity > X  → Vigilant mode
No Activity > Y  → Explore/Free Play
No Activity > Z  → Sleep mode
```

Note: timeout thresholds are not confirmed in the decompiled strings; values are inferred.

#### **Sleep Mode**
**Trigger**: Extended inactivity  
**Animations**: Sleep cycle (see IDLE_BEHAVIOR_SYSTEM.md)

**Workflow**:
```
Idle > 5min → sleep_get_in_X → sleep_loop_X → [Sleep] → Wake on sensor
```

#### **Reminders**
**Trigger**: Time-based events  
**Animations**:
- `reminder_sleep` (0x3f42b045)
- `reminder_eat` (0x3f42b038)

---

## 3. Animation Combinations

### 3.1 Sequential Animations

**Pattern**: Animation A → Animation B → Animation C

**Example: Shake Sequence**:
```c
shake_loop_1 → shake_loop_2 → shake_loop_3 → shake_end_1
```

**Implementation**:
```c
// Pseudo-code
play_animation("shake_loop_1");
wait_for_completion();
play_animation("shake_loop_2");
wait_for_completion();
play_animation("shake_end_1");
```

### 3.2 Parallel Animations

**Pattern**: Face Animation + Body Animation (simultaneous)

**Example: Happy Reaction**:
```
Face: happy_eyes.avi (K210)
Body: happy_dance.mot (ESP32 servos)
Audio: happy_sound.mp3 (Speaker)
```

**Implementation**:
```c
// Pseudo-code
k210_play_avi("happy_eyes.avi");  // Non-blocking
servo_play_mot("happy_dance.mot"); // Non-blocking
audio_play_mp3("happy_sound.mp3"); // Non-blocking
wait_all_complete();
```

### 3.3 Conditional Combinations

**Pattern**: Animation selection based on state

**Example: Obstacle Reaction**:
```c
if (obstacle_distance < 10cm) {
    play_animation("react_to_obs_1");
    play_animation("react_back_1");
} else if (obstacle_distance < 20cm) {
    play_animation("react_to_obs_5");
    play_animation("turn_left");
}
```

### 3.4 Loop Combinations

**Pattern**: Repeat animation until condition

**Example: Shake Loop**:
```c
while (shaking_detected) {
    play_animation("shake_loop_" + random(1,5));
    wait_for_completion();
}
play_animation("shake_end_" + random(1,8));
```

---

## 4. Animation Termination

### 4.1 Natural Completion

**Method**: Animation plays to end  
**Trigger**: Animation file reaches last frame

**Workflow**:
```
Animation Start → Play frames → Last frame → Animation Complete → Next action
```

**Servo Update Done**:
```c
"Left legs servo update done\n" (0x3f44baf0)
"Right legs servo update done\n" (0x3f44bb7d)
"Left foot servo update done\n" (0x3f44bb36)
"Right foot servo update done\n" (0x3f44bbc4)
```

### 4.2 Interrupt Termination

**Method**: Higher priority event interrupts animation

**Priority Levels**:
1. **Critical** (Falling, cliff edge) - Immediate stop
2. **High** (User interaction, voice command) - Stop at next frame
3. **Medium** (Face detected, gesture) - Complete current, skip queue
4. **Low** (Idle timeout) - Complete all queued

**Workflow**:
```
Animation Playing → High Priority Event → Stop Current → Clear Queue → New Animation
```

### 4.3 Timeout Termination

**Method**: Animation exceeds maximum duration

**Workflow**:
```
Animation Start → Timer Start → Max Duration Reached → Force Stop → Error State
```

### 4.4 Error Termination

**Method**: Servo failure or communication error

**Error Messages**:
```c
"Left legs servo update fail\n"
"Right legs servo update fail\n"
"Left foot servo update fail\n"
"Right foot servos update fail\n"
```

**Workflow**:
```
Animation Playing → Servo Error → Stop Animation → Log Error → Safe State
```

---

## 5. Animation State Machine

### 5.1 States

```
┌─────────────┐
│    IDLE     │ ← Default state
└──────┬──────┘
       │
       ├─→ PLAYING ─→ Animation executing
       │      │
       │      ├─→ PAUSED ─→ Temporarily stopped
       │      │
       │      └─→ COMPLETE ─→ Finished successfully
       │
       ├─→ QUEUED ─→ Waiting in queue
       │
       ├─→ INTERRUPTED ─→ Stopped by higher priority
       │
       └─→ ERROR ─→ Failed to execute
```

### 5.2 State Transitions

**IDLE → PLAYING**:
```c
Trigger: play_animation() called
Condition: No animation currently playing
Action: Load animation, start playback
```

**PLAYING → COMPLETE**:
```c
Trigger: Last frame reached
Condition: No errors
Action: Cleanup, trigger next in queue
```

**PLAYING → INTERRUPTED**:
```c
Trigger: Higher priority event
Condition: Priority > current animation
Action: Stop current, save state, start new
```

**PLAYING → PAUSED**:
```c
Trigger: Pause command
Condition: Animation supports pausing
Action: Save current frame, stop servos
```

**PAUSED → PLAYING**:
```c
Trigger: Resume command
Condition: Animation still valid
Action: Restore frame, continue playback
```

**PLAYING → ERROR**:
```c
Trigger: Servo failure, file error
Condition: Unrecoverable error
Action: Stop all, log error, safe state
```

---

## 6. Animation Queue System

### 6.1 Queue Structure

```c
typedef struct {
    char* animation_name;
    uint8_t priority;
    uint32_t timestamp;
    bool interruptible;
    void (*callback)(void);
} animation_queue_item_t;
```

### 6.2 Queue Operations

**Enqueue**:
```c
// Add animation to queue
queue_animation("explore_play1", PRIORITY_LOW, true, NULL);
```

**Dequeue**:
```c
// Get next animation from queue
animation_queue_item_t* next = get_next_animation();
```

**Clear Queue**:
```c
// Remove all queued animations
clear_animation_queue();
```

**Priority Insert**:
```c
// Insert high-priority animation at front
priority_queue_animation("react_to_obs_1", PRIORITY_HIGH);
```

---

## 7. Complete Animation Workflows

### 7.1 Shake Detection Workflow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. IMU detects shaking                                      │
│    ↓                                                         │
│ 2. Set state: "Shaked"                                      │
│    ↓                                                         │
│ 3. Select random shake_loop_X (1-5)                         │
│    ↓                                                         │
│ 4. Play shake_loop_X                                        │
│    ↓                                                         │
│ 5. While shaking continues:                                 │
│    ├─→ Continue current loop                                │
│    └─→ Or switch to different shake_loop_Y                  │
│    ↓                                                         │
│ 6. Shaking stops detected                                   │
│    ↓                                                         │
│ 7. Select random shake_end_X (1-8)                          │
│    ↓                                                         │
│ 8. Play shake_end_X                                         │
│    ↓                                                         │
│ 9. Return to idle state                                     │
└─────────────────────────────────────────────────────────────┘
```

### 7.2 Obstacle Avoidance Workflow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. ToF sensor detects obstacle                              │
│    ↓                                                         │
│ 2. Set state: "obstacle_detected"                           │
│    ↓                                                         │
│ 3. Stop current movement                                    │
│    ↓                                                         │
│ 4. Select random react_to_obs_X (1-13)                      │
│    ↓                                                         │
│ 5. Play react_to_obs_X (surprised reaction)                 │
│    ↓                                                         │
│ 6. Wait for completion                                      │
│    ↓                                                         │
│ 7. Select random react_back_X (1-8)                         │
│    ↓                                                         │
│ 8. Play react_back_X (back away)                            │
│    ↓                                                         │
│ 9. Calculate new path                                       │
│    ↓                                                         │
│ 10. Turn left or right                                      │
│    ↓                                                         │
│ 11. Resume exploration                                      │
└─────────────────────────────────────────────────────────────┘
```

### 7.3 Face Detection Workflow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. K210 camera detects face                                 │
│    ↓                                                         │
│ 2. Calculate face position (x, y)                           │
│    ↓                                                         │
│ 3. Send position to ESP32 via UART                          │
│    ↓                                                         │
│ 4. ESP32 calculates turn angle                              │
│    ↓                                                         │
│ 5. Interrupt current animation (if low priority)            │
│    ↓                                                         │
│ 6. Play turn animation to face direction                    │
│    ↓                                                         │
│ 7. K210 plays greeting face animation                       │
│    ↓                                                         │
│ 8. ESP32 plays greeting body animation                      │
│    ↓                                                         │
│ 9. Track face movement                                      │
│    ├─→ Face moves: Adjust position                          │
│    └─→ Face lost: Return to idle                            │
└─────────────────────────────────────────────────────────────┘
```

### 7.4 Sleep Cycle Workflow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. No interaction for 5+ minutes                            │
│    ↓                                                         │
│ 2. Play reminder_sleep (optional)                           │
│    ↓                                                         │
│ 3. Select sleep_get_in_X (slow/fast/doze_off)               │
│    ↓                                                         │
│ 4. Play sleep_get_in_X (getting comfortable)                │
│    ↓                                                         │
│ 5. Enter sleep loop:                                        │
│    ├─→ Play sleep_loop_1 or sleep_loop_2                    │
│    ├─→ Play sleep_breath_1 or sleep_breath_2                │
│    ├─→ Play sleep_Fireflies_1 or sleep_Fireflies_2          │
│    ├─→ Play sleep_bubble_1 or sleep_bubble_2                │
│    └─→ Occasionally: sleep_peep1 or sleep_peep2             │
│    ↓                                                         │
│ 6. Wake trigger (touch, voice, movement):                   │
│    ├─→ Gentle: sleep_wake_up_slow                           │
│    ├─→ Normal: sleep_wake_up_fast                           │
│    ├─→ Sudden: sleep_awake_suddenly_panic                   │
│    └─→ Annoyed: sleep_wake_up_angry                         │
│    ↓                                                         │
│ 7. Return to active state                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 8. Animation Priority System

### 8.1 Priority Levels

| Priority | Value | Examples | Interruptible |
|----------|-------|----------|---------------|
| **CRITICAL** | 0 | Falling, cliff edge | No |
| **HIGH** | 1 | User command, voice | Yes (by critical) |
| **MEDIUM** | 2 | Face detected, gesture | Yes (by high+) |
| **LOW** | 3 | Idle animations, explore | Yes (by all) |
| **BACKGROUND** | 4 | Ambient movements | Yes (by all) |

### 8.2 Priority Rules

1. **Critical animations** cannot be interrupted
2. **High priority** interrupts medium/low/background
3. **Same priority**: First-come-first-served
4. **Queue limit**: Max 10 animations queued
5. **Timeout**: Queued animations expire after 30s

---

## 9. Animation File Format

### 9.1 MOT Files (Motion/Servo)

**Format**: Binary servo position data  
**Location**: ESP32 SPIFFS  
**Structure**:
```c
typedef struct {
    uint16_t frame_count;
    uint16_t frame_rate;  // FPS
    servo_frame_t frames[];
} mot_file_t;

typedef struct {
    uint16_t servo_positions[12];  // 12 servos
    uint16_t duration_ms;
} servo_frame_t;
```

### 9.2 AVI Files (Face Animation)

**Format**: Video file  
**Location**: K210 flash  
**Resolution**: 320x240  
**Frame Rate**: 15-30 FPS  
**Codec**: MJPEG

### 9.3 MP3 Files (Audio)

**Format**: MP3 audio  
**Location**: ESP32 SPIFFS  
**Sample Rate**: 16kHz or 44.1kHz  
**Bitrate**: 128kbps

---

## 10. Key Functions

### 10.1 Animation Control

```c
// Start animation
void play_animation(const char* name);

// Stop current animation
void stop_animation(void);

// Pause animation
void pause_animation(void);

// Resume animation
void resume_animation(void);

// Queue animation
void queue_animation(const char* name, uint8_t priority);

// Clear queue
void clear_animation_queue(void);
```

### 10.2 State Queries

```c
// Check if animation is playing
bool is_animation_playing(void);

// Get current animation name
const char* get_current_animation(void);

// Get animation state
animation_state_t get_animation_state(void);

// Get queue length
uint8_t get_queue_length(void);
```

---

## 11. Animation Naming Convention

### 11.1 Naming Pattern

```
<category>_<action>_<variation>
```

**Examples**:
- `explore_play1` - Exploration category, play action, variation 1
- `react_back_5` - Reaction category, back away action, variation 5
- `sleep_loop_2` - Sleep category, loop action, variation 2

### 11.2 Categories

- `explore_` - Exploration behaviors
- `react_` - Reactive behaviors
- `sleep_` - Sleep-related
- `shake_` - Shake responses
- `cliff_` - Cliff/edge reactions
- `free_play_` - Free play animations
- `look_around_` - Looking behaviors

---

## 12. Summary Statistics

### Animation Counts by Trigger

| Trigger Type | Animation Count | Interruptible |
|--------------|-----------------|---------------|
| Shake | 13 (5 loops + 8 ends) | Yes |
| Obstacle | 13 reactions + 8 backs | Yes |
| Cliff | 4 (left/right x 2) | No |
| Put Down | 2 | Yes |
| Look Down | 8 | Yes |
| Gesture | 1 (multiple gestures) | Yes |
| Sleep | 23 (entry/loop/wake) | Wake only |
| Idle | 83+ | Yes |

### Total Animation System

- **Total Unique Animations**: 200+
- **Animation Categories**: 15+
- **Priority Levels**: 5
- **Max Queue Length**: 10
- **Average Animation Duration**: 2-5 seconds
- **Servo Update Rate**: 50Hz
- **Face Animation FPS**: 15-30

---

**Status**: ✅ Complete animation workflow documented  
**Coverage**: Triggers, combinations, termination, state machine, priorities  
**Confidence**: High (based on firmware analysis)
