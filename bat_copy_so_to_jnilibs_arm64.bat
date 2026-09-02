@echo off
setlocal EnableExtensions

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

if exist "%SERVER_SO%" (
  copy /Y "%SERVER_SO%" "%ANDROID_PROJECT_JNILIBS%\libcspb_server_android_arm64.so" >NUL
  copy /Y "%SERVER_SO%" "%ANDROID_PROJECT_JNILIBS%\libhl_android_arm64.so" >NUL
  copy /Y "%SERVER_SO%" "%ANDROID_PROJECT_JNILIBS%\libserver_android_arm64.so" >NUL
  copy /Y "%SERVER_SO%" "%ANDROID_PROJECT_JNILIBS%\libserver.so" >NUL
  copy /Y "%SERVER_SO%" "%ANDROID_PROJECT_JNILIBS%\libhl.so" >NUL
  echo [OK] Copied server and aliases
)

if exist "%CLIENT_SO%" (
  copy /Y "%CLIENT_SO%" "%ANDROID_PROJECT_JNILIBS%\libcspb_client_android_arm64.so" >NUL
  copy /Y "%CLIENT_SO%" "%ANDROID_PROJECT_JNILIBS%\libclient_android_arm64.so" >NUL
  copy /Y "%CLIENT_SO%" "%ANDROID_PROJECT_JNILIBS%\libclient.so" >NUL
  echo [OK] Copied client and aliases
)

set "VGUI_SO=%ROOT_DIR%\xash3d-fwgs\build\android_arm64-v8a\libvgui_support.so"
if exist "%VGUI_SO%" copy /Y "%VGUI_SO%" "%ANDROID_PROJECT_JNILIBS%\libvgui_support.so" >NUL

echo [OK] Updated files in jniLibs:
dir "%ANDROID_PROJECT_JNILIBS%\*.so"
exit /b 0
