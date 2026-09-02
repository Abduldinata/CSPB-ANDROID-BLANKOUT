<p align="center">
  <img src="icon/icon.png" width="120" height="120" alt="CS:PB Android Blankout Logo" />
</p>

<h1 align="center">CS:PB Android Blankout (v1.0)</h1>

<p align="center">
  <em>Modern Point Blank Experience on Android (ARM64 Native Engine + CSPB Mod SDK)</em>
</p>

---

## Ringkasan Proyek

**CS:PB Android Blankout** adalah port dan adaptasi mod Point Blank berbasis engine Xash3D FWGS dan CSPB SDK untuk arsitektur Android 64-bit (`arm64-v8a`). Proyek ini menghadirkan mekanik gameplay, audio vox, kill feed dinamis, optical sight & dynamic crosshair, serta performa native yang mulus di perangkat Android.

---

## Workflow Aktif

Pakai script ini saja sebagai entry point:

- `clean-native.bat`
- `clean-gradle.bat`
- `clean-gradle-force.bat`
- `build-native.bat`
- `package-release.bat`
- `deploy-release.bat`
- `full-rebuild-release.bat`

## Urutan Yang Disarankan

Rebuild penuh:

1. `.\clean-native.bat`
2. `.\clean-gradle.bat`
3. `.\build-native.bat`
4. `.\package-release.bat`
5. `.\deploy-release.bat`

Atau langsung satu file:

1. `.\full-rebuild-release.bat`

`full-rebuild-release.bat` akan mencoba `clean-gradle.bat` dulu, lalu otomatis fallback ke `clean-gradle-force.bat` kalau cleanup biasa masih mengembalikan status gagal.

Kalau hanya ingin memastikan APK dan install device ikut refresh:

1. `.\clean-gradle.bat`
2. `.\package-release.bat`
3. `.\deploy-release.bat`

Kalau cache Gradle persistent sedang terkunci dan ingin dicoba bersihkan lebih agresif, gunakan `.\clean-gradle-force.bat` sebelum langkah package.

## Struktur Singkat

- `CSPB-ANDROID-OPEN-SOURCE/`: source mod/game
- `xash3d-fwgs/`: source engine Android
- `archive/`: script dan dokumen workflow lama

## Catatan

- `bat_build_*` dan `bat_copy_*` adalah script inti yang dipanggil wrapper baru.
- Script legacy yang overlap sudah dipindahkan ke `archive/old-scripts/`.
- `clean-gradle.bat` fokus ke output build dan cache Gradle per-run.
- `clean-gradle-force.bat` dipakai hanya saat `.gradle-user-home` utama sedang bandel.
- `build-native.bat` sekarang membuat log terpisah di `build_logs/native/<timestamp>/`.
- `package-release.bat` sekarang membuat log terpisah di `build_logs/package/<timestamp>/`.
- `deploy-release.bat` sekarang membuat log terpisah di `build_logs/deploy/<timestamp>/`.
- `build-native.bat` dan `package-release.bat` sekarang tetap menampilkan output live di terminal sambil menyimpan log ke file.
- Console `build-native.bat` sekarang juga menampilkan `warning count` dan artifact `.so` hasil build supaya kelihatan kalau compile native benar-benar jalan.
- Folder `xash_build_output/` dipakai sebagai snapshot backup native `.so`. Saat ini server tetap dibackup sebelum build client, dan client juga disnapshot setelah build supaya hasil native run terakhir mudah diverifikasi.
- Folder `build_logs/native/latest/` dan `build_logs/package/latest/` selalu menyimpan salinan log run terakhir.
- Folder `build_logs/deploy/latest/` juga menyimpan salinan log install device terakhir.
- `deploy-release.bat` tidak lagi rename/restore `/sdcard/Android/data/com.cspb.blankout` secara otomatis.
  CSPB cenderung membuat runtime baru setelah install, jadi deploy sekarang fokus ke uninstall/install bersih. Kalau butuh runtime lama, buka app sekali, keluar, lalu copy manual file yang diperlukan ke runtime baru.
- Cari file `*-summary.log` untuk status cepat `SUCCESS` / `FAILED`, lalu buka log step-nya kalau perlu detail warning atau error.
- Lihat `BUILD_WORKFLOW.md` untuk penjelasan per tahap.

## Flow Terminal Biasa

Kalau mau jalankan manual lewat terminal dan tetap rapi, pakai urutan ini:

1. `.\clean-native.bat`
2. `.\clean-gradle-force.bat`
3. `.\build-native.bat`
4. `.\package-release.bat`
5. `.\deploy-release.bat`

Log akan tetap terpisah per tahap:
- native: `build_logs/native/latest/`
- package: `build_logs/package/latest/`
- deploy: `build_logs/deploy/latest/`

Saat `deploy-release.bat`:
- bisa pilih uninstall app lama dulu
- setelah install, biarkan CSPB membuat runtime baru sendiri dulu
- kalau perlu restore runtime lama, pindahkan file/subfolder tertentu secara manual ke runtime baru
