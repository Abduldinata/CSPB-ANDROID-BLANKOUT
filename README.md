# CSPB Android Blankout

Workspace root ini sudah dirapikan supaya alur build lebih jelas.

## Workflow Aktif

Pakai script ini saja sebagai entry point:

- `clean-native.bat`
- `clean-gradle.bat`
- `clean-gradle-force.bat`
- `build-native.bat`
- `package-release.bat`
- `deploy-release.bat`

## Urutan Yang Disarankan

Rebuild penuh:

1. `.\clean-native.bat`
2. `.\clean-gradle.bat`
3. `.\build-native.bat`
4. `.\package-release.bat`
5. `.\deploy-release.bat`

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
- Lihat `BUILD_WORKFLOW.md` untuk penjelasan per tahap.
