import wave
import os
import shutil

ui_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\ui"

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    print("NumPy not found. Installing numpy or using simpler approach...")

def reduce_wav_numpy(input_path, output_path):
    """Reduce WAV file using numpy"""
    with wave.open(input_path, 'rb') as wav_in:
        # Get parameters
        channels = wav_in.getnchannels()
        width = wav_in.getsampwidth()
        rate = wav_in.getframerate()
        frames = wav_in.getnframes()
        
        # Read audio
        audio_bytes = wav_in.readframes(frames)
        
        print(f"  Original: {channels}ch, {width*8}bit, {rate}Hz, {len(audio_bytes)/1024:.1f}KB")
        
        # Convert bytes to numpy array
        if width == 1:
            dtype = np.uint8
        elif width == 2:
            dtype = np.int16
        else:
            dtype = np.int32
        
        audio = np.frombuffer(audio_bytes, dtype=dtype)
        
        # Stereo to mono: average channels
        if channels == 2:
            audio = audio.reshape(-1, 2).mean(axis=1).astype(dtype)
        
        # Downsample from original rate to 22050 Hz
        if rate != 22050:
            step = rate // 22050
            audio = audio[::step]
        
        # Convert to 8-bit
        if width == 2:  # 16-bit to 8-bit
            audio = ((audio.astype(np.float32) / 256) + 128).astype(np.uint8)
        elif width == 4:  # 32-bit to 8-bit
            audio = ((audio.astype(np.float64) / 16777216) + 128).astype(np.uint8)
        
        # Write optimized WAV
        with wave.open(output_path, 'wb') as wav_out:
            wav_out.setnchannels(1)
            wav_out.setsampwidth(1)
            wav_out.setframerate(22050)
            wav_out.writeframes(audio.tobytes())
        
        new_size = os.path.getsize(output_path)
        old_size = os.path.getsize(input_path)
        print(f"  Optimized: 1ch, 8bit, 22050Hz, {new_size/1024:.1f}KB")
        print(f"  Reduction: {(1 - new_size/old_size)*100:.1f}%\n")
        return True

def reduce_wav_simple(input_path, output_path):
    """Simple reduction: just downsample rate, keep other params"""
    with wave.open(input_path, 'rb') as wav_in:
        channels = wav_in.getnchannels()
        width = wav_in.getsampwidth()
        rate = wav_in.getframerate()
        frames = wav_in.getnframes()
        
        audio_bytes = wav_in.readframes(frames)
        print(f"  Original: {channels}ch, {width*8}bit, {rate}Hz, {len(audio_bytes)/1024:.1f}KB")
        
        # Simple approach: skip every other frame to halve rate
        step = 2 if rate > 22050 else 1
        frame_size = channels * width
        reduced_audio = audio_bytes[::step*frame_size]
        
        with wave.open(output_path, 'wb') as wav_out:
            wav_out.setnchannels(channels)
            wav_out.setsampwidth(width)
            wav_out.setframerate(rate // step)
            wav_out.writeframes(reduced_audio)
        
        new_size = os.path.getsize(output_path)
        old_size = os.path.getsize(input_path)
        print(f"  Optimized: {channels}ch, {width*8}bit, {rate//step}Hz, {new_size/1024:.1f}KB")
        print(f"  Reduction: {(1 - new_size/old_size)*100:.1f}%\n")
        return True

# Backup and optimize
backup_dir = os.path.join(ui_dir, "backup_original")
os.makedirs(backup_dir, exist_ok=True)

print("=== WAV File Optimizer ===\n")
print(f"Method: {'NumPy (best quality)' if HAS_NUMPY else 'Simple downsample'}\n")
print(f"Backing up to: {backup_dir}\n")

wav_files = [f for f in os.listdir(ui_dir) if f.endswith('.wav')]

for wav_file in wav_files:
    input_path = os.path.join(ui_dir, wav_file)
    backup_path = os.path.join(backup_dir, wav_file)
    temp_path = os.path.join(ui_dir, f"temp_{wav_file}")
    
    print(f"Processing: {wav_file}")
    
    # Backup
    if not os.path.exists(backup_path):
        shutil.copy2(input_path, backup_path)
    
    try:
        # Choose method based on availability
        if HAS_NUMPY:
            reduce_wav_numpy(input_path, temp_path)
        else:
            reduce_wav_simple(input_path, temp_path)
        
        os.replace(temp_path, input_path)
        print(f"  [OK] Success\n")
    except Exception as e:
        print(f"  [ERROR] Error: {e}\n")
        if os.path.exists(temp_path):
            os.remove(temp_path)

print("=== Complete ===")
print(f"Backups in: {backup_dir}")
