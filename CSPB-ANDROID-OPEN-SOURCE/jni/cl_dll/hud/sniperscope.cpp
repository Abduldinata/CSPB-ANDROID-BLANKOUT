/*
hud_overlays.cpp - HUD Overlays
Copyright (C) 2015-2016 a1batross

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 2 of the License, or (at
your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software Foundation,
Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

In addition, as a special exception, the author gives permission to
link the code of this program with the Half-Life Game Engine ("HL
Engine") and Modified Game Libraries ("MODs") developed by Valve,
L.L.C ("Valve").  You must obey the GNU General Public License in all
respects for all of the code used other than the HL Engine and MODs
from Valve.  If you modify this file, you may extend this exception
to your version of the file, but you are not obligated to do so.  If
you do not wish to do so, delete this exception statement from your
version.

*/
#include "hud.h"
#include "triangleapi.h"
#include "r_efx.h"
#include "cl_util.h"

#include "draw_util.h"

#include "stdio.h"
#include "stdlib.h"
#include "math.h"

#include "hud.h"
#include "cl_util.h"
#include "parsemsg.h"
#include <string.h>
#include "eventscripts.h"


#include "const.h"
#include "entity_state.h"
#include "cl_entity.h"
#include <string.h>
#include <stdio.h>
#include "event_api.h"
#include "com_weapons.h"


//#include "const/const_client.h"
#include "triangleapi.h"

enum WeaponIdType
{
	WEAPON_NONE,
	WEAPON_P228,
	WEAPON_GLOCK,
	WEAPON_SCOUT,
	WEAPON_HEGRENADE,
	WEAPON_XM1014,
	WEAPON_C4,
	WEAPON_MAC10,
	WEAPON_AUG,
	WEAPON_SMOKEGRENADE,
	WEAPON_ELITE,
	WEAPON_FIVESEVEN,
	WEAPON_UMP45,
	WEAPON_SG550,
	WEAPON_GALIL,
	WEAPON_FAMAS,
	WEAPON_USP,
	WEAPON_GLOCK18,
	WEAPON_AWP,
	WEAPON_MP5N,
	WEAPON_M249,
	WEAPON_M3,
	WEAPON_M4A1,
	WEAPON_TMP,
	WEAPON_G3SG1,
	WEAPON_FLASHBANG,
	WEAPON_DEAGLE,
	WEAPON_SG552,
	WEAPON_AK47,
	WEAPON_KNIFE,
	WEAPON_P90,
	WEAPON_SHIELDGUN = 99
};

DECLARE_MESSAGE(m_SniperScope, Reddot_Scope);
DECLARE_COMMAND(m_SniperScope, CommandActiveReddot);

DECLARE_MESSAGE(m_SniperScope, Eotech_Scope);
DECLARE_COMMAND(m_SniperScope, CommandActiveEotech);

DECLARE_MESSAGE(m_SniperScope, Acog_Scope);
DECLARE_COMMAND(m_SniperScope, CommandActiveAcog);

DECLARE_MESSAGE(m_SniperScope, Dot_l_Scope);
DECLARE_COMMAND(m_SniperScope, CommandActiveDot_l);

DECLARE_MESSAGE(m_SniperScope, Telescopic_Scope);
DECLARE_COMMAND(m_SniperScope, CommandActiveTelescopic);

DECLARE_MESSAGE(m_SniperScope, EotechCrb_Scope);
DECLARE_COMMAND(m_SniperScope, CommandActiveEotechCrb);

DECLARE_MESSAGE(m_SniperScope, EotechPandora_Scope);
DECLARE_COMMAND(m_SniperScope, CommandActiveEotechPandora);

DECLARE_MESSAGE(m_SniperScope, Sks_Scope);
DECLARE_COMMAND(m_SniperScope, CommandActiveSksScope);

DECLARE_MESSAGE(m_SniperScope, Sniper_Scope);
DECLARE_COMMAND(m_SniperScope, CommandActiveSniperScope);

DECLARE_MESSAGE(m_SniperScope, Azure_Scope);
DECLARE_COMMAND(m_SniperScope, CommandActiveAzureScope);

DECLARE_MESSAGE(m_SniperScope, EotechDot_Scope);
DECLARE_COMMAND(m_SniperScope, CommandActiveEotechDot);

DECLARE_MESSAGE(m_SniperScope, Disable_Scope);
DECLARE_COMMAND(m_SniperScope, CommandActiveDisableScope);

DECLARE_MESSAGE(m_SniperScope, Custom_Scope);
DECLARE_COMMAND(m_SniperScope, CommandActiveCustomScope);


void CHudSniperScope::UserCmd_CommandActiveCustomScope(void)
{
gHUD.disable_scope = FALSE;
active_Reddot = FALSE; 
active_Eotech = FALSE;
active_Acog = FALSE;
active_Dot_l = FALSE;
active_Telescopic = FALSE;
active_EotechCrb = FALSE;
active_EotechPandora = FALSE;
active_SksScope = FALSE;
active_SniperScope = FALSE;
active_AzureScope = FALSE;
active_EotechDot = FALSE;
active_CustomSight = TRUE; 
}


void CHudSniperScope::UserCmd_CommandActiveDisableScope(void)
{
gHUD.disable_scope = TRUE;
gHUD.reddot_scope = FALSE;

active_Reddot = FALSE; 
active_Eotech = FALSE;
active_Acog = FALSE;
active_Dot_l = FALSE;
active_Telescopic = FALSE;
active_EotechCrb = FALSE;
active_EotechPandora = FALSE;
active_SksScope = FALSE;
active_SniperScope = FALSE;
active_AzureScope = FALSE;
active_EotechDot = FALSE;
active_CustomSight = FALSE; 
}

void CHudSniperScope::UserCmd_CommandActiveReddot(void)
{
gHUD.disable_scope = FALSE;
gHUD.reddot_scope = TRUE;
active_Reddot = true;
active_Eotech= false;
active_Acog= false;
active_Dot_l= false;
active_Telescopic= false;
active_EotechCrb= false;
active_EotechPandora= false;
active_SksScope= false;
active_SniperScope= false;
active_AzureScope= false;
active_EotechDot= false;
active_CustomSight = false; 
}

void CHudSniperScope::UserCmd_CommandActiveEotech(void)
{
gHUD.disable_scope = FALSE;
active_Eotech = true;
active_Reddot= false; 
active_Acog= false;
active_Dot_l= false;
active_Telescopic= false;
active_EotechCrb= false;
active_EotechPandora= false;
active_SksScope= false;
active_SniperScope= false;
active_AzureScope= false;
active_EotechDot= false;
active_CustomSight = false; 
}

void CHudSniperScope::UserCmd_CommandActiveAcog(void)
{
gHUD.disable_scope = FALSE;
active_Acog = true;
active_Reddot= false; 
active_Eotech= false;
active_Dot_l= false;
active_Telescopic= false;
active_EotechCrb= false;
active_EotechPandora= false;
active_SksScope= false;
active_SniperScope= false;
active_AzureScope= false;
active_EotechDot= false;
active_CustomSight = false; 
}

void CHudSniperScope::UserCmd_CommandActiveDot_l(void)
{
gHUD.disable_scope = FALSE;
gHUD.reddot_scope = TRUE;
active_Dot_l = true;
active_Reddot= false; 
active_Eotech= false;
active_Acog= false;
active_Telescopic= false;
active_EotechCrb= false;
active_EotechPandora= false;
active_SksScope= false;
active_SniperScope= false;
active_AzureScope= false;
active_EotechDot= false;
active_CustomSight = false; 
}

void CHudSniperScope::UserCmd_CommandActiveTelescopic(void)
{
gHUD.disable_scope = FALSE;
active_Telescopic = true;
active_Reddot= false; 
active_Eotech= false;
active_Acog= false;
active_Dot_l= false;
active_EotechCrb= false;
active_EotechPandora= false;
active_SksScope= false;
active_SniperScope= false;
active_AzureScope= false;
active_EotechDot= false;
active_CustomSight = false; 
}

void CHudSniperScope::UserCmd_CommandActiveEotechCrb(void)
{
gHUD.disable_scope = FALSE;
active_EotechCrb = true;
active_Reddot= false; 
active_Eotech= false;
active_Acog= false;
active_Dot_l= false;
active_Telescopic= false;
active_EotechPandora= false;
active_SksScope= false;
active_SniperScope= false;
active_AzureScope= false;
active_EotechDot= false;
active_CustomSight = false; 
}

void CHudSniperScope::UserCmd_CommandActiveEotechPandora(void)
{
gHUD.disable_scope = FALSE;
active_EotechPandora = true;
active_Reddot= false; 
active_Eotech= false;
active_Acog= false;
active_Dot_l= false;
active_Telescopic= false;
active_EotechCrb= false;
active_SksScope= false;
active_SniperScope= false;
active_AzureScope= false;
active_EotechDot= false;
active_CustomSight = false; 
}

void CHudSniperScope::UserCmd_CommandActiveSksScope(void)
{
gHUD.disable_scope = FALSE;
active_SksScope = true;
active_Reddot= false; 
active_Eotech= false;
active_Acog= false;
active_Dot_l= false;
active_Telescopic= false;
active_EotechCrb= false;
active_EotechPandora= false;
active_SniperScope= false;
active_AzureScope= false;
active_EotechDot= false;
active_CustomSight = false; 
}

void CHudSniperScope::UserCmd_CommandActiveSniperScope(void)
{
gHUD.disable_scope = FALSE;
active_SniperScope = true;
active_Reddot= false; 
active_Eotech= false;
active_Acog= false;
active_Dot_l= false;
active_Telescopic= false;
active_EotechCrb= false;
active_EotechPandora= false;
active_SksScope= false;
active_AzureScope= false;
active_EotechDot= false;
active_CustomSight = false; 
}

void CHudSniperScope::UserCmd_CommandActiveAzureScope(void)
{
gHUD.disable_scope = FALSE;
active_AzureScope = true;
active_Reddot= false; 
active_Eotech= false;
active_Acog= false;
active_Dot_l= false;
active_Telescopic= false;
active_EotechCrb= false;
active_EotechPandora= false;
active_SksScope= false;
active_SniperScope= false;
active_EotechDot= false;
active_CustomSight = false; 
}

void CHudSniperScope::UserCmd_CommandActiveEotechDot(void)
{
gHUD.disable_scope = FALSE;
gHUD.reddot_scope = TRUE;
active_EotechDot = true;
active_Reddot= false; 
active_Eotech= false;
active_Acog= false;
active_Dot_l= false;
active_Telescopic= false;
active_EotechCrb= false;
active_EotechPandora= false;
active_SksScope= false;
active_SniperScope= false;
active_AzureScope= false;
active_CustomSight = false; 
}


int CHudSniperScope::MsgFunc_Disable_Scope(const char *pszName, int iSize, void *pbuf )
{
	UserCmd_CommandActiveDisableScope();
	return 1;
}

int CHudSniperScope::MsgFunc_Reddot_Scope(const char *pszName, int iSize, void *pbuf )
{
	UserCmd_CommandActiveReddot();
	return 1;
}
int CHudSniperScope::MsgFunc_Eotech_Scope(const char *pszName, int iSize, void *pbuf )
{
	UserCmd_CommandActiveEotech();
	return 1;
}
int CHudSniperScope::MsgFunc_Acog_Scope(const char *pszName, int iSize, void *pbuf )
{
	UserCmd_CommandActiveAcog();
	return 1;
}
int CHudSniperScope::MsgFunc_Dot_l_Scope(const char *pszName, int iSize, void *pbuf )
{
	UserCmd_CommandActiveDot_l();
	return 1;
}
int CHudSniperScope::MsgFunc_Telescopic_Scope(const char *pszName, int iSize, void *pbuf )
{
	UserCmd_CommandActiveTelescopic();
	return 1;
}
int CHudSniperScope::MsgFunc_EotechCrb_Scope(const char *pszName, int iSize, void *pbuf )
{
	UserCmd_CommandActiveEotechCrb();
	return 1;
}
int CHudSniperScope::MsgFunc_EotechPandora_Scope(const char *pszName, int iSize, void *pbuf )
{
	UserCmd_CommandActiveEotechPandora();
	return 1;
}
int CHudSniperScope::MsgFunc_Sks_Scope(const char *pszName, int iSize, void *pbuf )
{
	UserCmd_CommandActiveSksScope();
	return 1;
}
int CHudSniperScope::MsgFunc_Sniper_Scope(const char *pszName, int iSize, void *pbuf )
{
	UserCmd_CommandActiveSniperScope();
	return 1;
}
int CHudSniperScope::MsgFunc_Azure_Scope(const char *pszName, int iSize, void *pbuf )
{
	UserCmd_CommandActiveAzureScope();
	return 1;
}
int CHudSniperScope::MsgFunc_EotechDot_Scope(const char *pszName, int iSize, void *pbuf )
{
	UserCmd_CommandActiveEotechDot();
	return 1;
}
int CHudSniperScope::MsgFunc_Custom_Scope(const char *pszName, int iSize, void *pbuf )
{
	UserCmd_CommandActiveCustomScope();
	return 1;
}


int CHudSniperScope::Init()
{
	gHUD.AddHudElem(this);
	m_iFlags = HUD_DRAW;

HOOK_MESSAGE(Reddot_Scope);
HOOK_COMMAND("reddot_scope", CommandActiveReddot);
HOOK_COMMAND("Reddot_Scope", CommandActiveReddot);

HOOK_MESSAGE(Eotech_Scope);
HOOK_COMMAND("eotech_scope", CommandActiveEotech);
HOOK_COMMAND("Eotech_Scope", CommandActiveEotech);

HOOK_MESSAGE(Acog_Scope);
HOOK_COMMAND("acog_scope", CommandActiveAcog);
HOOK_COMMAND("Acog_Scope", CommandActiveAcog);

HOOK_MESSAGE(Dot_l_Scope);
HOOK_COMMAND("dot_l_scope", CommandActiveDot_l);
HOOK_COMMAND("Dot_l_Scope", CommandActiveDot_l);

HOOK_MESSAGE(Telescopic_Scope);
HOOK_COMMAND("telescopic_scope", CommandActiveTelescopic);
HOOK_COMMAND("Telescopic_Scope", CommandActiveTelescopic);

HOOK_MESSAGE(EotechCrb_Scope);
HOOK_COMMAND("eotechcrb_scope", CommandActiveEotechCrb);
HOOK_COMMAND("EotechCrb_Scope", CommandActiveEotechCrb);

HOOK_MESSAGE(EotechPandora_Scope);
HOOK_COMMAND("eotechpandora_scope", CommandActiveEotechPandora);
HOOK_COMMAND("EotechPandora_Scope", CommandActiveEotechPandora);

HOOK_MESSAGE(Sks_Scope);
HOOK_COMMAND("sks_scope", CommandActiveSksScope);
HOOK_COMMAND("Sks_Scope", CommandActiveSksScope);

HOOK_MESSAGE(Sniper_Scope);
HOOK_COMMAND("sniper_scope", CommandActiveSniperScope);
HOOK_COMMAND("Sniper_Scope", CommandActiveSniperScope);

HOOK_MESSAGE(Azure_Scope);
HOOK_COMMAND("azure_scope", CommandActiveAzureScope);
HOOK_COMMAND("Azure_Scope", CommandActiveAzureScope);

HOOK_MESSAGE(EotechDot_Scope);
HOOK_COMMAND("eotechdot_scope", CommandActiveEotechDot);
HOOK_COMMAND("EotechDot_Scope", CommandActiveEotechDot);

HOOK_MESSAGE(Disable_Scope);
HOOK_COMMAND("disable_scope", CommandActiveDisableScope);
HOOK_COMMAND("Disable_Scope", CommandActiveDisableScope);

HOOK_MESSAGE(Custom_Scope);
HOOK_COMMAND("custom_scope", CommandActiveCustomScope);
HOOK_COMMAND("Custom_Scope", CommandActiveCustomScope);
	return 1;
}

static void R_InitTextureScope(UniqueTexture &tex, const char *primaryPath, const char *fallbackPath = nullptr)
{
	R_InitTexture(tex, primaryPath);
	if (!tex && fallbackPath)
		R_InitTexture(tex, fallbackPath);
}

int CHudSniperScope::VidInit()
{
	// Optical sights (full frames and scopes when aiming)
	R_InitTextureScope(m_sight[0], "gfx/billflx/newsight/dotsight.png");
	R_InitTextureScope(m_sight[1], "gfx/billflx/newsight/eotech.png");
	R_InitTextureScope(m_sight[2], "gfx/billflx/newsight/holographic.png");
	R_InitTextureScope(m_sight[3], "gfx/billflx/newsight/acog.png");
	R_InitTextureScope(m_sight[4], "gfx/billflx/newsight/dotsight.png");
	R_InitTextureScope(m_sight[5], "gfx/billflx/newsight/acog+.png");
	R_InitTextureScope(m_sight[6], "gfx/billflx/newsight/eotech crb.png");
	R_InitTextureScope(m_sight[7], "gfx/billflx/newsight/holographic.png");
	R_InitTextureScope(m_sight[8], "gfx/billflx/newsight/sks.png");
	R_InitTextureScope(m_sight[9], "gfx/billflx/newsight/sniper.png");
	R_InitTextureScope(m_sight[10], "gfx/billflx/newsight/dotsight.png");
	R_InitTextureScope(m_sight[11], "gfx/billflx/newsight/azure.png");

	// Scoped Reticle Overlays (for scopes with hollow sight housings)
	R_InitTextureScope(m_reticleEotech, "gfx/billflx/crosshair/crosshair_eotech.png");
	R_InitTextureScope(m_reticleLaser, "gfx/billflx/crosshair/crosshair_laser.png");

	for (int i = 0; i < 50; i++)
	{
		char customPath[128];
		char fallbackPath[128];
		sprintf(customPath, "gfx/billflx/newsight/sight%d.png", i);
		sprintf(fallbackPath, "gfx/sight/custom/custom%d.png", i);
		R_InitTextureScope(m_CustomSight[i], customPath, fallbackPath);
	}

left = (ScreenWidth - ScreenHeight)/2;
right = left + ScreenHeight;
centerx = ScreenWidth/2;
centery = ScreenHeight/2;
	return 1;
}

int CHudSniperScope::Draw(float flTime)
{
	if (gHUD.m_iFOV >= 90 || gHUD.m_iFOV == 0)
	{
		gHUD.reddot_scope = FALSE;
		return 0;
	}

	const int idx = gEngfuncs.GetLocalPlayer()->index;
	if (g_PlayerExtraInfo[idx].dead == true)
		return 0;

	if (gHUD.disable_scope)
	{
		return 0;
	}

	gEngfuncs.pTriAPI->RenderMode(kRenderTransAlpha);
	gEngfuncs.pTriAPI->Brightness(1.0);
	gEngfuncs.pTriAPI->Color4ub(255, 255, 255, 255);

	bool anyActive = (active_CustomSight || active_AzureScope || active_Dot_l || active_Reddot ||
	                  active_Eotech || active_EotechDot || active_Acog || active_Telescopic ||
	                  active_EotechCrb || active_EotechPandora || active_SksScope || active_SniperScope);

	if (!anyActive && gHUD.m_Ammo.m_pWeapon)
	{
		int wid = gHUD.m_Ammo.m_pWeapon->iId;
		const char *wname = gHUD.m_Ammo.m_pWeapon->szName;
		WeaponScriptConfig cfg = GetWeaponScriptConfig(wname);

		if (!cfg.szSightTga.empty() && cfg.szSightTga != "None")
		{
			if (cfg.szSightTga.find("sniper.png") != std::string::npos)
				active_SniperScope = true;
			else if (cfg.szSightTga.find("sks.png") != std::string::npos)
				active_SksScope = true;
			else if (cfg.szSightTga.find("acog+.png") != std::string::npos)
				active_Telescopic = true;
			else if (cfg.szSightTga.find("acog.png") != std::string::npos)
				active_Acog = true;
			else if (cfg.szSightTga.find("eotech crb.png") != std::string::npos)
				active_EotechCrb = true;
			else if (cfg.szSightTga.find("eotech.png") != std::string::npos)
			{
				if (cfg.szSightCrosshairTga.find("crosshair_laser") != std::string::npos)
					active_EotechDot = true;
				else
					active_Eotech = true;
			}
			else if (cfg.szSightTga.find("dotsight.png") != std::string::npos)
				active_Reddot = true;
			else if (cfg.szSightTga.find("holographic.png") != std::string::npos)
				active_EotechPandora = true;
			else if (cfg.szSightTga.find("azure.png") != std::string::npos)
				active_AzureScope = true;
		}
		else if (cfg.szSightTga == "None")
		{
			// Explicitly no scope overlay (iron sight zoom / slash)
		}
		else
		{
			// Fallback by ID/Name
			if (wid == WEAPON_AWP || wid == WEAPON_SCOUT || wid == WEAPON_G3SG1 ||
			    strstr(wname, "awp") || strstr(wname, "cheytac") || strstr(wname, "m82a1") || strstr(wname, "tactilite") ||
			    strstr(wname, "kar98") || strstr(wname, "rangemaster") || strstr(wname, "pgm") || strstr(wname, "dragunov"))
			{
				active_SniperScope = true;
			}
			else if (strstr(wname, "sks"))
			{
				active_SksScope = true;
			}
			else if (strstr(wname, "crb"))
			{
				active_EotechCrb = true;
			}
			else if (wid == WEAPON_AUG || strstr(wname, "aug"))
			{
				active_EotechDot = true;
			}
			else if (strstr(wname, "groza") || strstr(wname, "p90"))
			{
				active_Reddot = true;
			}
			else if (strstr(wname, "mp7") || strstr(wname, "kriss") || strstr(wname, "famas") || strstr(wname, "oa93") || strstr(wname, "t77"))
			{
				active_Eotech = true;
			}
			else if (wid == WEAPON_SG552 || strstr(wname, "g36c") || strstr(wname, "m4a1") || strstr(wname, "sig") || strstr(wname, "pindad") || strstr(wname, "xm8") || strstr(wname, "sc2010"))
			{
				active_Acog = true;
			}
			else
			{
				active_EotechDot = true;
			}
		}
	}

	//custom 
	if (active_CustomSight)
	{
		int custom_idx = (int)gHUD.custom_scope_cmd->value;
		if (custom_idx >= 1 && custom_idx < 50)
		{
			if (m_CustomSight[custom_idx])
				m_CustomSight[custom_idx]->Bind();
			else
				gEngfuncs.Con_DPrintf("[TEXTURE] MISSING m_CustomSight[%d] bypassed\n", custom_idx);
		}

		DrawUtils::Draw2DQuad((ScreenWidth - ScreenHeight)/2, 0, (ScreenWidth - ScreenHeight)/2 + ScreenHeight, ScreenHeight);

		if (gHUD.custom_scope_cmd->value >= 40)
		{
			FillRGBABlend( 0, 0, (ScreenWidth - ScreenHeight) / 2 + 2, ScreenHeight, 0, 0, 0, 255 );
			FillRGBABlend( (ScreenWidth - ScreenHeight) / 2 - 2 + ScreenHeight, 0, (ScreenWidth - ScreenHeight) / 2 + 2, ScreenHeight, 0, 0, 0, 255 );
		}
		else if (gHUD.custom_scope_cmd->value >= 25)
		{
			FillRGBABlend( 0, 0, (ScreenWidth - ScreenHeight) / 2.005 + 2, ScreenHeight, 0, 0, 0, 170 );
			FillRGBABlend( (ScreenWidth - ScreenHeight) / 1.994 - 2 + ScreenHeight, 0, (ScreenWidth - ScreenHeight) / 2 + 2, ScreenHeight, 0, 0, 0, 170 );
		}
	}



//azure
if (active_AzureScope)
{
if (m_sight[11]) m_sight[11]->Bind(); else gEngfuncs.Con_DPrintf("[TEXTURE] MISSING m_sight[11] bypassed\n");
DrawUtils::Draw2DQuad((ScreenWidth - ScreenHeight)/2, 0, (ScreenWidth - ScreenHeight)/2 + ScreenHeight, ScreenHeight);
}

if (active_Dot_l)
{
if (m_sight[4]) m_sight[4]->Bind(); else gEngfuncs.Con_DPrintf("[TEXTURE] MISSING m_sight[4] bypassed\n");
DrawUtils::Draw2DQuad((ScreenWidth - ScreenHeight)/2, 0, (ScreenWidth - ScreenHeight)/2 + ScreenHeight, ScreenHeight);
}
//reddot
if (active_Reddot)
{
	if (m_sight[0]) {
		m_sight[0]->Bind();
		DrawUtils::Draw2DQuad((ScreenWidth - ScreenHeight)/2, 0, (ScreenWidth - ScreenHeight)/2 + ScreenHeight, ScreenHeight);
	}
	if (m_reticleLaser) {
		m_reticleLaser->Bind();
		DrawUtils::Draw2DQuad(centerx - 4, centery - 4, centerx + 4, centery + 4);
	}

	FillRGBABlend( 0, 0, (ScreenWidth - ScreenHeight) / 2.005 + 2, ScreenHeight, 0, 0, 0, 170 );
	FillRGBABlend( (ScreenWidth - ScreenHeight) / 1.994 - 2 + ScreenHeight, 0, (ScreenWidth - ScreenHeight) / 2 + 2, ScreenHeight, 0, 0, 0, 170 );
}

//eotech
if (active_Eotech)
{
	if (m_sight[1]) {
		m_sight[1]->Bind();
		DrawUtils::Draw2DQuad((ScreenWidth - ScreenHeight)/2, 0, (ScreenWidth - ScreenHeight)/2 + ScreenHeight, ScreenHeight);
	}
	if (m_reticleEotech) {
		m_reticleEotech->Bind();
		DrawUtils::Draw2DQuad((ScreenWidth - ScreenHeight)/2, 0, (ScreenWidth - ScreenHeight)/2 + ScreenHeight, ScreenHeight);
	}
}

//eotech_dot (AUG A3 / EOTech with Center Red Dot)
if (active_EotechDot)
{
	if (m_sight[1]) {
		m_sight[1]->Bind();
		DrawUtils::Draw2DQuad((ScreenWidth - ScreenHeight)/2, 0, (ScreenWidth - ScreenHeight)/2 + ScreenHeight, ScreenHeight);
	}
	if (m_reticleLaser) {
		m_reticleLaser->Bind();
		DrawUtils::Draw2DQuad(centerx - 4, centery - 4, centerx + 4, centery + 4);
	}
}

//acog (ACOG housing with Center Laser Dot)
if (active_Acog)
{
	if (m_sight[3]) {
		m_sight[3]->Bind();
		DrawUtils::Draw2DQuad((ScreenWidth - ScreenHeight)/2, 0, (ScreenWidth - ScreenHeight)/2 + ScreenHeight, ScreenHeight);
	}
	if (m_reticleLaser) {
		m_reticleLaser->Bind();
		DrawUtils::Draw2DQuad(centerx - 4, centery - 4, centerx + 4, centery + 4);
	}

	FillRGBABlend( 0, 0, (ScreenWidth - ScreenHeight) / 2.005 + 2, ScreenHeight, 0, 0, 0, 170 );
	FillRGBABlend( (ScreenWidth - ScreenHeight) / 1.994 - 2 + ScreenHeight, 0, (ScreenWidth - ScreenHeight) / 2 + 2, ScreenHeight, 0, 0, 0, 170 );
}

//telescopic (ACOG+ integrated reticle)
if (active_Telescopic)
{
	if (m_sight[5]) {
		m_sight[5]->Bind();
		DrawUtils::Draw2DQuad((ScreenWidth - ScreenHeight)/2, 0, (ScreenWidth - ScreenHeight)/2 + ScreenHeight, ScreenHeight);
	}

	FillRGBABlend( 0, 0, (ScreenWidth - ScreenHeight) / 2.005 + 2, ScreenHeight, 0, 0, 0, 170 );
	FillRGBABlend( (ScreenWidth - ScreenHeight) / 1.994 - 2 + ScreenHeight, 0, (ScreenWidth - ScreenHeight) / 2 + 2, ScreenHeight, 0, 0, 0, 170 );
}

//crb eotech (EOTech CRB housing with EOTech Reticle)
if (active_EotechCrb)
{
	if (m_sight[6]) {
		m_sight[6]->Bind();
		DrawUtils::Draw2DQuad((ScreenWidth - ScreenHeight)/2, 0, (ScreenWidth - ScreenHeight)/2 + ScreenHeight, ScreenHeight);
	}
	if (m_reticleEotech) {
		m_reticleEotech->Bind();
		DrawUtils::Draw2DQuad((ScreenWidth - ScreenHeight)/2, 0, (ScreenWidth - ScreenHeight)/2 + ScreenHeight, ScreenHeight);
	}
}

//eotechpandora (Holographic)
if (active_EotechPandora)
{
	if (m_sight[7]) {
		m_sight[7]->Bind();
		DrawUtils::Draw2DQuad((ScreenWidth - ScreenHeight)/2, 0, (ScreenWidth - ScreenHeight)/2 + ScreenHeight, ScreenHeight);
	}
}

//sks
if (active_SksScope)
{
	if (m_sight[8]) {
		m_sight[8]->Bind();
		DrawUtils::Draw2DQuad((ScreenWidth - ScreenHeight)/2, 0, (ScreenWidth - ScreenHeight)/2 + ScreenHeight, ScreenHeight);
	}

	FillRGBABlend( 0, 0, (ScreenWidth - ScreenHeight) / 2 + 2, ScreenHeight, 0, 0, 0, 255 );
	FillRGBABlend( (ScreenWidth - ScreenHeight) / 2 - 2 + ScreenHeight, 0, (ScreenWidth - ScreenHeight) / 2 + 2, ScreenHeight, 0, 0, 0, 255 );
}

//sniper
if (active_SniperScope)
{
	if (m_sight[9]) {
		m_sight[9]->Bind();
		DrawUtils::Draw2DQuad((ScreenWidth - ScreenHeight)/2, 0, (ScreenWidth - ScreenHeight)/2 + ScreenHeight, ScreenHeight);
	}

	FillRGBABlend( 0, 0, (ScreenWidth - ScreenHeight) / 2 + 2, ScreenHeight, 0, 0, 0, 255 );
	FillRGBABlend( (ScreenWidth - ScreenHeight) / 2 - 2 + ScreenHeight, 0, (ScreenWidth - ScreenHeight) / 2 + 2, ScreenHeight, 0, 0, 0, 255 );
}

//azure
if (active_AzureScope)
{
	if (m_sight[11]) {
		m_sight[11]->Bind();
		DrawUtils::Draw2DQuad((ScreenWidth - ScreenHeight)/2, 0, (ScreenWidth - ScreenHeight)/2 + ScreenHeight, ScreenHeight);
	}
	if (m_reticleLaser) {
		m_reticleLaser->Bind();
		DrawUtils::Draw2DQuad(centerx - 4, centery - 4, centerx + 4, centery + 4);
	}

	FillRGBABlend( 0, 0, (ScreenWidth - ScreenHeight) / 2.005 + 2, ScreenHeight, 0, 0, 0, 170 );
	FillRGBABlend( (ScreenWidth - ScreenHeight) / 1.994 - 2 + ScreenHeight, 0, (ScreenWidth - ScreenHeight) / 2 + 2, ScreenHeight, 0, 0, 0, 170 );
}

	gEngfuncs.pTriAPI->RenderMode(kRenderNormal);
	gEngfuncs.pTriAPI->Color4ub(255, 255, 255, 255);
	return 0;
}
