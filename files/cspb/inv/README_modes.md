# Mode Templates (`.cfgb`)

File di folder ini sengaja memakai ekstensi `.cfgb` supaya **tidak aktif otomatis**.

## Cara pakai

- Kalau masih mau disimpan sebagai template: biarkan `.cfgb`
- Kalau mau dipakai:
  - rename jadi `.cfg`, lalu `exec` file itu
  - atau copy isi file `.cfgb` ke `.cfg` lain yang memang kamu panggil

## Tujuan

Template ini dipakai untuk mengunci kombinasi:

- `mp_gamemode`
- `inv_profile`

Jadi nanti mode dan inventory bisa kamu aktifkan bareng, tapi tetap aman selama masih `.cfgb`.

## Contoh

- `mode_tdm_default.cfgb`
- `mode_sniper_only.cfgb`
- `mode_shotgun_only.cfgb`
- `mode_knife_only.cfgb`
- `mode_primary_only.cfgb`

## Catatan

- `inv_profile default` = kembali ke list weapon normal
- profile lain seperti `sniperonly`, `shotgunonly`, `knifeonly`, `primaryonly` hanya akan benar-benar terasa kalau file override inventory terkait memang ada / nanti kamu siapkan
- untuk sekarang file ini aku buat sebagai **template dormant** dulu biar tidak mengganggu flow yang sudah ada
