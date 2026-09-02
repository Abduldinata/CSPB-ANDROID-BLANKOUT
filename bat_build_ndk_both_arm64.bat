@echo off
setlocal

rem Build both CSPB server and client shared libraries (arm64-v8a) together

set "ROOT_DIR=C:\CSPB_PROJECT\CSPB_ANDROID_BLANKOUT"
set "NDK_BUILD=C:\Users\gitzr\AppData\Local\Android\Sdk\ndk\30.0.14904198\ndk-build.cmd"
set "CSPB_JNI_DIR=%ROOT_DIR%\CSPB-ANDROID-OPEN-SOURCE"

echo [NDK] Build server + client arm64
echo ROOT: %ROOT_DIR%
echo JNI : %CSPB_JNI_DIR%

if not exist "%NDK_BUILD%" (
  echo [ERROR] NDK build not found: %NDK_BUILD%
  exit /b 1
)
if not exist "%CSPB_JNI_DIR%\jni\Android.mk" (
  echo [ERROR] CSPB JNI project not found: %CSPB_JNI_DIR%
  exit /b 1
)

cd /d "%CSPB_JNI_DIR%"
call "%NDK_BUILD%" APP_ABI=arm64-v8a APP_PLATFORM=android-21 APP_MODULES="cspb_server_android_arm64 cspb_client_android_arm64" -j8
if %ERRORLEVEL% NEQ 0 (
  echo [ERROR] NDK build failed (server + client)
  exit /b %ERRORLEVEL%
)

echo [OK] Built server and client in: %CSPB_JNI_DIR%\libs\arm64-v8a
exit /b 0
