@echo off
setlocal

set "ROOT_DIR=%~dp0"

echo [PACKAGE-RELEASE] Packaging signed release APK...
call "%ROOT_DIR%bat_build_release_signed.bat"
exit /b %errorlevel%
