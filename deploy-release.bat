@echo off
setlocal

set "ROOT_DIR=%~dp0"

echo [DEPLOY-RELEASE] Installing signed release APK to device...
call "%ROOT_DIR%bat_copy_release_apk_to_phone_and_install.bat"
exit /b %errorlevel%
