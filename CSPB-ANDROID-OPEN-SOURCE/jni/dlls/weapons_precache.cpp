#include "extdll.h"
#include "util.h"
#include "cbase.h"
#include "player.h"
#include "gamerules.h"
#include "weapons.h"
#include "weapons_precache.h"
#include "model_helper.h"

#ifndef CSPB_LOG_DIAG
#define CSPB_LOG_DIAG(msg) ALERT(at_console, "%s\n", msg)
#endif

// Keep this symbol for compatibility if other files reference it.
bool g_bCSPBStartupWeaponPrecachePhase = false;

// called by worldspawn
void W_Precache()
{
	CSPB_LOG_DIAG("=== W_Precache START (Smart Pool Precache) ===");
	Q_memset(CBasePlayerItem::ItemInfoArray, 0, ARRAYSIZE(CBasePlayerItem::ItemInfoArray));
	Q_memset(CBasePlayerItem::AmmoInfoArray, 0, ARRAYSIZE(CBasePlayerItem::AmmoInfoArray));
	giAmmoIndex = 0;
	g_bCSPBStartupWeaponPrecachePhase = true;

	// common world objects & items
	UTIL_PrecacheOther("item_suit");
	UTIL_PrecacheOther("item_battery");
	UTIL_PrecacheOther("item_antidote");
	UTIL_PrecacheOther("item_security");
	UTIL_PrecacheOther("item_longjump");
	UTIL_PrecacheOther("item_kevlar");
	UTIL_PrecacheOther("item_assaultsuit");
	UTIL_PrecacheOther("item_thighpack");

	// Standard ammunition types
	UTIL_PrecacheOther("ammo_338magnum");
	UTIL_PrecacheOther("ammo_762nato");
	UTIL_PrecacheOther("ammo_556natobox");
	UTIL_PrecacheOther("ammo_556nato");
	UTIL_PrecacheOther("ammo_buckshot");
	UTIL_PrecacheOther("ammo_45acp");
	UTIL_PrecacheOther("ammo_57mm");
	UTIL_PrecacheOther("ammo_50ae");
	UTIL_PrecacheOther("ammo_9mm");
	UTIL_PrecacheOther("ammo_357sig");

	// Standard equipment
	UTIL_PrecacheOtherWeapon("weapon_flashbang");
	UTIL_PrecacheOtherWeapon("weapon_c4");

	// Secondary / Pistols
	UTIL_PrecacheOtherWeapon("weapon_colt_python");
	UTIL_PrecacheOtherWeapon("weapon_deagle_dual");
	UTIL_PrecacheOtherWeapon("weapon_dual_handgun");
	UTIL_PrecacheOtherWeapon("weapon_taurus_raging_bull");
	UTIL_PrecacheOtherWeapon("weapon_deagle");
	UTIL_PrecacheOtherWeapon("weapon_usp");
	UTIL_PrecacheOtherWeapon("weapon_glock18");

	// Primary Weapons (Top Core PB Weapons)
	UTIL_PrecacheOtherWeapon("weapon_ak47");
	UTIL_PrecacheOtherWeapon("weapon_aksopmod");
	UTIL_PrecacheOtherWeapon("weapon_aug");
	UTIL_PrecacheOtherWeapon("weapon_p90");
	UTIL_PrecacheOtherWeapon("weapon_kriss_sv");
	UTIL_PrecacheOtherWeapon("weapon_kriss_sv_silence");
	UTIL_PrecacheOtherWeapon("weapon_m4a1");
	UTIL_PrecacheOtherWeapon("weapon_mp7");
	UTIL_PrecacheOtherWeapon("weapon_oa93");
	UTIL_PrecacheOtherWeapon("weapon_groza");
	UTIL_PrecacheOtherWeapon("weapon_sc2010");
	UTIL_PrecacheOtherWeapon("weapon_awp");
	UTIL_PrecacheOtherWeapon("weapon_cheytac_m200");
	UTIL_PrecacheOtherWeapon("weapon_m82a1");
	UTIL_PrecacheOtherWeapon("weapon_tactilite_t2");
	UTIL_PrecacheOtherWeapon("weapon_m1887");
	UTIL_PrecacheOtherWeapon("weapon_spas_15");
	UTIL_PrecacheOtherWeapon("weapon_m3");

	// Melee weapons
	UTIL_PrecacheOtherWeapon("weapon_knife");
	UTIL_PrecacheOtherWeapon("weapon_amok");
	UTIL_PrecacheOtherWeapon("weapon_fangblade");
	UTIL_PrecacheOtherWeapon("weapon_combat");
	UTIL_PrecacheOtherWeapon("weapon_dual_knife");
	UTIL_PrecacheOtherWeapon("weapon_keris");

	// Explosives & Special Items
	UTIL_PrecacheOtherWeapon("weapon_hegrenade");
	UTIL_PrecacheOtherWeapon("weapon_smokegrenade");
	UTIL_PrecacheOtherWeapon("weapon_c4");

	if (g_pGameRules && g_pGameRules->IsDeathmatch())
	{
		// container for dropped deathmatch weapons
		UTIL_PrecacheOther("weaponbox");
	}

	g_sModelIndexFireball = PRECACHE_MODEL("sprites/zerogxplode.spr");	// fireball
	g_sModelIndexWExplosion = PRECACHE_MODEL("sprites/WXplo1.spr");		// underwater fireball
	g_sModelIndexSmoke = PRECACHE_MODEL("sprites/steam1.spr");		// smoke
	g_sModelIndexBubbles = PRECACHE_MODEL("sprites/bubble.spr");		// bubbles
	g_sModelIndexBloodSpray = PRECACHE_MODEL("sprites/bloodspray.spr");	// initial blood
	g_sModelIndexBloodDrop = PRECACHE_MODEL("sprites/blood.spr");		// splattered blood

	g_sModelIndexSmokePuff = PRECACHE_MODEL("sprites/smokepuff.spr");
	g_sModelIndexFireball2 = PRECACHE_MODEL("sprites/eexplo.spr");
	g_sModelIndexFireball3 = PRECACHE_MODEL("sprites/fexplo.spr");
	g_sModelIndexFireball4 = PRECACHE_MODEL("sprites/fexplo1.spr");
	g_sModelIndexRadio = PRECACHE_MODEL("sprites/radio.spr");

	g_sModelIndexCTGhost = PRECACHE_MODEL("sprites/b-tele1.spr");
	g_sModelIndexTGhost = PRECACHE_MODEL("sprites/c-tele1.spr");
	g_sModelIndexC4Glow = PRECACHE_MODEL("sprites/ledglow.spr");

	g_sModelIndexLaser = PRECACHE_MODEL((char*)g_pModelNameLaser);
	g_sModelIndexLaserDot = PRECACHE_MODEL("sprites/laserdot.spr");

	// used by explosions
	PRECACHE_MODEL("models/grenade.mdl");
	PRECACHE_MODEL("sprites/explode1.spr");

	PRECACHE_SOUND("weapons/debris1.wav");		// explosion aftermaths
	PRECACHE_SOUND("weapons/debris2.wav");		// explosion aftermaths
	PRECACHE_SOUND("weapons/debris3.wav");		// explosion aftermaths

	PRECACHE_SOUND("weapons/grenade_hit1.wav");	// grenade
	PRECACHE_SOUND("weapons/grenade_hit2.wav");	// grenade
	PRECACHE_SOUND("weapons/grenade_hit3.wav");	// grenade

	PRECACHE_SOUND("weapons/bullet_hit1.wav");	// hit by bullet
	PRECACHE_SOUND("weapons/bullet_hit2.wav");	// hit by bullet

	PRECACHE_SOUND("items/weapondrop1.wav");	// weapon falls to the ground
	PRECACHE_SOUND("weapons/generic_reload.wav");

	g_bCSPBStartupWeaponPrecachePhase = false;
	CSPB_LOG_DIAG("=== W_Precache END - Smart Pool precache complete ===");
}
