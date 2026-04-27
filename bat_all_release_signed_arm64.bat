@echo off
setlocal

rem One-click pipeline: build server+client, copy .so, clean, assembleRelease (signed)

set "ROOT_DIR=E:\Games\PROJECT_LOBBY_CSPB\com.cspb.m"

echo ============================================================
echo [CSPB] ALL-IN-ONE (arm64-v8a) SIGNED RELEASE
echo ROOT: %ROOT_DIR%
echo ============================================================

call "%ROOT_DIR%\bat_build_ndk_server_arm64.bat"
if %ERRORLEVEL% NEQ 0 exit /b %ERRORLEVEL%

call "%ROOT_DIR%\bat_copy_so_to_jnilibs_arm64.bat"
if %ERRORLEVEL% NEQ 0 exit /b %ERRORLEVEL%

call "%ROOT_DIR%\bat_build_ndk_client_arm64.bat"
if %ERRORLEVEL% NEQ 0 exit /b %ERRORLEVEL%

call "%ROOT_DIR%\bat_copy_so_to_jnilibs_arm64.bat"
if %ERRORLEVEL% NEQ 0 exit /b %ERRORLEVEL%

call "%ROOT_DIR%\bat_build_release_signed.bat"
if %ERRORLEVEL% NEQ 0 exit /b %ERRORLEVEL%

echo ============================================================
echo SUCCESS
echo ============================================================
pause
exit /b 0
