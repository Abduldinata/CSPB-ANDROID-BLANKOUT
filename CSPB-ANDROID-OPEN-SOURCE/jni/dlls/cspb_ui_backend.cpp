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

int g_iNumActivePrimary = 0;
int g_iNumActiveSecondary = 0;
int g_iNumActiveMelee = 0;

void CSPB_LoadActiveWeapons()
{
	g_iNumActivePrimary = 0;
	g_iNumActiveSecondary = 0;
	g_iNumActiveMelee = 0;

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
		return;
	}

	char *pData = pFile;
	char line[256];
	int mode = 0; // 1 = PRIMARY, 2 = SECONDARY, 3 = MELEE

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
	}

	if (bIsMalloc)
		free(pFile);
	else
		FREE_FILE(pFile);
	
	ALERT(at_console, "[CSPB] Loaded %d Primary, %d Secondary, %d Melee active weapons.\n", 
		g_iNumActivePrimary, g_iNumActiveSecondary, g_iNumActiveMelee);
}

void CSPB_PrecacheActiveWeapons()
{
	for (int i = 0; i < g_iNumActivePrimary; i++)
		UTIL_PrecacheOtherWeapon(g_ActivePrimaryWeapons[i]);
	for (int i = 0; i < g_iNumActiveSecondary; i++)
		UTIL_PrecacheOtherWeapon(g_ActiveSecondaryWeapons[i]);
	for (int i = 0; i < g_iNumActiveMelee; i++)
		UTIL_PrecacheOtherWeapon(g_ActiveMeleeWeapons[i]);
}

void CSPB_UpdateTouchButton(CBasePlayer *pPlayer, const char *btnName, const char *weaponName)
{
	// Resolve texture path. If weapon_m4a1, it's usually gfx/billflx/weapons/v_m4a1 or weapon_m4a1.
	// The user's touch cfg has: touch_addbutton "prim2" "gfx/billflx/weapons/wpn_empty"
	// So we need to remove the button and add it again with the correct weapon icon.
	
	// Format is typically gfx/billflx/weapons/<classname> or maybe v_<weapon>.
	// Wait, the standard PB icons in this mod usually use the classname directly if they match,
	// e.g. gfx/billflx/weapons/weapon_ak47. Let's use weaponName directly.
	char texturePath[128];
	snprintf(texturePath, sizeof(texturePath), "gfx/billflx/weapons/%s", weaponName);

	// Remove old button
	char cmd[256];
	snprintf(cmd, sizeof(cmd), "touch_removebutton \"%s\"\n", btnName);
	CLIENT_COMMAND(pPlayer->edict(), cmd);

	// Add new button
	// Note: We need coordinates. In the user's config:
	// prim: 0.450000 0.177778 0.550000 0.266667
	// sec: 0.450000 0.311111 0.550000 0.400000
	// melee: 0.450000 0.441111 0.550000 0.530000
	float x1, y1, x2, y2;
	if (!strcmp(btnName, "prim2")) { x1=0.45f; y1=0.177778f; x2=0.55f; y2=0.266667f; }
	else if (!strcmp(btnName, "sec2")) { x1=0.45f; y1=0.311111f; x2=0.55f; y2=0.4f; }
	else if (!strcmp(btnName, "melee2")) { x1=0.45f; y1=0.441111f; x2=0.55f; y2=0.53f; }
	else return; // unknown button

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
			CSPB_UpdateTouchButton(pPlayer, "prim2", g_ActivePrimaryWeapons[pPlayer->m_iMenuPrimIdx]);
		}
		return true;
	}
	else if (FStrEq(pcmd, "next_sec"))
	{
		if (g_iNumActiveSecondary > 0)
		{
			pPlayer->m_iMenuSecIdx = (pPlayer->m_iMenuSecIdx + 1) % g_iNumActiveSecondary;
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
			CSPB_UpdateTouchButton(pPlayer, "sec2", g_ActiveSecondaryWeapons[pPlayer->m_iMenuSecIdx]);
		}
		return true;
	}
	else if (FStrEq(pcmd, "next_melee"))
	{
		if (g_iNumActiveMelee > 0)
		{
			pPlayer->m_iMenuMeleeIdx = (pPlayer->m_iMenuMeleeIdx + 1) % g_iNumActiveMelee;
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
			CSPB_UpdateTouchButton(pPlayer, "melee2", g_ActiveMeleeWeapons[pPlayer->m_iMenuMeleeIdx]);
		}
		return true;
	}
	else if (FStrEq(pcmd, "close_inventory"))
	{
		// Save pending choices
		if (g_iNumActivePrimary > 0)
			strncpy(pPlayer->m_szPendingPrimary, g_ActivePrimaryWeapons[pPlayer->m_iMenuPrimIdx], 63);
		if (g_iNumActiveSecondary > 0)
			strncpy(pPlayer->m_szPendingSecondary, g_ActiveSecondaryWeapons[pPlayer->m_iMenuSecIdx], 63);
		if (g_iNumActiveMelee > 0)
			strncpy(pPlayer->m_szPendingMelee, g_ActiveMeleeWeapons[pPlayer->m_iMenuMeleeIdx], 63);
		
		ClientPrint(pPlayer->pev, HUD_PRINTCENTER, "Loadout Tersimpan. Senjata diberikan saat Respawn.");
		return true;
	}

	return false;
}
