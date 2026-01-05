# EMO Animation Extraction Guide

Note: Extraction details come from the SPIFFS partition and scripts, not from the decompiled firmware strings.

## Overview

This guide explains how to extract animation files (.avi, .mot, .mp3, .json) from the EMO ESP32 firmware storage partition.

## Files Provided

1. **extract_spiffs.py** - Advanced extraction script (recommended)
2. **extract_animations.py** - Simple extraction script (fallback)
3. **run_extraction.bat** - Windows batch file to run extraction

## Quick Start

### Method 1: Using Python Script (Recommended)

```bash
python extract_spiffs.py
```

This will:
- Try to use `mkspiffs` tool if available (best results)
- Fall back to manual extraction if mkspiffs not found
- Extract all animation files to `extracted_animations/` folder

### Method 2: Using Batch File (Windows)

Double-click `run_extraction.bat`

## What Gets Extracted

The script will create the following structure:

```
extracted_animations/
├── avi/              # Face animation videos
│   ├── animation_0000.avi
│   ├── animation_0001.avi
│   └── ...
├── mot/              # Motion/servo animation files
│   ├── motion_0000.mot
│   ├── motion_0001.mot
│   └── ...
├── mp3/              # Audio files
│   ├── audio_0000.mp3
│   └── ...
├── json/             # Configuration files
│   ├── config_0000.json
│   └── ...
└── filenames.txt     # List of original filenames found
```

## File Types

### .avi Files (Face Animations)
- Video files played on K210's screen
- Examples: mood_sad, face_id, reg_face_success
- Format: Standard AVI video format

### .mot Files (Motion Animations)
- Servo motion data for legs/body
- Contains: servo angles, timing, interpolation
- Format: Custom binary format (4 servos × frames)

### .mp3 Files (Audio)
- Background music or sound effects
- Played during animations

### .json Files (Configuration)
- Animation metadata
- Profile settings
- System configuration

## Advanced: Using mkspiffs Tool

For best results, install the `mkspiffs` tool:

### Option 1: PlatformIO
```bash
# Install PlatformIO
pip install platformio

# mkspiffs will be automatically available
```

### Option 2: Manual Installation
Download from: https://github.com/igrr/mkspiffs/releases

Place `mkspiffs` or `mkspiffs.exe` in:
- Same directory as the script
- System PATH
- `~/.platformio/packages/tool-mkspiffs/`

### Using mkspiffs Manually
```bash
mkspiffs -u extracted_animations -p 256 -b 4096 -s 1048576 "emo_esp32_firmware splitted/storage.bin"
```

Parameters:
- `-u` : Unpack to directory
- `-p 256` : Page size (256 bytes)
- `-b 4096` : Block size (4KB)
- `-s 1048576` : Partition size (1MB)

## Troubleshooting

### No files extracted
- Check that `storage.bin` exists in `emo_esp32_firmware splitted/` folder
- Try running with administrator privileges
- Check Python version (requires Python 3.6+)

### Corrupted files
- Some files may be partially overwritten in SPIFFS
- Try different extraction methods
- Check `filenames.txt` for original names

### Missing animations
- Not all animations may be stored in SPIFFS
- Some may be in OTA partitions
- Check both `ota_0_out.bin` and `ota_1_out.bin`

## Understanding the Results

### filenames.txt
This file contains original filenames found in the SPIFFS partition:

```
0x00012340: /spiffs/avi/mood_sad.avi
0x00023450: /spiffs/mot/move_forward.mot
0x00034560: /spiffs/mp3/dance_music.mp3
```

Use this to rename extracted files to their original names.

### File Naming
Extracted files are numbered sequentially:
- `animation_0000.avi` → First AVI file found
- `motion_0000.mot` → First MOT file found

Cross-reference with `filenames.txt` to identify them.

## Next Steps

After extraction:

1. **Analyze .mot files** - Use hex editor to understand format
2. **Play .avi files** - Use VLC or similar video player
3. **Parse motion data** - Create parser for .mot format
4. **Recreate animations** - Use extracted data in your own firmware

## Technical Details

### SPIFFS Partition
- **Offset**: 0xa20000 (10,616,832 bytes)
- **Size**: 1,048,576 bytes (1MB)
- **Type**: DATA
- **Subtype**: 130 (SPIFFS)

### Extraction Method

The script uses multiple strategies:

1. **Signature-based**: Looks for file headers (RIFF, ID3, etc.)
2. **Pattern-based**: Identifies MOT files by servo data patterns
3. **Metadata search**: Finds filenames in SPIFFS metadata
4. **mkspiffs tool**: Uses official tool if available

### MOT File Detection

MOT files are detected by:
- Sequences of 16-bit values in servo range (500-2500µs or 0-180°)
- Consistent frame structure (4 servos per frame)
- Reasonable file size (< 10KB per animation)

## References

- [SPIFFS Documentation](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/storage/spiffs.html)
- [mkspiffs Tool](https://github.com/igrr/mkspiffs)
- [Animation Playback System](ANIMATION_PLAYBACK_SYSTEM.md)
- [K210 Communication Protocol](K210_COMMUNICATION_PROTOCOL.md)

## Support

If you encounter issues:
1. Check that all files are in the correct location
2. Verify Python is installed (`python --version`)
3. Try both extraction scripts
4. Check the console output for error messages

---

**Note**: The extraction process is non-destructive and does not modify the original firmware files.
