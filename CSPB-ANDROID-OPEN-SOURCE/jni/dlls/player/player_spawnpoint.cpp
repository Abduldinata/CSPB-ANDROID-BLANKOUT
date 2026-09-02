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
		// if ent is a living player, don't spawn on 'em
		if (ent->IsPlayer() && ent != pPlayer && ent->pev->health > 0 && ent->pev->deadflag == DEAD_NO)
			return FALSE;
	}

	return TRUE;
}

edict_t *EntSelectSpawnPoint(CBaseEntity *pPlayer)
{
	CBaseEntity *pSpot = NULL;
	edict_t *player = pPlayer->edict();
	int iTeam = ((CBasePlayer *)pPlayer)->m_iTeam;
	const char *szTeamClass = (iTeam == TERRORIST) ? "info_player_deathmatch" : "info_player_start";
	const char *szAltClass  = (iTeam == TERRORIST) ? "info_player_start" : "info_player_deathmatch";

	// 1. VIP spawn point
	if (g_pGameRules->IsDeathmatch() && ((CBasePlayer *)pPlayer)->m_bIsVIP)
	{
		pSpot = UTIL_FindEntityByClassname(NULL, "info_vip_start");
		if (!FNullEnt(pSpot) && pSpot->pev->origin != g_vecZero)
			goto ReturnSpot;
	}

	// 2. Try preferred team spawn points
	pSpot = (iTeam == TERRORIST) ? g_pLastTerroristSpawn : g_pLastCTSpawn;
	if (((CBasePlayer *)pPlayer)->SelectSpawnSpot(szTeamClass, pSpot))
	{
		if (!FNullEnt(pSpot) && pSpot->pev->origin != g_vecZero)
			goto ReturnSpot;
	}

	// 3. Fallback: ANY spawn point belonging to the player's OWN team
	pSpot = UTIL_FindEntityByClassname(NULL, szTeamClass);
	while (!FNullEnt(pSpot))
	{
		if (pSpot->pev->origin != g_vecZero)
			goto ReturnSpot;
		pSpot = UTIL_FindEntityByClassname(pSpot, szTeamClass);
	}

	// 4. Fallback if map has 0 spawn points for this team: use opposite team or coop spawn
	pSpot = UTIL_FindEntityByClassname(NULL, szAltClass);
	while (!FNullEnt(pSpot))
	{
		if (pSpot->pev->origin != g_vecZero)
			goto ReturnSpot;
		pSpot = UTIL_FindEntityByClassname(pSpot, szAltClass);
	}

	pSpot = UTIL_FindEntityByClassname(NULL, "info_player_coop");
	while (!FNullEnt(pSpot))
	{
		if (pSpot->pev->origin != g_vecZero)
			goto ReturnSpot;
		pSpot = UTIL_FindEntityByClassname(pSpot, "info_player_coop");
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