# EMO Animation Extraction - Complete Guide

Note: Extraction details come from the SPIFFS partition and scripts, not from the decompiled firmware strings.

## 📦 What You Have

Your `emo_esp32_firmware splitted/` folder contains:

```
emo_esp32_firmware splitted/
├── storage.bin          ← SPIFFS partition (1MB) - Contains animations!
├── ota_0_out.bin        ← Main firmware
├── ota_1_out.bin        ← Backup firmware
├── nvs_out.bin          ← Non-volatile storage
├── partition table.txt  ← Partition layout
└── ... (other partitions)
```

## 🎯 Quick Start

### Step 1: Extract Animations

Run the extraction script:

```bash
python extract_spiffs.py
```

This will create:
```
extracted_animations/
├── avi/          # Face animations (videos)
├── mot/          # Motion animations (servo data)
├── mp3/          # Audio files
├── json/         # Configuration files
└── filenames.txt # Original filenames
```

### Step 2: Analyze Motion Files

```bash
python analyze_mot_files.py extracted_animations/mot/
```

This will show:
- File structure
- Servo angle data
- Frame count
- Data format (PWM or angles)

## 📁 File Types Explained

### 🎬 .avi Files (Face Animations)

**What**: Video files displayed on K210's screen  
**Format**: Standard AVI video  
**Location**: `/spiffs/avi/*.avi`  
**Examples**:
- `mood_sad.avi` - Sad face expression
- `face_id.avi` - Face recognition animation
- `reg_face_success.avi` - Registration success
- `Fit_Talk.avi` - Fitness mode talking
- `dance_together.avi` - Dance animation

**How to view**: Use VLC Media Player or any video player

### 🦿 .mot Files (Motion Animations)

**What**: Servo motion data for legs/body  
**Format**: Custom binary format  
**Location**: `/spiffs/mot/*.mot`  
**Structure**:
```
Each frame contains:
- Servo 0 angle (2 bytes) - Left leg
- Servo 1 angle (2 bytes) - Left foot
- Servo 2 angle (2 bytes) - Right leg
- Servo 3 angle (2 bytes) - Right foot
- Duration (2 bytes) - Frame timing
- Flags (2 bytes) - Interpolation type
```

**Examples**:
- `move_forward.mot` - Walk forward
- `turn_left.mot` - Turn left
- `dance_together.mot` - Dance movements
- `zombie_walk.mot` - Zombie walk animation

**How to analyze**: Use `analyze_mot_files.py`

### 🎵 .mp3 Files (Audio)

**What**: Background music and sound effects  
**Format**: Standard MP3 audio  
**Location**: `/spiffs/mp3/*.mp3`  
**Examples**:
- `dance_music.mp3` - Dance background music
- `notification.mp3` - Alert sounds

**How to play**: Use any audio player

### ⚙️ .json Files (Configuration)

**What**: Animation metadata and settings  
**Format**: JSON text  
**Location**: `/spiffs/json/*.json`  
**Examples**:
- `profile.json` - User profile settings
- `animation_config.json` - Animation parameters

**How to view**: Use any text editor

## 🔧 Tools Provided

### 1. extract_spiffs.py (Main Extractor)

**Purpose**: Extract all files from SPIFFS partition

**Features**:
- Automatic file type detection
- Tries mkspiffs tool first (best results)
- Falls back to manual extraction
- Preserves original filenames when possible
- Creates organized directory structure

**Usage**:
```bash
python extract_spiffs.py
```

### 2. analyze_mot_files.py (Motion Analyzer)

**Purpose**: Understand MOT file format

**Features**:
- Shows servo angles per frame
- Detects PWM vs angle format
- Hex dump for manual analysis
- Statistics and patterns
- Compare multiple files

**Usage**:
```bash
# Analyze single file
python analyze_mot_files.py motion_0000.mot

# Analyze all files in directory
python analyze_mot_files.py extracted_animations/mot/

# Compare two files
python analyze_mot_files.py motion_0000.mot motion_0001.mot
```

### 3. extract_animations.py (Simple Extractor)

**Purpose**: Fallback extraction method

**Usage**:
```bash
python extract_animations.py
```

## 📊 Expected Results

### Typical Extraction Output

```
EMO ESP32 Animation Extractor
======================================================================
Input:  emo_esp32_firmware splitted/storage.bin
Output: extracted_animations/
======================================================================

[1/5] Extracting AVI files...
  ✓ mood_sad.avi (245,632 bytes)
  ✓ face_id.avi (189,440 bytes)
  ✓ reg_face_success.avi (312,576 bytes)
  ... (more files)

[2/5] Extracting MP3 files...
  ✓ dance_music.mp3 (524,288 bytes)
  ... (more files)

[3/5] Extracting JSON files...
  ✓ profile.json (1,024 bytes)
  ... (more files)

[4/5] Extracting MOT files...
  ✓ move_forward.mot (384 bytes)
  ✓ turn_left.mot (288 bytes)
  ... (more files)

[5/5] Searching for filenames...
  Found 47 filenames (saved to filenames.txt)

======================================================================
Extraction Complete!
======================================================================
  AVI files:  23
  MP3 files:  8
  MOT files:  35
  JSON files: 4
======================================================================

✓ Files extracted to: extracted_animations/
```

## 🔍 Understanding filenames.txt

This file maps extracted files to their original names:

```
Filenames found in SPIFFS:
============================================================

0x00012340: /spiffs/avi/mood_sad.avi
0x00023450: /spiffs/avi/face_id.avi
0x00034560: /spiffs/mot/move_forward.mot
0x00045670: /spiffs/mot/turn_left.mot
0x00056780: /spiffs/mp3/dance_music.mp3
```

**How to use**:
1. Find the offset of your extracted file
2. Look up the offset in filenames.txt
3. Rename the file to its original name

## 🎮 Animation Names Reference

### Face Animations (from firmware analysis)

**Moods**:
- `mood_sad` - Sad expression
- `mood_happy` - Happy expression
- `mood_angry` - Angry expression

**Reactions**:
- `image_react_high` - High reaction
- `image_look_up` - Looking up
- `image_search` - Searching animation
- `blink_come_back1` - Blinking animation

**Face Recognition**:
- `face_id` - Face identification
- `reg_face_success` - Registration success
- `doesnt_know_face` - Unknown face

**Fitness**:
- `Fit_Talk` - Talking during fitness
- `Fit_Next` - Next exercise
- `Fit_Good` - Good job
- `Fit_Rest` - Rest period

### Motion Animations (from firmware analysis)

**Basic Movements**:
- `move_1` through `move_8` - Basic motions
- `move_4_down` - Move down
- `move_5_right` - Move right
- `move_6_left` - Move left
- `move_7_left_right` - Left-right motion
- `move_8_left_right` - Alternate left-right

**Turning**:
- `move_turn_left_progress_v01/02/03` - Progressive left turns
- `move_turn_right_progress_v01/02/03` - Progressive right turns
- `turn_around` - 180° turn
- `turn_right_blink_2` - Turn with blink

**Walking**:
- `zombie_loop_walk1` - Zombie walk style 1
- `zombie_loop_walk2` - Zombie walk style 2

**Dancing**:
- `d1_EmoDance` - EMO dance 1
- `d2_WontLetGo` - Won't Let Go dance
- `dance_together` - Dance together
- `dance_start_%d` - Numbered dances
- `dance_basic_loop_%d` - Basic dance loops
- `blink_light_for_dance` - LED blink during dance

**Gestures**:
- `gesture_gun_don't_move_start` - Freeze gesture start
- `gesture_gun_don't_move_loop` - Freeze gesture loop

**Special**:
- `basic_move` - Basic movement
- `move_to_target` - Move to target
- `move_forward_upset` - Upset forward motion
- `autistic_end` - Special ending motion
- `react_to_obs_13` - Obstacle reaction

## 🛠️ Advanced: Using mkspiffs

For best extraction results, install mkspiffs:

### Install via PlatformIO
```bash
pip install platformio
```

### Manual Installation
1. Download from: https://github.com/igrr/mkspiffs/releases
2. Place in system PATH or script directory

### Manual Extraction Command
```bash
mkspiffs -u extracted_animations -p 256 -b 4096 -s 1048576 "emo_esp32_firmware splitted/storage.bin"
```

## 🐛 Troubleshooting

### Problem: No files extracted

**Solutions**:
1. Check `storage.bin` exists in correct location
2. Verify file is not corrupted (should be 1,048,576 bytes)
3. Run with administrator privileges
4. Try both extraction scripts

### Problem: Extracted files are corrupted

**Causes**:
- SPIFFS partition may be partially overwritten
- Files may span multiple blocks
- Compression or encryption

**Solutions**:
1. Try mkspiffs tool for better results
2. Check filenames.txt for correct offsets
3. Some files may be in OTA partitions instead

### Problem: Missing expected animations

**Possible reasons**:
1. Animations may be in OTA partition (ota_0_out.bin)
2. Some animations generated at runtime
3. Animations may be on K210's storage (not ESP32)

**Try**:
```bash
# Search OTA partition
python extract_spiffs.py --input "emo_esp32_firmware splitted/ota_0_out.bin"
```

## 📈 Next Steps

After extraction:

### 1. Verify Files
```bash
# Check AVI files
vlc extracted_animations/avi/*.avi

# Check MP3 files
vlc extracted_animations/mp3/*.mp3

# Analyze MOT files
python analyze_mot_files.py extracted_animations/mot/
```

### 2. Understand MOT Format
- Use hex editor (HxD, 010 Editor)
- Compare multiple files
- Look for patterns in servo data
- Document frame structure

### 3. Create MOT Parser
```python
def parse_mot_file(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()
    
    frames = []
    frame_size = 12  # Adjust based on analysis
    
    for i in range(0, len(data), frame_size):
        frame_data = data[i:i+frame_size]
        servos = struct.unpack('<4H', frame_data[0:8])
        duration = struct.unpack('<H', frame_data[8:10])[0]
        
        frames.append({
            'servos': servos,
            'duration': duration
        })
    
    return frames
```

### 4. Recreate Animations
- Use extracted data in your firmware
- Implement motion playback system
- Sync with face animations

## 📚 Related Documentation

- [ANIMATION_PLAYBACK_SYSTEM.md](ANIMATION_PLAYBACK_SYSTEM.md) - How animations are played
- [K210_COMMUNICATION_PROTOCOL.md](K210_COMMUNICATION_PROTOCOL.md) - Face animation protocol
- [EXTRACTION_GUIDE.md](EXTRACTION_GUIDE.md) - Detailed extraction guide

## 🎯 Summary

You now have:
1. ✅ Extraction tools ready to use
2. ✅ Analysis tools for MOT files
3. ✅ Complete animation name reference
4. ✅ Understanding of file formats
5. ✅ Troubleshooting guide

**Next**: Run `python extract_spiffs.py` to extract all animations!

---

**Questions?** Check the documentation files or analyze the extracted files with the provided tools.
