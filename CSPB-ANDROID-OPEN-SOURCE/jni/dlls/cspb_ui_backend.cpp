#include "extdll.h"
#include "util.h"
#include "cbase.h"
#include "player.h"
#include "weapons.h"
#include "cspb_ui_backend.h"

#include <android/log.h>
#define CSPB_LOG_DIAG(fmt, ...) __android_log_print(ANDROID_LOG_DEBUG, "CSPB_DEBUG", fmt, ##__VA_ARGS__)

char g_ActivePrimaryWeapons[MAX_ACTIVE_WEAPONS][64];
char g_ActiveSecondaryWeapons[MAX_ACTIVE_WEAPONS][64];
char g_ActiveMeleeWeapons[MAX_ACTIVE_WEAPONS][64];
char g_ActiveGrenadeWeapons[MAX_ACTIVE_WEAPONS][64];
char g_ActiveSpecialWeapons[MAX_ACTIVE_WEAPONS][64];

int g_iNumActivePrimary = 0;
int g_iNumActiveSecondary = 0;
int g_iNumActiveMelee = 0;
int g_iNumActiveGrenade = 0;
int g_iNumActiveSpecial = 0;

void CSPB_LoadActiveWeapons()
{
	g_iNumActivePrimary = 0;
	g_iNumActiveSecondary = 0;
	g_iNumActiveMelee = 0;
	g_iNumActiveGrenade = 0;
	g_iNumActiveSpecial = 0;

	int length = 0;
	bool bIsMalloc = false;
	char *pFile = (char *)LOAD_FILE_FOR_ME("active_weapons.txt", &length);

	if (!pFile)
	{
		CSPB_LOG_DIAG("[CSPB] LOAD_FILE_FOR_ME failed, trying fopen...");
		FILE *fp = fopen("/storage/emulated/0/Android/data/com.cspb.blankout/files/cspb/active_weapons.txt", "r");
		if (fp)
		{
			fseek(fp, 0, SEEK_END);
			length = ftell(fp);
			fseek(fp, 0, SEEK_SET);
			pFile = (char *)malloc(length + 1);
			fread(pFile, 1, length, fp);
			pFile[length] = '\0';
			fclose(fp);
			bIsMalloc = true;
			CSPB_LOG_DIAG("[CSPB] active_weapons.txt loaded via fopen! Length: %d", length);
		}
	}

	if (!pFile)
	{
		CSPB_LOG_DIAG("[CSPB] active_weapons.txt completely missing. Using fallbacks.");
		strcpy(g_ActivePrimaryWeapons[g_iNumActivePrimary++], "weapon_m4a1");
		strcpy(g_ActivePrimaryWeapons[g_iNumActivePrimary++], "weapon_ak47");
		strcpy(g_ActiveSecondaryWeapons[g_iNumActiveSecondary++], "weapon_usp");
		strcpy(g_ActiveSecondaryWeapons[g_iNumActiveSecondary++], "weapon_glock18");
		strcpy(g_ActiveMeleeWeapons[g_iNumActiveMelee++], "weapon_knife");
		strcpy(g_ActiveGrenadeWeapons[g_iNumActiveGrenade++], "weapon_hegrenade");
		strcpy(g_ActiveSpecialWeapons[g_iNumActiveSpecial++], "weapon_smokegrenade");
		strcpy(g_ActiveSpecialWeapons[g_iNumActiveSpecial++], "weapon_medkit");
		return;
	}

	char *pData = pFile;
	char line[256];
	int mode = 0; // 1 = PRIMARY, 2 = SECONDARY, 3 = MELEE, 4 = GRENADE, 5 = SPECIAL

	while (pData && *pData && pData - pFile < length)
	{
		char *pLineStart = pData;
		while (*pData && *pData != '\n' && pData - pFile < length)
			pData++;
		
		int lineLen = pData - pLineStart;
		if (lineLen > 255) lineLen = 255;
		strncpy(line, pLineStart, lineLen);
		line[lineLen] = '\0';
		
		if (pData - pFile < length && *pData == '\n') pData++;
		
		// Trim \r
		if (lineLen > 0 && line[lineLen-1] == '\r')
			line[lineLen-1] = '\0';

		if (line[0] == '\0' || line[0] == '/' || line[0] == '#')
			continue;

		if (strstr(line, "[PRIMARY]"))
		{
			mode = 1;
			continue;
		}
		else if (strstr(line, "[SECONDARY]"))
		{
			mode = 2;
			continue;
		}
		else if (strstr(line, "[MELEE]"))
		{
			mode = 3;
			continue;
		}
		else if (strstr(line, "[GRENADE]") || strstr(line, "[EXPLOSIVE]"))
		{
			mode = 4;
			continue;
		}
		else if (strstr(line, "[SPECIAL]"))
		{
			mode = 5;
			continue;
		}

		if (mode == 1 && g_iNumActivePrimary < MAX_ACTIVE_WEAPONS)
		{
			strncpy(g_ActivePrimaryWeapons[g_iNumActivePrimary++], line, 63);
		}
		else if (mode == 2 && g_iNumActiveSecondary < MAX_ACTIVE_WEAPONS)
		{
			strncpy(g_ActiveSecondaryWeapons[g_iNumActiveSecondary++], line, 63);
		}
		else if (mode == 3 && g_iNumActiveMelee < MAX_ACTIVE_WEAPONS)
		{
			strncpy(g_ActiveMeleeWeapons[g_iNumActiveMelee++], line, 63);
		}
		else if (mode == 4 && g_iNumActiveGrenade < MAX_ACTIVE_WEAPONS)
		{
			strncpy(g_ActiveGrenadeWeapons[g_iNumActiveGrenade++], line, 63);
		}
		else if (mode == 5 && g_iNumActiveSpecial < MAX_ACTIVE_WEAPONS)
		{
			strncpy(g_ActiveSpecialWeapons[g_iNumActiveSpecial++], line, 63);
		}
	}

	if (bIsMalloc)
		free(pFile);
	else
		FREE_FILE(pFile);

	// Ensure fallbacks if empty
	if (g_iNumActiveGrenade == 0)
		strcpy(g_ActiveGrenadeWeapons[g_iNumActiveGrenade++], "weapon_hegrenade");
	if (g_iNumActiveSpecial == 0)
	{
		strcpy(g_ActiveSpecialWeapons[g_iNumActiveSpecial++], "weapon_smokegrenade");
		strcpy(g_ActiveSpecialWeapons[g_iNumActiveSpecial++], "weapon_medkit");
	}
	
	ALERT(at_console, "[CSPB] Loaded %d Primary, %d Secondary, %d Melee, %d Grenade, %d Special active weapons.\n", 
		g_iNumActivePrimary, g_iNumActiveSecondary, g_iNumActiveMelee, g_iNumActiveGrenade, g_iNumActiveSpecial);
}

void CSPB_PrecacheActiveWeapons()
{
	for (int i = 0; i < g_iNumActivePrimary; i++)
		UTIL_PrecacheOtherWeapon(g_ActivePrimaryWeapons[i]);
	for (int i = 0; i < g_iNumActiveSecondary; i++)
		UTIL_PrecacheOtherWeapon(g_ActiveSecondaryWeapons[i]);
	for (int i = 0; i < g_iNumActiveMelee; i++)
		UTIL_PrecacheOtherWeapon(g_ActiveMeleeWeapons[i]);
	for (int i = 0; i < g_iNumActiveGrenade; i++)
		UTIL_PrecacheOtherWeapon(g_ActiveGrenadeWeapons[i]);
	for (int i = 0; i < g_iNumActiveSpecial; i++)
		UTIL_PrecacheOtherWeapon(g_ActiveSpecialWeapons[i]);
}

void CSPB_UpdateTouchButton(CBasePlayer *pPlayer, const char *btnName, const char *weaponName)
{
	char texturePath[128];
	snprintf(texturePath, sizeof(texturePath), "gfx/billflx/weapons/%s", weaponName);

	// Remove old button
	char cmd[256];
	snprintf(cmd, sizeof(cmd), "touch_removebutton \"%s\"\n", btnName);
	CLIENT_COMMAND(pPlayer->edict(), cmd);

	float x1 = 0.43f, y1 = 0.135556f, x2 = 0.57f, y2 = 0.288889f;
	if (!strcmp(btnName, "prim2") || !strcmp(btnName, "bg5_p")) { x1=0.43f; y1=0.135556f; x2=0.57f; y2=0.288889f; }
	else if (!strcmp(btnName, "sec2") || !strcmp(btnName, "bg5_s")) { x1=0.43f; y1=0.288889f; x2=0.57f; y2=0.422222f; }
	else if (!strcmp(btnName, "melee2") || !strcmp(btnName, "bg5_m")) { x1=0.43f; y1=0.418889f; x2=0.57f; y2=0.552222f; }
	else if (!strcmp(btnName, "exp2") || !strcmp(btnName, "bg5_e")) { x1=0.43f; y1=0.548889f; x2=0.57f; y2=0.682222f; }
	else if (!strcmp(btnName, "spe2") || !strcmp(btnName, "bg5_sp")) { x1=0.43f; y1=0.678889f; x2=0.57f; y2=0.812222f; }

	snprintf(cmd, sizeof(cmd), "touch_addbutton \"%s\" \"%s\" \"\" %f %f %f %f 255 255 255 255 6\n", 
		btnName, texturePath, x1, y1, x2, y2);
	CLIENT_COMMAND(pPlayer->edict(), cmd);
}

bool CSPB_HandleUICommand(CBasePlayer *pPlayer, const char *pcmd)
{
	if (FStrEq(pcmd, "next_prim"))
	{
		if (g_iNumActivePrimary > 0)
		{
			pPlayer->m_iMenuPrimIdx = (pPlayer->m_iMenuPrimIdx + 1) % g_iNumActivePrimary;
			CSPB_UpdateTouchButton(pPlayer, "bg5_p", g_ActivePrimaryWeapons[pPlayer->m_iMenuPrimIdx]);
			CSPB_UpdateTouchButton(pPlayer, "prim2", g_ActivePrimaryWeapons[pPlayer->m_iMenuPrimIdx]);
		}
		return true;
	}
	else if (FStrEq(pcmd, "prev_prim"))
	{
		if (g_iNumActivePrimary > 0)
		{
			pPlayer->m_iMenuPrimIdx = (pPlayer->m_iMenuPrimIdx - 1);
			if (pPlayer->m_iMenuPrimIdx < 0) pPlayer->m_iMenuPrimIdx = g_iNumActivePrimary - 1;
			CSPB_UpdateTouchButton(pPlayer, "bg5_p", g_ActivePrimaryWeapons[pPlayer->m_iMenuPrimIdx]);
			CSPB_UpdateTouchButton(pPlayer, "prim2", g_ActivePrimaryWeapons[pPlayer->m_iMenuPrimIdx]);
		}
		return true;
	}
	else if (FStrEq(pcmd, "next_sec"))
	{
		if (g_iNumActiveSecondary > 0)
		{
			pPlayer->m_iMenuSecIdx = (pPlayer->m_iMenuSecIdx + 1) % g_iNumActiveSecondary;
			CSPB_UpdateTouchButton(pPlayer, "bg5_s", g_ActiveSecondaryWeapons[pPlayer->m_iMenuSecIdx]);
			CSPB_UpdateTouchButton(pPlayer, "sec2", g_ActiveSecondaryWeapons[pPlayer->m_iMenuSecIdx]);
		}
		return true;
	}
	else if (FStrEq(pcmd, "prev_sec"))
	{
		if (g_iNumActiveSecondary > 0)
		{
			pPlayer->m_iMenuSecIdx = (pPlayer->m_iMenuSecIdx - 1);
			if (pPlayer->m_iMenuSecIdx < 0) pPlayer->m_iMenuSecIdx = g_iNumActiveSecondary - 1;
			CSPB_UpdateTouchButton(pPlayer, "bg5_s", g_ActiveSecondaryWeapons[pPlayer->m_iMenuSecIdx]);
			CSPB_UpdateTouchButton(pPlayer, "sec2", g_ActiveSecondaryWeapons[pPlayer->m_iMenuSecIdx]);
		}
		return true;
	}
	else if (FStrEq(pcmd, "next_melee"))
	{
		if (g_iNumActiveMelee > 0)
		{
			pPlayer->m_iMenuMeleeIdx = (pPlayer->m_iMenuMeleeIdx + 1) % g_iNumActiveMelee;
			CSPB_UpdateTouchButton(pPlayer, "bg5_m", g_ActiveMeleeWeapons[pPlayer->m_iMenuMeleeIdx]);
			CSPB_UpdateTouchButton(pPlayer, "melee2", g_ActiveMeleeWeapons[pPlayer->m_iMenuMeleeIdx]);
		}
		return true;
	}
	else if (FStrEq(pcmd, "prev_melee"))
	{
		if (g_iNumActiveMelee > 0)
		{
			pPlayer->m_iMenuMeleeIdx = (pPlayer->m_iMenuMeleeIdx - 1);
			if (pPlayer->m_iMenuMeleeIdx < 0) pPlayer->m_iMenuMeleeIdx = g_iNumActiveMelee - 1;
			CSPB_UpdateTouchButton(pPlayer, "bg5_m", g_ActiveMeleeWeapons[pPlayer->m_iMenuMeleeIdx]);
			CSPB_UpdateTouchButton(pPlayer, "melee2", g_ActiveMeleeWeapons[pPlayer->m_iMenuMeleeIdx]);
		}
		return true;
	}
	else if (FStrEq(pcmd, "next_exp"))
	{
		if (g_iNumActiveGrenade > 0)
		{
			pPlayer->m_iMenuExpIdx = (pPlayer->m_iMenuExpIdx + 1) % g_iNumActiveGrenade;
			CSPB_UpdateTouchButton(pPlayer, "bg5_e", g_ActiveGrenadeWeapons[pPlayer->m_iMenuExpIdx]);
			CSPB_UpdateTouchButton(pPlayer, "exp2", g_ActiveGrenadeWeapons[pPlayer->m_iMenuExpIdx]);
		}
		return true;
	}
	else if (FStrEq(pcmd, "prev_exp"))
	{
		if (g_iNumActiveGrenade > 0)
		{
			pPlayer->m_iMenuExpIdx = (pPlayer->m_iMenuExpIdx - 1);
			if (pPlayer->m_iMenuExpIdx < 0) pPlayer->m_iMenuExpIdx = g_iNumActiveGrenade - 1;
			CSPB_UpdateTouchButton(pPlayer, "bg5_e", g_ActiveGrenadeWeapons[pPlayer->m_iMenuExpIdx]);
			CSPB_UpdateTouchButton(pPlayer, "exp2", g_ActiveGrenadeWeapons[pPlayer->m_iMenuExpIdx]);
		}
		return true;
	}
	else if (FStrEq(pcmd, "next_spe"))
	{
		if (g_iNumActiveSpecial > 0)
		{
			pPlayer->m_iMenuSpeIdx = (pPlayer->m_iMenuSpeIdx + 1) % g_iNumActiveSpecial;
			CSPB_UpdateTouchButton(pPlayer, "bg5_sp", g_ActiveSpecialWeapons[pPlayer->m_iMenuSpeIdx]);
			CSPB_UpdateTouchButton(pPlayer, "spe2", g_ActiveSpecialWeapons[pPlayer->m_iMenuSpeIdx]);
		}
		return true;
	}
	else if (FStrEq(pcmd, "prev_spe"))
	{
		if (g_iNumActiveSpecial > 0)
		{
			pPlayer->m_iMenuSpeIdx = (pPlayer->m_iMenuSpeIdx - 1);
			if (pPlayer->m_iMenuSpeIdx < 0) pPlayer->m_iMenuSpeIdx = g_iNumActiveSpecial - 1;
			CSPB_UpdateTouchButton(pPlayer, "bg5_sp", g_ActiveSpecialWeapons[pPlayer->m_iMenuSpeIdx]);
			CSPB_UpdateTouchButton(pPlayer, "spe2", g_ActiveSpecialWeapons[pPlayer->m_iMenuSpeIdx]);
		}
		return true;
	}
	else if (FStrEq(pcmd, "close_inventory") || FStrEq(pcmd, "ok_buy"))
	{
		// Save pending choices for all 5 loadout slots
		if (g_iNumActivePrimary > 0 && pPlayer->m_iMenuPrimIdx >= 0 && pPlayer->m_iMenuPrimIdx < g_iNumActivePrimary)
			strncpy(pPlayer->m_szPendingPrimary, g_ActivePrimaryWeapons[pPlayer->m_iMenuPrimIdx], 63);
		if (g_iNumActiveSecondary > 0 && pPlayer->m_iMenuSecIdx >= 0 && pPlayer->m_iMenuSecIdx < g_iNumActiveSecondary)
			strncpy(pPlayer->m_szPendingSecondary, g_ActiveSecondaryWeapons[pPlayer->m_iMenuSecIdx], 63);
		if (g_iNumActiveMelee > 0 && pPlayer->m_iMenuMeleeIdx >= 0 && pPlayer->m_iMenuMeleeIdx < g_iNumActiveMelee)
			strncpy(pPlayer->m_szPendingMelee, g_ActiveMeleeWeapons[pPlayer->m_iMenuMeleeIdx], 63);
		if (g_iNumActiveGrenade > 0 && pPlayer->m_iMenuExpIdx >= 0 && pPlayer->m_iMenuExpIdx < g_iNumActiveGrenade)
			strncpy(pPlayer->m_szPendingGrenade, g_ActiveGrenadeWeapons[pPlayer->m_iMenuExpIdx], 63);
		if (g_iNumActiveSpecial > 0 && pPlayer->m_iMenuSpeIdx >= 0 && pPlayer->m_iMenuSpeIdx < g_iNumActiveSpecial)
			strncpy(pPlayer->m_szPendingSpecial, g_ActiveSpecialWeapons[pPlayer->m_iMenuSpeIdx], 63);
		
		ClientPrint(pPlayer->pev, HUD_PRINTCENTER, "Loadout Tersimpan. Senjata diberikan saat Respawn.");
		return true;
	}
	else if (FStrEq(pcmd, "special_attack") || FStrEq(pcmd, "specialattack") || FStrEq(pcmd, "special"))
	{
		if (pPlayer->m_pActiveItem != nullptr)
		{
			const char *curWpn = pPlayer->m_pActiveItem->pszName();
			if (!Q_stricmp(curWpn, "weapon_oa93"))
			{
				pPlayer->SelectItem("weapon_oa93_dual");
				return true;
			}
			else if (!Q_stricmp(curWpn, "weapon_oa93_dual"))
			{
				pPlayer->SelectItem("weapon_oa93");
				return true;
			}
			else if (!Q_stricmp(curWpn, "weapon_kriss_sv"))
			{
				pPlayer->SelectItem("weapon_kriss_sv_dual");
				return true;
			}
			else if (!Q_stricmp(curWpn, "weapon_kriss_sv_dual"))
			{
				pPlayer->SelectItem("weapon_kriss_sv");
				return true;
			}
			else if (!Q_stricmp(curWpn, "weapon_kriss_sv_crb"))
			{
				pPlayer->SelectItem("weapon_kriss_sv_dual_crb");
				return true;
			}
			else if (!Q_stricmp(curWpn, "weapon_kriss_sv_dual_crb"))
			{
				pPlayer->SelectItem("weapon_kriss_sv_crb");
				return true;
			}
			else if (!Q_stricmp(curWpn, "weapon_kriss_sv_silence"))
			{
				pPlayer->SelectItem("weapon_kriss_sv_dual_silence");
				return true;
			}
			else if (!Q_stricmp(curWpn, "weapon_kriss_sv_dual_silence"))
			{
				pPlayer->SelectItem("weapon_kriss_sv_silence");
				return true;
			}
			else if (!Q_stricmp(curWpn, "weapon_t77"))
			{
				pPlayer->SelectItem("weapon_t77_dual");
				return true;
			}
			else if (!Q_stricmp(curWpn, "weapon_t77_dual"))
			{
				pPlayer->SelectItem("weapon_t77");
				return true;
			}
			else
			{
				CBasePlayerWeapon *pWpn = (CBasePlayerWeapon *)pPlayer->m_pActiveItem;
				if (pWpn)
					pWpn->SecondaryAttack();
				return true;
			}
		}
		return true;
	}

	return false;
}
