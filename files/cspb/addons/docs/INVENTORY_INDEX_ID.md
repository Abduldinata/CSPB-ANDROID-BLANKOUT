# Inventory Index CSPB

Dokumen ini untuk addon `inventory_*`.

Catatan:
- Index di command addon adalah `0-based`.
- Jadi baris pertama daftar = index `0`.
- `inventory_primary` saat ini membaca urutan dari `files/cspb/weapon_list/inventory_all.txt`.

## Primary
`inventory_primary 0 = weapon_ak47`
`inventory_primary 1 = weapon_ak47_fc`
`inventory_primary 2 = weapon_aksopmod`
`inventory_primary 3 = weapon_aksopmod_cg`
`inventory_primary 4 = weapon_aug`
`inventory_primary 5 = weapon_augblitz`
`inventory_primary 6 = weapon_aug_esport`
`inventory_primary 7 = weapon_aug_a3_silencer`
`inventory_primary 8 = weapon_aug_hbar`
`inventory_primary 9 = weapon_f2000`
`inventory_primary 10 = weapon_famas_g2`
`inventory_primary 11 = weapon_g36c`
`inventory_primary 12 = weapon_groza`
`inventory_primary 13 = weapon_hk417`
`inventory_primary 14 = weapon_k2`
`inventory_primary 15 = weapon_m4a1`
`inventory_primary 16 = weapon_m4a1_s`
`inventory_primary 17 = weapon_msbs`
`inventory_primary 18 = weapon_pindad_ss2_v5`
`inventory_primary 19 = weapon_sig`
`inventory_primary 20 = weapon_sc2010`
`inventory_primary 21 = weapon_scar_carbine`
`inventory_primary 22 = weapon_sg550`
`inventory_primary 23 = weapon_tar`
`inventory_primary 24 = weapon_xm8`
`inventory_primary 25 = weapon_apc`
`inventory_primary 26 = weapon_k1`
`inventory_primary 27 = weapon_kriss_sv`
`inventory_primary 28 = weapon_kriss_sv_silence`
`inventory_primary 29 = weapon_kriss_sv_crb`
`inventory_primary 30 = weapon_m4_cqb_lv1`
`inventory_primary 31 = weapon_m4_cqb_lv2`
`inventory_primary 32 = weapon_mp5k`
`inventory_primary 33 = weapon_mp7`
`inventory_primary 34 = weapon_mp9`
`inventory_primary 35 = weapon_oa93`
`inventory_primary 36 = weapon_p90`
`inventory_primary 37 = weapon_p90_mc`
`inventory_primary 38 = weapon_spectre`
`inventory_primary 39 = weapon_t77`
`inventory_primary 40 = weapon_ump`
`inventory_primary 41 = weapon_water`
`inventory_primary 42 = weapon_fg42`
`inventory_primary 43 = weapon_as50`
`inventory_primary 44 = weapon_m82a1`
`inventory_primary 45 = weapon_cheytac_m200`
`inventory_primary 46 = weapon_dragunov`
`inventory_primary 47 = weapon_kar98k`
`inventory_primary 48 = weapon_awp`
`inventory_primary 49 = weapon_m4_spr_lv1`
`inventory_primary 50 = weapon_m4_spr_lv2`
`inventory_primary 51 = weapon_pgm`
`inventory_primary 52 = weapon_rangemaster_338`
`inventory_primary 53 = weapon_tactilite_t2`
`inventory_primary 54 = weapon_scout`
`inventory_primary 55 = weapon_sf`
`inventory_primary 56 = weapon_m3`
`inventory_primary 57 = weapon_m1887`
`inventory_primary 58 = weapon_m1887_w`
`inventory_primary 59 = weapon_spas_15`
`inventory_primary 60 = weapon_zombie_s`

## Secondary
`inventory_secondary 0 = weapon_usp`
`inventory_secondary 1 = weapon_colt_python`
`inventory_secondary 2 = weapon_deagle_dual`
`inventory_secondary 3 = weapon_dual_handgun`
`inventory_secondary 4 = weapon_taurus_raging_bull`
`inventory_secondary 5 = weapon_deagle`
`inventory_secondary 6 = weapon_glock18`
`inventory_secondary 7 = weapon_bow`

## Melee
`inventory_melee 0 = weapon_knife`
`inventory_melee 1 = weapon_amok`
`inventory_melee 2 = weapon_saber`
`inventory_melee 3 = weapon_arabian_sword`
`inventory_melee 4 = weapon_fangblade`
`inventory_melee 5 = weapon_combat`
`inventory_melee 6 = weapon_knifebone`
`inventory_melee 7 = weapon_brass_knuckle`
`inventory_melee 8 = weapon_candy_cane`
`inventory_melee 9 = weapon_dual_knife`
`inventory_melee 10 = weapon_keris`
`inventory_melee 11 = weapon_mini_axe`
`inventory_melee 12 = weapon_ice`
`inventory_melee 13 = weapon_karambit`
`inventory_melee 14 = weapon_butterfly`

## Shotgun
`inventory_shotgun 0 = weapon_sf`
`inventory_shotgun 1 = weapon_m3`
`inventory_shotgun 2 = weapon_m1887`
`inventory_shotgun 3 = weapon_m1887_w`
`inventory_shotgun 4 = weapon_spas_15`
`inventory_shotgun 5 = weapon_zombie_s`

## Sniper
`inventory_sniper 0 = weapon_as50`
`inventory_sniper 1 = weapon_m82a1`
`inventory_sniper 2 = weapon_cheytac_m200`
`inventory_sniper 3 = weapon_dragunov`
`inventory_sniper 4 = weapon_kar98k`
`inventory_sniper 5 = weapon_awp`
`inventory_sniper 6 = weapon_m4_spr_lv1`
`inventory_sniper 7 = weapon_m4_spr_lv2`
`inventory_sniper 8 = weapon_pgm`
`inventory_sniper 9 = weapon_rangemaster_338`
`inventory_sniper 10 = weapon_tactilite_t2`
`inventory_sniper 11 = weapon_scout`

## Special
`inventory_special 0 = weapon_smokegrenade`
`inventory_special 1 = weapon_medkit`
`inventory_special 2 = weapon_wpsmoke`

## Explosive
`inventory_explosive 0 = weapon_hegrenade`
`inventory_explosive 1 = weapon_gasbomb`
`inventory_explosive 2 = weapon_c5`
`inventory_explosive 3 = weapon_claymore`

## Contoh mismatch addon lama
`equip_aughbar` lama memakai `inventory_primary 31`, padahal sekarang index itu `weapon_m4_cqb_lv2`.

`equip_pgm` lama memakai `inventory_primary 54`, padahal sekarang index itu `weapon_scout`.

`equip_m1887w` lama memakai `inventory_primary 53`, padahal sekarang index itu `weapon_tactilite_t2`.

Kalau mau, file ini bisa dipakai sebagai acuan untuk remap seluruh folder `addons/neda/select_weapon/main`.
