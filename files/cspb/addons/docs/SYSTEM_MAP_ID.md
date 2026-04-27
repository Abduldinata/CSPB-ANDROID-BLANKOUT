# SYSTEM MAP ID - PROJECT LOBBY CSPB

Dokumen ini adalah versi Indonesia dari peta sistem lobby custom CSPB.
Sumber konfigurasi utama tetap berada di [../SYSTEM_MAP.md](../SYSTEM_MAP.md).

## 1. Startup Chain
Urutan load inti:

1. `addons/ineeda.db`
2. `addons/lobby.cfg`
3. `addons/inventory.cfg`

Peran singkat:
- `ineeda.db`: entry point startup dan pemanggil loader inti.
- `lobby.cfg`: deklarasi alias routing (`_load_*`).
- `inventory.cfg`: jembatan ke inventory global dan kategori.

### Trigger Dari Game Bawaan
Flow custom baru aktif saat user klik tombol touch `neda_menu`:

- `touch_addbutton "neda_menu" "addons/neda/image/icon.tga" "touch_setclientonly 1; exec addons/neda/lobby_menu.cfg" 0.920000 0.000000 0.980000 0.129438 255 255 255 178 2`

Sebelum klik tombol ini, game masih berada di flow bawaan CSPB.

## 2. Layer Sistem

### A. Root DB / Router
`ineeda.db` memanggil loader:
- `_load_char_db`
- `_load_main_db`
- `_load_secondary_db`
- `_load_melee_db`
- `_load_explosive_db`
- `_load_special_db`
- `_load_map_db`
- `_load_stat_db`
- `_load_mapmode_control`
- `_load_map_base`
- `_load_mode_base`
- `_load_stat_base`

### B. Alias Declaration Layer
`lobby.cfg` menyimpan definisi alias loader.
Contoh:
- `_load_db` -> `exec addons/ineeda.db`
- `_load_char_db` -> `exec addons/neda/persist/char_db.cfg`
- `_load_main_db` -> `exec addons/neda/persist/main_db.cfg`
- `_load_mapmode_control` -> `exec addons/neda/mapmode_control.cfg`
- `_load_map_base` -> `exec addons/map.cfg`
- `_load_mode_base` -> `exec addons/mode.cfg`
- `_load_stat_base` -> `exec addons/stat.cfg`

### C. Category / Inventory Layer
`inventory.cfg` dan `addons/neda/*/inventory_*.cfg` menangani UI inventory:
- load DB,
- set image,
- tombol back/exit,
- remove alias,
- route kembali ke menu class.

## 3. Database Modular

| Kategori | Folder | Loader |
|---|---|---|
| Character | `addons/neda/persist/character/` | `char_db.cfg` |
| Main Weapon | `addons/neda/persist/main/` | `main_db.cfg` |
| Secondary | `addons/neda/persist/secondary/` | `secondary_db.cfg` |
| Melee | `addons/neda/persist/melee/` | `melee_db.cfg` |
| Explosive | `addons/neda/persist/explosive/` | `explosive_db.cfg` |
| Special | `addons/neda/persist/special/` | `special_db.cfg` |
| Map | `addons/neda/persist/map/` | `map_db.cfg` |
| Mode | `addons/neda/persist/mode/` | `mode_db.cfg` |
| Stat | `addons/neda/persist/stat/` | `stat_db.cfg` |

Catatan: `mapmode_control.cfg` lebih tepat disebut layer kontrol/routing, bukan murni database modular.

## 4. Character DB Routing

### Loader
`_load_char_db` mengeksekusi `addons/neda/persist/char_db.cfg`.

### Default Theme
`char_db.cfg` menentukan default, contoh:
- `_active_char_theme "_db_char_acidpool"`

### Router Per Class
`char_db.cfg` memetakan `_db_char_<class>` ke `db_<class>.cfg`.
Contoh:
- `_db_char_acidpool` -> `db_acidpool.cfg`
- `_db_char_dfox` -> `db_dfox.cfg`
- `_db_char_redbull` -> `db_redbull.cfg`

### Isi `db_<class>.cfg`
Umumnya menyimpan state:
- `_char_p1_badge`
- `_char_equip_badge`
- `_active_char_badge`
- `_active_char_detail`
- `_load_last_profile_class`

Fokus file ini adalah persistensi dan restore state.

## 5. Struktur Team dan Class

Blue team:
- `addons/neda/blueteam/acidpool/`
- `addons/neda/blueteam/keeneyes/`
- `addons/neda/blueteam/leopard/`
- `addons/neda/blueteam/hide/`
- `addons/neda/blueteam/judychou/`

Red team:
- `addons/neda/redteam/redbull/`
- `addons/neda/redteam/tarantula/`
- `addons/neda/redteam/dfox/`
- `addons/neda/redteam/viper/`
- `addons/neda/redteam/ricalopez/`

## 6. Struktur Image
Asset dibagi menjadi folder shared dan folder khusus class.

Shared:
- `addons/neda/image/select_char/`
- `addons/neda/image/select_weapon/`
- `addons/neda/image/team/`
- `addons/neda/image/map/`
- `addons/neda/image/mode/`
- `addons/neda/image/stat/`

Class-specific:
- `addons/neda/image/acidpool/`, `keeneyes/`, `leopard/`, `hide/`, `judychou/`
- `addons/neda/image/redbull/`, `tarantula/`, `dfox/`, `viper/`, `ricalopez/`

Nama file class umumnya seragam:
- `inventory_char.tga`, `inventory_main.tga`, `inventory_secondary.tga`
- `inventory_melee.tga`, `inventory_explosive.tga`, `inventory_special.tga`
- `lobby1.tga`, `lobby2.tga`, `lobby3.tga`, `lobby3_load.tga`
- `mission.tga`, `title.tga` , `clan.tga`

## 7. Makna `lobby_<class>.cfg`
Setiap file `lobby_<class>.cfg` adalah controller class:
- mengatur enter/back/remove,
- mengatur route inventory,
- mengatur pilih mode,
- mengatur ganti team,
- menjaga cleanup tombol touch per class.

## 8. Pola Routing Aktif
Back flow:
- inventory non-`2` -> `_back_3_<class>`
- inventory `*2` -> `_back_4_<class>`

Remove flow:
- `_rmv_out3_sub_<class>`
- `_rmv_back2_sub_<class>`
- `_rmv_back3_sub_<class>`

Last profile restore:
- `_load_last_profile_class` dipakai untuk memulihkan class terakhir.

## 9. Shortcut Path
Alias shortcut di `ineeda.db`:
- `_ni` -> `addons/neda/image`
- `_np` -> `addons/neda/persist`
- `_npu` -> `addons/neda/persist/use`
- `_null` -> kosong

## 10. Urutan Edit Aman
1. Ubah alias di `lobby.cfg`.
2. Ubah router di `ineeda.db` bila perlu.
3. Ubah file inventory/lobby per class.
4. Verifikasi `persist/character/db_<class>.cfg`.

Urutan ini mengurangi risiko alias putus atau flow freeze.

## 11. Update Runtime Terbaru (2026-04-26)

### Confirm Exit

- Popup confirm exit sekarang harus dianggap fitur global lintas layer:
  - `default/lobby_menu.cfg`
  - `default/lobby_menu2.cfg`
  - `default/lobby_menu3.cfg`
  - `default/lobby_menu4.cfg`
  - seluruh suffix `blueteam/*/lobby_menu*.cfg`
  - seluruh suffix `redteam/*/lobby_menu*.cfg`
- Standar command exit yang dipakai sekarang:
  - `_tap_cnd_back; _show_confirm_exit`

### Map List Close

- Penutupan list map tidak lagi boleh hanya menghapus `_select_open`.
- `addons/map.cfg` sekarang punya helper:
  - `_rmv_map_page1`
  - `_rmv_map_page2`
  - `_rmv_map_page3`
  - `_rmv_map_all_pages`
- `_rmv_mapf` sekarang dipakai sebagai close total:
  - hapus command page 1/2/3
  - hapus image/button page 1/2/3
  - hapus tombol global open/close map

### Inventory Logic: Status Saat Ini

- Yang sudah stabil:
  - border selection weapon/char tetap berbasis CFG slot
  - badge persist masih berbasis alias DB modular:
    - weapon: `persist/main_db.cfg`, `secondary_db.cfg`, `melee_db.cfg`, `explosive_db.cfg`, `special_db.cfg`
    - character: `persist/character/db_<class>.cfg`
- Yang masih belum final:
  - overlay active weapon `select_weapon/equip/equip.png`
  - overlay active character `select_char/change/change.png`
  - blocker command saat item aktif sedang dipilih
  - cleanup scroll lama saat next/prev page inventory

### Batas CFG vs C++

- CFG tetap cocok untuk:
  - page layout
  - koordinat tombol
  - daftar item / page routing
- C++ lebih cocok untuk:
  - active state
  - persist value inti
  - active-check logic
  - blocker logic tombol equip/change
  - cache resource yang sering dipanggil
