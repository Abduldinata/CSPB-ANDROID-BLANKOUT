@echo off
setlocal EnableExtensions

set "ROOT_DIR=%~dp0"
if "%ROOT_DIR:~-1%"=="\" set "ROOT_DIR=%ROOT_DIR:~0,-1%"
set "ANDROID_PROJECT_DIR=%ROOT_DIR%\xash3d-fwgs\android"
set "GRADLEW=%ANDROID_PROJECT_DIR%\gradlew.bat"

echo [CLEAN-GRADLE] Removing Gradle/Android build artifacts...

if exist "%GRADLEW%" (
  echo [STOP] Requesting Gradle daemon shutdown...
  pushd "%ANDROID_PROJECT_DIR%" >NUL
  call ".\gradlew.bat" --stop >NUL 2>&1
  popd >NUL
) else (
  echo [SKIP] gradlew.bat not found, cannot request Gradle stop
)

call :RemoveOne "%ANDROID_PROJECT_DIR%\app\.cxx"
call :RemoveOne "%ANDROID_PROJECT_DIR%\app\build"
call :RemoveOne "%ANDROID_PROJECT_DIR%\build"

set "FOUND_MATCH="
for /d %%D in ("%ANDROID_PROJECT_DIR%\.gradle-user-home-run-*") do (
  set "FOUND_MATCH=1"
  call :RemoveOne "%%~fD"
)
if not defined FOUND_MATCH (
  echo [SKIP] No matches for %ANDROID_PROJECT_DIR%\.gradle-user-home-run-*
)

if defined GRADLE_USER_HOME (
  call :RemoveOne "%GRADLE_USER_HOME%"
) else (
  echo [SKIP] GRADLE_USER_HOME is not set
)

if exist "%ANDROID_PROJECT_DIR%\.gradle-user-home" (
  echo [INFO] Persistent cache exists: %ANDROID_PROJECT_DIR%\.gradle-user-home
  echo [INFO] This folder is optional to clean. Use clean-gradle-force.bat if you want to try removing it too.
) else (
  echo [SKIP] Persistent cache not found: %ANDROID_PROJECT_DIR%\.gradle-user-home
)

echo [DONE] Gradle cleanup finished.
exit /b 0

:RemoveOne
if exist "%~1" (
  echo [REMOVE] %~1
  rmdir /s /q "%~1"
  if exist "%~1" (
    >nul ping 127.0.0.1 -n 3
    rmdir /s /q "%~1"
  )
  if exist "%~1" (
    echo [WARN] Failed to remove %~1 ^(likely locked by Gradle/Java process^)
  ) else (
    echo [OK] Removed %~1
  )
) else (
  echo [SKIP] Not found: %~1
)
goto :eof
