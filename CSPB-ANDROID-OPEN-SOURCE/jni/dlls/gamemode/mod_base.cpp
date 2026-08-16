#include "extdll.h"
#include "util.h"
#include "cbase.h"
#include "player.h"
#include "game.h"
#include "enginecallback.h"

#include "bmodels.h"

#include "mod_base.h"

#include "player/csdm_randomspawn.h"

void IBaseMod::InstallPlayerModStrategy(CBasePlayer *player)
{
	std::unique_ptr<CPlayerModStrategy_Default> up(new CPlayerModStrategy_Default(player));
	player->m_pModStrategy = std::move(up);
}

void _IBaseMod_RemoveObjects_CheckMapConditions_impl(IBaseMod *mod)
{
	//CHalfLifeMultiplay::CheckMapConditions();
	
	// Check to see if this map has a bomb target in it
	mod->m_bMapHasBombTarget = false;
	mod->m_bMapHasBombZone = false;

	// Check to see if this map has hostage rescue zones
	mod->m_bMapHasRescueZone = false;

	// See if the map has func_buyzone entities
	// Used by CBasePlayer::HandleSignals() to support maps without these entities
	mod->m_bMapHasBuyZone = (UTIL_FindEntityByClassname(NULL, "func_buyzone") != NULL);

	// GOOSEMAN : See if this map has func_escapezone entities
	mod->m_bMapHasEscapeZone = false;

	// Check to see if this map has VIP safety zones
	mod->m_iMapHasVIPSafetyZone = MAP_HAVE_VIP_SAFETYZONE_NO;

	// Hostage
	/*CBaseEntity *hostage = nullptr;
	while ((hostage = UTIL_FindEntityByClassname(hostage, "hostage_entity")) != nullptr)
	{
		// should be removed.
		REMOVE_ENTITY(hostage->edict());
	}*/
}

BOOL _IBaseMod_RemoveObjects_IsAllowedToSpawn_impl(IBaseMod *mod, CBaseEntity *pEntity) {
	if (!Q_strcmp(STRING(pEntity->pev->classname), "func_bomb_target") ||
	    !Q_strcmp(STRING(pEntity->pev->classname), "info_bomb_target")) {
		return FALSE;
	}
	if (!Q_strcmp(STRING(pEntity->pev->classname), "func_hostage_rescue")) {
		return FALSE;
	}
	if (!Q_strcmp(STRING(pEntity->pev->classname), "func_escapezone")) {
		return FALSE;
	}
	if (!Q_strcmp(STRING(pEntity->pev->classname), "func_vip_safetyzone")) {
		return FALSE;
	}
	if (!Q_strcmp(STRING(pEntity->pev->classname), "hostage_entity")) {
		return FALSE;
	}
	return TRUE;
}

edict_t *_IBaseMod_RandomSpawn_GetPlayerSpawnSpot_impl(IBaseMod *mod, CBasePlayer *pPlayer)
{
	// completely rewrites it

	// Get valid spawn point for the player's ACTUAL team (fallback if CSDM fails)
	edict_t *pentSpawnSpot = EntSelectSpawnPoint(pPlayer);

	// Move the player to the place it said.
	if (!CSDM_DoRandomSpawn(pPlayer))
	{
		Vector vecSpawnOrigin = VARS(pentSpawnSpot)->origin;

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

		Vector vecFinalOrigin = vecSpawnOrigin + Vector(0, 0, 1);
		CBaseEntity *pOther = NULL;
		int iNudge = 0;
		while ((pOther = UTIL_FindEntityInSphere(pOther, vecFinalOrigin, 36.0f)) != NULL)
		{
			if (pOther->IsPlayer() && pOther->edict() != pPlayer->edict() && pOther->IsAlive())
			{
				iNudge++;
				float flRad = (float)iNudge * 1.047197f;
				vecFinalOrigin.x = vecSpawnOrigin.x + cosf(flRad) * (36.0f * iNudge);
				vecFinalOrigin.y = vecSpawnOrigin.y + sinf(flRad) * (36.0f * iNudge);
				vecFinalOrigin.z = vecSpawnOrigin.z + 1.0f;
			}
		}

		pPlayer->pev->origin = vecFinalOrigin;
		pPlayer->pev->v_angle = g_vecZero;
		pPlayer->pev->velocity = g_vecZero;
		pPlayer->pev->angles = VARS(pentSpawnSpot)->angles;
	}

	pPlayer->pev->punchangle = g_vecZero;
	pPlayer->pev->fixangle = 1;

	if (mod->IsMultiplayer())
	{
		if (pentSpawnSpot->v.target)
		{
			FireTargets(STRING(pentSpawnSpot->v.target), pPlayer, pPlayer, USE_TOGGLE, 0);
		}
	}

	return pentSpawnSpot;
}
