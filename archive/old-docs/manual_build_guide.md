# Panduan Build Manual CSPB Android (arm64-v8a)

Gunakan panduan ini jika kamu ingin memastikan setiap perubahan kode (Engine maupun Mod) benar-benar masuk ke dalam APK.

## Persiapan Lingkungan (Terminal)
Setiap kali membuka Terminal baru, pastikan NDK Home sudah di-set:
```powershell
$env:ANDROID_NDK_HOME="C:\Users\gitzr\AppData\Local\Android\Sdk\ndk\30.0.14904198"
```

---

## Langkah 1: Rebuild Engine (Xash3D)
Lakukan ini jika ada perubahan di folder `xash3d-fwgs` (seperti fix memori 22MB).

1. Masuk ke folder android engine:
   ```powershell
   cd E:\Games\PROJECT_LOBBY_CSPB\com.cspb.m\xash3d-fwgs\android
   ```
2. Jalankan Build (Gunakan `--rerun-tasks` jika ingin benar-benar bersih):
   ```powershell
   .\gradlew assembleDebug --rerun-tasks
   ```
3. Tunggu sampai muncul **BUILD SUCCESSFUL**.

---

## Langkah 2: Build Game Logic (Mod CSPB)
Lakukan ini jika ada perubahan di folder `CSPB-ANDROID-OPEN-SOURCE` (seperti fix crash vsnprintf).

1. Masuk ke folder root project:
   ```powershell
   cd E:\Games\PROJECT_LOBBY_CSPB\com.cspb.m
   ```
2. Build Server:
   ```powershell
   .\bat_build_ndk_server_arm64.bat
   ```
3. Build Client:
   ```powershell
   .\bat_build_ndk_client_arm64.bat
   ```

---

## Langkah 3: Sinkronisasi Library (.so)
Langkah ini untuk mengumpulkan hasil build dari Langkah 1 & 2 ke dalam folder yang siap dibungkus APK.

1. Jalankan skrip copy:
   ```powershell
   .\bat_copy_so_to_jnilibs_arm64.bat
   ```

---

## Langkah 4: Build APK Final
Langkah terakhir untuk membuat file APK yang bisa diinstall.

1. Jalankan skrip build APK:
   ```powershell
   .\bat_build_release_signed.bat
   ```
2. File APK akan ada di:
   `E:\Games\PROJECT_LOBBY_CSPB\com.cspb.m\xash3d-fwgs\android\app\build\outputs\apk\release\app-release.apk`

---

## Tips Troubleshooting
* **Jika Stuck di "Initializing":** Tunggu saja, Gradle sedang mendownload dependensi atau menyiapkan daemon.
* **Jika Error "SDL not found":** Pastikan folder `3rdparty/SDL` ada di tempatnya.
* **Jika APK masih berat:** Ulangi Langkah 1 dengan flag `--rerun-tasks`.
