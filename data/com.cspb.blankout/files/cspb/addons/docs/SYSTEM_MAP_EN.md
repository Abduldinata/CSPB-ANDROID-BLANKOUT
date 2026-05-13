# SYSTEM MAP EN - PROJECT LOBBY CSPB

This is the English version of the CSPB custom lobby system map.
Primary source file remains [../SYSTEM_MAP.md](../SYSTEM_MAP.md).

## 1. Startup Chain
Core load order:

1. `addons/ineeda.db`
2. `addons/lobby.cfg`
3. `addons/inventory.cfg`

Short roles:
- `ineeda.db`: startup entry point and core loader trigger.
- `lobby.cfg`: alias declaration layer (`_load_*`).
- `inventory.cfg`: bridge to global inventory and category routes.

### Trigger From Default Game UI
The custom flow starts only after the user taps `neda_menu`:

- `touch_addbutton "neda_menu" "addons/neda/image/icon.tga" "touch_setclientonly 1; exec addons/neda/lobby_menu.cfg" 0.920000 0.000000 0.980000 0.129438 255 255 255 178 2`

Before this button is tapped, the game is still on default CSPB flow/UI.

## 2. System Layers

### A. Root DB / Router
`ineeda.db` triggers these loaders:
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
`lobby.cfg` stores loader alias definitions.
Examples:
- `_load_db` -> `exec addons/ineeda.db`
- `_load_char_db` -> `exec addons/neda/persist/char_db.cfg`
- `_load_main_db` -> `exec addons/neda/persist/main_db.cfg`
- `_load_mapmode_control` -> `exec addons/neda/mapmode_control.cfg`
- `_load_map_base` -> `exec addons/map.cfg`
- `_load_mode_base` -> `exec addons/mode.cfg`
- `_load_stat_base` -> `exec addons/stat.cfg`

### C. Category / Inventory Layer
`inventory.cfg` and `addons/neda/*/inventory_*.cfg` handle inventory UI:
- DB load,
- image setup,
- back/exit touch buttons,
- per-class remove aliases,
- return routes to class menus.

## 3. Modular Databases

| Category | Folder | Loader |
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

Note: `mapmode_control.cfg` is better categorized as control/routing layer, not a pure modular DB file.

## 4. Character DB Routing

### Loader
`_load_char_db` executes `addons/neda/persist/char_db.cfg`.

### Default Theme
`char_db.cfg` sets a default, for example:
- `_active_char_theme "_db_char_acidpool"`

### Per-Class Router
`char_db.cfg` maps `_db_char_<class>` into `db_<class>.cfg`.
Examples:
- `_db_char_acidpool` -> `db_acidpool.cfg`
- `_db_char_dfox` -> `db_dfox.cfg`
- `_db_char_redbull` -> `db_redbull.cfg`

### `db_<class>.cfg` Content
Usually stores state such as:
- `_char_p1_badge`
- `_char_equip_badge`
- `_active_char_badge`
- `_active_char_detail`
- `_load_last_profile_class`

These files are for persistence and state restore.

## 5. Team and Class Structure

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

## 6. Image Structure
Assets are split into shared folders and class-specific folders.

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

Common per-class file naming pattern:
- `inventory_char.tga`, `inventory_main.tga`, `inventory_secondary.tga`
- `inventory_melee.tga`, `inventory_explosive.tga`, `inventory_special.tga`
- `lobby1.tga`, `lobby2.tga`, `lobby3.tga`, `lobby3_load.tga`
- `mission.tga`, `title.tga` , `clan.tga`

## 7. Meaning of `lobby_<class>.cfg`
Each `lobby_<class>.cfg` is a class controller that handles:
- enter/back/remove routes,
- inventory routes,
- mode selection,
- team switching,
- class-scoped touch button cleanup.

## 8. Active Routing Pattern
Back flow:
- non-`2` inventory -> `_back_3_<class>`
- `*2` inventory -> `_back_4_<class>`

Remove flow:
- `_rmv_out3_sub_<class>`
- `_rmv_back2_sub_<class>`
- `_rmv_back3_sub_<class>`

Last profile restore:
- `_load_last_profile_class` is used to restore the last active class.

## 9. Path Shortcuts
`ineeda.db` path shortcuts:
- `_ni` -> `addons/neda/image`
- `_np` -> `addons/neda/persist`
- `_npu` -> `addons/neda/persist/use`
- `_null` -> empty

## 10. Safe Edit Order
1. Update aliases in `lobby.cfg`.
2. Update router calls in `ineeda.db` if required.
3. Update class inventory/lobby files.
4. Re-check `persist/character/db_<class>.cfg`.

This order helps avoid alias breaks and freeze-prone routes.
