@echo off
call "C:\Users\gitzr\AppData\Local\Android\Sdk\ndk\30.0.14904198\ndk-build.cmd" APP_ABI=arm64-v8a NDK_PROJECT_PATH=. APP_BUILD_SCRIPT=jni/Android.mk > build_log.txt 2>&1
