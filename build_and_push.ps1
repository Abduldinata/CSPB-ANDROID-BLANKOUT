# CSPB Build + Hot Push for KernelSU (kernel root, not Magisk)
# Usage: Right-click -> Run with PowerShell, or: powershell -ExecutionPolicy Bypass -File .\build_and_push.ps1

$NDK_BUILD = "C:\Users\gitzr\AppData\Local\Android\Sdk\ndk\30.0.14904198\ndk-build.cmd"
$PROJ_DIR  = "C:\CSPB_PROJECT\CSPB_ANDROID_BLANKOUT\CSPB-ANDROID-OPEN-SOURCE"
$SO_DIR    = "$PROJ_DIR\libs\arm64-v8a"
$PKG       = "com.cspb.blankout"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  CSPB Build + Hot Push (KernelSU)" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

# === Step 1: Build ===
Write-Host "`n[1/3] Building native libs..." -ForegroundColor Yellow
$buildLog = "$PROJ_DIR\build_log.txt"
& cmd /c "`"$NDK_BUILD`" APP_ABI=arm64-v8a NDK_PROJECT_PATH=`"$PROJ_DIR`" APP_BUILD_SCRIPT=`"$PROJ_DIR\jni\Android.mk`" > `"$buildLog`" 2>&1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "[FAIL] Build failed! Errors:" -ForegroundColor Red
    Get-Content $buildLog | Select-String "error:|Error|FAILED"
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "[OK] Build success." -ForegroundColor Green

# === Step 2: Find nativeLibraryDir via KernelSU ===
Write-Host "`n[2/3] Finding native lib dir on device (KernelSU)..." -ForegroundColor Yellow

# With KernelSU, use: adb shell su 0 -c "..."
$libDir = adb shell su 0 -c "pm dump $PKG | grep nativeLibraryDir" 2>$null
if (-not $libDir) {
    # Fallback: try without su (some KernelSU configs allow adb shell as root already)
    $libDir = adb shell "pm dump $PKG | grep nativeLibraryDir" 2>$null
}

if (-not $libDir) {
    Write-Host "[ERROR] Could not find nativeLibraryDir. Is the app installed?" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Parse: "    nativeLibraryDir=/data/app/.../lib/arm64"
$nativeLibPath = ($libDir -split "=", 2)[1].Trim()

if (-not $nativeLibPath -or $nativeLibPath -eq "") {
    Write-Host "[ERROR] Could not parse path from: $libDir" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[INFO] Native lib path: $nativeLibPath" -ForegroundColor Cyan

# === Step 3: Push .so files via KernelSU ===
Write-Host "`n[3/3] Pushing .so files to device..." -ForegroundColor Yellow

$serverSo = "$SO_DIR\libcspb_server_android_arm64.so"
$clientSo = "$SO_DIR\libcspb_client_android_arm64.so"

# Push via adb, then use su to move into protected directory
# First push to /sdcard (accessible without root), then su cp to target
Write-Host "  Pushing server lib..." -ForegroundColor Gray
adb push $serverSo "/sdcard/libcspb_server_android_arm64.so"
adb shell su 0 -c "cp /sdcard/libcspb_server_android_arm64.so `"$nativeLibPath/libcspb_server_android_arm64.so`" && chmod 755 `"$nativeLibPath/libcspb_server_android_arm64.so`" && echo OK_SERVER"

Write-Host "  Pushing client lib..." -ForegroundColor Gray
adb push $clientSo "/sdcard/libcspb_client_android_arm64.so"
adb shell su 0 -c "cp /sdcard/libcspb_client_android_arm64.so `"$nativeLibPath/libcspb_client_android_arm64.so`" && chmod 755 `"$nativeLibPath/libcspb_client_android_arm64.so`" && echo OK_CLIENT"

# Clean up sdcard temp files
adb shell "rm /sdcard/libcspb_server_android_arm64.so /sdcard/libcspb_client_android_arm64.so"

Write-Host "`n[DONE] Build + Push complete! Launch the game now." -ForegroundColor Green
Write-Host "If it crashes, check log with: adb logcat -s Xash3d,CSPB" -ForegroundColor Gray
Read-Host "Press Enter to exit"
