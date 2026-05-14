# 🎮 PROJECT LOBBY CSPB BY INEEDA
> **GAME VERSION**: 20.1 (Credit: Billflx) [cite: 1]
> **STATUS**: Stable & Optimized v20.1.1 (Antigravity Patch) [cite: 1]
> **DOKUMENTASI ARSITEKTUR**: [SYSTEM_MAP.md](file:///e:/Games/PROJECT%20LOBBY%20CSPB/com.cspb.m/files/cspb/addons/SYSTEM_MAP.md) (Peta Teknis & Folder)

---

## 🏆 PROJECT CREDITS
| Role | Developer/Creator |
| :--- | :--- |
| **New Lobby Config** | [@INEEDA](https://youtube.com/@INEEDA) [cite: 2] |
| **Game Foundation** | [@BILLFLX](https://youtube.com/@BILLFLX) [cite: 3] |
| **Base Config** | [@Fiko R] (https://youtube.com/@FikoR) (Legacy) [cite: 3] |
| **Knowledge Base** | [@LORAYNA] (https://youtube.com/@Lorayna) [cite: 3] |
| **Optimization** | **Antigravity AI** [cite: 4] |

---

## ✨ KEY FEATURES (Patch 2026-02-03)
- 🚀 **Dynamic Persistence**: Sistem mengingat halaman terakhir yang dibuka (Resume Lobby)[cite: 5].
- 🧹 **Automatic Cleanup**: Menghilangkan badge "ghosting" saat pindah halaman[cite: 6].
- ⚡ **Optimized Code**: Struktur script bersih tanpa teks credit berulang di setiap file[cite: 7].
- 🗺️ **Visual Restore**: Mengembalikan preview map & mode secara otomatis saat re-entry[cite: 8].

---

## 📄 RECENT CHANGE LOG (2026-02-03)
#### **[SISTEM PERSISTENSI]**
- **FIX**: Memperbaiki masalah "Ghosting" di mana badge EQUIP/USE menimbun saat pindah halaman[cite: 9].
- **NEW**: Implementasi `_resume_lobby`. Sistem sekarang mengingat halaman terakhir yang dibuka (Lobby 1-4, Inventory, dsb)[cite: 9].
- **NEW**: Implementasi Auto-Restore Visual. Map preview dan Mode badge otomatis muncul kembali saat masuk kembali ke menu[cite: 10].

#### **[OPTIMASI & PEMBERSIHAN]**
- **CLEAN**: Menghapus baris credit berulang di 50+ file `.cfg` untuk meringankan beban parsing game[cite: 11, 12].
- **DOCS**: Sentralisasi seluruh informasi team & credits ke dalam `log.txt`[cite: 13].

#### **[ASSET FIXES]**
- **FIX**: Memperbaiki path karakter Blue Team (Leopard, Hide, Judy Chou) yang salah folder[cite: 14].
- **FIX**: Sinkronisasi nama file Map TGA agar sesuai dengan file fisik[cite: 15].

---

## 📜 HISTORICAL UPDATE LOG (2023 - 2026)

#### **[LOG PERIODE 2023]**
1: log/history update lobby.cfg (still use previous tga of cspb v11 - soon i'll change it to v12.8) [cite: 16]
3: 09-08-2023 add lobby menu1, lobby menu2, lobby menu3, lobby menu4 [cite: 16]
4: 09-09-2023 add details info open and close [cite: 16]
5: 09-11-2023 add clan menu [cite: 16]
6: 09-16-2023 add choose menu team [cite: 16]
7: 09-17-2023 add notice 2 on lobby2 [cite: 16]
8: 09-24-2023 add fade in , fade out change red and blue team [cite: 16]
9: 09-25-2023 add friend list open and close [cite: 16]
10: 09-28-2023 add team blue , team red menu [cite: 16]
11: 10-01-2023 add title menu, personal mission menu [cite: 16]
12: 10-6-2023 add cmd for lobby menu3 [cite: 16]
13: 10-6-2023 add inventory main, inventory character [cite: 16]
14: 10-13-2023 add page inventory main (page1-page9) [cite: 16]
15: 10-15-2023 add page inventory char (page1-page2) [cite: 16]
16: 10-18-2023 add cmd for lobby menu4 [cite: 16]
17: 10-23-2023 add inventory secondary [cite: 16]
18: 10-26-2023 add inventory explosive [cite: 16]
19: 10-27-2023 add inventory special [cite: 16]
20: 11-01-2023 add blank after start choose character/ class [cite: 16]
21: 11-05-2023 add map select 1 for select map list 1 [cite: 16]
22: 11-07-2023 fix map select 2 for select map list 2 [cite: 16]
23: 11-12-2023 add map select 3, fix image map selected [cite: 16]
24: 11-17-2023 add use image in inventory if equip [cite: 16]
25: 11-20-2023 add use image in inventory if equip (main, secondary, melee, explosive, special) all done [cite: 16]
26: 11-21-2023 add equip image in character if change (i will add logic if change character, back/prevmenu is to menu depend on your change character) [cite: 17]
27: 11-21-2023 add lobby menu3 load image (just load if prevmenu from lobby4 to lobby3 or lobby2 to lobby3, just tryna a pb style pc:v) [cite: 17]
28: 11-22-2023 test add logic if chose the select menu lobby will saved and if open it again, the config load on selected character before [cite: 17]
29: 11-22-2023 remove inventory, clan, mission, title, detail if not select anny character (remove cmd) [cite: 17]
30: 11-22-2023 add lobby logic on red team (redbull , tarantula, dfox) done [cite: 17]
31: 11-22-2023 add menu logic redbull,tarantula,dfox (if you out all lobby and you back to open neda_menu on touch profile will auto save depend of your selected character before) *note :only if you in game. [cite: 18]
- if quit and open auto reset to default lobby [cite: 19]
32: 11-23-2023 add lobby logic on red team (viper, ricalopez) done [cite: 19]
33: 11-23-2023 add menu logic viper, ricalopez (only in game) [cite: 19]
34: 11-24-2023 add lobby logic on blue team (acidpool) done [cite: 19]
35: 11-24-2023 add menu logic acidpool (only in game) [cite: 19]
36: 11-25-2023 add lobby logic on blue team (keeneyes) done [cite: 19]
37: 11-26-2023 fix sound bug with _click_ (because its used buymenu) already change to _tap_ [cite: 19]
38: 11-26-2023 add new method to exec anny cfg (more simple and less lag) [cite: 19]
39: 11-26-2023 add lobby logic on blue team (hide) done [cite: 19]
40: 11-26-2023 add lobby logic on blue team (judychou) done [cite: 19]
41: 11-30-2023 fix bug on character inventory (still bug if from char inven to weapon sometimes idk i dont found a solution) [cite: 20]
42: 12-03-2023 fix bug if you tap on whatever inventory page it will must you use the (weapon/etc). and now the cmd has fix to select another (weapon/etc) but you not must used it on (RED TEAM) [cite: 20, 21]
43: 12-04-2023 fix bug if you tap on whatever inventory page it will must you use the (weapon/etc). and now the cmd has fix to select another (weapon/etc) but you not must used it on (BLUE TEAM) [cite: 21, 22]
44: 12-06-2023 deleted a little of text for resize config and less long process [cite: 22]
45: 12-10-2023 add credit image of my yt ch [cite: 22]

#### **[LOG PERIODE 2024]**
46: 01-08-2024 fix cmd fangblade use can't gone after use another melee [cite: 22]
47: 01-08-2024 add cmd rmv_all for nextpage on melee and secondary bug use image n use cmd cant gone if user go to next page (forgot to add) [cite: 22]
48: 03-16-2024 rewrite all cfg (especialy on inventory fix bug all page because this not yet available in the remaining update accord to last log change, resize command) [cite: 22, 23]
49: 03-16-2024 rewrite cfg on blueteam acidpool (char, weapons, melee, secondary, explosive, special ) [cite: 23]
50: 03-24-2024 rewrite stat cfg (tga not include) [cite: 23]
51: 04-05-2024 rewrite cfg on blueteam keeneyes (char, weapons, melee, secondary, explosive, special ) [cite: 23]
52: 08-13-2024 fix wrong cmd cfg on blueteam acidpool (char, melee ) [cite: 23]
53: 08-17-2024 change cmd map select (crackdown_v1 with Crackdown_Deserted, crackdown_v2 with Crackdown_2) [cite: 23]
54: 09-26-2024 add mode select in lobby tdm and bomb mission (switch mode tdm/bm) [cite: 23]
55: 09-26-2024 add mode select in lobby knife mode, shotgun mode, sniper mode on blue team (acidpool) [cite: 23]
56: 10-26-2024 fix cmd mode select in lobby knife mode, shotgun mode, sniper mode on blue team (acidpool) [cite: 23, 24]
57: 10-26-2024 change cmd mode select in lobby knife mode, shotgun mode, sniper mode on blue team (acidpool) not effect on bot only (overall change the gamemode) [cite: 24]
58: 12-24-2024 rewrite stat weapon cfg (not include tga) [cite: 24]
59: 12-27-2024 fix cmd main inventory when back to previous (lobby 3) or (exit lobby menu) auto delete all cmd and tga on blue team (acidpool) [cite: 24]
60: 12-27-2024 add stat cmd (include tga wip) main inventory, weapons, weapons 2 on blue team (acidpool) [cite: 24]
61: (focus only test in one char : acid pool from blue team , to complete a cmd without bug and addapt to all char soon) [cite: 24, 25]

#### **[LOG PERIODE 2025]**
62: 10-04-2025 I used a 20.1 version cspb and manny change cmd from source by bill so I learn that again before continue this lobby cfg [cite: 25]
63: 10-21-2025 bug found if I from character change in the loby menu4 always reset image to none character but the feature like gamemode not remove [cite: 25]
64: 10-21-2025 cmd weapon on inventory has been changed , example : if I'm buy p90 then after i die not buy a p90 but another weapon . the reason is cmd change from source (bill) [cite: 25, 26]
65: 10-21-2025 bug cmd mode from character change still work now fixed (can't press cmd after cancel or exit from lobby in acid or lobby4 ) [cite: 26]
66: 10-21-2025 found bug in character select (loby4 acidpool) if I open map select, button change team still spear (still active) I hope I can fix when I open change team map can't touch and if I open the map too [cite: 26]
67: 10-21-2025 remove sl_mapf cmd on acid pool cause bug , is that function to add button open and close map . I move that to lobby 4 (acidpool) withtout alias (caused bug) [cite: 26, 27]
68: 10-21-2025 add // Map Select on lobby4 (acid pool) [cite: 27]
69: 10-21-2025 found bug , if I change from team anything red/blue. if I close or back on previous select (chose red or blue menu) and then I press cancel back to lobby 4 not current lobby char I selected [cite: 27, 28]
70: 10-22-2025 I found how to fix big lobby4 , just make change team on any side of team (blue/red) soon I fix [cite: 28]
71: 10-26-2025 fix bug change team after cancel / back ref to loby4 wihtout char select, now already fixed (add blue,red, change team on each team character) ex : acidpool work [cite: 28]
72: 10-26-2025 tested change cmd from change team acidpool and work [cite: 28]
73: 10-27-2025 add "exec addons/lobby_acidpool.cfg" on lobby_menu acidpool, function : call alias cmd from loby_acidpool.cfg then make cmd can exec (not only from lobby selected acidpool) [cite: 28, 29]

#### **[LOG PERIODE 2026]**
[LOG - 2026-01-30]
- PROJECT: NEDA UI SYNCHRONIZATION (BLUE TEAM & RED TEAM) [cite: 30]
- Synchronized all Unit Character configuration files by injecting 'rmv_all_stat' into 'touch_addbutton' commands[cite: 30]. This ensures UI consistency and prevents status leaks[cite: 30, 31].
- BLUE TEAM SYNC: Characters (Acid Pool, Hide, Judy Chou, Keen Eyes, Leopard). Actions: Global 'rmv_all_stat' injection & cleanup of redundant commands[cite: 31, 32].
- RED TEAM SYNC: Characters (D-Fox, Red Bull, Rica Lopez, Tarantula, Viper). Actions: Fixed distorted '_set_sound_default;' in Red Bull & Rica Lopez[cite: 32, 33, 34].
- GLOBAL ADDONS AUDIT: Fixed 'adddons' typo in 'lobby.cfg', injected 'rmv_all_stat' into Team Selection, Map Selection, and Mode selection UI[cite: 35, 36, 37].

[LOG - 2026-01-30 - EVENING SESSION]
- PROJECT: LOBBY 4 BUTTON FIXES - MAP/MODE SELECT + POPUP PROTECTION [cite: 38]
- 1. FIXED MISSING STAT COMMANDS (RED TEAM WEAPONS2): Added rmv_all_stat and stat_[weapon] to all weapon buttons in 5 files. STATUS: FIXED (TGA images still needed)[cite: 38].
- 2. ADDED MAP/MODE SELECT BUTTONS TO ALL CHARACTERS: Created addons/neda/mapmode_control.cfg. Updated 9 characters (Keen Eyes, Leopard, etc.)[cite: 38, 39].
- 3. IMPLEMENTED POPUP PROTECTION SYSTEM: Hide/show buttons using touch_removebutton/touch_addbutton during "Change Team" flow in 21 files[cite: 39, 40].
- 4. CONSOLE OUTPUT SUPPRESSION: Added developer 0 & con_notifytime 0 to addons/ineeda.db[cite: 41].

[LOG - 2026-01-31]
- PROJECT: CHARACTER SELECTION STABILITY & INVENTORY 2 NAVIGATION FIXES [cite: 42]
- 1. FIXED CHARACTER SELECTION CRASH: Restored '_selected_red_class_X' across 16 files because 'exec' commands caused blank screen[cite: 42, 43, 44, 45, 46, 47].
- 2. RED TEAM INVENTORY 2 NAVIGATION: Corrected '_wp_prevpage2_' to '_wp_prevpage1b_' for all Red Team classes[cite: 48, 49, 50].
- 3. REPAIRED BROKEN SCRIPTS: Fixed syntax 'rmv exec' in 'ricalopez/team_red.cfg' and incorrect selection indices[cite: 51, 52, 53].

[LOG - 2026-01-31 - AUDIT SESSION]
- PROJECT: INVENTORY ASSET STANDARDIZATION & COMMAND CLEANUP [cite: 56]
- 1. MELEE WEAPON STANDARDIZATION: Standardized Hide & Judy Chou melee sets to match 'acidpool' reference[cite: 57, 58].
- 2. TEAM SELECTION CANCEL BUG: Updated 'lobby_[char].cfg' aliases to point to correct subdirectories[cite: 60, 61, 62].
- 3. "STUCK" COMMAND AUDIT: Injected '_rmv_use_all' into navigation and Exit/Back buttons to clear ghost UI elements[cite: 63, 64, 65, 66, 67, 68].

[LOG - 2026-02-03 - INDICATOR REFINEMENT]
- PROJECT: DECOUPLED INDICATOR SYSTEM - EQUIP vs USE BADGE SEPARATION [cite: 69]
- 1. DECOUPLED PERSISTENCE DATABASE: Modified persist_db.cfg to only execute Use badges (checkmark). Removed automatic Equip badge from 80 item aliases[cite: 69, 70, 71, 72].
- 2. INDIVIDUAL INDICATOR SYSTEM: Created reset_individual_indicators.cfg with 80 aliases. Behavior: Checkmark persists in slot, Dark overlay only appears on click[cite: 73].
- 3. NAVIGATION FIXES: Modified 120 files. Standardized Back redirects and fixed typos like '_rmv_rmv_persist_all'[cite: 74].

---

## 🛠️ TECHNICAL NOTES
- Map Pagination: Page 1 (7 maps) → Page 2 (7 maps) → Page 3 (2 maps) = 16 total[cite: 42].
- Alias Convention: _rmv_mapmode, _add_mapmode, _sl_map1/2/3, _mode_tdm/bomb[cite: 42].
- Known Issue: Stat TGA images missing in addons/neda/image/stat/ (Needs image assets)[cite: 42].

---
*Clean Code. Better Gameplay. Produced by Antigravity AI.* [cite: 76]

---

## [LOG - 2026-04-06 - ROUTING CONSISTENCY & SYSTEM DOCUMENTATION]
- PROJECT: CLASS ROUTING STANDARDIZATION + ARCHITECTURE DOCUMENTATION UPDATE.
- 1. CLASS FLOW NORMALIZATION (BLUE + RED): Menyamakan pola back/enter/remove alias agar konsisten antar class folder (inventory non-2 -> `_back_3_<class>`, inventory `*2` -> `_back_4_<class>`).
- 2. UI CLEANUP STANDARD: Menyatukan pola remove button class-scoped (`_rmv_out3_sub_<class>`, `_rmv_back2_sub_<class>`, `_rmv_back3_sub_<class>`) untuk mengurangi konflik tombol touch saat pindah menu.
- 3. RECOVERY ACTION: Setelah terdeteksi overwrite massal yang membuat beberapa file class tertukar isi, file class dipulihkan dari backup dan disinkronkan ulang sesuai template class masing-masing.
- 4. CHARACTER DB FLOW VALIDATION: Memastikan chain aktif karakter berjalan benar dari `ineeda.db` -> `lobby.cfg` -> `char_db.cfg` -> `persist/character/db_<class>.cfg` (termasuk validasi `_db_char_acidpool` dan `_active_char_theme`).
- 5. SYSTEM MAP DOCUMENTATION: Menambah/merapikan `SYSTEM_MAP.md` agar mencakup startup chain, modular DB, peran `lobby_<class>.cfg`, struktur image shared vs class-specific, serta pola routing terbaru.
- 6. ENTRY TRIGGER NOTE ADDED: Dokumentasi sekarang menegaskan bahwa flow custom mulai saat user klik touch button `neda_menu` (`touch_setclientonly 1; exec addons/neda/lobby_menu.cfg`), sedangkan sebelum klik tetap UI bawaan CSPB.

Status: STABLE (Documentation synchronized with current config flow).