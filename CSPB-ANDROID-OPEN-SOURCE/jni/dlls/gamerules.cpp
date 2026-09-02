
#include "extdll.h"
#include "util.h"
#include "cbase.h"
#include "player.h"
#include "weapons.h"
#include "gamerules.h"
#include "training_gamerules.h"
#include "skill.h"
#include "game.h"
#include "globals.h"

#include "utllinkedlist.h"
#include "pm_shared.h"

#include "game_shared/GameEvent.h"
#include "game_shared/bot/bot_util.h"


#include "game_shared/steam_util.h"
#include "game_shared/bot/bot_manager.h"

#include "game_shared/shared_util.h"
#include "game_shared/bot/bot_profile.h"

#include "game_shared/bot/nav.h"
#include "game_shared/bot/improv.h"
#include "game_shared/bot/nav_node.h"
#include "game_shared/bot/nav_area.h"
#include "game_shared/bot/nav_file.h"
#include "game_shared/bot/nav_path.h"

#include "bot/bot_constants.h"
#include "bot/cs_bot_manager.h"

#include "cvardef.h"
#include "gamemode/mods.h"

/*
* Globals initialization
*/
CHalfLifeMultiplay *g_pGameRules = NULL;

BOOL CGameRules::CanHaveAmmo(CBasePlayer *pPlayer, const char *pszAmmoName, int iMaxCarry)
{
	int iAmmoIndex;

	if (pszAmmoName != NULL)
	{
		iAmmoIndex = pPlayer->GetAmmoIndex(pszAmmoName);

		if (iAmmoIndex > -1)
		{
			if (pPlayer->AmmoInventory(iAmmoIndex) < iMaxCarry)
			{
				// player has room for more of this type of ammo
				return TRUE;
			}
		}
	}

	return FALSE;
}

edict_t *CGameRules::GetPlayerSpawnSpot(CBasePlayer *pPlayer)
{
	// get valid spawn point
	edict_t *pentSpawnSpot = EntSelectSpawnPoint(pPlayer);

	Vector vecSpawnOrigin = VARS(pentSpawnSpot)->origin;

	// If spawn point has zero origin (worldspawn fallback), try to find any valid player spawn
	if (vecSpawnOrigin == g_vecZero)
	{
		CBaseEntity *pFallback = UTIL_FindEntityByClassname(NULL, "info_player_start");
		while (pFallback != NULL)
		{
			if (pFallback->pev->origin != g_vecZero)
			{
				pentSpawnSpot = pFallback->edict();
				vecSpawnOrigin = pFallback->pev->origin;
				break;
			}
			pFallback = UTIL_FindEntityByClassname(pFallback, "info_player_start");
		}

		if (vecSpawnOrigin == g_vecZero)
		{
			pFallback = UTIL_FindEntityByClassname(NULL, "info_player_deathmatch");
			while (pFallback != NULL)
			{
				if (pFallback->pev->origin != g_vecZero)
				{
					pentSpawnSpot = pFallback->edict();
					vecSpawnOrigin = pFallback->pev->origin;
					break;
				}
				pFallback = UTIL_FindEntityByClassname(pFallback, "info_player_deathmatch");
			}
		}
	}

	// Anti-stuck: If another player/bot is already standing at the spawn point, offset slightly
	Vector vecFinalOrigin = vecSpawnOrigin + Vector(0, 0, 1);
	CBaseEntity *pOther = NULL;
	int iNudge = 0;
	while ((pOther = UTIL_FindEntityInSphere(pOther, vecFinalOrigin, 36.0f)) != NULL)
	{
		if (pOther->IsPlayer() && pOther->edict() != pPlayer->edict() && pOther->IsAlive())
		{
			iNudge++;
			float flRad = (float)iNudge * 1.047197f; // ~60 deg
			vecFinalOrigin.x = vecSpawnOrigin.x + cosf(flRad) * (36.0f * iNudge);
			vecFinalOrigin.y = vecSpawnOrigin.y + sinf(flRad) * (36.0f * iNudge);
			vecFinalOrigin.z = vecSpawnOrigin.z + 1.0f;
		}
	}

	pPlayer->pev->origin = vecFinalOrigin;
	pPlayer->pev->v_angle = g_vecZero;
	pPlayer->pev->velocity = g_vecZero;
	pPlayer->pev->angles = VARS(pentSpawnSpot)->angles;
	pPlayer->pev->punchangle = g_vecZero;
	pPlayer->pev->fixangle = 1;
	pPlayer->pev->flags |= FL_ONGROUND;
	DROP_TO_FLOOR(pPlayer->edict());

	return pentSpawnSpot;
}

BOOL CGameRules::CanHavePlayerItem(CBasePlayer *pPlayer, CBasePlayerItem *pWeapon)
{
	// only living players can have items
	if (pPlayer->pev->deadflag != DEAD_NO)
	{
		return FALSE;
	}

	CCSBotManager *ctrl = TheCSBots();

	if (pPlayer->IsBot() && ctrl != NULL && !ctrl->IsWeaponUseable(pWeapon))
	{
		return FALSE;
	}

	if (pWeapon->pszAmmo1())
	{
		if (!CanHaveAmmo(pPlayer, pWeapon->pszAmmo1(), pWeapon->iMaxAmmo1()))
		{
			// we can't carry anymore ammo for this gun. We can only
			// have the gun if we aren't already carrying one of this type
			if (pPlayer->HasPlayerItem(pWeapon))
			{
				return FALSE;
			}
		}
	}
	else
	{
		// weapon doesn't use ammo, don't take another if you already have it.
		if (pPlayer->HasPlayerItem(pWeapon))
		{
			return FALSE;
		}
	}

	// note: will fall through to here if GetItemInfo doesn't fill the struct!
	return TRUE;
}

void CGameRules::RefreshSkillData()
{
	int iSkill = (int)CVAR_GET_FLOAT("skill");

	if (iSkill < 1)
		iSkill = 1;

	else if (iSkill > 3)
		iSkill = 3;

	gSkillData.iSkillLevel = iSkill;
	ALERT(at_console, "\nGAME SKILL LEVEL:%d\n", iSkill);

	gSkillData.monDmg12MM = 8;
	gSkillData.monDmgMP5 = 3;
	gSkillData.monDmg9MM = 5;
	gSkillData.suitchargerCapacity = 75;
	gSkillData.batteryCapacity = 15;
	gSkillData.healthchargerCapacity = 50;
	gSkillData.healthkitCapacity = 15;
}

CGameRules *InstallGameRules()
{
	SERVER_COMMAND("exec game.cfg\n");
	SERVER_EXECUTE();

	if (!gpGlobals->deathmatch)
		return new CHalfLifeTraining;

	//return new CHalfLifeMultiplay;
	InstallBteMod(gamemode.string);
	return g_pModRunning;
}
