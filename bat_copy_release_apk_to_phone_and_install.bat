@echo off
setlocal

rem ============================================================
rem Copy signed release APK to phone + install directly via adb
rem Workspace: E:\Games\PROJECT_LOBBY_CSPB\com.cspb.m
rem ============================================================

set "ROOT_DIR=C:\CSPB_PROJECT\CSPB_ANDROID_BLANKOUT"
set "ANDROID_PROJECT_DIR=%ROOT_DIR%\xash3d-fwgs\android"
set "APK_PATH=%ANDROID_PROJECT_DIR%\app\build\outputs\apk\release\app-release.apk"
set "PHONE_APK_PATH=/sdcard/Download/com.cspb.blankout-release.apk"
if not defined APP_PACKAGE set "APP_PACKAGE=com.cspb.blankout"
if not defined UNINSTALL_FIRST set "UNINSTALL_FIRST=0"
if not defined DEPLOY_RUN_LOG_DIR set "DEPLOY_RUN_LOG_DIR=%ROOT_DIR%\build_logs\deploy\manual"

echo ============================================================
echo [CSPB] COPY RELEASE APK TO PHONE + INSTALL
echo APK   : %APK_PATH%
echo PHONE : %PHONE_APK_PATH%
echo PKG   : %APP_PACKAGE%
echo UNINS : %UNINSTALL_FIRST%
echo ============================================================

where adb >NUL 2>&1
if %ERRORLEVEL% NEQ 0 (
  echo [ERROR] adb not found in PATH
  goto :fail
)

if not exist "%APK_PATH%" (
  echo [ERROR] APK not found: %APK_PATH%
  goto :fail
)

echo.
echo [1/4] Checking adb device...
adb get-state 1>NUL 2>NUL
if %ERRORLEVEL% NEQ 0 (
  echo [ERROR] No adb device detected. Check USB/debugging/authorization.
  goto :fail
)

if "%UNINSTALL_FIRST%"=="1" (
  echo.
  echo [2/4] Uninstalling old app...
  adb uninstall "%APP_PACKAGE%"
  if %ERRORLEVEL% NEQ 0 (
    echo [WARN] Uninstall returned non-zero. Continuing with install...
  )
)

echo.
echo [3/4] Copying APK to phone...
adb push "%APK_PATH%" "%PHONE_APK_PATH%"
if %ERRORLEVEL% NEQ 0 (
  echo [ERROR] Failed to copy APK to phone
  goto :fail
)

echo.
echo [4/4] Installing APK...
adb install -r "%APK_PATH%"
if %ERRORLEVEL% NEQ 0 (
  echo [ERROR] Failed to install APK
  goto :fail
)

echo.
echo [DONE] Install finished.
echo APK copied to: %PHONE_APK_PATH%
echo Installed from: %APK_PATH%
echo Note: launch once first so CSPB recreates runtime folders, then copy old runtime files manually if needed.
echo.
if not defined NO_PAUSE pause
exit /b 0

:fail
echo.
echo Process failed.
if not defined NO_PAUSE pause
exit /b 1
