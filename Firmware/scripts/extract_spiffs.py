#!/usr/bin/env python3
"""
Advanced SPIFFS extractor for EMO ESP32 firmware
Extracts .avi, .mot, .mp3, and .json files from storage partition
"""

import os
import struct
import sys
from pathlib import Path
import subprocess

def try_mkspiffs_extraction(storage_file, output_dir):
    """Try to use mkspiffs tool if available"""
    print("\nAttempting extraction with mkspiffs tool...")
    
    # Check if mkspiffs is available
    mkspiffs_paths = [
        "mkspiffs",
        "mkspiffs.exe",
        os.path.expanduser("~/.platformio/packages/tool-mkspiffs/mkspiffs"),
        os.path.expanduser("~/.platformio/packages/tool-mkspiffs/mkspiffs.exe"),
    ]
    
    mkspiffs_cmd = None
    for path in mkspiffs_paths:
        try:
            result = subprocess.run([path, "--version"], 
                                  capture_output=True, 
                                  timeout=5)
            if result.returncode == 0 or b"mkspiffs" in result.stdout or b"mkspiffs" in result.stderr:
                mkspiffs_cmd = path
                print(f"Found mkspiffs: {path}")
                break
        except:
            continue
    
    if not mkspiffs_cmd:
        print("mkspiffs not found. Using manual extraction method.")
        return False
    
    # Try to unpack with mkspiffs
    try:
        # mkspiffs -u output_dir -p 256 -b 4096 -s 1048576 storage.bin
        cmd = [
            mkspiffs_cmd,
            "-u", output_dir,
            "-p", "256",      # Page size
            "-b", "4096",     # Block size
            "-s", "1048576",  # Size (1MB)
            storage_file
        ]
        
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✓ Successfully extracted with mkspiffs!")
            return True
        else:
            print(f"mkspiffs failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error running mkspiffs: {e}")
        return False


def manual_extraction(storage_file, output_dir):
    """Manual extraction by searching for file signatures"""
    print("\nPerforming manual extraction...")
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    with open(storage_file, 'rb') as f:
        data = f.read()
    
    print(f"Storage size: {len(data):,} bytes")
    
    stats = {
        'avi': 0,
        'mp3': 0,
        'mot': 0,
        'json': 0,
        'txt': 0
    }
    
    # Create subdirectories
    (output_path / "avi").mkdir(exist_ok=True)
    (output_path / "mot").mkdir(exist_ok=True)
    (output_path / "mp3").mkdir(exist_ok=True)
    (output_path / "json").mkdir(exist_ok=True)
    
    # Extract AVI files
    print("\n[1/5] Extracting AVI files...")
    stats['avi'] = extract_avi_files(data, output_path / "avi")
    
    # Extract MP3 files
    print("\n[2/5] Extracting MP3 files...")
    stats['mp3'] = extract_mp3_files(data, output_path / "mp3")
    
    # Extract JSON files
    print("\n[3/5] Extracting JSON files...")
    stats['json'] = extract_json_files(data, output_path / "json")
    
    # Extract MOT files
    print("\n[4/5] Extracting MOT files...")
    stats['mot'] = extract_mot_files(data, output_path / "mot")
    
    # Find filenames
    print("\n[5/5] Searching for filenames...")
    filenames = find_filenames(data)
    
    if filenames:
        with open(output_path / "filenames.txt", 'w') as f:
            f.write("Filenames found in SPIFFS:\n")
            f.write("=" * 60 + "\n\n")
            for name, offset in filenames:
                f.write(f"0x{offset:08x}: {name}\n")
        print(f"  Found {len(filenames)} filenames (saved to filenames.txt)")
    
    return stats


def extract_avi_files(data, output_dir):
    """Extract AVI video files"""
    count = 0
    i = 0
    
    while i < len(data) - 12:
        # Look for RIFF header
        if data[i:i+4] == b'RIFF':
            # Check for AVI signature
            if data[i+8:i+12] == b'AVI ':
                # Get file size from RIFF header
                size = struct.unpack('<I', data[i+4:i+8])[0] + 8
                
                # Sanity check
                if size > 10 * 1024 * 1024:  # Max 10MB
                    i += 4
                    continue
                
                if i + size > len(data):
                    size = len(data) - i
                
                file_data = data[i:i+size]
                
                # Try to find a meaningful name
                filename = f"animation_{count:04d}.avi"
                
                # Look backwards for potential filename
                name = find_nearby_filename(data, i, '.avi')
                if name:
                    filename = name.replace('/', '_').replace('\\', '_')
                    if not filename.endswith('.avi'):
                        filename += '.avi'
                
                filepath = output_dir / filename
                with open(filepath, 'wb') as f:
                    f.write(file_data)
                
                print(f"  ✓ {filename} ({size:,} bytes)")
                count += 1
                i += size
            else:
                i += 4
        else:
            i += 1
    
    return count


def extract_mp3_files(data, output_dir):
    """Extract MP3 audio files"""
    count = 0
    i = 0
    
    while i < len(data) - 10:
        # Look for ID3 tag or MP3 frame sync
        if data[i:i+3] == b'ID3' or (data[i] == 0xFF and (data[i+1] & 0xE0) == 0xE0):
            start = i
            
            # Find end of MP3 file (look for next file signature or silence)
            end = start + 1024 * 1024  # Max 1MB
            
            # Look for next file start
            next_sig = find_next_signature(data, start + 100, [b'RIFF', b'ID3', b'\xFF\xFB'])
            if next_sig and next_sig < end:
                end = next_sig
            
            if end > len(data):
                end = len(data)
            
            size = end - start
            if size < 1000:  # Too small
                i += 1
                continue
            
            file_data = data[start:end]
            
            filename = f"audio_{count:04d}.mp3"
            
            # Look for nearby filename
            name = find_nearby_filename(data, start, '.mp3')
            if name:
                filename = name.replace('/', '_').replace('\\', '_')
                if not filename.endswith('.mp3'):
                    filename += '.mp3'
            
            filepath = output_dir / filename
            with open(filepath, 'wb') as f:
                f.write(file_data)
            
            print(f"  ✓ {filename} ({size:,} bytes)")
            count += 1
            i = end
        else:
            i += 1
    
    return count


def extract_json_files(data, output_dir):
    """Extract JSON configuration files"""
    count = 0
    i = 0
    
    while i < len(data) - 10:
        if data[i] == ord('{'):
            # Try to find matching closing brace
            depth = 0
            end = i
            
            for j in range(i, min(i + 100000, len(data))):
                if data[j] == ord('{'):
                    depth += 1
                elif data[j] == ord('}'):
                    depth -= 1
                    if depth == 0:
                        end = j + 1
                        break
            
            if end > i + 10:  # At least some content
                file_data = data[i:end]
                
                # Validate it's actually JSON
                try:
                    text = file_data.decode('utf-8', errors='ignore')
                    if text.count('{') > 0 and text.count('}') > 0:
                        filename = f"config_{count:04d}.json"
                        
                        # Look for nearby filename
                        name = find_nearby_filename(data, i, '.json')
                        if name:
                            filename = name.replace('/', '_').replace('\\', '_')
                            if not filename.endswith('.json'):
                                filename += '.json'
                        
                        filepath = output_dir / filename
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(text)
                        
                        print(f"  ✓ {filename} ({len(file_data)} bytes)")
                        count += 1
                        i = end
                    else:
                        i += 1
                except:
                    i += 1
            else:
                i += 1
        else:
            i += 1
    
    return count


def extract_mot_files(data, output_dir):
    """Extract MOT motion files"""
    count = 0
    i = 0
    
    # MOT files contain servo angle data
    # Look for sequences of 16-bit values in servo range
    
    while i < len(data) - 100:
        if is_mot_data(data, i):
            # Found potential MOT file
            size = estimate_mot_size(data, i)
            
            if size >= 24:  # At least 2 frames
                file_data = data[i:i+size]
                
                filename = f"motion_{count:04d}.mot"
                
                # Look for nearby filename
                name = find_nearby_filename(data, i, '.mot')
                if name:
                    filename = name.replace('/', '_').replace('\\', '_')
                    if not filename.endswith('.mot'):
                        filename += '.mot'
                
                filepath = output_dir / filename
                with open(filepath, 'wb') as f:
                    f.write(file_data)
                
                print(f"  ✓ {filename} ({size} bytes)")
                count += 1
                i += size
            else:
                i += 1
        else:
            i += 1
    
    return count


def is_mot_data(data, offset):
    """Check if data looks like MOT motion data"""
    if offset + 12 > len(data):
        return False
    
    try:
        # Check for 4 consecutive 16-bit values in servo range
        values = struct.unpack('<4H', data[offset:offset+8])
        
        # PWM range: 500-2500 microseconds
        # Angle range: 0-180 degrees
        in_pwm_range = all(500 <= v <= 2500 for v in values)
        in_angle_range = all(0 <= v <= 180 for v in values)
        
        # Also check next frame for consistency
        if offset + 20 <= len(data):
            next_values = struct.unpack('<4H', data[offset+12:offset+20])
            next_pwm = all(500 <= v <= 2500 for v in next_values)
            next_angle = all(0 <= v <= 180 for v in next_values)
            
            return (in_pwm_range and next_pwm) or (in_angle_range and next_angle)
        
        return in_pwm_range or in_angle_range
    except:
        return False


def estimate_mot_size(data, offset):
    """Estimate MOT file size"""
    frame_size = 12  # 4 servos × 2 bytes + duration + flags
    max_frames = 1000
    size = 0
    
    for i in range(max_frames):
        pos = offset + i * frame_size
        if pos + frame_size > len(data):
            break
        if not is_mot_data(data, pos):
            break
        size += frame_size
    
    return size


def find_nearby_filename(data, offset, extension):
    """Look for filename near the data offset"""
    # Search backwards up to 1KB
    search_start = max(0, offset - 1024)
    search_end = offset
    
    for i in range(search_end - 1, search_start, -1):
        if data[i] == ord('/'):
            # Found potential path start
            end = i + 1
            while end < search_end and end < i + 256:
                c = data[end]
                if 32 <= c <= 126 and c not in [0, ord('*'), ord('?')]:
                    end += 1
                else:
                    break
            
            if end > i + 4:
                try:
                    path = data[i:end].decode('ascii', errors='ignore')
                    if extension in path:
                        return path.split('/')[-1]  # Get filename only
                except:
                    pass
    
    return None


def find_next_signature(data, start, signatures):
    """Find next occurrence of any signature"""
    positions = []
    for sig in signatures:
        pos = data.find(sig, start)
        if pos != -1:
            positions.append(pos)
    
    return min(positions) if positions else None


def find_filenames(data):
    """Find all filenames in SPIFFS"""
    filenames = []
    i = 0
    
    while i < len(data) - 4:
        if data[i] == ord('/'):
            end = i + 1
            while end < len(data) and end < i + 256:
                c = data[end]
                if 32 <= c <= 126 and c not in [0, ord('*'), ord('?'), ord('<'), ord('>')]:
                    end += 1
                else:
                    break
            
            if end > i + 4:
                try:
                    path = data[i:end].decode('ascii', errors='ignore')
                    if any(ext in path for ext in ['.avi', '.mot', '.mp3', '.json', '.txt', '.bin']):
                        filenames.append((path, i))
                except:
                    pass
        
        i += 1
    
    return filenames


def main():
    storage_file = "emo_esp32_firmware splitted/storage.bin"
    output_dir = "extracted_animations"
    
    print("=" * 70)
    print("EMO ESP32 Animation Extractor")
    print("=" * 70)
    print(f"Input:  {storage_file}")
    print(f"Output: {output_dir}/")
    print("=" * 70)
    
    if not os.path.exists(storage_file):
        print(f"\n❌ Error: {storage_file} not found!")
        print("\nMake sure you have extracted the firmware partitions first.")
        return 1
    
    # Try mkspiffs first
    success = try_mkspiffs_extraction(storage_file, output_dir)
    
    if not success:
        # Fall back to manual extraction
        stats = manual_extraction(storage_file, output_dir)
        
        print("\n" + "=" * 70)
        print("Extraction Complete!")
        print("=" * 70)
        print(f"  AVI files:  {stats['avi']}")
        print(f"  MP3 files:  {stats['mp3']}")
        print(f"  MOT files:  {stats['mot']}")
        print(f"  JSON files: {stats['json']}")
        print("=" * 70)
        print(f"\n✓ Files extracted to: {output_dir}/")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
