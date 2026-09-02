#ifndef CSPB_UI_BACKEND_H
#define CSPB_UI_BACKEND_H
#pragma once

#define MAX_ACTIVE_WEAPONS 32

extern char g_ActivePrimaryWeapons[MAX_ACTIVE_WEAPONS][64];
extern char g_ActiveSecondaryWeapons[MAX_ACTIVE_WEAPONS][64];
extern char g_ActiveMeleeWeapons[MAX_ACTIVE_WEAPONS][64];
extern char g_ActiveGrenadeWeapons[MAX_ACTIVE_WEAPONS][64];
extern char g_ActiveSpecialWeapons[MAX_ACTIVE_WEAPONS][64];

extern int g_iNumActivePrimary;
extern int g_iNumActiveSecondary;
extern int g_iNumActiveMelee;
extern int g_iNumActiveGrenade;
extern int g_iNumActiveSpecial;

void CSPB_LoadActiveWeapons();
void CSPB_PrecacheActiveWeapons();
bool CSPB_HandleUICommand(class CBasePlayer *pPlayer, const char *pcmd);

#endif // CSPB_UI_BACKEND_H
