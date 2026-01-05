#!/usr/bin/env python3
"""
Analyze extracted MOT motion files
Helps understand the format and structure
"""

import struct
import sys
from pathlib import Path

def analyze_mot_file(filepath):
    """Analyze a single MOT file"""
    print(f"\n{'='*70}")
    print(f"Analyzing: {filepath.name}")
    print(f"{'='*70}")
    
    with open(filepath, 'rb') as f:
        data = f.read()
    
    print(f"File size: {len(data)} bytes")
    
    # Try to detect format
    print("\n[Header Analysis]")
    if len(data) >= 16:
        # Check for magic number
        magic = struct.unpack('<I', data[0:4])[0]
        print(f"First 4 bytes (magic?): 0x{magic:08x}")
        
        # Try to read as header
        try:
            header = struct.unpack('<4I', data[0:16])
            print(f"Potential header (4 x uint32):")
            for i, val in enumerate(header):
                print(f"  [{i}] = {val} (0x{val:08x})")
        except:
            pass
    
    # Analyze as servo data
    print("\n[Servo Data Analysis]")
    
    # Try PWM format (500-2500 microseconds)
    print("\nAssuming PWM format (500-2500 µs):")
    analyze_as_pwm(data)
    
    # Try angle format (0-180 degrees)
    print("\nAssuming Angle format (0-180°):")
    analyze_as_angles(data)
    
    # Show hex dump
    print("\n[Hex Dump - First 128 bytes]")
    dump_hex(data, 0, min(128, len(data)))
    
    # Show statistics
    print("\n[Statistics]")
    show_statistics(data)


def analyze_as_pwm(data):
    """Analyze assuming PWM microseconds format"""
    frame_size = 8  # 4 servos × 2 bytes
    num_frames = len(data) // frame_size
    
    print(f"Potential frames: {num_frames}")
    
    valid_frames = 0
    for i in range(min(10, num_frames)):  # Show first 10 frames
        offset = i * frame_size
        try:
            servos = struct.unpack('<4H', data[offset:offset+8])
            
            # Check if in PWM range
            in_range = all(500 <= s <= 2500 for s in servos)
            
            if in_range:
                valid_frames += 1
                print(f"  Frame {i:3d}: [{servos[0]:4d}, {servos[1]:4d}, {servos[2]:4d}, {servos[3]:4d}] µs {'✓' if in_range else '✗'}")
        except:
            break
    
    if num_frames > 10:
        print(f"  ... ({num_frames - 10} more frames)")
    
    print(f"Valid PWM frames: {valid_frames}/{min(10, num_frames)}")


def analyze_as_angles(data):
    """Analyze assuming angle degrees format"""
    frame_size = 8  # 4 servos × 2 bytes
    num_frames = len(data) // frame_size
    
    print(f"Potential frames: {num_frames}")
    
    valid_frames = 0
    for i in range(min(10, num_frames)):  # Show first 10 frames
        offset = i * frame_size
        try:
            servos = struct.unpack('<4H', data[offset:offset+8])
            
            # Check if in angle range
            in_range = all(0 <= s <= 180 for s in servos)
            
            if in_range:
                valid_frames += 1
                print(f"  Frame {i:3d}: [{servos[0]:3d}°, {servos[1]:3d}°, {servos[2]:3d}°, {servos[3]:3d}°] {'✓' if in_range else '✗'}")
        except:
            break
    
    if num_frames > 10:
        print(f"  ... ({num_frames - 10} more frames)")
    
    print(f"Valid angle frames: {valid_frames}/{min(10, num_frames)}")


def dump_hex(data, offset, length):
    """Dump hex data"""
    for i in range(0, length, 16):
        hex_str = ' '.join(f'{b:02x}' for b in data[offset+i:offset+i+16])
        ascii_str = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in data[offset+i:offset+i+16])
        print(f"{offset+i:08x}  {hex_str:<48}  {ascii_str}")


def show_statistics(data):
    """Show file statistics"""
    # Byte value distribution
    byte_counts = [0] * 256
    for b in data:
        byte_counts[b] += 1
    
    # Find most common bytes
    common = sorted(enumerate(byte_counts), key=lambda x: x[1], reverse=True)[:5]
    print("Most common bytes:")
    for val, count in common:
        print(f"  0x{val:02x} ({val:3d}): {count:5d} times ({count*100/len(data):.1f}%)")
    
    # Check for patterns
    print("\nPattern detection:")
    
    # Check for repeating sequences
    for seq_len in [2, 4, 8]:
        repeats = find_repeating_sequences(data, seq_len)
        if repeats:
            print(f"  {seq_len}-byte sequences: {len(repeats)} unique patterns")


def find_repeating_sequences(data, length):
    """Find repeating byte sequences"""
    sequences = {}
    for i in range(len(data) - length):
        seq = data[i:i+length]
        seq_tuple = tuple(seq)
        sequences[seq_tuple] = sequences.get(seq_tuple, 0) + 1
    
    # Return sequences that appear more than once
    return {k: v for k, v in sequences.items() if v > 1}


def analyze_directory(directory):
    """Analyze all MOT files in directory"""
    mot_files = list(Path(directory).glob("*.mot"))
    
    if not mot_files:
        print(f"No .mot files found in {directory}")
        return
    
    print(f"Found {len(mot_files)} MOT files")
    
    for filepath in sorted(mot_files):
        analyze_mot_file(filepath)
        
        if len(mot_files) > 1:
            response = input("\nPress Enter for next file, or 'q' to quit: ")
            if response.lower() == 'q':
                break


def compare_mot_files(file1, file2):
    """Compare two MOT files"""
    print(f"\n{'='*70}")
    print(f"Comparing MOT files")
    print(f"{'='*70}")
    
    with open(file1, 'rb') as f:
        data1 = f.read()
    with open(file2, 'rb') as f:
        data2 = f.read()
    
    print(f"File 1: {file1.name} ({len(data1)} bytes)")
    print(f"File 2: {file2.name} ({len(data2)} bytes)")
    
    # Find common header
    common_len = 0
    for i in range(min(len(data1), len(data2))):
        if data1[i] == data2[i]:
            common_len += 1
        else:
            break
    
    print(f"\nCommon header: {common_len} bytes")
    
    if common_len > 0:
        print("Common header data:")
        dump_hex(data1, 0, min(common_len, 64))


def main():
    if len(sys.argv) < 2:
        print("MOT File Analyzer")
        print("=" * 70)
        print("\nUsage:")
        print("  python analyze_mot_files.py <file.mot>          # Analyze single file")
        print("  python analyze_mot_files.py <directory>         # Analyze all .mot files")
        print("  python analyze_mot_files.py <file1> <file2>     # Compare two files")
        print("\nExample:")
        print("  python analyze_mot_files.py extracted_animations/mot/")
        print("  python analyze_mot_files.py motion_0000.mot")
        return
    
    path = Path(sys.argv[1])
    
    if len(sys.argv) == 3:
        # Compare mode
        file2 = Path(sys.argv[2])
        if path.is_file() and file2.is_file():
            compare_mot_files(path, file2)
        else:
            print("Error: Both arguments must be files for comparison")
    elif path.is_file():
        # Single file mode
        analyze_mot_file(path)
    elif path.is_dir():
        # Directory mode
        analyze_directory(path)
    else:
        print(f"Error: {path} not found")


if __name__ == "__main__":
    main()
