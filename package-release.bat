@echo off
setlocal

set "ROOT_DIR=%~dp0"
if "%ROOT_DIR:~-1%"=="\" set "ROOT_DIR=%ROOT_DIR:~0,-1%"
set "LOG_ROOT=%ROOT_DIR%\build_logs\package"
set "STAMP="

for /f %%I in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss"') do set "STAMP=%%I"
if not defined STAMP set "STAMP=manual"

set "RUN_LOG_DIR=%LOG_ROOT%\%STAMP%"
set "LATEST_LOG_DIR=%LOG_ROOT%\latest"
set "SUMMARY_LOG=%RUN_LOG_DIR%\package-release-summary.log"
set "PACKAGE_LOG=%RUN_LOG_DIR%\signed-release-build.log"

if not exist "%RUN_LOG_DIR%" mkdir "%RUN_LOG_DIR%"
if not exist "%LATEST_LOG_DIR%" mkdir "%LATEST_LOG_DIR%"

> "%SUMMARY_LOG%" echo [PACKAGE-RELEASE] Started %date% %time%
>> "%SUMMARY_LOG%" echo [PACKAGE-RELEASE] Log folder: %RUN_LOG_DIR%

echo [PACKAGE-RELEASE] Packaging signed release APK...
echo [PACKAGE-RELEASE] Log folder: %RUN_LOG_DIR%
echo [PACKAGE-RELEASE] Live output is shown below and saved to: %PACKAGE_LOG%
powershell -NoProfile -Command "& { cmd /c '\"%ROOT_DIR%\bat_build_release_signed.bat\"' 2>&1 | Tee-Object -FilePath '%PACKAGE_LOG%'; exit $LASTEXITCODE }"
set "PACKAGE_EXIT=%ERRORLEVEL%"

if not "%PACKAGE_EXIT%"=="0" (
  >> "%SUMMARY_LOG%" echo [PACKAGE-RELEASE][FAILED] Exit code %PACKAGE_EXIT%
  >> "%SUMMARY_LOG%" echo [PACKAGE-RELEASE][FAILED] Step log: %PACKAGE_LOG%
  copy /Y "%SUMMARY_LOG%" "%LATEST_LOG_DIR%\package-release-summary.log" >NUL
  copy /Y "%PACKAGE_LOG%" "%LATEST_LOG_DIR%\signed-release-build.log" >NUL
  powershell -NoProfile -Command "Write-Host '[PACKAGE-RELEASE][FAILED] Signed package failed.' -ForegroundColor Red"
  echo [PACKAGE-RELEASE][FAILED] Signed package failed. Summary: %SUMMARY_LOG%
  exit /b %PACKAGE_EXIT%
)

>> "%SUMMARY_LOG%" echo [PACKAGE-RELEASE][SUCCESS] Completed %date% %time%
>> "%SUMMARY_LOG%" echo [PACKAGE-RELEASE][SUCCESS] Step log: %PACKAGE_LOG%
copy /Y "%SUMMARY_LOG%" "%LATEST_LOG_DIR%\package-release-summary.log" >NUL
copy /Y "%PACKAGE_LOG%" "%LATEST_LOG_DIR%\signed-release-build.log" >NUL
powershell -NoProfile -Command "Write-Host '[PACKAGE-RELEASE][SUCCESS] Signed package finished.' -ForegroundColor Green"
echo [PACKAGE-RELEASE][SUCCESS] Signed package finished. Summary: %SUMMARY_LOG%
exit /b 0
