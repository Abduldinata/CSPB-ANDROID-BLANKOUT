@echo off
setlocal EnableExtensions

rem Copy latest CSPB .so files into Android jniLibs (arm64-v8a)
rem This BAT is intentionally written without IF (...) ELSE (...) blocks
rem to avoid CMD parsing edge cases.

set "ROOT_DIR=C:\CSPB_PROJECT\CSPB_ANDROID_BLANKOUT"
set "CSPB_JNI_DIR=%ROOT_DIR%\CSPB-ANDROID-OPEN-SOURCE"
set "ANDROID_PROJECT_DIR=%ROOT_DIR%\xash3d-fwgs\android"
set "ANDROID_PROJECT_JNILIBS=%ANDROID_PROJECT_DIR%\app\src\main\jniLibs\arm64-v8a"

set "SERVER_SO=%CSPB_JNI_DIR%\libs\arm64-v8a\libcspb_server_android_arm64.so"
set "CLIENT_SO=%CSPB_JNI_DIR%\libs\arm64-v8a\libcspb_client_android_arm64.so"

echo [COPY] CSPB .so -> Android jniLibs arm64-v8a
echo FROM: %CSPB_JNI_DIR%\libs\arm64-v8a
echo TO  : %ANDROID_PROJECT_JNILIBS%

if not exist "%ANDROID_PROJECT_JNILIBS%" mkdir "%ANDROID_PROJECT_JNILIBS%"

set "COPIED=0"

if exist "%SERVER_SO%" copy /Y "%SERVER_SO%" "%ANDROID_PROJECT_JNILIBS%\libcspb_server_android_arm64.so" >NUL
if exist "%SERVER_SO%" echo [OK] Copied server: %SERVER_SO%
if exist "%SERVER_SO%" set "COPIED=1"
if not exist "%SERVER_SO%" echo [WARN] Server .so not found (skipping): %SERVER_SO%

set "VGUI_SO=%ROOT_DIR%\xash3d-fwgs\build\android_arm64-v8a\libvgui_support.so"
if exist "%VGUI_SO%" copy /Y "%VGUI_SO%" "%ANDROID_PROJECT_JNILIBS%\libvgui_support.so" >NUL
if exist "%VGUI_SO%" echo [OK] Copied VGUI support: %VGUI_SO%

if exist "%CLIENT_SO%" copy /Y "%CLIENT_SO%" "%ANDROID_PROJECT_JNILIBS%\libcspb_client_android_arm64.so" >NUL
if exist "%CLIENT_SO%" echo [OK] Copied client: %CLIENT_SO%
if exist "%CLIENT_SO%" set "COPIED=1"
if not exist "%CLIENT_SO%" echo [WARN] Client .so not found (skipping): %CLIENT_SO%

if "%COPIED%"=="0" (
  echo [ERROR] Nothing copied. Build server/client first.
  exit /b 1
)

echo [OK] Updated files:
dir /-C "%ANDROID_PROJECT_JNILIBS%\libcspb_*android_arm64.so"
exit /b 0
