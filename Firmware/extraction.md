# Extraction

How to get the animation (`.avi`, `.mot`), audio (`.mp3`) and config (`.json`) files out of the ESP32 SPIFFS partition. What the files do is covered in [Animation system](animation_system.md).

These steps rely on the partition table and the scripts in [`scripts/`](scripts), not on the decompiled code.

## Input

A flash dump split into partitions, in a folder called `emo_esp32_firmware splitted/`:

```
emo_esp32_firmware splitted/
├── storage.bin          ← SPIFFS partition (1 MB): animations, audio, config
├── ota_0_out.bin        ← main firmware
├── ota_1_out.bin        ← backup firmware
├── nvs_out.bin          ← non-volatile storage
└── partition table.txt
```

SPIFFS partition (`storage.bin`):

| Field | Value |
| --- | --- |
| Offset | `0xa20000` (10,616,832) |
| Size | 1,048,576 bytes (1 MB) |
| Type / subtype | DATA / 130 (SPIFFS) |
| Page size | 256 bytes |
| Block size | 4096 bytes |

## Quick start

Requires Python 3.6+. Both scripts use paths relative to the current directory, so run them from the folder that contains `emo_esp32_firmware splitted/`:

```bash
python path/to/Firmware/scripts/extract_spiffs.py
python path/to/Firmware/scripts/analyze_mot_files.py extracted_animations/mot/
```

Earlier notes also mentioned a simpler fallback extractor, `extract_animations.py`, and a Windows launcher, `run_extraction.bat`. Neither is in this repository.

### `extract_spiffs.py`

1. Tries `mkspiffs` first (best results; keeps the original file names).
2. If `mkspiffs` isn't found, falls back to carving files out of the image:
   - **Signatures**: file headers (`RIFF`, `ID3`, `{`, …)
   - **MOT heuristics**: runs of 16-bit values in servo range (500–2500 µs or 0–180°), a 4-servo frame structure, files under 10 KB
   - The MOT heuristic assumes the [guessed frame layout](animation_system.md#mot-format-inferred), so files it finds by carving can't be used to confirm that layout
   - **Metadata search**: `/spiffs/...` file names in SPIFFS metadata, written to `filenames.txt`

### `analyze_mot_files.py`

```bash
python analyze_mot_files.py <file.mot>          # one file
python analyze_mot_files.py <directory>         # every .mot in a directory
python analyze_mot_files.py <file1> <file2>     # compare two files
```

It shows servo values per frame, guesses PWM vs angle encoding, and prints a hex dump and statistics.

## Output

```
extracted_animations/
├── avi/            face animations (K210 screen)
├── mot/            motion / servo data
├── mp3/            audio
├── json/           configuration (e.g. profile.json)
└── filenames.txt   original names found in the image
```

Files carved without `mkspiffs` are numbered (`animation_0000.avi`, `motion_0000.mot`, `audio_0000.mp3`, `config_0000.json`). Use `filenames.txt` to restore the original names:

```
0x00012340: /spiffs/avi/mood_sad.avi
0x00034560: /spiffs/mot/move_forward.mot
```

### Example output (illustrative)

This sample run comes from earlier notes. It was **not** produced by a real run, and file names like `dance_music.mp3`, `notification.mp3`, `turn_left.mot`, `zombie_walk.mot` and `animation_config.json` were placeholders.

```
[1/5] Extracting AVI files...
  ✓ mood_sad.avi (245,632 bytes)
  ✓ face_id.avi (189,440 bytes)
  ✓ reg_face_success.avi (312,576 bytes)
[2/5] Extracting MP3 files...
  ✓ dance_music.mp3 (524,288 bytes)
[3/5] Extracting JSON files...
  ✓ profile.json (1,024 bytes)
[4/5] Extracting MOT files...
  ✓ move_forward.mot (384 bytes)
  ✓ turn_left.mot (288 bytes)
[5/5] Searching for filenames...
  Found 47 filenames (saved to filenames.txt)

  AVI files:  23
  MP3 files:  8
  MOT files:  35
  JSON files: 4
```

Earlier notes gave expected counts of ~20–30 AVI, ~30–40 MOT, ~5–10 MP3 and ~2–5 JSON files, but those were never measured (**Inferred**). Please update this page with real numbers once you've run the extraction.

### Viewing the files

| Type | Tool |
| --- | --- |
| `.avi` | VLC or any video player |
| `.mp3` | any audio player |
| `.json` | text editor |
| `.mot` | `analyze_mot_files.py`, a hex editor (HxD, 010 Editor) |

## Using mkspiffs directly

Install it with PlatformIO (`pip install platformio`, which provides `~/.platformio/packages/tool-mkspiffs/`) or download it from <https://github.com/igrr/mkspiffs/releases>, then put it on `PATH`.

```bash
mkspiffs -u extracted_animations -p 256 -b 4096 -s 1048576 "emo_esp32_firmware splitted/storage.bin"
```

`-u` unpacks to a directory, `-p` is the page size, `-b` the block size, `-s` the partition size.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| No files extracted | `storage.bin` is in `emo_esp32_firmware splitted/` and is exactly 1,048,576 bytes; you're running from the right directory; try running with administrator privileges |
| Script errors | Python 3.6+ and any missing dependencies are installed |
| Corrupted files | Use `mkspiffs`. Carved files can span several blocks, parts of SPIFFS may have been overwritten, or files may be compressed or encrypted. Check `filenames.txt` for the right offsets |
| Expected animations missing | Some may live in the OTA partitions (`ota_0_out.bin`, `ota_1_out.bin`) or on the K210 side, or be generated at runtime. Earlier notes suggested `python extract_spiffs.py --input "emo_esp32_firmware splitted/ota_0_out.bin"`, but the script takes no arguments: change the hard-coded `storage_file` in `main()` instead |

Extraction only reads the dump and never modifies it.

## References

- [SPIFFS in ESP-IDF](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/storage/spiffs.html)
- [mkspiffs](https://github.com/igrr/mkspiffs)
