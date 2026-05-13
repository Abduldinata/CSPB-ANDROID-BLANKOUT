@echo off
setlocal

set "ROOT_DIR=%~dp0"
if "%ROOT_DIR:~-1%"=="\" set "ROOT_DIR=%ROOT_DIR:~0,-1%"
set "CSPB_SRC_DIR=%ROOT_DIR%\CSPB-ANDROID-OPEN-SOURCE"

echo [CLEAN-NATIVE] Removing native build artifacts...

call :remove_dir "%CSPB_SRC_DIR%\obj"
call :remove_dir "%CSPB_SRC_DIR%\libs"

echo [DONE] Native cleanup finished.
exit /b 0

:remove_dir
set "TARGET_DIR=%~1"
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
