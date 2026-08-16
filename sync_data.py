import subprocess
import sys
import os
import json

def run(cmd, check_su_error=False):
    print(f"Running: {cmd}")
    try:
        out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode('utf-8').strip()
        if check_su_error and ("inaccessible or not found" in out or "Permission denied" in out):
            print(f"[ERROR] KernelSU error: {out}")
            print(">>> PLEASE OPEN KERNELSU APP ON YOUR PHONE AND GRANT 'SUPERUSER' PERMISSION TO 'Shell' (UID 2000) <<<")
            sys.exit(1)
        return out
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {cmd}")
        print(e.output.decode('utf-8') if e.output else "")
        sys.exit(1)

def get_files_with_mtime(directory):
    files_state = {}
    for root, _, files in os.walk(directory):
        for f in files:
            filepath = os.path.join(root, f)
            rel_path = os.path.relpath(filepath, directory).replace('\\', '/')
            files_state[rel_path] = os.path.getmtime(filepath)
    return files_state

def main():
    source_dir = "data/com.cspb.blankout/files/cspb"
    state_file = ".sync_state.json"
    
    if not os.path.exists(source_dir):
        print(f"ERROR: {source_dir} not found!")
        sys.exit(1)

    # Load previous state
    prev_state = {}
    if os.path.exists(state_file):
        try:
            with open(state_file, 'r') as f:
                prev_state = json.load(f)
        except Exception:
            pass

    # Get current state
    curr_state = get_files_with_mtime(source_dir)
    
    # Find changed or new files
    changed_files = []
    for rel_path, mtime in curr_state.items():
        if rel_path not in prev_state or prev_state[rel_path] != mtime:
            changed_files.append(rel_path)

    if not changed_files:
        print("Tidak ada file yang berubah. Semua sudah sinkron.")
        sys.exit(0)

    print(f"\n[1] Menemukan {len(changed_files)} file yang berubah/baru.")
    print("Mempersiapkan folder sementara di HP (/data/local/tmp/cspb_sync)...")
    run('adb shell "rm -rf /data/local/tmp/cspb_sync"')
    
    print("\n[2] Sinkronisasi file dari PC ke HP...")
    for rel_path in changed_files:
        local_path = os.path.join(source_dir, rel_path)
        remote_path = f"/data/local/tmp/cspb_sync/{rel_path}"
        
        # Buat folder jika belum ada di remote
        remote_dir = "/".join(remote_path.split("/")[:-1])
        run(f'adb shell "mkdir -p {remote_dir}"')
        
        print(f"Pushing: {rel_path}")
        run(f'adb push "{local_path}" "{remote_path}"')

    print("\n[3] Memindahkan file ke folder data game menggunakan akses Root (KernelSU)...")
    # Copy files from temp to app data recursively
    cmd_cp = 'adb shell "su -c \\"cp -rf /data/local/tmp/cspb_sync/* /storage/emulated/0/Android/data/com.cspb.blankout/files/cspb/\\""'
    run(cmd_cp, check_su_error=True)

    print("\n[4] Mengatur permission (chmod)...")
    cmd_chmod = 'adb shell "su -c \\"chmod -R 777 /storage/emulated/0/Android/data/com.cspb.blankout/files/cspb/\\""'
    run(cmd_chmod, check_su_error=True)

    # Save new state
    with open(state_file, 'w') as f:
        json.dump(curr_state, f)

    print("\n[SUCCESS] Sinkronisasi data CSPB selesai! File berhasil dikirim via KernelSU.")

if __name__ == "__main__":
    main()
