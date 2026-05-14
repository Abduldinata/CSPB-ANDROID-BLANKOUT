@echo off
setlocal enabledelayedexpansion

rem ============================================================
rem CSPB - Build NDK [arm64-v8a] + Copy .so + Build SIGNED Release APK
rem Workspace: C:\CSPB_PROJECT\CSPB_ANDROID_BLANKOUT
rem ============================================================

set "ROOT_DIR=C:\CSPB_PROJECT\CSPB_ANDROID_BLANKOUT"
set "NDK_BUILD=C:\Users\gitzr\AppData\Local\Android\Sdk\ndk\30.0.14904198\ndk-build.cmd"

set "CSPB_JNI_DIR=%ROOT_DIR%\CSPB-ANDROID-OPEN-SOURCE"
set "ANDROID_PROJECT_DIR=%ROOT_DIR%\xash3d-fwgs\android"
set "ANDROID_PROJECT_JNILIBS=%ANDROID_PROJECT_DIR%\app\src\main\jniLibs\arm64-v8a"
set "SERVER_SO_BACKUP=%ROOT_DIR%\xash_build_output\libcspb_server_android_arm64.so"

rem Avoid permission/lock issues under %USERPROFILE%\.gradle on some Windows setups.
set "GRADLE_USER_HOME=%ANDROID_PROJECT_DIR%\.gradle-user-home"

set "APK_OUT=%ANDROID_PROJECT_DIR%\app\build\outputs\apk\release\app-release.apk"

echo ============================================================
echo [CSPB] BUILD + DEPLOY [SIGNED RELEASE]
echo ROOT  : %ROOT_DIR%
echo NDK   : %NDK_BUILD%
echo JNI   : %CSPB_JNI_DIR%
echo ANDR  : %ANDROID_PROJECT_DIR%
echo JNI64 : %ANDROID_PROJECT_JNILIBS%
echo ============================================================

rem ============================================================
rem Interactive options
rem ============================================================
set "DO_NDK_BUILD=Y"
set /p "DO_NDK_BUILD=Build NDK modules [server+client]? (Y/N) [Y]: "
if "%DO_NDK_BUILD%"=="" set "DO_NDK_BUILD=Y"

set "ENABLE_NO_SKIP=N"
set /p "ENABLE_NO_SKIP=No-skip mode [enable weapon_apc precache]? (Y/N) [N]: "
if "%ENABLE_NO_SKIP%"=="" set "ENABLE_NO_SKIP=N"

rem ---- clean old build artifacts ----
echo [CLEAN] Removing old build and .cxx folders...
if exist "%ANDROID_PROJECT_DIR%\app\.cxx" rmdir /s /q "%ANDROID_PROJECT_DIR%\app\.cxx"
if exist "%ANDROID_PROJECT_DIR%\app\build" rmdir /s /q "%ANDROID_PROJECT_DIR%\app\build"
if exist "%ANDROID_PROJECT_DIR%\build" rmdir /s /q "%ANDROID_PROJECT_DIR%\build"

set "APC_VAL=0"
if /I "%ENABLE_NO_SKIP%"=="Y" set "APC_VAL=1"

rem ---- sanity checks ----
if not exist "%NDK_BUILD%" (
  echo [ERROR] NDK build not found: %NDK_BUILD%
  goto :fail
)
if not exist "%CSPB_JNI_DIR%\jni\Android.mk" (
  echo [ERROR] CSPB JNI project not found: %CSPB_JNI_DIR%
  goto :fail
)
if not exist "%ANDROID_PROJECT_DIR%\gradlew.bat" (
  echo [ERROR] Android Gradle project not found: %ANDROID_PROJECT_DIR%
  goto :fail
)

rem ---- signing checks [keystore.properties + .jks] ----
if not exist "%ANDROID_PROJECT_DIR%\keystore.properties" (
  echo [ERROR] Missing %ANDROID_PROJECT_DIR%\keystore.properties
  echo         Release will NOT be signed without it.
  goto :fail
)

set "STORE_FILE_REL="
for /f "usebackq tokens=1,* delims==" %%A in (`findstr /i "^storeFile=" "%ANDROID_PROJECT_DIR%\keystore.properties"`) do (
  set "STORE_FILE_REL=%%B"
)
if "%STORE_FILE_REL%"=="" (
  echo [ERROR] keystore.properties: storeFile is empty
  goto :fail
)

set "STORE_FILE_ABS=%ANDROID_PROJECT_DIR%\%STORE_FILE_REL%"
if not exist "%STORE_FILE_ABS%" (
  echo [ERROR] Keystore not found: %STORE_FILE_ABS%
  goto :fail
)

echo [OK] Signing enabled. Keystore: %STORE_FILE_ABS%

rem ============================================================
rem 1) Build native: server + client [arm64-v8a]
rem ============================================================
if /I "%DO_NDK_BUILD%"=="N" goto :skip_ndk

echo.
echo [1/4] Building NDK server: cspb_server_android_arm64...
echo       CSPB_ENABLE_WEAPON_APC=%APC_VAL% [0=skip, 1=no-skip]
cd /d "%CSPB_JNI_DIR%"
call "%NDK_BUILD%" -B APP_ABI=arm64-v8a APP_PLATFORM=android-21 APP_MODULES=cspb_server_android_arm64 APP_CPPFLAGS=-DCSPB_ENABLE_WEAPON_APC=%APC_VAL% -j8
if %ERRORLEVEL% NEQ 0 (
  echo [ERROR] NDK build failed [server]
  goto :fail
)

rem ndk-build may wipe libs/arm64-v8a when building the next module.
if not exist "%CSPB_JNI_DIR%\libs\arm64-v8a\libcspb_server_android_arm64.so" (
  echo [ERROR] Server .so was not generated!
  goto :fail
)

if not exist "%ROOT_DIR%\xash_build_output" mkdir "%ROOT_DIR%\xash_build_output"
copy /Y "%CSPB_JNI_DIR%\libs\arm64-v8a\libcspb_server_android_arm64.so" "%SERVER_SO_BACKUP%" >NUL

echo.
echo [2/4] Building NDK client: cspb_client_android_arm64...
cd /d "%CSPB_JNI_DIR%"
call "%NDK_BUILD%" -B APP_ABI=arm64-v8a APP_PLATFORM=android-21 APP_MODULES=cspb_client_android_arm64 -j8
if %ERRORLEVEL% NEQ 0 (
  echo [ERROR] NDK build failed [client]
  goto :fail
)

rem Restore server .so after client build if it was wiped.
if not exist "%CSPB_JNI_DIR%\libs\arm64-v8a\libcspb_server_android_arm64.so" (
  if exist "%SERVER_SO_BACKUP%" (
    copy /Y "%SERVER_SO_BACKUP%" "%CSPB_JNI_DIR%\libs\arm64-v8a\libcspb_server_android_arm64.so" >NUL
  )
)
if exist "%SERVER_SO_BACKUP%" del /Q "%SERVER_SO_BACKUP%"

goto :ndk_ok

:skip_ndk
echo.
echo [1/4] Skipping NDK build [using existing .so in %CSPB_JNI_DIR%\libs\arm64-v8a\]
:ndk_ok

rem ============================================================
rem 2) Copy .so into Android jniLibs/arm64-v8a
rem ============================================================
echo.
echo [3/4] Copying .so into Android jniLibs [arm64-v8a]...
if not exist "%ANDROID_PROJECT_JNILIBS%" mkdir "%ANDROID_PROJECT_JNILIBS%"

if not exist "%CSPB_JNI_DIR%\libs\arm64-v8a\libcspb_server_android_arm64.so" (
  echo [ERROR] Missing server .so: %CSPB_JNI_DIR%\libs\arm64-v8a\libcspb_server_android_arm64.so
  goto :fail
)
if not exist "%CSPB_JNI_DIR%\libs\arm64-v8a\libcspb_client_android_arm64.so" (
  echo [ERROR] Missing client .so: %CSPB_JNI_DIR%\libs\arm64-v8a\libcspb_client_android_arm64.so
  goto :fail
)

copy /Y "%CSPB_JNI_DIR%\libs\arm64-v8a\libcspb_server_android_arm64.so" "%ANDROID_PROJECT_JNILIBS%\" >NUL
copy /Y "%CSPB_JNI_DIR%\libs\arm64-v8a\libcspb_client_android_arm64.so" "%ANDROID_PROJECT_JNILIBS%\" >NUL

echo [OK] Updated:
dir /-C "%ANDROID_PROJECT_JNILIBS%\libcspb_*android_arm64.so"

rem ============================================================
rem 3) Clean + assembleRelease [SIGNED]
rem ============================================================
echo.
echo [4/4] Gradle clean + assembleRelease [signed]...
cd /d "%ANDROID_PROJECT_DIR%"
call .\gradlew.bat clean
if %ERRORLEVEL% NEQ 0 (
  echo [ERROR] Gradle clean failed
  goto :fail
)

call .\gradlew.bat app:assembleRelease
if %ERRORLEVEL% NEQ 0 (
  echo [ERROR] Gradle assembleRelease failed
  goto :fail
)

if not exist "%APK_OUT%" (
  echo [ERROR] APK not found: %APK_OUT%
  goto :fail
)

echo.
echo ============================================================
echo SUCCESS!
echo Signed Release APK:
echo %APK_OUT%
echo ============================================================
echo.
pause
exit /b 0

:fail
echo.
echo Build failed.
pause
exit /b 1
