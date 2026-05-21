@echo off
setlocal

set "ROOT_DIR=%~dp0"
if "%ROOT_DIR:~-1%"=="\" set "ROOT_DIR=%ROOT_DIR:~0,-1%"
set "CSPB_LIB_DIR=%ROOT_DIR%\CSPB-ANDROID-OPEN-SOURCE\libs\arm64-v8a"
set "BACKUP_DIR=%ROOT_DIR%\xash_build_output"
set "LOG_ROOT=%ROOT_DIR%\build_logs\native"
set "SERVER_SO=%CSPB_LIB_DIR%\libcspb_server_android_arm64.so"
set "CLIENT_SO=%CSPB_LIB_DIR%\libcspb_client_android_arm64.so"
set "SERVER_SO_BACKUP=%BACKUP_DIR%\libcspb_server_android_arm64.so"
set "CLIENT_SO_BACKUP=%BACKUP_DIR%\libcspb_client_android_arm64.so"
set "JNILIBS_DIR=%ROOT_DIR%\xash3d-fwgs\android\app\src\main\jniLibs\arm64-v8a"
set "JNILIBS_SERVER_SO=%JNILIBS_DIR%\libcspb_server_android_arm64.so"
set "JNILIBS_CLIENT_SO=%JNILIBS_DIR%\libcspb_client_android_arm64.so"
set "STAMP="
set "START_EPOCH="
set "END_EPOCH="
set "TOTAL_DURATION=0"

for /f %%I in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd_HHmmss"') do set "STAMP=%%I"
if not defined STAMP set "STAMP=manual"
for /f %%I in ('powershell -NoProfile -Command "[DateTimeOffset]::Now.ToUnixTimeSeconds()"') do set "START_EPOCH=%%I"

set "RUN_LOG_DIR=%LOG_ROOT%\%STAMP%"
set "LATEST_LOG_DIR=%LOG_ROOT%\latest"
set "MASTER_LOG=%RUN_LOG_DIR%\native-build-summary.log"
set "SERVER_LOG=%RUN_LOG_DIR%\01-server-arm64.log"
set "CLIENT_LOG=%RUN_LOG_DIR%\02-client-arm64.log"
set "COPY_LOG=%RUN_LOG_DIR%\03-copy-jnilibs.log"

if not exist "%RUN_LOG_DIR%" mkdir "%RUN_LOG_DIR%"
if not exist "%LATEST_LOG_DIR%" mkdir "%LATEST_LOG_DIR%"

> "%MASTER_LOG%" echo [BUILD-NATIVE] Started %date% %time%
>> "%MASTER_LOG%" echo [BUILD-NATIVE] Log folder: %RUN_LOG_DIR%

echo [BUILD-NATIVE] Log folder: %RUN_LOG_DIR%

echo [BUILD-NATIVE] Building server arm64...
call :run_step "server arm64" "%ROOT_DIR%\bat_build_ndk_server_arm64.bat" "%SERVER_LOG%"
if errorlevel 1 goto :build_failed
call :report_artifact "server output" "%SERVER_SO%"

if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"
if exist "%SERVER_SO%" (
  copy /Y "%SERVER_SO%" "%SERVER_SO_BACKUP%" >NUL
  echo [BUILD-NATIVE] Backed up server .so: %SERVER_SO_BACKUP%
  >> "%MASTER_LOG%" echo [BUILD-NATIVE] Backed up server .so: %SERVER_SO_BACKUP%
) else (
  echo [WARN] Server .so missing immediately after server build: %SERVER_SO%
  >> "%MASTER_LOG%" echo [WARN] Server .so missing immediately after server build: %SERVER_SO%
)

echo [BUILD-NATIVE] Building client arm64...
call :run_step "client arm64" "%ROOT_DIR%\bat_build_ndk_client_arm64.bat" "%CLIENT_LOG%"
if errorlevel 1 goto :build_failed
call :report_artifact "client output" "%CLIENT_SO%"

if exist "%CLIENT_SO%" (
  copy /Y "%CLIENT_SO%" "%CLIENT_SO_BACKUP%" >NUL
  echo [BUILD-NATIVE] Backed up client .so: %CLIENT_SO_BACKUP%
  >> "%MASTER_LOG%" echo [BUILD-NATIVE] Backed up client .so: %CLIENT_SO_BACKUP%
) else (
  echo [ERROR] Client .so missing immediately after client build: %CLIENT_SO%
  >> "%MASTER_LOG%" echo [ERROR] Client .so missing immediately after client build: %CLIENT_SO%
  cmd /c exit /b 1
  goto :build_failed
)

if not exist "%SERVER_SO%" if exist "%SERVER_SO_BACKUP%" (
  copy /Y "%SERVER_SO_BACKUP%" "%SERVER_SO%" >NUL
  echo [BUILD-NATIVE] Client build removed server .so, restored from backup.
  >> "%MASTER_LOG%" echo [BUILD-NATIVE] Client build removed server .so, restored from backup.
)
if not exist "%SERVER_SO%" (
  echo [ERROR] Server .so missing after client build and no valid backup restore succeeded: %SERVER_SO%
  >> "%MASTER_LOG%" echo [ERROR] Server .so missing after client build and no valid backup restore succeeded: %SERVER_SO%
  cmd /c exit /b 1
  goto :build_failed
)

echo [BUILD-NATIVE] Copying .so into jniLibs...
call :run_step "copy so to jniLibs" "%ROOT_DIR%\bat_copy_so_to_jnilibs_arm64.bat" "%COPY_LOG%"
if errorlevel 1 goto :build_failed
call :report_artifact "jniLibs server" "%JNILIBS_SERVER_SO%"
call :report_artifact "jniLibs client" "%JNILIBS_CLIENT_SO%"
call :report_total_duration

>> "%MASTER_LOG%" echo [BUILD-NATIVE][SUCCESS] Completed %date% %time%
>> "%MASTER_LOG%" echo [BUILD-NATIVE][SUCCESS] Total duration: %TOTAL_DURATION%s
copy /Y "%MASTER_LOG%" "%LATEST_LOG_DIR%\native-build-summary.log" >NUL
copy /Y "%SERVER_LOG%" "%LATEST_LOG_DIR%\01-server-arm64.log" >NUL
copy /Y "%CLIENT_LOG%" "%LATEST_LOG_DIR%\02-client-arm64.log" >NUL
copy /Y "%COPY_LOG%" "%LATEST_LOG_DIR%\03-copy-jnilibs.log" >NUL
echo [BUILD-NATIVE][SUCCESS] Native build finished in %TOTAL_DURATION%s. Summary: %MASTER_LOG%
exit /b 0

:build_failed
set "BUILD_EXIT=%ERRORLEVEL%"
call :report_total_duration
>> "%MASTER_LOG%" echo [BUILD-NATIVE][FAILED] Exit code %BUILD_EXIT% at %date% %time%
>> "%MASTER_LOG%" echo [BUILD-NATIVE][FAILED] Total duration: %TOTAL_DURATION%s
copy /Y "%MASTER_LOG%" "%LATEST_LOG_DIR%\native-build-summary.log" >NUL
if exist "%SERVER_LOG%" copy /Y "%SERVER_LOG%" "%LATEST_LOG_DIR%\01-server-arm64.log" >NUL
if exist "%CLIENT_LOG%" copy /Y "%CLIENT_LOG%" "%LATEST_LOG_DIR%\02-client-arm64.log" >NUL
if exist "%COPY_LOG%" copy /Y "%COPY_LOG%" "%LATEST_LOG_DIR%\03-copy-jnilibs.log" >NUL
echo [BUILD-NATIVE][FAILED] After %TOTAL_DURATION%s. See summary: %MASTER_LOG%
exit /b %BUILD_EXIT%

:run_step
set "STEP_NAME=%~1"
set "STEP_CMD=%~2"
set "STEP_LOG=%~3"
set "STEP_START_EPOCH="
set "STEP_END_EPOCH="
set "STEP_DURATION=0"

echo [BUILD-NATIVE] Running %STEP_NAME%...
>> "%MASTER_LOG%" echo.
>> "%MASTER_LOG%" echo ===== %STEP_NAME% =====
>> "%MASTER_LOG%" echo [BUILD-NATIVE] Command: %STEP_CMD%
for /f %%I in ('powershell -NoProfile -Command "[DateTimeOffset]::Now.ToUnixTimeSeconds()"') do set "STEP_START_EPOCH=%%I"
powershell -NoProfile -Command "& { cmd /c '\"%STEP_CMD%\"' 2>&1 | Tee-Object -FilePath '%STEP_LOG%'; exit $LASTEXITCODE }"
set "STEP_EXIT=%ERRORLEVEL%"
for /f %%I in ('powershell -NoProfile -Command "[DateTimeOffset]::Now.ToUnixTimeSeconds()"') do set "STEP_END_EPOCH=%%I"
if defined STEP_START_EPOCH if defined STEP_END_EPOCH set /a STEP_DURATION=STEP_END_EPOCH-STEP_START_EPOCH
set "WARNING_COUNT=0"
for /f %%W in ('find /I /C "warning:" ^< "%STEP_LOG%"') do set "WARNING_COUNT=%%W"
if not "%STEP_EXIT%"=="0" (
  >> "%MASTER_LOG%" echo [FAILED] %STEP_NAME% ^(exit %STEP_EXIT%^)
  >> "%MASTER_LOG%" echo [FAILED] Duration: %STEP_DURATION%s
  >> "%MASTER_LOG%" echo [FAILED] Step log: %STEP_LOG%
  echo [BUILD-NATIVE][FAILED] %STEP_NAME% ^(%STEP_DURATION%s, see %STEP_LOG%^)
  exit /b %STEP_EXIT%
)

>> "%MASTER_LOG%" echo [OK] %STEP_NAME%
>> "%MASTER_LOG%" echo [OK] Duration: %STEP_DURATION%s
>> "%MASTER_LOG%" echo [OK] Warning count: %WARNING_COUNT%
>> "%MASTER_LOG%" echo [OK] Step log: %STEP_LOG%
if not "%WARNING_COUNT%"=="0" call :report_top_warnings "%STEP_LOG%"
echo [BUILD-NATIVE][OK] %STEP_NAME% ^(%STEP_DURATION%s, warnings: %WARNING_COUNT%^)
exit /b 0

:report_artifact
set "ARTIFACT_LABEL=%~1"
set "ARTIFACT_PATH=%~2"

if exist "%ARTIFACT_PATH%" (
  for %%F in ("%ARTIFACT_PATH%") do (
    >> "%MASTER_LOG%" echo [ARTIFACT] %ARTIFACT_LABEL%: %%~fF ^| size=%%~zF ^| modified=%%~tF
    echo [BUILD-NATIVE][ARTIFACT] %ARTIFACT_LABEL% -> %%~nxF ^| %%~zF bytes ^| %%~tF
  )
) else (
  >> "%MASTER_LOG%" echo [ARTIFACT][MISSING] %ARTIFACT_LABEL%: %ARTIFACT_PATH%
  echo [BUILD-NATIVE][ARTIFACT][MISSING] %ARTIFACT_LABEL%
)
exit /b 0

:report_top_warnings
set "WARN_LOG=%~1"
echo [BUILD-NATIVE][WARNINGS] Top warnings from %WARN_LOG%:
powershell -NoProfile -Command "$matches = Select-String -Path '%WARN_LOG%' -Pattern 'warning:'; $matches | Select-Object -First 3 | ForEach-Object { $_.Line }"
>> "%MASTER_LOG%" echo [WARNINGS] Top warnings from %WARN_LOG%:
powershell -NoProfile -Command "$matches = Select-String -Path '%WARN_LOG%' -Pattern 'warning:'; $matches | Select-Object -First 3 | ForEach-Object { $_.Line }" >> "%MASTER_LOG%"
exit /b 0

:report_total_duration
for /f %%I in ('powershell -NoProfile -Command "[DateTimeOffset]::Now.ToUnixTimeSeconds()"') do set "END_EPOCH=%%I"
if defined START_EPOCH if defined END_EPOCH set /a TOTAL_DURATION=END_EPOCH-START_EPOCH
exit /b 0
