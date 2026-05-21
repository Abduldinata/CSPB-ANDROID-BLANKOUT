@echo off
setlocal

set "ROOT_DIR=%~dp0"
if "%ROOT_DIR:~-1%"=="\" set "ROOT_DIR=%ROOT_DIR:~0,-1%"
set "APP_PACKAGE=com.cspb.blankout"
set "LOG_ROOT=%ROOT_DIR%\build_logs\deploy"
set "STAMP="
set "UNINSTALL_FIRST=0"

for /f %%I in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss"') do set "STAMP=%%I"
if not defined STAMP set "STAMP=manual"

set "RUN_LOG_DIR=%LOG_ROOT%\%STAMP%"
set "LATEST_LOG_DIR=%LOG_ROOT%\latest"
set "SUMMARY_LOG=%RUN_LOG_DIR%\deploy-release-summary.log"
set "DEPLOY_LOG=%RUN_LOG_DIR%\device-install.log"
set "NO_PAUSE=1"

if not exist "%RUN_LOG_DIR%" mkdir "%RUN_LOG_DIR%"
if not exist "%LATEST_LOG_DIR%" mkdir "%LATEST_LOG_DIR%"

echo [DEPLOY-RELEASE] Package: %APP_PACKAGE%
echo [DEPLOY-RELEASE] Note: CSPB currently prefers creating a fresh runtime folder after install.
echo [DEPLOY-RELEASE]       If you need old runtime data, launch once, close the app, then copy files manually.
echo.
choice /C YN /N /M "[DEPLOY-RELEASE] Uninstall old app before install? [Y/N]: "
if errorlevel 2 (
  set "UNINSTALL_FIRST=0"
) else (
  set "UNINSTALL_FIRST=1"
)

> "%SUMMARY_LOG%" echo [DEPLOY-RELEASE] Started %date% %time%
>> "%SUMMARY_LOG%" echo [DEPLOY-RELEASE] Log folder: %RUN_LOG_DIR%
>> "%SUMMARY_LOG%" echo [DEPLOY-RELEASE] Package: %APP_PACKAGE%
>> "%SUMMARY_LOG%" echo [DEPLOY-RELEASE] Uninstall first: %UNINSTALL_FIRST%

echo [DEPLOY-RELEASE] Installing signed release APK to device...
echo [DEPLOY-RELEASE] Log folder: %RUN_LOG_DIR%
echo [DEPLOY-RELEASE] Live output is shown below and saved to: %DEPLOY_LOG%
powershell -NoProfile -Command "& { $env:APP_PACKAGE='%APP_PACKAGE%'; $env:UNINSTALL_FIRST='%UNINSTALL_FIRST%'; $env:DEPLOY_RUN_LOG_DIR='%RUN_LOG_DIR%'; cmd /c '\"%ROOT_DIR%\bat_copy_release_apk_to_phone_and_install.bat\"' 2>&1 | Tee-Object -FilePath '%DEPLOY_LOG%'; exit $LASTEXITCODE }"
set "DEPLOY_EXIT=%ERRORLEVEL%"

if not "%DEPLOY_EXIT%"=="0" (
  >> "%SUMMARY_LOG%" echo [DEPLOY-RELEASE][FAILED] Exit code %DEPLOY_EXIT%
  >> "%SUMMARY_LOG%" echo [DEPLOY-RELEASE][FAILED] Step log: %DEPLOY_LOG%
  copy /Y "%SUMMARY_LOG%" "%LATEST_LOG_DIR%\deploy-release-summary.log" >NUL
  copy /Y "%DEPLOY_LOG%" "%LATEST_LOG_DIR%\device-install.log" >NUL
  powershell -NoProfile -Command "Write-Host '[DEPLOY-RELEASE][FAILED] Device install failed.' -ForegroundColor Red"
  echo [DEPLOY-RELEASE][FAILED] Device install failed. Summary: %SUMMARY_LOG%
  exit /b %DEPLOY_EXIT%
)

>> "%SUMMARY_LOG%" echo [DEPLOY-RELEASE][SUCCESS] Completed %date% %time%
>> "%SUMMARY_LOG%" echo [DEPLOY-RELEASE][SUCCESS] Step log: %DEPLOY_LOG%
copy /Y "%SUMMARY_LOG%" "%LATEST_LOG_DIR%\deploy-release-summary.log" >NUL
copy /Y "%DEPLOY_LOG%" "%LATEST_LOG_DIR%\device-install.log" >NUL
powershell -NoProfile -Command "Write-Host '[DEPLOY-RELEASE][SUCCESS] Device install finished.' -ForegroundColor Green"
echo [DEPLOY-RELEASE][SUCCESS] Device install finished. Summary: %SUMMARY_LOG%
exit /b 0
