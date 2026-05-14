# SYSTEM MAP: PROJECT LOBBY CSPB

Dokumen ini merangkum alur routing, database, persist, dan struktur file utama di `addons`.
Tujuannya adalah supaya file-file yang terlihat mirip tetap mudah dibedakan menurut fungsinya.

## 1. Startup Chain
Urutan load awal yang paling penting:

1. [addons/ineeda.db](ineeda.db)
2. [addons/lobby.cfg](lobby.cfg)
3. [addons/inventory.cfg](inventory.cfg)

`ineeda.db` adalah entry point yang menyalakan database dan alias inti.
`lobby.cfg` adalah tempat deklarasi alias loader/routing.
`inventory.cfg` adalah bridge ke inventory global dan category routing.

### A. Trigger Awal Dari Game Bawaan
Config custom CSPB ini baru benar-benar mulai saat user klik tombol touch `neda_menu` di `[addons/neda/add_menu.cfg](neda/add_menu.cfg)`.
Contoh trigger-nya:

- `touch_addbutton "neda_menu" "addons/neda/image/icon.tga" "touch_setclientonly 1; exec addons/neda/lobby_menu.cfg" 0.920000 0.000000 0.980000 0.129438 255 255 255 178 2`

Sebelum tombol itu dipencet, yang tampil masih alur dan UI bawaan game CSPB.
Sesudah diklik, client-only mode aktif lalu masuk ke `lobby_menu.cfg`, dan dari sana flow custom `neda` mulai berjalan.

## 2. Peran Tiap Layer

### A. Root DB / Router
`ineeda.db` dipakai sebagai hub awal.
File ini memanggil loader seperti:
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
`lobby.cfg` mendeklarasikan alias-alias `_load_*` di atas.
Contoh bentuknya:
- `_load_db` -> `exec addons/ineeda.db`
- `_load_main_db` -> `exec addons/neda/persist/main_db.cfg`
- `_load_char_db` -> `exec addons/neda/persist/char_db.cfg`
- `_load_mapmode_control` -> `exec addons/neda/mapmode_control.cfg`
- `_load_map_base` -> `exec addons/map.cfg`
- `_load_mode_base` -> `exec addons/mode.cfg`
- `_load_stat_base` -> `exec addons/stat.cfg`

Jadi, `ineeda.db` memanggil alias, sedangkan `lobby.cfg` menyimpan definisinya.

### C. Category / Inventory Layer
`inventory.cfg` dan `addons/neda/*/inventory_*.cfg` mengatur layar inventory.
Biasanya file inventory berisi:
- `_load_db`
- image path
- `touch_addbutton` untuk exit/back
- alias remove button per class
- route back ke `lobby_menu3` atau `team_blue_class*` / `team_red_class*`

## 3. Database Modular
Pola database dibagi per kategori supaya alias tidak terlalu panjang dan logika tetap terpisah.

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

Catatan: `mapmode_control.cfg` bukan database modular murni. File itu lebih tepat dianggap routing/control layer karena dipanggil dari `ineeda.db` lewat `_load_mapmode_control`, sementara `mode.cfg` dan `map.cfg` adalah base file yang juga memuat database persisten masing-masing.

## 4. Character DB Routing
Character DB dipisah dari lobby routing.

### A. Loader ke Character DB
`_load_char_db` di `lobby.cfg` menjalankan:
- `exec addons/neda/persist/char_db.cfg`

### B. Default Character Theme
Di `char_db.cfg` ada routing tema karakter default, misalnya:
- `_active_char_theme "_db_char_acidpool"`

### C. Character Module per Class
`char_db.cfg` kemudian menunjuk ke file per class:
- `_db_char_acidpool` -> `exec addons/neda/persist/character/db_acidpool.cfg`
- `_db_char_dfox` -> `exec addons/neda/persist/character/db_dfox.cfg`
- `_db_char_redbull` -> `exec addons/neda/persist/character/db_redbull.cfg`
- dan seterusnya

### D. Isi `db_<class>.cfg`
File seperti `db_acidpool.cfg` biasanya menyimpan state berikut:
- `_char_p1_badge`
- `_char_equip_badge`
- `_active_char_badge`
- `_active_char_detail`
- `_load_last_profile_class`

Fungsi utamanya adalah persistency dan restore state, bukan navigasi utama.

## 5. Folder Class Structure

### Blue Team
- `addons/neda/blueteam/acidpool/`
- `addons/neda/blueteam/keeneyes/`
- `addons/neda/blueteam/leopard/`
- `addons/neda/blueteam/hide/`
- `addons/neda/blueteam/judychou/`

### Red Team
- `addons/neda/redteam/redbull/`
- `addons/neda/redteam/tarantula/`
- `addons/neda/redteam/dfox/`
- `addons/neda/redteam/viper/`
- `addons/neda/redteam/ricalopez/`

### Image Structure
Image assets are split into shared folders and class-specific folders.

| Image Folder | Purpose |
|---|---|
| `addons/neda/image/acidpool/` | Acidpool images for lobby, inventory, mission, title, clan. |
| `addons/neda/image/keeneyes/` | Keen Eyes images for the same class UI set. |
| `addons/neda/image/leopard/` | Leopard images for the same class UI set. |
| `addons/neda/image/hide/` | Hide images for the same class UI set. |
| `addons/neda/image/judychou/` | Judy Chou images for the same class UI set. |
| `addons/neda/image/redbull/` | Redbull images for the same class UI set. |
| `addons/neda/image/tarantula/` | Tarantula images for the same class UI set. |
| `addons/neda/image/dfox/` | D-Fox images for the same class UI set. |
| `addons/neda/image/viper/` | Viper images for the same class UI set. |
| `addons/neda/image/ricalopez/` | Rica Lopez images for the same class UI set. |
| `addons/neda/image/select_char/` | Shared character select assets such as `border/`, `change/`, and `equip/`. |
| `addons/neda/image/select_weapon/` | Shared weapon select assets such as `border/`, `equip/`, and `use/`. |
| `addons/neda/image/team/` | Team UI assets. |
| `addons/neda/image/map/` | Map selection assets. |
| `addons/neda/image/mode/` | Mode selection assets. |
| `addons/neda/image/stat/` | Stat screen assets. |

Each class image folder usually contains the same naming pattern:
- `inventory_char.tga`
- `inventory_main.tga`
- `inventory_secondary.tga`
- `inventory_melee.tga`
- `inventory_explosive.tga`
- `inventory_special.tga`
- `lobby1.tga`
- `lobby2.tga`
- `lobby3.tga`
- `lobby3_load.tga`
- `mission.tga`
- `title.tga`

## 6. Per-File Lobby Meaning
File `lobby_<class>.cfg` adalah controller spesifik class. Isinya hampir sama, tetapi beda pada class target, inventory target, dan team selector yang dipanggil.

| Lobby File | Team | Class Slot | Fungsi Utama |
|---|---|---|---|
| `lobby_acidpool.cfg` | Blue | `team_blue_class1` | Controller class Acidpool. Menyediakan remove/enter/back, change team, choose mode, credit, dan redirect inventory ke Acidpool. |
| `lobby_keeneyes.cfg` | Blue | `team_blue_class2` | Controller class Keen Eyes. Struktur sama, tetapi semua alias mengarah ke folder `keeneyes` dan slot blue class 2. |
| `lobby_leopard.cfg` | Blue | `team_blue_class3` | Controller class Leopard. Dipakai untuk navigasi class Leopard dan inventory Leopard. |
| `lobby_hide.cfg` | Blue | `team_blue_class4` | Controller class Hide. Dipakai untuk navigasi class Hide dan inventory Hide. |
| `lobby_judychou.cfg` | Blue | `team_blue_class5` | Controller class Judy Chou. Dipakai untuk navigasi class Judy Chou dan inventory Judy Chou. |
| `lobby_redbull.cfg` | Red | `team_red_class1` | Controller class Redbull. Struktur sama, tetapi targetnya red team slot 1. |
| `lobby_tarantula.cfg` | Red | `team_red_class2` | Controller class Tarantula. Mengatur route inventory dan back/enter untuk slot red 2. |
| `lobby_dfox.cfg` | Red | `team_red_class3` | Controller class D-Fox. Dipakai untuk inventory dan menu class D-Fox. |
| `lobby_viper.cfg` | Red | `team_red_class4` | Controller class Viper. Mengatur menu class dan inventory Viper. |
| `lobby_ricalopez.cfg` | Red | `team_red_class5` | Controller class Rica Lopez. Mengatur semua navigasi class red slot 5. |

Catatan umum untuk semua `lobby_<class>.cfg`:
- alias `_remove_*_<class>` menampilkan halaman class atau menghapus menu lama
- alias `_enter_*_<class>` membuka halaman class tertentu
- alias `_back_*_<class>` dipakai untuk kembali ke level menu yang sesuai
- alias `_rmv_out3_sub_<class>`, `_rmv_back2_sub_<class>`, dan `_rmv_back3_sub_<class>` dipakai untuk membersihkan tombol touch UI
- alias `_choose_1_<class>` membuka menu pilih mode
- alias `_change_team_<class>` membuka/menutup pergantian team
- alias `_weapon_inventory_<class>`, `_char_inventory_<class>`, dan kategori lain mengarah ke inventory class masing-masing

## 7. File Roles Inside a Class Folder
Setiap class folder biasanya berisi file seperti:

- `lobby_menu.cfg` / `lobby_menu2.cfg` / `lobby_menu3.cfg`
- `inventory_character.cfg` / `inventory_character2.cfg`
- `inventory_weapon.cfg` / `inventory_weapon2.cfg`
- `inventory_secondary.cfg` / `inventory_secondary2.cfg`
- `inventory_melee.cfg` / `inventory_melee2.cfg`
- `inventory_explosive.cfg` / `inventory_explosive2.cfg`
- `inventory_special.cfg` / `inventory_special2.cfg`
- `team_blue.cfg` / `team_red.cfg`
- `mission.cfg` / `mission2.cfg`
- `title.cfg` / `title2.cfg`
- `remove_*.cfg`

## 8. Routing Pattern

### A. Back Flow
Pola yang dipakai sekarang:
- non-`2` inventory -> `_back_3_<class>`
- `*2` inventory -> `_back_4_<class>`

### B. Remove Button Flow
Pola yang dipakai sekarang:
- `_rmv_out3_sub_<class>`
- `_rmv_back2_sub_<class>`
- `_rmv_back3_sub_<class>`

Ini membuat tombol UI dihapus lewat alias class-scoped, bukan inline `touch_removebutton` langsung.

### C. Last Profile Restore
`_load_last_profile_class` dipakai di inventory character untuk mengembalikan class aktif saat back/exit.

## 9. Common File Path Shortcuts
Alias path pendek di `ineeda.db` dipakai supaya string logic lebih pendek:
- `_ni` -> `addons/neda/image`
- `_np` -> `addons/neda/persist`
- `_npu` -> `addons/neda/persist/use`
- `_null` -> kosong

## 10. Praktik Aman
Kalau ingin mengubah struktur ini, urutan aman biasanya:
1. ubah alias di `lobby.cfg`
2. ubah router di `ineeda.db` jika perlu
3. ubah file class inventory/lobby
4. cek ulang `persist/character/db_<class>.cfg`

Kalau langkah ini dibalik, risiko alias putus atau flow freeze lebih besar.

