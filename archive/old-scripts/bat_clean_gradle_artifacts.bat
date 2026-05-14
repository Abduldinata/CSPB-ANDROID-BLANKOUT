@echo off
setlocal

rem Cleanup khusus artefak Gradle/Android build agar terpisah dari pipeline release.
rem Folder yang dihapus:
rem - xash3d-fwgs\android\app\.cxx
rem - xash3d-fwgs\android\app\build
rem - xash3d-fwgs\android\build
rem - optional: GRADLE_USER_HOME jika sudah diset di environment

set "ROOT_DIR=%~dp0"
if "%ROOT_DIR:~-1%"=="\" set "ROOT_DIR=%ROOT_DIR:~0,-1%"

set "ANDROID_PROJECT_DIR=%ROOT_DIR%\xash3d-fwgs\android"

echo [CLEAN] Starting Gradle artifact cleanup...

call :remove_dir "%ANDROID_PROJECT_DIR%\app\.cxx"
call :remove_dir "%ANDROID_PROJECT_DIR%\app\build"
call :remove_dir "%ANDROID_PROJECT_DIR%\build"

if defined GRADLE_USER_HOME (
  call :remove_dir "%GRADLE_USER_HOME%"
) else (
  echo [SKIP] GRADLE_USER_HOME is not set
)

echo [DONE] Gradle cleanup finished.
exit /b 0

:remove_dir
set "TARGET_DIR=%~1"
if not defined TARGET_DIR exit /b 0

if exist "%TARGET_DIR%" (
  echo [REMOVE] %TARGET_DIR%
  rmdir /s /q "%TARGET_DIR%"
  if exist "%TARGET_DIR%" (
    echo [WARN] Failed to remove %TARGET_DIR%
  ) else (
    echo [OK] Removed %TARGET_DIR%
  )
) else (
  echo [SKIP] Not found: %TARGET_DIR%
)

exit /b 0
