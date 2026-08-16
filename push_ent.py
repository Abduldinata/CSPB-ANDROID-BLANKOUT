import os
import subprocess

def run_cmd(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    else:
        print(f"Success: {result.stdout}")
    return result.returncode == 0

def main():
    # Push to temp
    run_cmd("adb push data/com.cspb.blankout/files/cspb/downloaded/maps/ent/pb_mstation.ent /data/local/tmp/pb_mstation.ent")
    
    # KSU copy
    ksu_cmd = (
        'adb shell "su -c \''
        'cp /data/local/tmp/pb_mstation.ent /data/data/com.cspb.blankout/files/cspb/downloaded/maps/ent/pb_mstation.ent && touch /data/data/com.cspb.blankout/files/cspb/downloaded/maps/ent/pb_mstation.ent && '
        'chmod 644 /data/data/com.cspb.blankout/files/cspb/downloaded/maps/ent/pb_mstation.ent && '
        'chown 10263:10263 /data/data/com.cspb.blankout/files/cspb/downloaded/maps/ent/pb_mstation.ent'
        '\'"'
    )
    run_cmd(ksu_cmd)
    
    # Launch game to test
    run_cmd('adb shell "am force-stop com.cspb.blankout"')
    run_cmd('adb shell "am start -n com.cspb.blankout/in.celest.xash3d.SplashActivity"')
    
    print("Done! Game launched.")

if __name__ == "__main__":
    main()
