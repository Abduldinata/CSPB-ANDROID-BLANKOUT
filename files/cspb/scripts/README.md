# Weapon Scripts (`files/cspb/scripts`) — V16 Notes

Folder ini berisi metadata weapon per item (`weapon_*.txt`) yang dipakai untuk UI/inventory/buy flow dan beberapa parameter gameplay.

## 1) File naming
- Nama file: `weapon_<id>.txt`
- `<id>` harus konsisten dengan ID weapon yang dipanggil di command `pbbuy weapon_<id>`.

## 2) `WeaponTga:` (icon buy/inventory)
Di versi ini, icon buy/inventory dibaca dari field:

```
WeaponTga: gfx/billflx/weapons/weapon_<id>.png
```

Catatan penting:
- Walaupun field namanya `WeaponTga`, path boleh `.png`.
- Icon inventory/buy yang benar ada di `gfx/billflx/weapons/` dan **prefix file wajib** `weapon_`.

## 3) `DamageTga:` / `SightTga:` (opsional)
Beberapa script juga punya:
- `DamageTga:` (mis. `gfx/billflx/weapon_damage/wpdamage0.tga`)
- `SightTga:` (mis. `gfx/sight/newsight/null.tga`)

Ini tetap optional tergantung weapon.

## 4) Jangan pakai `materials/pb/...` untuk icon baru
Untuk migrasi asset sekarang, hindari path lama seperti:
- `materials/pb/weapons/...`

Gunakan `gfx/billflx/...` supaya konsisten dengan folder `files/cspb/gfx/`.

## 5) Tips troubleshoot
Kalau buy menu/inventory “kosong” atau icon tidak muncul:
- Pastikan `WeaponTga:` mengarah ke file yang benar.
- Pastikan file PNG ada di `files/cspb/gfx/billflx/weapons/`.
- Pastikan weapon ID-nya memang ada di source v16 (lihat `report/v16_weapon_coverage.md`).

