import subprocess
import re
import sys

def run(cmd, check_su_error=False):
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

print("1. Pushing to /data/local/tmp ...")
run('adb push "CSPB-ANDROID-OPEN-SOURCE/libs/arm64-v8a/libcspb_server_android_arm64.so" "/data/local/tmp/"')
run('adb push "CSPB-ANDROID-OPEN-SOURCE/libs/arm64-v8a/libcspb_client_android_arm64.so" "/data/local/tmp/"')

print("2. Finding nativeLibraryDir ...")
dump = run('adb shell "dumpsys package com.cspb.blankout"')
match = re.search(r'(?:legacyNativeLibraryDir|nativeLibraryPath|nativeLibraryDir)=([^\s]+)', dump)
if not match:
    print("Could not find nativeLibraryDir in dumpsys. Trying another method...")
    # Alternative: find it dynamically
    out = run('adb shell "su -c \\"find /data/app -name com.cspb.blankout* -type d | head -n 1\\""')
    if out and "com.cspb.blankout" in out:
        lib_dir = out.strip() + "/lib/arm64"
    else:
        print("Could not find nativeLibraryDir. Is the app installed?")
        sys.exit(1)
else:
    lib_dir = match.group(1)
    if not lib_dir.endswith("arm64"):
        lib_dir = lib_dir + "/arm64"

print(f"Target: {lib_dir}")

print("3. Copying via KernelSU ...")
cmd_cp = f'adb shell su -c "cp /data/local/tmp/libcspb_*.so {lib_dir}/"'
run(cmd_cp, check_su_error=True)

cmd_chmod = f'adb shell su -c "chmod 755 {lib_dir}/libcspb_*.so"'
run(cmd_chmod, check_su_error=True)

print("\n[SUCCESS] Libraries hot-swapped successfully! You can launch the game now.")
