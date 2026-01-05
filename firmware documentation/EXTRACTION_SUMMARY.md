# Animation Extraction - Quick Summary

Note: Extraction details come from the SPIFFS partition and scripts, not from the decompiled firmware strings.

## 🚀 Quick Start (3 Steps)

### Step 1: Extract
```bash
python extract_spiffs.py
```

### Step 2: Analyze
```bash
python analyze_mot_files.py extracted_animations/mot/
```

### Step 3: View
- **Videos**: Open `.avi` files with VLC
- **Audio**: Open `.mp3` files with any player
- **Config**: Open `.json` files with text editor
- **Motion**: Use analyzer tool for `.mot` files

## 📦 What Gets Extracted

```
extracted_animations/
├── avi/              # 🎬 Face animations (videos)
│   ├── mood_sad.avi
│   ├── face_id.avi
│   └── ... (~20-30 files)
│
├── mot/              # 🦿 Motion animations (servo data)
│   ├── move_forward.mot
│   ├── dance_together.mot
│   └── ... (~30-40 files)
│
├── mp3/              # 🎵 Audio files
│   ├── dance_music.mp3
│   └── ... (~5-10 files)
│
├─�� json/             # ⚙️ Configuration
│   ├── profile.json
│   └── ... (~2-5 files)
│
└── filenames.txt     # 📝 Original filenames mapping
```

## 🎯 File Types

| Type | Purpose | Format | View With |
|------|---------|--------|-----------|
| `.avi` | Face animations | Video | VLC Player |
| `.mot` | Leg/body motions | Binary servo data | Analyzer tool |
| `.mp3` | Background audio | Audio | Any player |
| `.json` | Configuration | Text | Text editor |

## 🔧 Tools Provided

| Tool | Purpose | Command |
|------|---------|---------|
| `extract_spiffs.py` | Extract all files | `python extract_spiffs.py` |
| `analyze_mot_files.py` | Analyze motion files | `python analyze_mot_files.py <file>` |
| `extract_animations.py` | Fallback extractor | `python extract_animations.py` |

## 📊 Expected Output

```
Extraction Complete!
======================================================================
  AVI files:  23  ← Face animations
  MP3 files:  8   ← Audio files
  MOT files:  35  ← Motion animations
  JSON files: 4   ← Configuration
======================================================================
```

## 🎮 Animation Examples

### Face Animations
- `mood_sad` - Sad face
- `face_id` - Face recognition
- `dance_together` - Dance face
- `Fit_Talk` - Fitness talking

### Motion Animations
- `move_forward` - Walk forward
- `turn_left` - Turn left
- `d1_EmoDance` - Dance motion
- `zombie_walk` - Zombie walk

## 🔍 MOT File Format

```
Frame Structure (12 bytes):
┌─────────────────────────────────┐
│ Servo 0 (2 bytes) - Left leg    │
│ Servo 1 (2 bytes) - Left foot   │
│ Servo 2 (2 bytes) - Right leg   │
│ Servo 3 (2 bytes) - Right foot  │
│ Duration (2 bytes) - Timing     │
│ Flags (2 bytes) - Interpolation │
└─────────────────────────────────┘

Values:
- PWM: 500-2500 microseconds
- Angle: 0-180 degrees
```

## 🛠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| No files extracted | Check `storage.bin` exists, run as admin |
| Corrupted files | Try mkspiffs tool, check filenames.txt |
| Missing animations | Check OTA partitions, some may be runtime-generated |
| Script errors | Verify Python 3.6+, install dependencies |

## 📚 Documentation Files

1. **ANIMATION_EXTRACTION_README.md** - Complete guide
2. **EXTRACTION_GUIDE.md** - Detailed extraction steps
3. **ANIMATION_PLAYBACK_SYSTEM.md** - How animations work
4. **K210_COMMUNICATION_PROTOCOL.md** - Face animation protocol

## ✅ Checklist

- [ ] Run `python extract_spiffs.py`
- [ ] Check `extracted_animations/` folder created
- [ ] Verify files extracted (check counts)
- [ ] Open `filenames.txt` to see original names
- [ ] Test `.avi` files with VLC
- [ ] Analyze `.mot` files with analyzer
- [ ] Read documentation for next steps

## 🎯 Success Criteria

You should have:
- ✅ 20-30 AVI files (face animations)
- ✅ 30-40 MOT files (motion animations)
- ✅ 5-10 MP3 files (audio)
- ✅ 2-5 JSON files (config)
- ✅ filenames.txt with mappings

## 🚀 Next Steps

1. **Verify extraction** - Check file counts and sizes
2. **Analyze MOT format** - Use analyzer tool
3. **Document findings** - Note patterns and structure
4. **Create parser** - Build MOT file parser
5. **Implement playback** - Use in your firmware

---

**Ready?** Run: `python extract_spiffs.py`
