# Weapon List (`files/cspb/weapon_list`) — V16 Behavior Notes

Folder ini dipakai untuk menentukan **daftar weapon yang muncul/diizinkan** di inventory/buy flow (OINV/NEDA), tanpa perlu edit CPP lagi.

## 1) Default files (selalu jadi fallback)
File default yang dibaca kalau tidak ada override:

- `inventory_all.txt` (Primary: tdm/none/default)
- `inventory_shotgun.txt` (Primary: sg/sgb)
- `inventory_sniper.txt` (Primary: sniper/sniperB)
- `inventory_secondary.txt`
- `inventory_melee.txt`
- `inventory_explosive.txt`
- `inventory_special.txt`

Format isi file: satu weapon per baris, **wajib** `weapon_<id>`:
```
weapon_ak47
weapon_m4a1
weapon_awp
```

Komentar boleh:
- Baris yang diawali `#` atau `//` diabaikan.

## 2) Override rules: `inv_profile` (prioritas tertinggi)
Di V16 sekarang ada cvar baru:

- `inv_profile` (default: `default`)

Kalau `inv_profile` bukan `default` / bukan kosong, client akan cari file override:

```
inventory_all_<inv_profile>.txt
inventory_shotgun_<inv_profile>.txt
inventory_sniper_<inv_profile>.txt
inventory_secondary_<inv_profile>.txt
inventory_melee_<inv_profile>.txt
inventory_explosive_<inv_profile>.txt
inventory_special_<inv_profile>.txt
```

Contoh:
- `inv_profile sniperonly`
  - `inventory_secondary_sniperonly.txt` bisa **kosong** untuk disable secondary.
  - `inventory_explosive_sniperonly.txt` bisa **kosong** untuk disable explosive.

Catatan:
- Kalau file override **ada tapi kosong**, itu dianggap “category di-disable” (tidak fallback ke default).
- Kalau file override **tidak ada**, baru fallback ke default.

## 3) Override rules: `<mp_gamemode>` (fallback kedua)
Kalau `inv_profile=default`, client akan coba override berdasarkan `mp_gamemode`:

```
inventory_all_<mp_gamemode>.txt
inventory_secondary_<mp_gamemode>.txt
...dst
```

Lalu fallback ke file default.

## 4) Primary list selection (sniper/sg)
- Kalau `inv_profile` mengandung kata `sniper` → primary pakai list sniper.
- Kalau `inv_profile` mengandung `sg` atau `shotgun` → primary pakai list shotgun.
- Selain itu → pakai list `inventory_all*`.

Ini biar lobby bisa enforce “sniper only / sg only” walau server mode-nya TDM/eliminate.

## 5) Penting: list harus match weapon code v16
Kalau kamu masukin `weapon_<id>` yang **belum ada codenya** di v16, biasanya efeknya:
- buy/inventory kosong / command beli gagal / weapon tidak muncul.

Referensi daftar weapon yang ada di v16 ada di:
- `report/v16_weapon_coverage.md`

