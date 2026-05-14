@echo off
set NDK_PATH=C:\Users\gitzr\AppData\Local\Android\Sdk\ndk\30.0.14904198\ndk-build.cmd
set CSPB_JNI_DIR=C:\CSPB_PROJECT\CSPB_ANDROID_BLANKOUT\CSPB-ANDROID-OPEN-SOURCE
set ANDROID_PROJECT_DIR=C:\CSPB_PROJECT\CSPB_ANDROID_BLANKOUT\xash3d-fwgs\android
set ANDROID_PROJECT_JNILIBS=%ANDROID_PROJECT_DIR%\app\src\main\jniLibs\arm64-v8a

echo [1/3] Memulai Compile Native Code (ndk-build)...
cd /d "%CSPB_JNI_DIR%"
call "%NDK_PATH%" -j8

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Gagal melakukan compile C++! Cek log di atas.
    pause
    exit /b %ERRORLEVEL%
)

echo [2/3] Menyalin file .so terbaru ke folder Android Project...
if not exist "%ANDROID_PROJECT_JNILIBS%" mkdir "%ANDROID_PROJECT_JNILIBS%"

rem KOREKSI NAMA: NDK menghasilkan libcspb_client_android_arm64.so
copy /Y "%CSPB_JNI_DIR%\libs\arm64-v8a\libcspb_client_android_arm64.so" "%ANDROID_PROJECT_JNILIBS%\"
copy /Y "%CSPB_JNI_DIR%\libs\arm64-v8a\libcspb_server_android_arm64.so" "%ANDROID_PROJECT_JNILIBS%\"

echo [INFO] Library C++ berhasil diperbarui di jniLibs.

echo [3/3] Memulai Build APK (gradlew assembleDebug)...
cd /d "%ANDROID_PROJECT_DIR%"
call .\gradlew.bat assembleDebug

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Gagal mem-build APK! Pastikan Android Studio/Gradle tidak sedang terkunci.
    pause
    exit /b %ERRORLEVEL%
)

echo ======================================================
echo SEMUA BERHASIL! 
echo 1. Library C++ (dengan LOG Diagnostik) sudah masuk APK.
echo 2. APK Baru siap di: %ANDROID_PROJECT_DIR%\app\build\outputs\apk\debug\
echo ======================================================
pause

