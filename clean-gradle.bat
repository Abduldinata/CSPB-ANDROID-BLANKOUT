@echo off
setlocal EnableExtensions

set "ROOT_DIR=%~dp0"
if "%ROOT_DIR:~-1%"=="\" set "ROOT_DIR=%ROOT_DIR:~0,-1%"
set "ANDROID_PROJECT_DIR=%ROOT_DIR%\xash3d-fwgs\android"
set "GRADLEW=%ANDROID_PROJECT_DIR%\gradlew.bat"
set "PERSISTENT_GRADLE_HOME=%ANDROID_PROJECT_DIR%\.gradle-user-home"

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
  if /I "%GRADLE_USER_HOME%"=="%PERSISTENT_GRADLE_HOME%" (
    echo [KEEP] GRADLE_USER_HOME points to persistent cache, preserving: %GRADLE_USER_HOME%
  ) else (
    call :RemoveOne "%GRADLE_USER_HOME%"
  )
) else (
  echo [SKIP] GRADLE_USER_HOME is not set
)

if exist "%PERSISTENT_GRADLE_HOME%" (
  echo [INFO] Persistent cache exists: %PERSISTENT_GRADLE_HOME%
  echo [INFO] This dependency cache is preserved to avoid repeated downloads.
) else (
  echo [SKIP] Persistent cache not found: %PERSISTENT_GRADLE_HOME%
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
