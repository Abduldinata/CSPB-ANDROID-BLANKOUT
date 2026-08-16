import os
import subprocess

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result

# Path in android 13 is often /sdcard/xash/engine.log or /data/data/com.cspb.blankout/files/xash/engine.log
out = run_cmd('adb shell "su -c \'cat /data/data/com.cspb.blankout/files/cspb/engine.log\'"')
if out.returncode == 0 and out.stdout.strip():
    with open("engine.log", "w") as f:
        f.write(out.stdout)
    print("engine.log extracted!")
else:
    out = run_cmd('adb shell "su -c \'cat /sdcard/xash/engine.log\'"')
    if out.returncode == 0 and out.stdout.strip():
        with open("engine.log", "w") as f:
            f.write(out.stdout)
        print("engine.log extracted from sdcard!")
    else:
        print("Could not find engine.log")
