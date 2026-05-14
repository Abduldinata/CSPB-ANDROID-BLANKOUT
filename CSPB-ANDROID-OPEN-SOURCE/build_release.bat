@echo off
echo [1/3] Cleaning old build...
call "C:\Users\gitzr\AppData\Local\Android\Sdk\ndk\30.0.14904198\ndk-build.cmd" NDK_PROJECT_PATH=. APP_BUILD_SCRIPT=jni/Android.mk clean

echo [2/3] Starting STABLE RELEASE build for arm64-v8a...
call "C:\Users\gitzr\AppData\Local\Android\Sdk\ndk\30.0.14904198\ndk-build.cmd" APP_ABI=arm64-v8a NDK_PROJECT_PATH=. APP_BUILD_SCRIPT=jni/Android.mk > build_log_release.txt 2>&1

if %ERRORLEVEL% EQU 0 (
    echo [3/3] Build SUCCESS! Deploying to Game Files and Android Project...
    
    :: Deploy to Game Files
    copy /Y "E:\Games\PROJECT_LOBBY_CSPB\com.cspb.m\CSPB-ANDROID-OPEN-SOURCE\libs\arm64-v8a\libcspb_server_android_arm64.so" "E:\Games\PROJECT_LOBBY_CSPB\com.cspb.m\files\cspb\dlls\"
    copy /Y "E:\Games\PROJECT_LOBBY_CSPB\com.cspb.m\CSPB-ANDROID-OPEN-SOURCE\libs\arm64-v8a\libcspb_client_android_arm64.so" "E:\Games\PROJECT_LOBBY_CSPB\com.cspb.m\files\cspb\cl_dlls\"
    
    :: Deploy to Android Studio Project (Main)
    mkdir "E:\Games\PROJECT_LOBBY_CSPB\com.cspb.m\xash3d-fwgs\android\app\src\main\jniLibs\arm64-v8a"
    copy /Y "E:\Games\PROJECT_LOBBY_CSPB\com.cspb.m\CSPB-ANDROID-OPEN-SOURCE\libs\arm64-v8a\*.so" "E:\Games\PROJECT_LOBBY_CSPB\com.cspb.m\xash3d-fwgs\android\app\src\main\jniLibs\arm64-v8a\"
    
    echo DONE! Bos bisa langsung Build APK di Android Studio sekarang.
) else (
    echo Build FAILED! Check build_log_release.txt
)
