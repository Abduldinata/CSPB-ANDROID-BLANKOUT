#!/system/bin/sh
# ASAN runtime wrapper for arm64-v8a
export LD_PRELOAD=/data/local/tmp/libclang_rt.asan-aarch64-android.so
export ASAN_OPTIONS=log_to_syslog=false,allow_user_segv_handler=1,abort_on_error=1,disable_coredump=0,detect_leaks=0
exec "$@"
