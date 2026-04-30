# How to decompile the EMO Pet firmwares

Software used:

- Ghidra 12.0
- Modified version of [esp32_image_parser](https://github.com/emo-libre/esp32_image_parser) from https://github.com/tenable/esp32_image_parser

Helpful other guides:

- Convert ESP32 Firmware from bin to ELF: https://olof-astrand.medium.com/reverse-engineering-of-esp32-flash-dumps-with-ghidra-or-ida-pro-8c7c58871e68

The Firmwares used are from the OTA and dumped with [EmoProxy](https://github.com/emo-libre/Proxy).

## ESP32

- Use File from OTA (aprox. 2,19 MB)
- convert to ELF with esp32_image_parser
- run: python3 esp32_image_parser.py create_elf `<bin file from OTA>` -output `<name of the elf file>` -v -appimage
- Import ELF with default options
- Analyse with all options

## Kendryte K210

- Use File from OTA (aprox. 1,26 MB)
- Import with options:
  - Language: RISCV 64 little endian
  - Base Address: 0x80000000
  - File Offset: 0x1D
  - Length: [modify as told by ghidra]
- Analyse with default options
