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
set "XASH_CXX_ROOT=%ANDROID_PROJECT_DIR%\app\build\intermediates\cxx\RelWithDebInfo"
set "XASH_CXX_FALLBACK=%ANDROID_PROJECT_DIR%\app\.cxx\RelWithDebInfo"

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

set "LATEST_XASH_SO="
for /f "delims=" %%F in ('powershell -NoProfile -Command "$root='%XASH_CXX_ROOT%'; if(Test-Path $root){Get-ChildItem -Path $root -Recurse -Filter libxash.so | Sort-Object LastWriteTime -Descending | Select-Object -First 1 -ExpandProperty FullName}"') do set "LATEST_XASH_SO=%%F"
if not defined LATEST_XASH_SO for /f "delims=" %%F in ('powershell -NoProfile -Command "$root='%XASH_CXX_FALLBACK%'; if(Test-Path $root){Get-ChildItem -Path $root -Recurse -Filter libxash.so | Sort-Object LastWriteTime -Descending | Select-Object -First 1 -ExpandProperty FullName}"') do set "LATEST_XASH_SO=%%F"
if defined LATEST_XASH_SO copy /Y "%LATEST_XASH_SO%" "%ANDROID_PROJECT_JNILIBS%\libxash.so" >NUL
if defined LATEST_XASH_SO echo [OK] Copied libxash: %LATEST_XASH_SO%
if not defined LATEST_XASH_SO echo [WARN] libxash.so not found in CMake outputs yet (skipping)

if "%COPIED%"=="0" (
  echo [ERROR] Nothing copied. Build server/client first.
  exit /b 1
)

echo [OK] Updated files:
dir /-C "%ANDROID_PROJECT_JNILIBS%\libcspb_*android_arm64.so"
exit /b 0
