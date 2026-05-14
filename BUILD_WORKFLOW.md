# Build Workflow

## Entry Points

- `clean-native.bat`
  Menghapus `CSPB-ANDROID-OPEN-SOURCE\obj` dan `CSPB-ANDROID-OPEN-SOURCE\libs`.

- `clean-gradle.bat`
  Menghapus:
  - `xash3d-fwgs\android\app\.cxx`
  - `xash3d-fwgs\android\app\build`
  - `xash3d-fwgs\android\build`
  - `.gradle-user-home-run-*`
  - `GRADLE_USER_HOME` jika sedang diset

- `clean-gradle-force.bat`
  Versi agresif. Selain langkah `clean-gradle.bat`, script ini juga mencoba:
  - stop Gradle
  - kill `java.exe` dan `javaw.exe`
  - hapus `.gradle-user-home`
  - fallback rename-then-delete bila lock transient masih muncul

- `build-native.bat`
  Build server, build client, lalu copy `.so` ke `jniLibs`.

- `package-release.bat`
  Package signed release APK.

- `deploy-release.bat`
  Install APK release ke device.

## Full Refresh

1. `clean-native.bat`
2. `clean-gradle.bat`
3. `build-native.bat`
4. `package-release.bat`
5. `deploy-release.bat`

## Repackage Only

1. `clean-gradle.bat`
2. `package-release.bat`
3. `deploy-release.bat`

## Kapan Pakai Force

Pakai `clean-gradle-force.bat` hanya jika cache `.gradle-user-home` memang sedang bandel atau kamu ingin mencoba sapu cache Gradle lebih agresif sebelum packaging.
