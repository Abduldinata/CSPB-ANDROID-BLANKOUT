# Weapon Tracking CSPB

Dokumen ini merangkum hasil tracking dari source `CSPB-ANDROID-OPEN-SOURCE/jni/dlls/wpn_shared` dan data aktif `files/cspb/weapon_list`.

## Kesimpulan utama

`weapon_pgm` dan `weapon_m1887_w` bukan weapon "bekas setengah jadi" di source ini.

Bukti:
- `weapon_pgm` punya class sendiri di [wpn_pgm.cpp](/E:/Games/PROJECT_LOBBY_CSPB/com.cspb.m/CSPB-ANDROID-OPEN-SOURCE/jni/dlls/wpn_shared/wpn_pgm.cpp)
  - `LINK_ENTITY_TO_CLASS(weapon_pgm, CPGM)` pada line 40
  - `Spawn` pada line 42
  - `Precache` pada line 54
  - `Deploy` pada line 92
- `weapon_m1887_w` punya class sendiri di [wpn_m1887.cpp](/E:/Games/PROJECT_LOBBY_CSPB/com.cspb.m/CSPB-ANDROID-OPEN-SOURCE/jni/dlls/wpn_shared/wpn_m1887.cpp)
  - `LINK_ENTITY_TO_CLASS(weapon_m1887_w, CM1887_W)` pada line 483
  - `Precache` pada line 497
  - `Deploy` pada line 536

Artinya:
- keduanya memang sudah diregister di DLL
- keduanya memang dipanggil di precache
- FC lebih mungkin karena runtime load/precache/asset mismatch, bukan karena weapon belum didaftarkan sama sekali

## Batch weapon baru Bill di inventory utama

Urutan ini terlihat di [client.cpp](/E:/Games/PROJECT_LOBBY_CSPB/com.cspb.m/CSPB-ANDROID-OPEN-SOURCE/jni/dlls/client.cpp) dan [weapons_precache.cpp](/E:/Games/PROJECT_LOBBY_CSPB/com.cspb.m/CSPB-ANDROID-OPEN-SOURCE/jni/dlls/weapons_precache.cpp).

Batch `new`:
- `46 = weapon_aksopmod_cg`
- `47 = weapon_aug_esport`
- `48 = weapon_t77`
- `49 = weapon_apc`
- `50 = weapon_fg42`
- `51 = weapon_msbs`
- `52 = weapon_as50`
- `53 = weapon_m1887_w`
- `54 = weapon_pgm`
- `55 = weapon_ump`
- `56 = weapon_sig`
- `57 = weapon_spectre`
- `58 = weapon_tar`
- `59 = weapon_xm8`
- `60 = weapon_water`

## Urutan load setelah PGM

Di [weapons_precache.cpp](/E:/Games/PROJECT_LOBBY_CSPB/com.cspb.m/CSPB-ANDROID-OPEN-SOURCE/jni/dlls/weapons_precache.cpp), setelah `weapon_pgm` urutannya adalah:

1. `weapon_ump`
2. `weapon_sig`
3. `weapon_spectre`
4. `weapon_tar`
5. `weapon_xm8`
6. `weapon_water`

Kalau log terakhir berhenti "setelah pgm", maka kandidat berikutnya adalah block ini, bukan medkit.

## Weapon custom yang ada di source tapi bukan inventory utama

Weapon berikut ada class di source, tetapi tidak muncul di `inventory_all.txt`:
- `weapon_amok`
- `weapon_arabian_sword`
- `weapon_auggold`
- `weapon_bow`
- `weapon_brass_knuckle`
- `weapon_butterfly`
- `weapon_c4`
- `weapon_candy_cane`
- `weapon_colt_python`
- `weapon_combat`
- `weapon_deagle`
- `weapon_deagle_dual`
- `weapon_dual_handgun`
- `weapon_dual_knife`
- `weapon_fangblade`
- `weapon_flashbang`
- `weapon_gasbomb`
- `weapon_glock18`
- `weapon_hegrenade`
- `weapon_ice`
- `weapon_karambit`
- `weapon_keris`
- `weapon_knife`
- `weapon_knifebone`
- `weapon_kriss_sv_dual`
- `weapon_kriss_sv_dual_crb`
- `weapon_kriss_sv_dual_silence`
- `weapon_m4_azure`
- `weapon_medkit`
- `weapon_mini_axe`
- `weapon_oa93_dual`
- `weapon_python`
- `weapon_pyton`
- `weapon_saber`
- `weapon_smokegrenade`
- `weapon_t77_dual`
- `weapon_taurus_raging_bull`
- `weapon_usp`

Catatan:
- banyak dari daftar ini memang masuk kategori lain seperti `secondary`, `melee`, `special`, `explosive`
- beberapa sisanya adalah variant/internal alias dan tidak selalu muncul di buy menu utama

## Item yang ada di inventory utama tapi tidak ada class source dengan nama yang sama

Daftar ini perlu perhatian khusus:
- `weapon_ak47_fc`
- `weapon_hk417`
- `weapon_sf`

Artinya nama di inventory aktif tidak punya `LINK_ENTITY_TO_CLASS` dengan nama identik di folder `wpn_shared` yang dicek.

Kemungkinan:
- ada alias/redirect di file lain
- atau datanya diwariskan dari versi lama tetapi code class-nya sekarang beda nama

## Medkit

`weapon_medkit` memang ada dan valid di source:
- class ada di [wpn_medkit.cpp](/E:/Games/PROJECT_LOBBY_CSPB/com.cspb.m/CSPB-ANDROID-OPEN-SOURCE/jni/dlls/wpn_shared/wpn_medkit.cpp)
- diprecache di [weapons_precache.cpp](/E:/Games/PROJECT_LOBBY_CSPB/com.cspb.m/CSPB-ANDROID-OPEN-SOURCE/jni/dlls/weapons_precache.cpp)

Tetapi medkit bukan bagian blok setelah `weapon_pgm`, jadi kecil kemungkinan menjadi penyebab FC yang terjadi tepat setelah load sniper/custom rifle batch akhir.

## Hipotesis kerja saat ini

Yang paling mungkin sekarang:
- `weapon_pgm` memang valid, tetapi crash bisa terjadi:
  - saat `weapon_pgm` runtime load asset/script tertentu
  - atau pada weapon setelahnya: `ump`, `sig`, `spectre`, `tar`, `xm8`, `water`
- ada mismatch asset/script lama vs struktur Bill baru, terutama transisi asset ke `gfx/billflx`

## Next step yang disarankan

1. Build ulang dengan log granular precache yang sudah dipasang.
2. Ambil log baru.
3. Lihat `START/DONE` terakhir pada block:
   - `weapon_pgm`
   - `weapon_ump`
   - `weapon_sig`
   - `weapon_spectre`
   - `weapon_tar`
   - `weapon_xm8`
4. Setelah nama weapon terakhir diketahui, audit source + script weapon itu secara spesifik.
