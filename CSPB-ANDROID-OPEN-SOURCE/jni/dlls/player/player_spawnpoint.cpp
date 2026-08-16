#include "extdll.h"
#include "util.h"
#include "cbase.h"
#include "player.h"
#include "gamerules.h"

// global vars
DLL_GLOBAL CBaseEntity *g_pLastSpawn;
DLL_GLOBAL CBaseEntity *g_pLastCTSpawn, *g_pLastTerroristSpawn;

// utils
inline int FNullEnt(CBaseEntity *ent) { return (!ent) || FNullEnt(ent->edict()); }

// main code

BOOL IsSpawnPointValid(CBaseEntity *pPlayer, CBaseEntity *pSpot)
{
	CBaseEntity *ent = NULL;

	if (!pSpot->IsTriggered(pPlayer))
		return FALSE;

	while ((ent = UTIL_FindEntityInSphere(ent, pSpot->pev->origin, 64)) != NULL)
	{
		// if ent is a client, don't spawn on 'em
		if (ent->IsPlayer() && ent != pPlayer)
			return FALSE;
	}

	return TRUE;
}

edict_t *EntSelectSpawnPoint(CBaseEntity *pPlayer)
{
	CBaseEntity *pSpot = NULL;
	edict_t *player = pPlayer->edict();
	int iTeam = ((CBasePlayer *)pPlayer)->m_iTeam;

	// 1. VIP spawn point
	if (g_pGameRules->IsDeathmatch() && ((CBasePlayer *)pPlayer)->m_bIsVIP)
	{
		pSpot = UTIL_FindEntityByClassname(NULL, "info_vip_start");
		if (!FNullEnt(pSpot) && pSpot->pev->origin != g_vecZero)
			goto ReturnSpot;
	}

	// 2. Try preferred team spawn points
	if (iTeam == TERRORIST)
	{
		pSpot = g_pLastTerroristSpawn;
		if (((CBasePlayer *)pPlayer)->SelectSpawnSpot("info_player_deathmatch", pSpot))
		{
			if (!FNullEnt(pSpot) && pSpot->pev->origin != g_vecZero)
				goto ReturnSpot;
		}

		// Fallback: any info_player_deathmatch
		pSpot = UTIL_FindEntityByClassname(NULL, "info_player_deathmatch");
		while (!FNullEnt(pSpot))
		{
			if (pSpot->pev->origin != g_vecZero)
				goto ReturnSpot;
			pSpot = UTIL_FindEntityByClassname(pSpot, "info_player_deathmatch");
		}

		// Fallback to CT spawn if T spawn doesn't exist
		pSpot = UTIL_FindEntityByClassname(NULL, "info_player_start");
		while (!FNullEnt(pSpot))
		{
			if (pSpot->pev->origin != g_vecZero)
				goto ReturnSpot;
			pSpot = UTIL_FindEntityByClassname(pSpot, "info_player_start");
		}
	}
	else
	{
		// CT or UNASSIGNED or SPECTATOR
		pSpot = g_pLastCTSpawn;
		if (((CBasePlayer *)pPlayer)->SelectSpawnSpot("info_player_start", pSpot))
		{
			if (!FNullEnt(pSpot) && pSpot->pev->origin != g_vecZero)
				goto ReturnSpot;
		}

		// Fallback: any info_player_start
		pSpot = UTIL_FindEntityByClassname(NULL, "info_player_start");
		while (!FNullEnt(pSpot))
		{
			if (pSpot->pev->origin != g_vecZero)
				goto ReturnSpot;
			pSpot = UTIL_FindEntityByClassname(pSpot, "info_player_start");
		}

		// Fallback to T spawn if CT spawn doesn't exist
		pSpot = UTIL_FindEntityByClassname(NULL, "info_player_deathmatch");
		while (!FNullEnt(pSpot))
		{
			if (pSpot->pev->origin != g_vecZero)
				goto ReturnSpot;
			pSpot = UTIL_FindEntityByClassname(pSpot, "info_player_deathmatch");
		}
	}

	// 3. Fallback: co-op / single-player spawn points
	pSpot = UTIL_FindEntityByClassname(NULL, "info_player_coop");
	while (!FNullEnt(pSpot))
	{
		if (pSpot->pev->origin != g_vecZero)
			goto ReturnSpot;
		pSpot = UTIL_FindEntityByClassname(pSpot, "info_player_coop");
	}

	// 4. Fallback: any entity on map with valid non-zero origin
	{
		const char *szClasses[] = { "armoury_entity", "hostage_entity", "info_target", "func_buyzone", "info_bomb_target" };
		for (size_t i = 0; i < sizeof(szClasses)/sizeof(szClasses[0]); i++)
		{
			pSpot = UTIL_FindEntityByClassname(NULL, szClasses[i]);
			while (!FNullEnt(pSpot))
			{
				if (pSpot->pev->origin != g_vecZero)
					goto ReturnSpot;
				pSpot = UTIL_FindEntityByClassname(pSpot, szClasses[i]);
			}
		}
	}

ReturnSpot:
	if (FNullEnt(pSpot))
	{
		ALERT(at_error, "EntSelectSpawnPoint: No spawn point found on map!\n");
		return INDEXENT(0);
	}

	if (iTeam == TERRORIST)
		g_pLastTerroristSpawn = pSpot;
	else
		g_pLastCTSpawn = pSpot;

	return pSpot->edict();
}