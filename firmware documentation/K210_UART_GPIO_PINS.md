# K210 UART GPIO Configuration

## Overview

The ESP32 communicates with the K210 AI chip via UART. The decompiled firmware confirms the UART tasks and message strings, but does not expose explicit GPIO pin mapping or baud rate in readable strings.

Confirmation status:
- Confirmed: `k210_uart_recv_task`, `k210_uart_trans_task`, UART error strings.
- Not confirmed: UART port number, GPIO pin mapping, baud rate, buffer sizes.

---

## UART Configuration

### UART Port
**UART Number**: Not confirmed in decompiled strings  
**Purpose**: Communication between ESP32 and K210 AI chip

### GPIO Pins

| Function | GPIO Pin | Direction | Description |
|----------|----------|-----------|-------------|
| **TX** | Unconfirmed | Output | ESP32 transmits data to K210 |
| **RX** | Unconfirmed | Input | ESP32 receives data from K210 |

---

## Firmware Evidence

### K210 UART Tasks

**Receive Task**:
```c
"k210_uart_recv_task"
Location: 0x3f40c4bf
Function: FUN_401d8768 (0x401d8768)
Purpose: Receives data from K210 via UART
```

**Transmit Task**:
```c
"k210_uart_trans_task"
Location: 0x3f40c4d3
Function: FUN_401d9080 (0x401d9080)
Purpose: Transmits data to K210 via UART
```

### UART Configuration

**UART Driver Installation**:
- Task priority: Configured in FreeRTOS
- Stack size: Allocated for both TX and RX tasks
- Buffer sizes are not present in the readable strings

**UART Parameters**:
- Baud rate is not confirmed in the decompiled strings
- Data bits, parity, stop bits, and flow control are not confirmed

---

## Pin Configuration Code

Example configuration for a reimplementation (unconfirmed; verify on hardware):

```c
// UART configuration
uart_config_t uart_config = {
    .baud_rate = 115200,  // placeholder; not confirmed from decompiled code
    .data_bits = UART_DATA_8_BITS,
    .parity = UART_PARITY_DISABLE,
    .stop_bits = UART_STOP_BITS_1,
    .flow_ctrl = UART_HW_FLOWCTRL_DISABLE
};

// Install UART driver
uart_driver_install(UART_NUM_2, 3072, 3072, 0, NULL, 0); // buffer sizes unconfirmed

// Configure UART parameters
uart_param_config(UART_NUM_2, &uart_config);

// Set UART pins
uart_set_pin(UART_NUM_2, 
             17,  // TX pin (example; unconfirmed)
             16,  // RX pin (example; unconfirmed)
             UART_PIN_NO_CHANGE,  // RTS (not used)
             UART_PIN_NO_CHANGE); // CTS (not used)
```

---

## K210 Communication Protocol

### Message Types

The ESP32 sends various commands to the K210:

**Face Detection**:
- K210 processes camera feed
- Detects faces and returns coordinates
- ESP32 receives face position data

**Object Recognition (YOLO)**:
```c
"EMO_SEND_YOLO_CLASS %d, x=%d, y=%d!!!\r\n"
Location: 0x3f426cba
```

**OTA Updates**:
```c
"SEND_RUN_OTA %d\r\n"
Location: 0x3f426ca8
```

**Small Packet Communication**:
```c
"small pack error\r"
Location: 0x3f426c96

"got SMALL_PACK_ACK!!!!!!!!!!\r"
Location: 0x3f426ce2
```

### Buffer Management

**Buffer sizes**: Not confirmed in the decompiled strings  
**Error Handling**: Buffer overflow detection strings are present

```c
"uart rx buffer length error(>128)"
Location: 0x3f4254b0

"uart tx buffer length error(>128 or 0)"
Location: 0x3f4254d2
```

---

## Hardware Connections

### ESP32 Side (Example Wiring, Unconfirmed)

| ESP32 Pin | Function | K210 Pin |
|-----------|----------|----------|
| GPIO 16 | UART_RX | K210 TX |
| GPIO 17 | UART_TX | K210 RX |
| GND | Ground | GND |

### Voltage Levels

- **ESP32**: 3.3V logic
- **K210**: 3.3V logic
- **Compatible**: Direct connection (no level shifter needed)

---

## Testing UART Communication

### Monitor UART Traffic

To monitor the communication between ESP32 and K210:

```bash
# Connect USB-to-Serial adapter
# TX -> GPIO 16 (ESP32 RX)  # example; unconfirmed
# RX -> GPIO 17 (ESP32 TX)  # example; unconfirmed
# GND -> GND

# Open serial monitor
screen /dev/ttyUSB0 115200  # baud rate unconfirmed
# or
minicom -D /dev/ttyUSB0 -b 115200  # baud rate unconfirmed
```

### Send Test Commands

You can send commands to the K210 via the ESP32:

```c
// Example: Send command to K210 (UART port unconfirmed)
const char* command = "test_command\r\n";
uart_write_bytes(UART_NUM_2, command, strlen(command));

// Wait for response
uint8_t data[128];
int len = uart_read_bytes(UART_NUM_2, data, sizeof(data), 100 / portTICK_PERIOD_MS);
```

---

## Troubleshooting

### No Communication

1. **Check wiring**: Ensure TX->RX and RX->TX crossover
2. **Verify baud rate**: Both sides must match
3. **Check power**: K210 must be powered and initialized
4. **Monitor buffers**: Check for buffer overflow errors

### Garbled Data

1. **Baud rate mismatch**: Try common baud rates (115200/921600 are common but unconfirmed)
2. **Noise**: Add pull-up resistors (4.7kΩ) on RX/TX lines
3. **Cable length**: Keep UART cables short (<30cm)

### Buffer Overflows

```c
// Increase buffer size if needed (UART port unconfirmed)
uart_driver_install(UART_NUM_2, 
                    4096,  // RX buffer (increased)
                    4096,  // TX buffer (increased)
                    0, NULL, 0);
```

---

## Summary

**K210 UART Configuration**:
- **UART Port**: Not confirmed
- **TX Pin**: Unconfirmed
- **RX Pin**: Unconfirmed
- **Baud Rate**: Not confirmed
- **Buffer Size**: Not confirmed (error strings indicate length limits)
- **Tasks**: `k210_uart_recv_task` and `k210_uart_trans_task` (confirmed)

**Communication Purpose**:
- Face detection results
- Object recognition (YOLO)
- OTA updates
- General AI processing commands

---

**Status**: Partially confirmed from firmware analysis  
**Confidence**: Medium (task names confirmed; wiring/baud unconfirmed)  
**Tested**: Requires hardware verification
