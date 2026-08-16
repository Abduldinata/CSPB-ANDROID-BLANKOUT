@echo off
setlocal

set "NDK_BUILD=C:\Users\gitzr\AppData\Local\Android\Sdk\ndk\30.0.14904198\ndk-build.cmd"
set "PROJ_DIR=C:\CSPB_PROJECT\CSPB_ANDROID_BLANKOUT\CSPB-ANDROID-OPEN-SOURCE"
set "SO_DIR=%PROJ_DIR%\libs\arm64-v8a"

echo ============================================
echo   CSPB Build + Hot Push (Root Device)
echo ============================================

echo [1/3] Building native libs (ndk-build)...
call "%NDK_BUILD%" APP_ABI=arm64-v8a NDK_PROJECT_PATH="%PROJ_DIR%" APP_BUILD_SCRIPT="%PROJ_DIR%\jni\Android.mk" > "%PROJ_DIR%\build_log.txt" 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [FAIL] Build failed! Check build_log.txt
    type "%PROJ_DIR%\build_log.txt" | findstr /C:"error:" /C:"Error" /C:"FAILED"
    pause
    exit /b 1
)
echo [OK] Build success.

echo [2/3] Getting root access and finding lib dir...
adb root
timeout /t 2 >nul

for /f "tokens=* usebackq" %%i in (`adb shell "pm dump com.cspb.blankout | grep nativeLibraryDir"`) do set "LIBLINE=%%i"
for /f "tokens=2 delims==" %%a in ("%LIBLINE%") do set "NATIVE_LIB_DIR=%%a"
set "NATIVE_LIB_DIR=%NATIVE_LIB_DIR: =%"

if "%NATIVE_LIB_DIR%"=="" (
    echo [ERROR] App not found on device. Make sure com.cspb.blankout is installed.
    pause
    exit /b 1
)
echo [INFO] Target: %NATIVE_LIB_DIR%

echo [3/3] Pushing updated .so files...
adb push "%SO_DIR%\libcspb_server_android_arm64.so" "%NATIVE_LIB_DIR%/libcspb_server_android_arm64.so"
adb push "%SO_DIR%\libcspb_client_android_arm64.so" "%NATIVE_LIB_DIR%/libcspb_client_android_arm64.so"

echo.
echo [DONE] Build + Push complete! Launch the game now.
pause
