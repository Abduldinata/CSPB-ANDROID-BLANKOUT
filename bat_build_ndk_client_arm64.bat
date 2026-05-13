@echo off
setlocal

rem Build CSPB client shared library (arm64-v8a)

set "ROOT_DIR=E:\Games\PROJECT_LOBBY_CSPB\com.cspb.m"
set "NDK_BUILD=C:\Users\gitzr\AppData\Local\Android\Sdk\ndk\30.0.14904198\ndk-build.cmd"
set "CSPB_JNI_DIR=%ROOT_DIR%\CSPB-ANDROID-OPEN-SOURCE"

echo [NDK] Build client arm64
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
call "%NDK_BUILD%" APP_ABI=arm64-v8a APP_PLATFORM=android-21 APP_MODULES=cspb_client_android_arm64 -j8
if %ERRORLEVEL% NEQ 0 (
  echo [ERROR] NDK build failed (client)
  exit /b %ERRORLEVEL%
)

echo [OK] Built: %CSPB_JNI_DIR%\libs\arm64-v8a\libcspb_client_android_arm64.so
exit /b 0
