@echo off
setlocal

rem One-click pipeline: build server+client, copy .so, clean, assembleRelease (signed)

set "ROOT_DIR=E:\Games\PROJECT_LOBBY_CSPB\com.cspb.m"
set "SERVER_SO_BACKUP=%ROOT_DIR%\xash_build_output\libcspb_server_android_arm64.so"

echo ============================================================
echo [CSPB] ALL-IN-ONE (arm64-v8a) SIGNED RELEASE
echo ROOT: %ROOT_DIR%
echo ============================================================

call "%ROOT_DIR%\bat_build_ndk_server_arm64.bat"
if %ERRORLEVEL% NEQ 0 exit /b %ERRORLEVEL%

rem ndk-build may wipe libs/arm64-v8a when building the next module.
rem Preserve the server .so before building client.
if exist "%ROOT_DIR%\CSPB-ANDROID-OPEN-SOURCE\libs\arm64-v8a\libcspb_server_android_arm64.so" (
  if not exist "%ROOT_DIR%\xash_build_output" mkdir "%ROOT_DIR%\xash_build_output"
  copy /Y "%ROOT_DIR%\CSPB-ANDROID-OPEN-SOURCE\libs\arm64-v8a\libcspb_server_android_arm64.so" "%SERVER_SO_BACKUP%" >NUL
)

call "%ROOT_DIR%\bat_build_ndk_client_arm64.bat"
if %ERRORLEVEL% NEQ 0 exit /b %ERRORLEVEL%

rem Restore server .so after client build if it was wiped.
if not exist "%ROOT_DIR%\CSPB-ANDROID-OPEN-SOURCE\libs\arm64-v8a\libcspb_server_android_arm64.so" (
  if exist "%SERVER_SO_BACKUP%" (
    copy /Y "%SERVER_SO_BACKUP%" "%ROOT_DIR%\CSPB-ANDROID-OPEN-SOURCE\libs\arm64-v8a\libcspb_server_android_arm64.so" >NUL
  )
)
if exist "%SERVER_SO_BACKUP%" del /Q "%SERVER_SO_BACKUP%"

call "%ROOT_DIR%\bat_copy_so_to_jnilibs_arm64.bat"
if %ERRORLEVEL% NEQ 0 exit /b %ERRORLEVEL%

call "%ROOT_DIR%\bat_build_release_signed.bat"
if %ERRORLEVEL% NEQ 0 exit /b %ERRORLEVEL%

echo ============================================================
echo SUCCESS
echo ============================================================
pause
exit /b 0
