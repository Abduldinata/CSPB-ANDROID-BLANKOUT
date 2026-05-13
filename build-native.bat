@echo off
setlocal

set "ROOT_DIR=%~dp0"
if "%ROOT_DIR:~-1%"=="\" set "ROOT_DIR=%ROOT_DIR:~0,-1%"
set "CSPB_LIB_DIR=%ROOT_DIR%\CSPB-ANDROID-OPEN-SOURCE\libs\arm64-v8a"
set "BACKUP_DIR=%ROOT_DIR%\xash_build_output"
set "SERVER_SO=%CSPB_LIB_DIR%\libcspb_server_android_arm64.so"
set "SERVER_SO_BACKUP=%BACKUP_DIR%\libcspb_server_android_arm64.so"

echo [BUILD-NATIVE] Building server arm64...
call "%ROOT_DIR%\bat_build_ndk_server_arm64.bat"
if errorlevel 1 exit /b %errorlevel%

if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"
if exist "%SERVER_SO%" (
  copy /Y "%SERVER_SO%" "%SERVER_SO_BACKUP%" >NUL
  echo [BUILD-NATIVE] Backed up server .so: %SERVER_SO_BACKUP%
) else (
  echo [WARN] Server .so missing immediately after server build: %SERVER_SO%
)

echo [BUILD-NATIVE] Building client arm64...
call "%ROOT_DIR%\bat_build_ndk_client_arm64.bat"
if errorlevel 1 exit /b %errorlevel%

if not exist "%SERVER_SO%" if exist "%SERVER_SO_BACKUP%" (
  copy /Y "%SERVER_SO_BACKUP%" "%SERVER_SO%" >NUL
  echo [BUILD-NATIVE] Restored server .so after client build.
)

echo [BUILD-NATIVE] Copying .so into jniLibs...
call "%ROOT_DIR%\bat_copy_so_to_jnilibs_arm64.bat"
exit /b %errorlevel%
