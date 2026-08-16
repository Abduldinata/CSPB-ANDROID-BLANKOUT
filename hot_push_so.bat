@echo off
setlocal

set "SO_DIR=C:\CSPB_PROJECT\CSPB_ANDROID_BLANKOUT\CSPB-ANDROID-OPEN-SOURCE\libs\arm64-v8a"
set "SERVER_SO=%SO_DIR%\libcspb_server_android_arm64.so"
set "CLIENT_SO=%SO_DIR%\libcspb_client_android_arm64.so"

echo [1/4] Checking ADB connection...
adb devices
adb shell "echo connected" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] No device connected. Enable USB Debugging and connect your phone.
    pause
    exit /b 1
)

echo [2/4] Finding native library dir on device...
for /f "tokens=* usebackq" %%i in (`adb shell "pm dump com.cspb.blankout | grep nativeLibraryDir"`) do (
    set "LIBLINE=%%i"
)

rem Extract the path after the = sign
for /f "tokens=2 delims==" %%a in ("%LIBLINE%") do set "NATIVE_LIB_DIR=%%a"
set "NATIVE_LIB_DIR=%NATIVE_LIB_DIR: =%"

if "%NATIVE_LIB_DIR%"=="" (
    echo [ERROR] Could not find nativeLibraryDir for com.cspb.blankout.
    echo Make sure the app is installed.
    pause
    exit /b 1
)

echo [INFO] Native lib dir: %NATIVE_LIB_DIR%

echo [3/4] Getting root access...
adb root
timeout /t 2 >nul

echo [4/4] Pushing .so files to device...
adb push "%SERVER_SO%" "%NATIVE_LIB_DIR%/libcspb_server_android_arm64.so"
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to push server .so
    pause
    exit /b 1
)

adb push "%CLIENT_SO%" "%NATIVE_LIB_DIR%/libcspb_client_android_arm64.so"
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to push client .so
    pause
    exit /b 1
)

echo.
echo [DONE] Libraries pushed! You can now start the game.
echo If it still crashes, run: adb logcat -s Xash3d CSPB
pause
