# How to decompile the EMO Pet firmwares

Software used:

- Ghidra 12.0
- Modified version of [esp32_image_parser](https://github.com/emo-libre/esp32_image_parser) from https://github.com/tenable/esp32_image_parser

Helpful other guides:

- Convert ESP32 Firmware from bin to ELF: https://olof-astrand.medium.com/reverse-engineering-of-esp32-flash-dumps-with-ghidra-or-ida-pro-8c7c58871e68

The Firmwares used are from the OTA and dumped with [EmoProxy](https://github.com/emo-libre/Proxy).

## ESP32

- Use File from OTA (approx. 2,19 MB)
- convert to ELF with esp32_image_parser
- run: `python3 esp32_image_parser.py create_elf <bin file from OTA> -output <name of the elf file> -v -appimage`
- Import ELF with default options
- Analyse with all options

## Kendryte K210

- Use File from OTA (approx. 1,26 MB)
- Import with options:
  - Language: RISCV 64 little endian
  - Base Address: 0x80000000
  - File Offset: 0x1D
  - Length: Take the value shown by Ghidra and subtract 0x3D (61)
- Analyse with default options

### K210 OTA File Format

The K210 OTA file is a Living.ai wrapper around the standard K210 binary.
It has 5 additional bytes prepended and a SHA-256 checksum appended:

| Offset        | Size     | Description                                              |
|---------------|----------|----------------------------------------------------------|
| 0x00          | 1 Byte   | Flag (always `0x00`)                                     |
| 0x01 – 0x04   | 4 Bytes  | LE32: filesize − 37 (= size of the pure K210 binary)    |
| 0x05 – End−33 | n Bytes  | Standard K210 binary (starts with magic `0xDEADBEEF`)   |
| End−32 – End  | 32 Bytes | SHA-256 checksum of all preceding bytes                  |

The LE32 value at bytes 1–4 allows the OTA handler on the ESP32 to know the exact
size of the K210 binary before flashing it, without parsing the K210 format itself.
The SHA-256 checksum covers the entire file except the checksum itself (`SHA256(data[:-32])`).

> **Note:** The File Offset `0x1D` (= 29 bytes) skips the 5-byte Living.ai header and
> the first 24 bytes of the standard K210 header up to the `0xDEADBEEF` magic.
> This offset is stable across all known firmware versions.
