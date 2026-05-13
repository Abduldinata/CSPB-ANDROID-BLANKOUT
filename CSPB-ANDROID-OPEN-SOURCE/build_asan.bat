@echo off
echo Cleaning old build...
call "C:\Users\gitzr\AppData\Local\Android\Sdk\ndk\30.0.14904198\ndk-build.cmd" NDK_PROJECT_PATH=. APP_BUILD_SCRIPT=jni/Android.mk clean

echo Starting ASAN build for arm64-v8a...
call "C:\Users\gitzr\AppData\Local\Android\Sdk\ndk\30.0.14904198\ndk-build.cmd" APP_ABI=arm64-v8a NDK_PROJECT_PATH=. APP_BUILD_SCRIPT=jni/Android.mk APP_ASAN=true > build_log_asan.txt 2>&1

if %ERRORLEVEL% EQU 0 (
    echo Build SUCCESS! Deploying libraries...
    copy /Y "E:\Games\PROJECT_LOBBY_CSPB\com.cspb.m\CSPB-ANDROID-OPEN-SOURCE\libs\arm64-v8a\libcspb_server_android_arm64.so" "E:\Games\PROJECT_LOBBY_CSPB\com.cspb.m\files\cspb\dlls\"
    copy /Y "E:\Games\PROJECT_LOBBY_CSPB\com.cspb.m\CSPB-ANDROID-OPEN-SOURCE\libs\arm64-v8a\libcspb_client_android_arm64.so" "E:\Games\PROJECT_LOBBY_CSPB\com.cspb.m\files\cspb\cl_dlls\"
    echo Deploy Finished!
) else (
    echo Build FAILED! Check build_log_asan.txt
)
