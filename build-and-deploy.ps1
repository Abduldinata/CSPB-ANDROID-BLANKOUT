<#
.SYNOPSIS
    CSPB Android Blankout — Build, Package & Deploy Pipeline
.DESCRIPTION
    Full-release workflow in PowerShell.
    Replaces the batch-based build chain.

    Steps:
      1. Clean Native (obj, libs)
      2. Clean Gradle (.cxx, build)
      3. Build native (server + client .so)
      4. Copy .so -> jniLibs
      5. Gradle assembleRelease (signed APK)
      6. Deploy APK via adb

.PARAMETER CleanNative
    Remove CSPB native build artifacts
    (obj, libs) before building.

.PARAMETER CleanGradle
    Remove Gradle/Android build artifacts
    (.cxx, build, .gradle) before packaging.

.PARAMETER ForceGradleClean
    Aggressive Gradle cleanup: kills Java
    processes, removes persistent caches.

.PARAMETER SkipNative
    Skip native build step (server + client .so).
    Uses existing .so files.

.PARAMETER SkipPackage
    Skip the Gradle APK packaging step.

.PARAMETER SkipDeploy
    Skip the adb install step.

.PARAMETER Uninstall
    Uninstall app from device before
    installing the new APK.

.PARAMETER DeployOnly
    Shortcut: SkipNative -SkipPackage
    (only deploy existing APK).

.PARAMETER NativeOnly
    Shortcut: SkipPackage -SkipDeploy
    (only build native .so).

.PARAMETER QuickBuild
    Shortcut: SkipClean -SkipDeploy
    (build + package, don't deploy).

.EXAMPLE
    .\build-and-deploy.ps1
    Full rebuild + deploy

.EXAMPLE
    .\build-and-deploy.ps1 -NativeOnly
    Only build .so files

.EXAMPLE
    .\build-and-deploy.ps1 -DeployOnly
    Only install existing APK

.EXAMPLE
    .\build-and-deploy.ps1 -QuickBuild
    Build + package, no deploy

.EXAMPLE
    .\build-and-deploy.ps1 -ForceGradleClean -Uninstall
    Fresh everything
#>

param(
    [switch]$CleanNative,
    [switch]$CleanGradle,
    [switch]$ForceGradleClean,
    [switch]$SkipNative,
    [switch]$SkipPackage,
    [switch]$SkipDeploy,
    [switch]$Uninstall,
    [switch]$DeployOnly,
    [switch]$NativeOnly,
    [switch]$QuickBuild
)

# ─── Paths ────────────────────────────────────────────────────────
$ROOT_DIR          = $PSScriptRoot
$CSPB_SRC_DIR      = Join-Path $ROOT_DIR "CSPB-ANDROID-OPEN-SOURCE"
$ANDROID_DIR       = Join-Path $ROOT_DIR "xash3d-fwgs" "android"
$JNILIBS_DIR       = Join-Path $ANDROID_DIR "app" "src" "main" `
                        "jniLibs" "arm64-v8a"
$APK_PATH          = Join-Path $ANDROID_DIR "app" "build" `
                        "outputs" "apk" "release" "app-release.apk"
$PHONE_APK_PATH    = "/sdcard/Download/com.cspb.blankout-release.apk"
$NDK_BUILD         = "$env:LOCALAPPDATA\Android\Sdk\ndk\" + `
                        "30.0.14904198\ndk-build.cmd"
$APP_PACKAGE       = "com.cspb.blankout"
$SERVER_MODULE     = "cspb_server_android_arm64"
$CLIENT_MODULE     = "cspb_client_android_arm64"
$SERVER_SO_NAME    = "lib${SERVER_MODULE}.so"
$CLIENT_SO_NAME    = "lib${CLIENT_MODULE}.so"
$BUILD_LOGS_DIR    = Join-Path $ROOT_DIR "build_logs"

# ─── Color Output Helpers ─────────────────────────────────────────
function Write-OK    { Write-Host "[OK] $($args -join ' ')" `
                          -ForegroundColor Green }
function Write-Warn  { Write-Host "[WARN] $($args -join ' ')" `
                          -ForegroundColor Yellow }
function Write-Error { Write-Host "[ERROR] $($args -join ' ')" `
                          -ForegroundColor Red }
function Write-Info  { Write-Host "[INFO] $($args -join ' ')" `
                          -ForegroundColor Cyan }
function Write-Step  { Write-Host "`n===== $($args -join ' ') " `
                          "=====" -ForegroundColor Magenta }

# ─── Shortcut logic ────────────────────────────────────────────────
if ($DeployOnly)   { $SkipNative = $true; $SkipPackage = $true }
if ($NativeOnly)   { $SkipPackage = $true; $SkipDeploy = $true }
if ($QuickBuild)   { $SkipDeploy = $true }

# ─── Log setup ─────────────────────────────────────────────────────
$timestamp      = Get-Date -Format "yyyyMMdd_HHmmss"
$RUN_LOG_DIR    = Join-Path $BUILD_LOGS_DIR "full" $timestamp
$LATEST_LOG_DIR = Join-Path $BUILD_LOGS_DIR "full" "latest"
$null = New-Item -ItemType Directory -Path $RUN_LOG_DIR -Force
$null = New-Item -ItemType Directory -Path $LATEST_LOG_DIR -Force

$GLOBAL_LOG = Join-Path $RUN_LOG_DIR "build-and-deploy.log"
$null = Out-File -FilePath $GLOBAL_LOG -Encoding utf8

function Write-Log {
    param([string]$Level, [string]$Message)
    $line = "[$Level] $(Get-Date -Format 'HH:mm:ss') $Message"
    Add-Content -Path $GLOBAL_LOG -Value $line
}

function Write-HostAndLog {
    param([string]$Level, [string]$Message)
    switch ($Level) {
        'OK'    { Write-OK $Message }
        'WARN'  { Write-Warn $Message }
        'ERROR' { Write-Error $Message }
        'INFO'  { Write-Info $Message }
        'STEP'  { Write-Step $Message }
        default { Write-Host $Message }
    }
    Write-Log -Level $Level -Message $Message
}

# ─── Utility functions ─────────────────────────────────────────────
function Remove-DirIfExists {
    param([string]$Path)
    if (Test-Path $Path) {
        Write-HostAndLog -Level INFO -Message "Removing: $Path"
        try {
            Remove-Item -Path $Path -Recurse -Force `
                -ErrorAction Stop
            if (-not (Test-Path $Path)) {
                Write-HostAndLog -Level OK -Message "Done: $Path"
            } else {
                Write-HostAndLog -Level WARN `
                    -Message "Failed to remove: $Path (locked)"
            }
        } catch {
            Write-HostAndLog -Level WARN `
                -Message "Failed: $Path ($($_.Exception.Message))"
            Start-Sleep -Seconds 2
            try {
                Remove-Item -Path $Path -Recurse -Force `
                    -ErrorAction Stop
                if (-not (Test-Path $Path)) {
                    Write-HostAndLog -Level OK -Message "Done: $Path (retry)"
                }
            } catch {
                Write-HostAndLog -Level WARN `
                    -Message "Still locked: $Path"
            }
        }
    } else {
        Write-HostAndLog -Level INFO `
            -Message "Not found, skipping: $Path"
    }
}

function Test-Command {
    param([string]$Path)
    return (Get-Command $Path -ErrorAction SilentlyContinue) -ne $null
}

function Invoke-GradleStop {
    $gradlew = Join-Path $ANDROID_DIR "gradlew.bat"
    if (Test-Path $gradlew) {
        Push-Location $ANDROID_DIR
        try {
            & $gradlew --stop 2>&1 | Out-Null
            Write-HostAndLog -Level INFO -Message "Gradle daemon stopped"
        } catch {
            # Graceful fail
        } finally {
            Pop-Location
        }
    }
}

# ─── Step 0: Clean Native ─────────────────────────────────────────
function Step-CleanNative {
    Write-Step "Step 0/5: Clean Native"
    Write-Log -Level STEP -Message "Clean Native"
    Remove-DirIfExists -Path (Join-Path $CSPB_SRC_DIR "obj")
    Remove-DirIfExists -Path (Join-Path $CSPB_SRC_DIR "libs")
    Write-HostAndLog -Level OK -Message "Native cleanup finished"
}

# ─── Step 1: Clean Gradle ─────────────────────────────────────────
function Step-CleanGradle {
    param([switch]$Force)
    Write-Step "Step 1/5: Clean Gradle"
    Write-Log -Level STEP -Message "Clean Gradle"

    if ($Force) {
        Write-HostAndLog -Level INFO -Message "Forced cleanup requested"
        Invoke-GradleStop
        try { Get-Process java -ErrorAction SilentlyContinue `
                | Stop-Process -Force } catch {}
        try { Get-Process javaw -ErrorAction SilentlyContinue `
                | Stop-Process -Force } catch {}
        Start-Sleep -Seconds 2
    } else {
        Invoke-GradleStop
    }

    Remove-DirIfExists -Path (Join-Path $ANDROID_DIR "app" ".cxx")
    Remove-DirIfExists -Path (Join-Path $ANDROID_DIR "app" "build")
    Remove-DirIfExists -Path (Join-Path $ANDROID_DIR "build")

    if ($Force) {
        Remove-DirIfExists -Path (Join-Path $ANDROID_DIR `
            ".gradle-user-home")
        Get-ChildItem -Path $ANDROID_DIR -Directory `
            -Filter ".gradle-user-home-run-*" | ForEach-Object {
                Remove-DirIfExists -Path $_.FullName
            }
    }

    if ($env:GRADLE_USER_HOME) {
        Remove-DirIfExists -Path $env:GRADLE_USER_HOME
    }

    Write-HostAndLog -Level OK -Message "Gradle cleanup finished"
}

# ─── Step 2: Build Native ─────────────────────────────────────────
function Step-BuildNative {
    Write-Step "Step 2/5: Build Native (server + client)"
    Write-Log -Level STEP -Message "Build Native"

    if (-not (Test-Path $NDK_BUILD)) {
        Write-HostAndLog -Level ERROR `
            -Message "NDK not found: $NDK_BUILD"
        return $false
    }

    $serverLog = Join-Path $RUN_LOG_DIR "01-server-arm64.log"
    $clientLog = Join-Path $RUN_LOG_DIR "02-client-arm64.log"

    # ── Build Server ──
    Write-HostAndLog -Level INFO -Message "Building server arm64..."
    Push-Location $CSPB_SRC_DIR
    try {
        $serverResult = & $NDK_BUILD APP_ABI=arm64-v8a `
            APP_PLATFORM=android-21 `
            APP_MODULES=$SERVER_MODULE -j8 2>&1 `
            | Tee-Object -FilePath $serverLog
        $serverExit = $LASTEXITCODE
        if ($serverExit -ne 0) {
            Write-HostAndLog -Level ERROR `
                -Message "Server build failed (exit $serverExit)"
            Write-HostAndLog -Level INFO -Message "See: $serverLog"
            return $false
        }
        Write-HostAndLog -Level OK -Message "Server built"
    } finally {
        Pop-Location
    }

    # ── Build Client ──
    Write-HostAndLog -Level INFO -Message "Building client arm64..."
    Push-Location $CSPB_SRC_DIR
    try {
        $clientResult = & $NDK_BUILD APP_ABI=arm64-v8a `
            APP_PLATFORM=android-21 `
            APP_MODULES=$CLIENT_MODULE -j8 2>&1 `
            | Tee-Object -FilePath $clientLog
        $clientExit = $LASTEXITCODE
        if ($clientExit -ne 0) {
            Write-HostAndLog -Level ERROR `
                -Message "Client build failed (exit $clientExit)"
            Write-HostAndLog -Level INFO -Message "See: $clientLog"
            return $false
        }
        Write-HostAndLog -Level OK -Message "Client built"
    } finally {
        Pop-Location
    }

    # ── Verify ──
    $serverSo = Join-Path $CSPB_SRC_DIR "libs" "arm64-v8a" `
        $SERVER_SO_NAME
    $clientSo = Join-Path $CSPB_SRC_DIR "libs" "arm64-v8a" `
        $CLIENT_SO_NAME

    if (-not (Test-Path $serverSo)) {
        Write-HostAndLog -Level ERROR `
            -Message "Server .so not found: $serverSo"
        return $false
    }
    if (-not (Test-Path $clientSo)) {
        Write-HostAndLog -Level ERROR `
            -Message "Client .so not found: $clientSo"
        return $false
    }

    $serverSize = (Get-Item $serverSo).Length
    $clientSize = (Get-Item $clientSo).Length
    Write-HostAndLog -Level OK `
        -Message "Server: $SERVER_SO_NAME ($serverSize bytes)"
    Write-HostAndLog -Level OK `
        -Message "Client: $CLIENT_SO_NAME ($clientSize bytes)"

    # Backup
    $backupDir = Join-Path $ROOT_DIR "xash_build_output"
    $null = New-Item -ItemType Directory -Path $backupDir -Force
    Copy-Item $serverSo (Join-Path $backupDir $SERVER_SO_NAME) -Force
    Copy-Item $clientSo (Join-Path $backupDir $CLIENT_SO_NAME) -Force
    Write-HostAndLog -Level INFO -Message "Backed up: $backupDir"

    return $true
}

# ─── Step 3: Copy .so to jniLibs ──────────────────────────────────
function Step-CopySoToJniLibs {
    Write-Step "Step 3/5: Copy .so to jniLibs"
    Write-Log -Level STEP -Message "Copy .so to jniLibs"

    $null = New-Item -ItemType Directory -Path $JNILIBS_DIR -Force

    $serverSo = Join-Path $CSPB_SRC_DIR "libs" "arm64-v8a" `
        $SERVER_SO_NAME
    $clientSo = Join-Path $CSPB_SRC_DIR "libs" "arm64-v8a" `
        $CLIENT_SO_NAME

    $copied = $false

    if (Test-Path $serverSo) {
        Copy-Item $serverSo (Join-Path $JNILIBS_DIR `
            $SERVER_SO_NAME) -Force
        Write-HostAndLog -Level OK -Message "Copied server"
        $copied = $true
    } else {
        Write-HostAndLog -Level WARN "Server .so not found"
    }

    if (Test-Path $clientSo) {
        Copy-Item $clientSo (Join-Path $JNILIBS_DIR `
            $CLIENT_SO_NAME) -Force
        Write-HostAndLog -Level OK -Message "Copied client"
        $copied = $true
    } else {
        Write-HostAndLog -Level WARN "Client .so not found"
    }

    # Copy libvgui_support.so if exists
    $vguiSo = Join-Path $ROOT_DIR "xash3d-fwgs" "build" `
        "android_arm64-v8a" "libvgui_support.so"
    if (Test-Path $vguiSo) {
        Copy-Item $vguiSo (Join-Path $JNILIBS_DIR `
            "libvgui_support.so") -Force
        Write-HostAndLog -Level OK -Message "Copied vgui support"
    }

    if (-not $copied) {
        Write-HostAndLog -Level ERROR -Message "No .so copied"
        return $false
    }

    Write-HostAndLog -Level OK -Message "jniLibs updated:"
    Get-ChildItem $JNILIBS_DIR -Filter "*.so" | ForEach-Object {
        Write-HostAndLog -Level OK -Message "  $($_.Name) "
            "($($_.Length) bytes)"
    }

    return $true
}

# ─── Step 4: Package Release ──────────────────────────────────────
function Step-PackageRelease {
    Write-Step "Step 4/5: Package Signed Release APK"
    Write-Log -Level STEP -Message "Package Signed Release APK"

    $gradlew = Join-Path $ANDROID_DIR "gradlew.bat"
    if (-not (Test-Path $gradlew)) {
        Write-HostAndLog -Level ERROR `
            -Message "gradlew.bat not found: $gradlew"
        return $false
    }

    $keystore = Join-Path $ANDROID_DIR "keystore.properties"
    if (-not (Test-Path $keystore)) {
        Write-HostAndLog -Level ERROR "keystore.properties not found"
        return $false
    }

    $packageLog = Join-Path $RUN_LOG_DIR "04-assemble-release.log"

    # Ensure jniLibs has latest .so
    $stepResult = Step-CopySoToJniLibs
    if (-not $stepResult) { return $false }

    # Run Gradle assembleRelease
    Write-HostAndLog -Level INFO -Message "Gradle assembleRelease..."
    Push-Location $ANDROID_DIR
    try {
        & $gradlew clean 2>&1 | Out-Null

        $gradleResult = & $gradlew app:assembleRelease 2>&1 `
            | Tee-Object -FilePath $packageLog
        $gradleExit = $LASTEXITCODE

        if ($gradleExit -ne 0) {
            Write-HostAndLog -Level WARN "Build failed, recovering..."
            Invoke-GradleStop

            $transformsDir = Join-Path $ANDROID_DIR `
                ".gradle-user-home\caches\9.2.1\transforms"
            $modulesDir = Join-Path $ANDROID_DIR `
                ".gradle-user-home\caches\modules-2"

            if (Test-Path $transformsDir) {
                Remove-Item $transformsDir -Recurse -Force `
                    -ErrorAction SilentlyContinue }
            if (Test-Path $modulesDir) {
                Remove-Item $modulesDir -Recurse -Force `
                    -ErrorAction SilentlyContinue }

            Remove-DirIfExists -Path (Join-Path $ANDROID_DIR `
                "app" "build")
            Remove-DirIfExists -Path (Join-Path $ANDROID_DIR "build")

            $null = Step-CopySoToJniLibs

            Write-HostAndLog -Level INFO "Retrying..."
            $gradleResult = & $gradlew app:assembleRelease `
                --rerun-tasks 2>&1 | Tee-Object -FilePath $packageLog
            $gradleExit = $LASTEXITCODE

            if ($gradleExit -ne 0) {
                Write-HostAndLog -Level ERROR `
                    "Gradle failed after recovery (exit $gradleExit)"
                Write-HostAndLog -Level INFO "See: $packageLog"
                return $false
            }
        }
    } finally {
        Pop-Location
    }

    if (-not (Test-Path $APK_PATH)) {
        Write-HostAndLog -Level ERROR "APK not found: $APK_PATH"
        return $false
    }

    $apkSize = (Get-Item $APK_PATH).Length
    Write-HostAndLog -Level OK "APK: $APK_PATH ($apkSize bytes)"

    $releaseDir = Join-Path $ROOT_DIR "release"
    $null = New-Item -ItemType Directory -Path $releaseDir -Force
    Copy-Item $APK_PATH (Join-Path $releaseDir `
        "CSPB-Blankout-release.apk") -Force
    Write-HostAndLog -Level OK "APK copied to release dir"

    return $true
}

# ─── Step 5: Deploy to Device ─────────────────────────────────────
function Step-Deploy {
    Write-Step "Step 5/5: Deploy to Device"
    Write-Log -Level STEP -Message "Deploy to Device"

    if (-not (Test-Command "adb")) {
        Write-HostAndLog -Level ERROR "adb not found in PATH"
        return $false
    }

    $deviceState = adb get-state 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-HostAndLog -Level ERROR "No device detected"
        return $false
    }

    $deviceName = (adb devices | Select-Object -Skip 1 `
        | Where-Object { $_ -match 'device$' } `
        | ForEach-Object { ($_ -split '\s+')[0] })
    Write-HostAndLog -Level OK "Device: $deviceName"

    if (-not (Test-Path $APK_PATH)) {
        Write-HostAndLog -Level ERROR "APK not found: $APK_PATH"
        return $false
    }

    if ($Uninstall) {
        Write-HostAndLog -Level INFO "Uninstalling..."
        $uninstallResult = adb uninstall $APP_PACKAGE 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-HostAndLog -Level WARN "Uninstall returned: "
                "$uninstallResult (continuing)"
        } else {
            Write-HostAndLog -Level OK "Uninstalled: $APP_PACKAGE"
        }
    }

    Write-HostAndLog -Level INFO "Pushing APK..."
    $pushResult = adb push "$APK_PATH" "$PHONE_APK_PATH" 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-HostAndLog -Level ERROR "Failed to push: $pushResult"
        return $false
    }
    Write-HostAndLog -Level OK "APK pushed to: $PHONE_APK_PATH"

    Write-HostAndLog -Level INFO "Installing..."
    $installResult = adb install -r "$APK_PATH" 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-HostAndLog -Level ERROR "Install failed: $installResult"
        return $false
    }

    Write-HostAndLog -Level OK "Install successful!"
    Write-HostAndLog -Level INFO "APK on device: $PHONE_APK_PATH"
    return $true
}

# ─── Main ─────────────────────────────────────────────────────────
Write-Host ""
Write-Host "╔═══════════════════════════════════════╗" `
    -ForegroundColor Cyan
Write-Host "║ CSPB Blankout — Build & Deploy ║" `
    -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════╝" `
    -ForegroundColor Cyan
Write-Host ""

Write-HostAndLog -Level INFO -Message "Root: $ROOT_DIR"
Write-HostAndLog -Level INFO -Message "Log : $GLOBAL_LOG"

$global:exitCode = 0

try {
    if ($CleanNative -and (-not $SkipNative)) {
        Step-CleanNative
    }

    if ($CleanGradle) {
        Step-CleanGradle
    } elseif ($ForceGradleClean) {
        Step-CleanGradle -Force
    }

    if (-not $SkipNative) {
        $result = Step-BuildNative
        if (-not $result) { throw "Native build failed" }
    } else {
        Write-HostAndLog -Level INFO "Skipping native build"
    }

    if (-not $SkipPackage) {
        $result = Step-CopySoToJniLibs
        if (-not $result) { throw "Copy .so failed" }
    }

    if (-not $SkipPackage) {
        $result = Step-PackageRelease
        if (-not $result) { throw "Package release failed" }
    } else {
        Write-HostAndLog -Level INFO "Skipping package"
    }

    if (-not $SkipDeploy) {
        $result = Step-Deploy
        if (-not $result) { throw "Deploy failed" }
    } else {
        Write-HostAndLog -Level INFO "Skipping deploy"
    }

    Write-Host ""
    Write-Host "[SUCCESS] All steps completed." `
        -ForegroundColor Green
    Write-Host "[SUCCESS] Full log: $GLOBAL_LOG" `
        -ForegroundColor Green

} catch {
    Write-Host ""
    Write-Host "[FAILED] $($_.Exception.Message)" `
        -ForegroundColor Red
    Write-Log -Level ERROR -Message $_.Exception.Message
    $global:exitCode = 1
} finally {
    $null = New-Item -ItemType Directory `
        -Path $LATEST_LOG_DIR -Force
    Copy-Item -Path $GLOBAL_LOG `
        -Destination (Join-Path $LATEST_LOG_DIR `
        "build-and-deploy.log") -Force -ErrorAction SilentlyContinue
}

exit $global:exitCode
