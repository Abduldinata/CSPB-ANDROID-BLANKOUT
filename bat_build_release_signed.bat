@echo off
setlocal

rem Clean + build SIGNED Release APK (uses android\keystore.properties)

set "ROOT_DIR=E:\Games\PROJECT_LOBBY_CSPB\com.cspb.m"
set "ANDROID_PROJECT_DIR=%ROOT_DIR%\xash3d-fwgs\android"
set "APK_OUT=%ANDROID_PROJECT_DIR%\app\build\outputs\apk\release\app-release.apk"

echo [GRADLE] clean + assembleRelease (signed)
echo ANDR: %ANDROID_PROJECT_DIR%

if not exist "%ANDROID_PROJECT_DIR%\gradlew.bat" (
  echo [ERROR] gradlew.bat not found: %ANDROID_PROJECT_DIR%
  exit /b 1
)
if not exist "%ANDROID_PROJECT_DIR%\keystore.properties" (
  echo [ERROR] Missing keystore.properties: %ANDROID_PROJECT_DIR%\keystore.properties
  exit /b 1
)

cd /d "%ANDROID_PROJECT_DIR%"
call .\gradlew.bat clean
if %ERRORLEVEL% NEQ 0 (
  echo [ERROR] Gradle clean failed
  exit /b %ERRORLEVEL%
)

call .\gradlew.bat app:assembleRelease
if %ERRORLEVEL% NEQ 0 (
  echo [ERROR] Gradle assembleRelease failed
  exit /b %ERRORLEVEL%
)

if not exist "%APK_OUT%" (
  echo [ERROR] APK not found: %APK_OUT%
  exit /b 1
)

echo [OK] Signed Release APK:
echo %APK_OUT%
exit /b 0

