@echo off
setlocal

rem Build SIGNED Release APK (uses android\keystore.properties)
rem Fast path preserves Gradle dependency cache and avoids clean unless recovery is needed.

set "ROOT_DIR=C:\CSPB_PROJECT\CSPB_ANDROID_BLANKOUT"
set "ANDROID_PROJECT_DIR=%ROOT_DIR%\xash3d-fwgs\android"
set "APK_OUT=%ANDROID_PROJECT_DIR%\app\build\outputs\apk\release\app-release.apk"

rem Persistent Gradle cache keeps dependencies downloaded between builds.
rem If this cache is really corrupt, use clean-gradle-force.bat intentionally.
set "GRADLE_USER_HOME=%ANDROID_PROJECT_DIR%\.gradle-user-home"
set "GRADLE_TRANSFORMS_DIR=%GRADLE_USER_HOME%\caches\9.2.1\transforms"

echo [GRADLE] assembleRelease (signed, cache-preserving)
echo ANDR: %ANDROID_PROJECT_DIR%
echo GRADLE_USER_HOME: %GRADLE_USER_HOME%

if not exist "%ANDROID_PROJECT_DIR%\gradlew.bat" (
  echo [ERROR] gradlew.bat not found: %ANDROID_PROJECT_DIR%
  exit /b 1
)
if not exist "%ANDROID_PROJECT_DIR%\keystore.properties" (
  echo [ERROR] Missing keystore.properties: %ANDROID_PROJECT_DIR%\keystore.properties
  exit /b 1
)

cd /d "%ANDROID_PROJECT_DIR%"
call .\gradlew.bat --stop >NUL 2>&1

rem Ensure APK always packages the freshly-built CSPB libraries.
call "%ROOT_DIR%\bat_copy_so_to_jnilibs_arm64.bat"
if %ERRORLEVEL% NEQ 0 (
  if exist "%ANDROID_PROJECT_DIR%\app\src\main\jniLibs\arm64-v8a\libcspb_server_android_arm64.so" if exist "%ANDROID_PROJECT_DIR%\app\src\main\jniLibs\arm64-v8a\libcspb_client_android_arm64.so" (
    echo [WARN] bat_copy_so_to_jnilibs_arm64.bat returned non-zero, but target .so files are present. Continuing.
    goto :copy_ok_initial
  )
  echo [ERROR] Failed to refresh jniLibs .so before assembleRelease
  exit /b %ERRORLEVEL%
)
:copy_ok_initial

call .\gradlew.bat app:assembleRelease
if %ERRORLEVEL% NEQ 0 (
  echo [WARN] Gradle assembleRelease failed, trying cache recovery
  call .\gradlew.bat --stop >NUL 2>&1
  if exist "%GRADLE_TRANSFORMS_DIR%" (
    echo [RECOVER] Removing corrupt Gradle transforms cache
    rmdir /s /q "%GRADLE_TRANSFORMS_DIR%"
  )
  if exist "%ANDROID_PROJECT_DIR%\app\build" (
    echo [RECOVER] Removing app build directory
    rmdir /s /q "%ANDROID_PROJECT_DIR%\app\build"
  )
  if exist "%ANDROID_PROJECT_DIR%\build" (
    echo [RECOVER] Removing android build directory
    rmdir /s /q "%ANDROID_PROJECT_DIR%\build"
  )
  call "%ROOT_DIR%\bat_copy_so_to_jnilibs_arm64.bat"
  if %ERRORLEVEL% NEQ 0 (
    if exist "%ANDROID_PROJECT_DIR%\app\src\main\jniLibs\arm64-v8a\libcspb_server_android_arm64.so" if exist "%ANDROID_PROJECT_DIR%\app\src\main\jniLibs\arm64-v8a\libcspb_client_android_arm64.so" (
      echo [WARN] bat_copy_so_to_jnilibs_arm64.bat returned non-zero during recovery, but target .so files are present. Continuing.
      goto :copy_ok_recovery
    )
    echo [ERROR] Failed to refresh jniLibs .so during recovery
    exit /b %ERRORLEVEL%
  )
  :copy_ok_recovery
  call .\gradlew.bat app:assembleRelease --rerun-tasks
  if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Gradle assembleRelease failed after cache recovery
    exit /b %ERRORLEVEL%
  )
)

rem If Gradle/CMake just rebuilt libxash.so, copy it into jniLibs and repackage once.
rem This keeps APK packaging synced without deleting caches or forcing a full rebuild.
call "%ROOT_DIR%\bat_copy_so_to_jnilibs_arm64.bat"
if %ERRORLEVEL% NEQ 0 (
  echo [ERROR] Failed to refresh jniLibs .so after assembleRelease
  exit /b %ERRORLEVEL%
)
call .\gradlew.bat app:assembleRelease
if %ERRORLEVEL% NEQ 0 (
  echo [ERROR] Gradle assembleRelease failed after post-CMake jniLibs refresh
  exit /b %ERRORLEVEL%
)

if not exist "%APK_OUT%" (
  echo [ERROR] APK not found: %APK_OUT%
  exit /b 1
)

echo [OK] Signed Release APK:
echo %APK_OUT%

exit /b 0
