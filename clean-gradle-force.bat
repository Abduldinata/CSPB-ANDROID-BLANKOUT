@echo off
setlocal EnableExtensions

set "ROOT_DIR=%~dp0"
if "%ROOT_DIR:~-1%"=="\" set "ROOT_DIR=%ROOT_DIR:~0,-1%"
set "ANDROID_PROJECT_DIR=%ROOT_DIR%\xash3d-fwgs\android"
set "GRADLEW=%ANDROID_PROJECT_DIR%\gradlew.bat"

echo [CLEAN-GRADLE-FORCE] Starting forced Gradle cleanup...

if exist "%GRADLEW%" (
  echo [STOP] Requesting Gradle daemon shutdown...
  pushd "%ANDROID_PROJECT_DIR%" >NUL
  call ".\gradlew.bat" --stop >NUL 2>&1
  popd >NUL
) else (
  echo [SKIP] gradlew.bat not found, cannot request Gradle stop
)

echo [KILL] Terminating java.exe and javaw.exe if still running...
taskkill /f /im java.exe >NUL 2>&1
taskkill /f /im javaw.exe >NUL 2>&1
>nul ping 127.0.0.1 -n 3

call :RemoveOne "%ANDROID_PROJECT_DIR%\app\.cxx"
call :RemoveOne "%ANDROID_PROJECT_DIR%\app\build"
call :RemoveOne "%ANDROID_PROJECT_DIR%\build"
call :RemoveOne "%ANDROID_PROJECT_DIR%\.gradle-user-home"

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

echo [DONE] Forced Gradle cleanup finished.
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
    echo [RENAME] Trying rename fallback for %~1
    call :RenameThenRemove "%~1"
  )
  if exist "%~1" (
    echo [WARN] Failed to remove %~1
  ) else (
    echo [OK] Removed %~1
  )
) else (
  echo [SKIP] Not found: %~1
)
goto :eof

:RenameThenRemove
set "TARGET_PATH=%~1"
set "TARGET_PARENT=%~dp1"
set "TARGET_NAME=%~nx1"
set "RENAMED_NAME=%TARGET_NAME%-delete-pending"

2>nul ren "%TARGET_PATH%" "%RENAMED_NAME%"
if exist "%TARGET_PARENT%%RENAMED_NAME%" (
  >nul ping 127.0.0.1 -n 3
  rmdir /s /q "%TARGET_PARENT%%RENAMED_NAME%"
  if not exist "%TARGET_PARENT%%RENAMED_NAME%" (
    echo [OK] Removed %TARGET_PATH% via rename fallback
  )
)
goto :eof
