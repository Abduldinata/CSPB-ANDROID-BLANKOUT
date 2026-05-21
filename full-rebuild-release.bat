@echo off
setlocal

set "ROOT_DIR=%~dp0"
if "%ROOT_DIR:~-1%"=="\" set "ROOT_DIR=%ROOT_DIR:~0,-1%"

echo [FULL-REBUILD] Step 1/5: clean-native
call "%ROOT_DIR%\clean-native.bat"
if errorlevel 1 goto :failed_clean_native

echo [FULL-REBUILD] Step 2/5: clean-gradle
call "%ROOT_DIR%\clean-gradle.bat"
if errorlevel 1 (
  echo [FULL-REBUILD][WARN] clean-gradle returned non-zero. Retrying with clean-gradle-force...
  call "%ROOT_DIR%\clean-gradle-force.bat"
  if errorlevel 1 goto :failed_clean_gradle
)

echo [FULL-REBUILD] Step 3/5: build-native
call "%ROOT_DIR%\build-native.bat"
if errorlevel 1 goto :failed_build_native

echo [FULL-REBUILD] Step 4/5: package-release
call "%ROOT_DIR%\package-release.bat"
if errorlevel 1 goto :failed_package_release

echo.
choice /C YN /N /M "[FULL-REBUILD] USB sudah dicolok dan mau lanjut deploy? [Y/N]: "
if errorlevel 2 goto :skip_deploy

echo [FULL-REBUILD] Step 5/5: deploy-release
call "%ROOT_DIR%\deploy-release.bat"
if errorlevel 1 goto :failed_deploy_release

echo.
powershell -NoProfile -Command "Write-Host '[FULL-REBUILD][SUCCESS] All steps completed.' -ForegroundColor Green"
echo [FULL-REBUILD][SUCCESS] All steps completed.
echo [FULL-REBUILD] Native summary : %ROOT_DIR%\build_logs\native\latest\native-build-summary.log
echo [FULL-REBUILD] Package summary: %ROOT_DIR%\build_logs\package\latest\package-release-summary.log
echo [FULL-REBUILD] Deploy summary : %ROOT_DIR%\build_logs\deploy\latest\deploy-release-summary.log
exit /b 0

:skip_deploy
echo.
powershell -NoProfile -Command "Write-Host '[FULL-REBUILD][SUCCESS] Build and package completed. Deploy skipped by user.' -ForegroundColor Green"
echo [FULL-REBUILD][SUCCESS] Build and package completed. Deploy skipped by user.
echo [FULL-REBUILD] Native summary : %ROOT_DIR%\build_logs\native\latest\native-build-summary.log
echo [FULL-REBUILD] Package summary: %ROOT_DIR%\build_logs\package\latest\package-release-summary.log
exit /b 0

:failed_clean_native
echo [FULL-REBUILD][FAILED] clean-native failed.
exit /b %errorlevel%

:failed_clean_gradle
echo [FULL-REBUILD][FAILED] clean-gradle failed.
exit /b %errorlevel%

:failed_build_native
echo [FULL-REBUILD][FAILED] build-native failed.
echo [FULL-REBUILD] See: %ROOT_DIR%\build_logs\native\latest\native-build-summary.log
exit /b %errorlevel%

:failed_package_release
echo [FULL-REBUILD][FAILED] package-release failed.
echo [FULL-REBUILD] See: %ROOT_DIR%\build_logs\package\latest\package-release-summary.log
exit /b %errorlevel%

:failed_deploy_release
echo [FULL-REBUILD][FAILED] deploy-release failed.
echo [FULL-REBUILD] See: %ROOT_DIR%\build_logs\deploy\latest\deploy-release-summary.log
exit /b %errorlevel%
