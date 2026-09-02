/*
player_mod_strategy.cpp - CSMoE Gameplay server : player strategy for gamemodes
Copyright (C) 2018 Moemod Hyakuya

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
*/

#include "extdll.h"
#include "util.h"
#include "cbase.h"
#include "player.h"
#include "client.h"
#include "monsters.h"
#include "player_mod_strategy.h"
#include "gamemode/mods.h"
#include "game.h"

#include "server_to_client.h"
#include "bot_include.h"

void CPlayerModStrategy_Default::CheckBuyZone()
{
	if (g_pGameRules->m_bMapHasBuyZone)
		return;
	CBasePlayer *player = m_pPlayer;

	const char *pszSpawnClass = nullptr;

	if (player->m_iTeam == TERRORIST)
		pszSpawnClass = "info_player_deathmatch";

	else if (player->m_iTeam == CT)
		pszSpawnClass = "info_player_start";

	if (pszSpawnClass != nullptr)
	{
		CBaseEntity *pSpot = nullptr;
		while ((pSpot = UTIL_FindEntityByClassname(pSpot, pszSpawnClass)) != nullptr)
		{
			if ((pSpot->pev->origin - player->pev->origin).Length() < 200.0f)
				player->m_signals.Signal(SIGNAL_BUY);
		}
	}
}

bool CPlayerModStrategy_Default::CanPlayerBuy(bool display)
{
	CBasePlayer *player = m_pPlayer;


	// is the player alive?
	if (player->pev->deadflag != DEAD_NO)
	{
		return false;
	}


	// is the player in a buy zone?
	if (!(player->m_signals.GetState() & SIGNAL_BUY))
	{
		return false;
	}

	int buyTime = (int)(CVAR_GET_FLOAT("mp_buytime") * 60.0f);

	if (buyTime < MIN_BUY_TIME)
	{
		buyTime = MIN_BUY_TIME;
		CVAR_SET_FLOAT("mp_buytime", (MIN_BUY_TIME / 60.0f));
	}

	if (gpGlobals->time - g_pGameRules->m_fRoundCount > buyTime)
	{
		if (display)
		{
			ClientPrint(player->pev, HUD_PRINTCENTER, "#Cant_buy", UTIL_dtos1(buyTime));
		}

		return false;
	}

	if (player->m_bIsVIP)
	{
		if (display)
		{
			ClientPrint(player->pev, HUD_PRINTCENTER, "#VIP_cant_buy");
		}

		return false;
	}

	if (g_pGameRules->m_bCTCantBuy && player->m_iTeam == CT)
	{
		if (display)
		{
			ClientPrint(player->pev, HUD_PRINTCENTER, "#CT_cant_buy");
		}

		return false;
	}

	if (g_pGameRules->m_bTCantBuy && player->m_iTeam == TERRORIST)
	{
		if (display)
		{
			ClientPrint(player->pev, HUD_PRINTCENTER, "#Terrorist_cant_buy");
		}

		return false;
	}

	return true;
}

void CPlayerModStrategy_Default::Pain(int m_LastHitGroup, bool HasArmour)
{

if ((int)CVAR_GET_FLOAT("sv_hithuman_sound"))
	{


	auto temp = RANDOM_LONG(0, 2);

	if (m_LastHitGroup == HITGROUP_HEAD)
	{
		if (m_pPlayer->m_iKevlar == ARMOR_TYPE_HELMET)
		{
			EMIT_SOUND(ENT(m_pPlayer->pev), CHAN_VOICE, "nautilus/misc/hit_human_1.wav", VOL_NORM, ATTN_NORM);

			return;
		}

		switch (temp)
		{
		case 0: EMIT_SOUND(ENT(m_pPlayer->pev), CHAN_VOICE, "nautilus/misc/hit_human_1.wav", VOL_NORM, ATTN_NORM); break;
		case 1: EMIT_SOUND(ENT(m_pPlayer->pev), CHAN_VOICE, "nautilus/misc/hit_human_1.wav", VOL_NORM, ATTN_NORM); break;
		default: EMIT_SOUND(ENT(m_pPlayer->pev), CHAN_VOICE, "nautilus/misc/hit_human_1.wav", VOL_NORM, ATTN_NORM); break;
		}
	}
	else
	{
		if (m_LastHitGroup != HITGROUP_LEFTLEG && m_LastHitGroup != HITGROUP_RIGHTLEG)
		{
			if (HasArmour)
			{
				EMIT_SOUND(ENT(m_pPlayer->pev), CHAN_VOICE, "nautilus/misc/hit_human_1.wav", VOL_NORM, ATTN_NORM);
				return;
			}
		}

		switch (temp)
		{
		case 0: EMIT_SOUND(ENT(m_pPlayer->pev), CHAN_VOICE, "nautilus/misc/hit_human_1.wav", VOL_NORM, ATTN_NORM); break;
		case 1: EMIT_SOUND(ENT(m_pPlayer->pev), CHAN_VOICE, "nautilus/misc/hit_human_1.wav", VOL_NORM, ATTN_NORM); break;
		default: EMIT_SOUND(ENT(m_pPlayer->pev), CHAN_VOICE, "nautilus/misc/hit_human_1.wav", VOL_NORM, ATTN_NORM); break;
		}
	}
}
else
{
auto temp = RANDOM_LONG(0, 2);

	if (m_LastHitGroup == HITGROUP_HEAD)
	{
		if (m_pPlayer->m_iKevlar == ARMOR_TYPE_HELMET)
		{
			EMIT_SOUND(ENT(m_pPlayer->pev), CHAN_VOICE, "player/bhit_helmet-1.wav", VOL_NORM, ATTN_NORM);

			return;
		}

		switch (temp)
		{
		case 0: EMIT_SOUND(ENT(m_pPlayer->pev), CHAN_VOICE, "player/headshot1.wav", VOL_NORM, ATTN_NORM); break;
		case 1: EMIT_SOUND(ENT(m_pPlayer->pev), CHAN_VOICE, "player/headshot2.wav", VOL_NORM, ATTN_NORM); break;
		default: EMIT_SOUND(ENT(m_pPlayer->pev), CHAN_VOICE, "player/headshot3.wav", VOL_NORM, ATTN_NORM); break;
		}
	}
	else
	{
		if (m_LastHitGroup != HITGROUP_LEFTLEG && m_LastHitGroup != HITGROUP_RIGHTLEG)
		{
			if (HasArmour)
			{
				EMIT_SOUND(ENT(m_pPlayer->pev), CHAN_VOICE, "player/bhit_kevlar-1.wav", VOL_NORM, ATTN_NORM);
				return;
			}
		}

		switch (temp)
		{
		case 0: EMIT_SOUND(ENT(m_pPlayer->pev), CHAN_VOICE, "player/bhit_flesh-1.wav", VOL_NORM, ATTN_NORM); break;
		case 1: EMIT_SOUND(ENT(m_pPlayer->pev), CHAN_VOICE, "player/bhit_flesh-2.wav", VOL_NORM, ATTN_NORM); break;
		default: EMIT_SOUND(ENT(m_pPlayer->pev), CHAN_VOICE, "player/bhit_flesh-3.wav", VOL_NORM, ATTN_NORM); break;
		}
	}
}

}

void CPlayerModStrategy_Default::DeathSound()
{

if (m_pPlayer->m_LastHitGroup == HITGROUP_HEAD)
		{
			switch (RANDOM_LONG(1, 4))
	{
	case 1: EMIT_SOUND(ENT(m_pPlayer->pev), CHAN_VOICE, "nautilus/misc/headshot1.wav", VOL_NORM, ATTN_NORM); break;
	case 2: EMIT_SOUND(ENT(m_pPlayer->pev), CHAN_VOICE, "nautilus/misc/headshot2.wav", VOL_NORM, ATTN_NORM); break;
	case 3: EMIT_SOUND(ENT(m_pPlayer->pev), CHAN_VOICE, "nautilus/misc/headshot3.wav", VOL_NORM, ATTN_NORM); break;
case 4: EMIT_SOUND(ENT(m_pPlayer->pev), CHAN_VOICE, "nautilus/misc/headshot4.wav", VOL_NORM, ATTN_NORM); break;
	}
	
	}
	else
	{
		

		switch (m_pPlayer->m_iModelName)
		{
		case MODEL_URBAN:
EMIT_SOUND(ENT(m_pPlayer->pev), CHAN_VOICE, "player/die1.wav", VOL_NORM, ATTN_NORM);
			break;
		case MODEL_GSG9:
			EMIT_SOUND(ENT(m_pPlayer->pev), CHAN_VOICE, "player/female/die1.wav", VOL_NORM, ATTN_NORM);
			break;
		case MODEL_SAS:
EMIT_SOUND(ENT(m_pPlayer->pev), CHAN_VOICE, "player/die1.wav", VOL_NORM, ATTN_NORM);
			break;
		case MODEL_GIGN:
EMIT_SOUND(ENT(m_pPlayer->pev), CHAN_VOICE, "player/female/die1.wav", VOL_NORM, ATTN_NORM);
			break;

                             case MODEL_SPETSNAZ:
EMIT_SOUND(ENT(m_pPlayer->pev), CHAN_VOICE, "player/female/die1.wav", VOL_NORM, ATTN_NORM);
			break;

                           case MODEL_TERROR:
EMIT_SOUND(ENT(m_pPlayer->pev), CHAN_VOICE, "player/die1.wav", VOL_NORM, ATTN_NORM);
			break;
		case MODEL_LEET:
EMIT_SOUND(ENT(m_pPlayer->pev), CHAN_VOICE, "player/female/die1.wav", VOL_NORM, ATTN_NORM);
			break;
		case MODEL_ARCTIC:
EMIT_SOUND(ENT(m_pPlayer->pev), CHAN_VOICE, "player/die1.wav", VOL_NORM, ATTN_NORM);
			break;
		case MODEL_GUERILLA:
EMIT_SOUND(ENT(m_pPlayer->pev), CHAN_VOICE, "player/female/die1.wav", VOL_NORM, ATTN_NORM);
			break;

case MODEL_MILITIA:
EMIT_SOUND(ENT(m_pPlayer->pev), CHAN_VOICE, "player/female/die1.wav", VOL_NORM, ATTN_NORM);
			break;

case MODEL_BLUEFEMALE1:
EMIT_SOUND(ENT(m_pPlayer->pev), CHAN_VOICE, "player/female/die1.wav", VOL_NORM, ATTN_NORM);
			break;

                           case MODEL_BLUEMALE1:
EMIT_SOUND(ENT(m_pPlayer->pev), CHAN_VOICE, "player/die1.wav", VOL_NORM, ATTN_NORM);
			break;

case MODEL_REDFEMALE1:
EMIT_SOUND(ENT(m_pPlayer->pev), CHAN_VOICE, "player/female/die1.wav", VOL_NORM, ATTN_NORM);
			break;

                           case MODEL_REDMALE1:
EMIT_SOUND(ENT(m_pPlayer->pev), CHAN_VOICE, "player/die1.wav", VOL_NORM, ATTN_NORM);
			break;

}

}

}

void CPlayerModStrategy_Default::lastinv()
{

}

void CPlayerModStrategy_Default::GiveDefaultItems()
{
	m_pPlayer->RemoveAllItems(FALSE);
	m_pPlayer->m_bHasPrimary = false;

	m_pPlayer->pev->round_frags = 0;
	m_pPlayer->pev->round_frags_sniper = 0;
	m_pPlayer->pev->round_frags_headshot = 0;

	// 1. Primary
	const char *szPrim = (m_pPlayer->m_szPendingPrimary[0] != '\0') ? m_pPlayer->m_szPendingPrimary : "weapon_m4a1";
	m_pPlayer->GiveNamedItem(szPrim);

	// 2. Secondary
	const char *szSec = (m_pPlayer->m_szPendingSecondary[0] != '\0') ? m_pPlayer->m_szPendingSecondary : "weapon_usp";
	m_pPlayer->GiveNamedItem(szSec);

	// 3. Melee
	const char *szMelee = (m_pPlayer->m_szPendingMelee[0] != '\0') ? m_pPlayer->m_szPendingMelee : "weapon_knife";
	m_pPlayer->GiveNamedItem(szMelee);

	// 4. Grenade (Slot 4: K400 / HE Grenade) - Exactly 1 grenade
	const char *szGrenade = (m_pPlayer->m_szPendingGrenade[0] != '\0') ? m_pPlayer->m_szPendingGrenade : "weapon_hegrenade";
	m_pPlayer->GiveNamedItem(szGrenade);

	// 5. Special (Slot 5: Medkit / Smoke) - Exactly 1 special
	const char *szSpecial = (m_pPlayer->m_szPendingSpecial[0] != '\0') ? m_pPlayer->m_szPendingSpecial : "weapon_smokegrenade";
	m_pPlayer->GiveNamedItem(szSpecial);

	// Full Ammo for all weapon classes
	m_pPlayer->GiveAmmo(280, "556Nato", 280);
	m_pPlayer->GiveAmmo(280, "556nato", 280);
	m_pPlayer->GiveAmmo(82, "buckshot", 82);
	m_pPlayer->GiveAmmo(82, "9mm", 82);
	m_pPlayer->GiveAmmo(280, "762Nato", 280);
	m_pPlayer->GiveAmmo(82, "50AE", 82);
	m_pPlayer->GiveAmmo(50, "338Magnum", 50);
	m_pPlayer->GiveAmmo(82, "357SIG", 82);
	m_pPlayer->GiveAmmo(50, "50bmg", 50);
	m_pPlayer->GiveAmmo(36, "46mm", 36);
	m_pPlayer->GiveAmmo(82, "57mm", 82);
	m_pPlayer->GiveAmmo(82, "45acp", 82);
	m_pPlayer->GiveAmmo(1, "HEGrenade", 1);
	m_pPlayer->GiveAmmo(1, "SmokeGrenade", 1);
}

void CPlayerModStrategy_Zombie::Pain(int m_LastHitGroup, bool HasArmour)
{
	CPlayerModStrategy_Default::Pain(m_LastHitGroup, HasArmour);
}

void CPlayerModStrategy_Zombie::DeathSound()
{
	CPlayerModStrategy_Default::DeathSound();
}

float CPlayerModStrategy_Zombie::AdjustDamageTaken(entvars_t *pevInflictor, entvars_t *pevAttacker, float flDamage, int bitsDamageType)
{
	// grenade damage 5x in zb mode
	if (!Q_strcmp(STRING(pevInflictor->classname), "grenade"))
	{
		if (bitsDamageType & DMG_EXPLOSION)
		{
				flDamage *= 5.0f;
			
		}
	}
	return CPlayerModStrategy_Default::AdjustDamageTaken(pevInflictor, pevAttacker, flDamage, bitsDamageType);
}

void CPlayerModStrategy_Zombie::GiveDefaultItems()
{
	if (!m_pPlayer->m_bIsZombie)
		return CPlayerModStrategy_Default::GiveDefaultItems();	

	m_pPlayer->RemoveAllItems(FALSE);
	m_pPlayer->m_bHasPrimary = false;

	m_pPlayer->GiveNamedItem("knife_zombi");

	if (!(m_pPlayer->m_flDisplayHistory & DHF_NIGHTVISION))
	{
		m_pPlayer->HintMessage("#Hint_use_nightvision");
		m_pPlayer->m_flDisplayHistory |= DHF_NIGHTVISION;
	}
	EMIT_SOUND(ENT(m_pPlayer->pev), CHAN_ITEM, "items/equip_nvg.wav", VOL_NORM, ATTN_NORM);
	m_pPlayer->m_bHasNightVision = true;
	SendItemStatus(m_pPlayer);
	
}
