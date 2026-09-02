/***
*
*	Copyright (c) 1996-2002, Valve LLC. All rights reserved.
*	
*	This product contains software technology licensed from Id 
*	Software, Inc. ("Id Technology").  Id Technology (c) 1996 Id Software, Inc. 
*	All Rights Reserved.
*
*   Use, distribution, and modification of this source code and/or resulting
*   object code is restricted to non-commercial enhancements to products from
*   Valve LLC.  All other use, distribution, or modification is prohibited
*   without written permission from Valve LLC.
*
****/
//
// death notice
//
#include "hud.h"
#include "cl_util.h"
#include "parsemsg.h"

#include <string.h>
#include <stdio.h>
#include "draw_util.h"

#include "triangleapi.h"

float color[3];

DECLARE_MESSAGE( m_DeathNotice, DeathMsg )

enum DrawBgType
{
	DB_NONE, 
	DB_KILL,
	DB_DEATH
};

struct DeathNoticeItem 
{
	char szKiller[MAX_PLAYER_NAME_LENGTH*2];
	char szVictim[MAX_PLAYER_NAME_LENGTH*2];
	int iId;	// the index number of the associated sprite
	bool bSuicide;
	bool bTeamKill;
	bool bNonPlayerKill;
	float flDisplayTime;
	float *KillerColor;
	float *VictimColor;
	int iHeadShotId;

	DrawBgType DrawBg;
};

#define MAX_DEATHNOTICES	4
static int DEATHNOTICE_DISPLAY_TIME = 6;
static int KILLEFFECT_DISPLAY_TIME = 4;
static int KILLICON_DISPLAY_TIME = 1;

#define DEATHNOTICE_TOP		32

DeathNoticeItem rgDeathNoticeList[ MAX_DEATHNOTICES + 1 ];

int CHudDeathNotice :: Init( void )
{
	gHUD.AddHudElem( this );

	HOOK_MESSAGE( DeathMsg );

	hud_deathnotice_time = CVAR_CREATE( "hud_deathnotice_time", "6", 0 );
	m_iFlags = HUD_DRAW;

	return 1;
}

static float piercingTime; 
static float PIERCINGTIME_EFFECT = 0.20f;


void CHudDeathNotice::Reset(void)
{
	m_killNums = 0;
	m_multiKills = 0;
	m_showIcon = false;
	m_showKill = false;
	m_iconIndex = 0;
	m_killEffectTime = 0;
	m_killIconTime = 0;
piercingTime = 0;

}

void CHudDeathNotice :: InitHUDData( void )
{
	memset( rgDeathNoticeList, 0, sizeof(rgDeathNoticeList) );
}


int CHudDeathNotice :: VidInit( void )
{
	m_HUD_d_skull = gHUD.GetSpriteIndex( "d_skull" );
	m_HUD_d_headshot = gHUD.GetSpriteIndex("d_headshot");

	m_KM_Number0 = gHUD.GetSpriteIndex("KM_Number0");
	m_KM_Number1 = gHUD.GetSpriteIndex("KM_Number1");
	m_KM_Number2 = gHUD.GetSpriteIndex("KM_Number2");
	m_KM_Number3 = gHUD.GetSpriteIndex("KM_Number3");
	m_KM_KillText = gHUD.GetSpriteIndex("KM_KillText");
	m_KM_Icon_Head = gHUD.GetSpriteIndex("KM_Icon_Head");
	m_KM_Icon_Knife = gHUD.GetSpriteIndex("KM_Icon_knife");
	m_KM_Icon_Frag = gHUD.GetSpriteIndex("KM_Icon_Frag");

	R_InitTexture(m_killBg[1], "gfx/billflx/death/ann_center");
	R_InitTexture(m_deathBg[1], "gfx/billflx/death/ann_center");
	R_InitTexture(m_ann_hs[0], "gfx/billflx/death/ann_headshot");

	return 1;
}

void CHudDeathNotice::Shutdown(void)
{
	std::fill(std::begin(m_killBg), std::end(m_killBg), nullptr);
	std::fill(std::begin(m_deathBg), std::end(m_deathBg), nullptr);
}

int CHudDeathNotice :: Draw( float flTime )
{
	int x, y, r, g, b, i;

	for( i = 0; i < MAX_DEATHNOTICES; i++ )
	{
		if ( rgDeathNoticeList[i].iId == 0 )
			break;  // we've gone through them all

		if ( rgDeathNoticeList[i].flDisplayTime < flTime )
		{ // display time has expired
			// remove the current item from the list
			memmove( &rgDeathNoticeList[i], &rgDeathNoticeList[i+1], sizeof(DeathNoticeItem) * (MAX_DEATHNOTICES - i) );
			i--;  // continue on the next item;  stop the counter getting incremented
			continue;
		}

		rgDeathNoticeList[i].flDisplayTime = min( rgDeathNoticeList[i].flDisplayTime, flTime + DEATHNOTICE_DISPLAY_TIME );

		// Hide when scoreboard drawing. It will break triapi
		//if ( gViewPort && gViewPort->AllowedToPrintText() )
		//if ( !gHUD.m_iNoConsolePrint )
		{
			// Draw the death notice
			if( !g_iUser1 )
			{
				y = YRES(DEATHNOTICE_TOP) + 2 + (25 * i);  //!!!
			}
			else
			{
				y = ScreenHeight / 5 + 2 + (25 * i);
			}

			int id = (rgDeathNoticeList[i].iId == -1) ? m_HUD_d_skull : rgDeathNoticeList[i].iId;
			x = ScreenWidth - DrawUtils::ConsoleStringLen(rgDeathNoticeList[i].szVictim) - (gHUD.GetSpriteRect(id).right - gHUD.GetSpriteRect(id).left) - (YRES(5) * 3);
			if( rgDeathNoticeList[i].iHeadShotId )
				x -= gHUD.GetSpriteRect(m_HUD_d_headshot).right - gHUD.GetSpriteRect(m_HUD_d_headshot).left;

			int xMin = x, xOffset = 3;

			if (!rgDeathNoticeList[i].bSuicide)
				xMin -= (5 + DrawUtils::ConsoleStringLen(rgDeathNoticeList[i].szKiller));

			gEngfuncs.pTriAPI->RenderMode(kRenderTransTexture);
			gEngfuncs.pTriAPI->Color4ub(255, 255, 255, 255);

			SharedTexture (*DrawBg)[3] = nullptr;
			switch (rgDeathNoticeList[i].DrawBg)
			{
			case DB_KILL:
				DrawBg = &m_killBg; break;
			case DB_DEATH:
				DrawBg = &m_deathBg; break;
			default:
				DrawBg = nullptr; break;
			}

			// 1. Draw background FIRST (behind text and weapon)
			if (DrawBg && (*DrawBg)[1])
			{
				(*DrawBg)[1]->Bind();
				gEngfuncs.pTriAPI->Color4ub(255, 255, 255, 255);
				gEngfuncs.pTriAPI->RenderMode(kRenderTransAlpha);
				DrawUtils::Draw2DQuadScaled(xMin - 6, y, ScreenWidth - (YRES(5) * 3), y + 26);
			}

			// 2. Draw killer name
			x = xMin;
			if (!rgDeathNoticeList[i].bSuicide)
			{
				if (rgDeathNoticeList[i].KillerColor)
					DrawUtils::SetConsoleTextColor(rgDeathNoticeList[i].KillerColor[0], rgDeathNoticeList[i].KillerColor[1], rgDeathNoticeList[i].KillerColor[2]);

				x = DrawUtils::DrawConsoleString(x, y, rgDeathNoticeList[i].szKiller) + 5;
			}

			r = 255; g = 255; b = 255;
			if (rgDeathNoticeList[i].bTeamKill)
			{
				r = 10; g = 240; b = 10; // display it in sickly green
			}

			// 3. Draw death weapon
			int weaponX = x;
			int weaponW = gHUD.GetSpriteRect(id).right - gHUD.GetSpriteRect(id).left;
			int weaponH = gHUD.GetSpriteRect(id).bottom - gHUD.GetSpriteRect(id).top;

			SPR_Set(gHUD.GetSprite(id), r, g, b);
			SPR_DrawAdditive(0, weaponX, y, &gHUD.GetSpriteRect(id));

			x += weaponW + 6;

			// 4. Draw headshot icon OVERLAYING (menimpa) directly on top of the weapon icon
			if (rgDeathNoticeList[i].iHeadShotId && m_ann_hs[0])
			{
				m_ann_hs[0]->Bind();
				gEngfuncs.pTriAPI->RenderMode(kRenderTransAlpha);
				gEngfuncs.pTriAPI->Brightness(1.0f);
				gEngfuncs.pTriAPI->Color4ub(255, 255, 255, 255);

				int hsW = m_ann_hs[0]->w();
				int hsH = m_ann_hs[0]->h();
				if (hsW <= 0 || hsH <= 0) { hsW = 80; hsH = 26; }
				float hsScale = 22.0f / (float)hsH;
				int drawW = (int)(hsW * hsScale);
				int drawH = 22;

				int hsCenterX = weaponX + weaponW / 2;
				int hsCenterY = y + (weaponH > 0 ? (weaponH / 2) : 11);

				DrawUtils::Draw2DQuad(hsCenterX - drawW / 2, hsCenterY - drawH / 2, hsCenterX + drawW / 2, hsCenterY + drawH / 2);
			}

			// 5. Draw victim name
			if (!rgDeathNoticeList[i].bNonPlayerKill)
			{
				if (rgDeathNoticeList[i].VictimColor)
					DrawUtils::SetConsoleTextColor(rgDeathNoticeList[i].VictimColor[0], rgDeathNoticeList[i].VictimColor[1], rgDeathNoticeList[i].VictimColor[2]);
				x = DrawUtils::DrawConsoleString(x, y, rgDeathNoticeList[i].szVictim);
			}
		}
	}

	if (m_showKill)
	{
		m_killEffectTime = min(m_killEffectTime, gHUD.m_flTime + KILLEFFECT_DISPLAY_TIME);

		piercingTime = min(piercingTime, gHUD.m_flTime + PIERCINGTIME_EFFECT); ;

	}

	return 1;
}

int CHudDeathNotice::MsgFunc_DeathMsg(const char *pszName, int iSize, void *pbuf)
{
	BufferReader reader( pszName, pbuf, iSize );

	int killer = reader.ReadByte();
	int victim = reader.ReadByte();
	int headshot = reader.ReadByte();
	char killedwith[32];
	strcpy( killedwith, "d_" );
	strncat( killedwith, reader.ReadString(), 32 );

	int idx = gEngfuncs.GetLocalPlayer()->index;

	if (g_iUser1)
		return 1;

	int multiKills = 0;
	for (int j = 0; j < MAX_DEATHNOTICES; j++)
	{
		if (rgDeathNoticeList[j].iId == 0)
			break;

		if (rgDeathNoticeList[j].DrawBg == DB_KILL)
			multiKills++;
	}

	if (1/*cl_killmessage->value*/)
	{
		if (killer == idx && victim != idx)
		{
			m_killNums++;
			m_showIcon = false;

			// mass
			if (!strcmp(killedwith, "d_grenade") || !strcmp(killedwith, "d_m3") || !strcmp(killedwith, "d_m1887_w") || !strcmp(killedwith, "d_m1887") || !strcmp(killedwith, "d_spas_15"))
			{
				// mass_time = TRUE;
			}
			else if (!strcmp(killedwith, "d_zombie_s"))
			{
				ClientCmd("spk vox/haha");
				// mass_time = TRUE;
			}
			else
			{
				// mass_time = FALSE;
			}

			// ch slugger 
			if (!strcmp(killedwith, "d_knife") || !strcmp(killedwith, "d_arabian_sword") || !strcmp(killedwith, "d_amok") || !strcmp(killedwith, "d_butterfly") || !strcmp(killedwith, "d_candy_cane") || !strcmp(killedwith, "d_combat") || !strcmp(killedwith, "d_dual_knife") || !strcmp(killedwith, "d_fangblade") || !strcmp(killedwith, "d_brass_knuckle") ||!strcmp(killedwith, "d_mini_axe") || !strcmp(killedwith, "d_ice") || !strcmp(killedwith, "d_karambit") || !strcmp(killedwith, "d_keris") || !strcmp(killedwith, "d_knifebone") || !strcmp(killedwith, "d_saber"))
			{
				gHUD.slugger_kill = TRUE;
			}
			else
			{
				gHUD.slugger_kill = FALSE;
			}

			// gunner
			if (!strcmp(killedwith, "d_k5") || !strcmp(killedwith, "d_bow") || !strcmp(killedwith, "d_colt_python") || !strcmp(killedwith, "d_deagle") || !strcmp(killedwith, "d_deagle_dual") || !strcmp(killedwith, "d_dual_handgun") || !strcmp(killedwith, "d_taurus_raging_bull") || !strcmp(killedwith, "d_glock18") || !strcmp(killedwith, "d_usp"))
			{
				gHUD.special_gunner = TRUE;
			}
			else
			{
				gHUD.special_gunner = FALSE;
			}

			// bomb_shot
			if (!strcmp(killedwith, "d_grenade"))
			{
				gHUD.bomb_shot = TRUE;
			}
			else
			{
				gHUD.bomb_shot = FALSE;
			}

			// Simultaneous / Rapid Kill Tracking (MassKill 2..8, Piercing 2..8)
			static int s_simultaneousKillCount = 0;
			if (gHUD.m_flTime < piercingTime)
			{
				s_simultaneousKillCount++;
				if (s_simultaneousKillCount < 2) s_simultaneousKillCount = 2;
				if (s_simultaneousKillCount > 8) s_simultaneousKillCount = 8;

				/* if (mass_time)
				{
					gHUD.mass_kill = s_simultaneousKillCount;
					gHUD.piercing_shot = 0;
				}
				else
				{
					gHUD.piercing_shot = s_simultaneousKillCount;
					gHUD.mass_kill = 0;
				} */
			}
			else
			{
				s_simultaneousKillCount = 1;
				gHUD.piercing_shot = 0;
				gHUD.mass_kill = 0;
			}

			piercingTime = gHUD.m_flTime + PIERCINGTIME_EFFECT;
			m_multiKills = s_simultaneousKillCount;

			if (headshot)
			{
				if (gHUD.slugger_kill)
				{
					gHUD.m_KillEffect.last_frag_id = 9; // Frag_MeleeHS
					gHUD.m_KillEffect.m_pending_frag_id = 9;
				}
				else
				{
					gHUD.m_KillEffect.last_frag_id = 1; // Frag_Headshot
					gHUD.m_KillEffect.m_pending_frag_id = 1;
				}
			}
			else if (gHUD.slugger_kill)
			{
				gHUD.m_KillEffect.last_frag_id = 5; // Frag_Melee
				gHUD.m_KillEffect.m_pending_frag_id = 5;
			}
		}
	}

	int i;
	for ( i = 0; i < MAX_DEATHNOTICES; i++ )
	{
		if ( rgDeathNoticeList[i].iId == 0 )
			break;
	}
	if ( i == MAX_DEATHNOTICES )
	{ // move the rest of the list forward to make room for this item
		memmove( rgDeathNoticeList, rgDeathNoticeList+1, sizeof(DeathNoticeItem) * MAX_DEATHNOTICES );
		i = MAX_DEATHNOTICES - 1;
	}

	gHUD.m_Scoreboard.GetAllPlayersInfo();

	// Get the Killer's name
	const char *killer_name = NULL;
	if (killer > 0 && killer <= MAX_PLAYERS)
	{
		GetPlayerInfo(killer, &g_PlayerInfoList[killer]);
		killer_name = g_PlayerInfoList[killer].name;
	}

	if (!killer_name || !killer_name[0])
	{
		if (killer == idx)
			killer_name = gEngfuncs.pfnGetCvarString("name");
	}

	if (!killer_name || !killer_name[0])
	{
		if (killer > 0 && killer <= MAX_PLAYERS)
			killer_name = (killer == idx) ? "Player" : "Bot";
		else
			killer_name = "";
	}

	if (killer_name && killer_name[0])
	{
		rgDeathNoticeList[i].KillerColor = GetClientColor(killer);
		strncpy(rgDeathNoticeList[i].szKiller, killer_name, MAX_PLAYER_NAME_LENGTH);
		rgDeathNoticeList[i].szKiller[MAX_PLAYER_NAME_LENGTH - 1] = 0;
	}
	else
	{
		rgDeathNoticeList[i].szKiller[0] = 0;
	}

	// Get the Victim's name
	const char *victim_name = NULL;
	if (((char)victim) != -1 && victim > 0 && victim <= MAX_PLAYERS)
	{
		GetPlayerInfo(victim, &g_PlayerInfoList[victim]);
		victim_name = g_PlayerInfoList[victim].name;
	}

	if (!victim_name || !victim_name[0])
	{
		if (victim == idx)
			victim_name = gEngfuncs.pfnGetCvarString("name");
	}

	if (!victim_name || !victim_name[0])
	{
		if (victim > 0 && victim <= MAX_PLAYERS)
			victim_name = (victim == idx) ? "Player" : "Bot";
		else
			victim_name = "";
	}

	if (victim_name && victim_name[0])
	{
		rgDeathNoticeList[i].VictimColor = (victim > 0 && victim <= MAX_PLAYERS) ? GetClientColor(victim) : NULL;
		strncpy(rgDeathNoticeList[i].szVictim, victim_name, MAX_PLAYER_NAME_LENGTH);
		rgDeathNoticeList[i].szVictim[MAX_PLAYER_NAME_LENGTH - 1] = 0;
	}
	else
	{
		rgDeathNoticeList[i].szVictim[0] = 0;
	}

	// Is it a non-player object kill?
	if ( ((char)victim) == -1 )
	{
		rgDeathNoticeList[i].bNonPlayerKill = true;

		// Store the object's name in the Victim slot (skip the d_ bit)
		strncpy( rgDeathNoticeList[i].szVictim, killedwith+2, sizeof(killedwith) );
	}
	else
	{
		if ( killer == victim || killer == 0 )
			rgDeathNoticeList[i].bSuicide = true;

		if ( !strncmp( killedwith, "d_teammate", sizeof(killedwith)  ) )
			rgDeathNoticeList[i].bTeamKill = true;
	}

	rgDeathNoticeList[i].iHeadShotId = headshot;

	// Find the sprite in the list
	int spr = gHUD.GetSpriteIndex( killedwith );
	if (spr <= 0)
	{
		spr = (m_HUD_d_skull > 0 ? m_HUD_d_skull : -1);
	}

	rgDeathNoticeList[i].iId = spr;

	rgDeathNoticeList[i].flDisplayTime = gHUD.m_flTime + hud_deathnotice_time->value;


	if (victim == idx)
		rgDeathNoticeList[i].DrawBg = DB_DEATH;
	else if (killer == idx)
		rgDeathNoticeList[i].DrawBg = DB_KILL;
	else
		rgDeathNoticeList[i].DrawBg = DB_NONE;

	if (rgDeathNoticeList[i].bNonPlayerKill)
	{
		ConsolePrint( rgDeathNoticeList[i].szKiller );
		ConsolePrint( " killed a " );
		ConsolePrint( rgDeathNoticeList[i].szVictim );
		ConsolePrint( "\n" );
	}
	else
	{
		// record the death notice in the console
		if ( rgDeathNoticeList[i].bSuicide )
		{
			ConsolePrint( rgDeathNoticeList[i].szVictim );

			if ( !strncmp( killedwith, "d_world", sizeof(killedwith)  ) )
			{
				ConsolePrint( " died" );
			}
			else
			{
				ConsolePrint( " killed self" );
			}
		}
		else if ( rgDeathNoticeList[i].bTeamKill )
		{
			ConsolePrint( rgDeathNoticeList[i].szKiller );
			ConsolePrint( " killed his teammate " );
			ConsolePrint( rgDeathNoticeList[i].szVictim );
		}
		else
		{
			if( headshot )
				ConsolePrint( "*** ");
			ConsolePrint( rgDeathNoticeList[i].szKiller );
			ConsolePrint( " killed " );
			ConsolePrint( rgDeathNoticeList[i].szVictim );
		}

		if ( *killedwith && (*killedwith > 13 ) && strncmp( killedwith, "d_world", sizeof(killedwith) ) && !rgDeathNoticeList[i].bTeamKill )
		{
			if ( headshot )
				ConsolePrint(" with a headshot from ");
			else
				ConsolePrint(" with ");

			ConsolePrint( killedwith+2 ); // skip over the "d_" part
		}

		if( headshot ) ConsolePrint( " ***");
		ConsolePrint( "\n" );
	}

	return 1;
}




