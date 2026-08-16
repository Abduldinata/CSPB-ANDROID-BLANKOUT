@echo off
setlocal

set "NDK_BUILD=C:\Users\gitzr\AppData\Local\Android\Sdk\ndk\30.0.14904198\ndk-build.cmd"
set "PROJ_DIR=C:\CSPB_PROJECT\CSPB_ANDROID_BLANKOUT"
set "SRC_DIR=%PROJ_DIR%\CSPB-ANDROID-OPEN-SOURCE"
set "APK_OUT=%PROJ_DIR%\xash3d-fwgs\android\app\build\outputs\apk\release\app-release.apk"

echo ============================================
echo   CSPB Full Build ^& Install (No Root Needed)
echo ============================================

echo [1/3] Building native libs (C++)...
call "%NDK_BUILD%" APP_ABI=arm64-v8a NDK_PROJECT_PATH="%SRC_DIR%" APP_BUILD_SCRIPT="%SRC_DIR%\jni\Android.mk" > "%SRC_DIR%\build_log.txt" 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [FAIL] Build failed! Check build_log.txt
    type "%SRC_DIR%\build_log.txt" | findstr /C:"error:" /C:"Error" /C:"FAILED"
    pause
    exit /b 1
)

echo [2/3] Building Release APK via Gradle...
call "%PROJ_DIR%\bat_build_release_signed.bat"
if %ERRORLEVEL% NEQ 0 (
    echo [FAIL] Gradle build failed!
    pause
    exit /b 1
)

echo [3/3] Installing APK to device...
adb install -r "%APK_OUT%"
if %ERRORLEVEL% NEQ 0 (
    echo [FAIL] Could not install APK to device. Check ADB connection.
    pause
    exit /b 1
)

echo.
echo [DONE] Success! The new engine with C++ fixes is installed.
echo You can now open the game.
pause
