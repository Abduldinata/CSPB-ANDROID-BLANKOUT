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

#include "port.h"

#include "extdll.h"
#include "util.h"
#include "cbase.h"
#include "monsters.h"

#define PLAYER_H
#include "weapons.h"
#undef PLAYER_H

#include "nodes.h"
#include "player.h"

#include "usercmd.h"
#include "../../public/entity_state.h"
#include "demo_api.h"
#include "pm_defs.h"
#include "event_api.h"
#include "r_efx.h"

#include "hud_iface.h"
#include "com_weapons.h"
#include "demo.h"

#include "cl_entity.h"

extern "C"
{
#include "pm_shared.h"
}

#include "wpn_shared.h"

#include "bte_weapons.h"

#include "minmax.h"

#if defined(__ANDROID__) && defined(CSPB_ENABLE_PRED_TRACE)
#include <android/log.h>
#define PRED_TAG "CSPB_PRED"
#define PRED_RAW(msg) __android_log_write( ANDROID_LOG_INFO, PRED_TAG, msg )
#define PRED_PTR(label, p) __android_log_print( ANDROID_LOG_INFO, PRED_TAG, "%s=%p", label, (void *)(p) )
#define PRED_INT(label, v) __android_log_print( ANDROID_LOG_INFO, PRED_TAG, "%s=%d", label, (int)(v) )
#define PRED_U32(label, v) __android_log_print( ANDROID_LOG_INFO, PRED_TAG, "%s=%u", label, (unsigned int)(v) )
#define PRED_STR(label, v) __android_log_print( ANDROID_LOG_INFO, PRED_TAG, "%s=%s", label, (v) ? (v) : "(null)" )
#else
#define PRED_RAW(msg)
#define PRED_PTR(label, p)
#define PRED_INT(label, v)
#define PRED_U32(label, v)
#define PRED_STR(label, v)
#endif

extern globalvars_t *gpGlobals;
extern int g_iUser1;
extern bool g_bGlockBurstMode;
extern int g_rseq;
extern int g_gaitseq;
extern Vector g_clorg;
extern Vector g_clang;

// Pool of client side entities/entvars_t
static entvars_t	ev[ 32 ];
static int			num_ents = 0;
static bool			g_cspb_hud_client_weapon_init = false;
static bool			s_cspb_hud_weapon_slot_used[ MAX_WEAPONS ] = { false };

// The entity we'll use to represent the local client
static CBasePlayer	player;

// Local version of game .dll global variables ( time, etc. )
static globalvars_t	Globals = { };

// ref from bte_weapons.cpp
CBasePlayerWeapon *g_pWpns[ MAX_WEAPONS ];


// CS Weapon placeholder entities
static CAK47 g_AK47;
static CAUG g_AUG;
static CAWP g_AWP;
static CC4 g_C4;
static CDEAGLE g_DEAGLE;
static CFlashbang g_Flashbang;
static CGLOCK18 g_GLOCK18;
static CHEGrenade g_HEGrenade;
static CKnife g_Knife;
static CM3 g_M3;
static CM4A1 g_M4A1;
static CP90 g_P90;
static CSCOUT g_SCOUT;
static CSG550 g_SG550;
static CSmokeGrenade g_SmokeGrenade;
static CUSP g_USP;

int    g_iWeaponFlags;
bool   g_bInBombZone;
int    g_iFreezeTimeOver;
bool   g_bHoldingShield;
bool   g_bHoldingKnife;
float  g_flPlayerSpeed;
int    g_iPlayerFlags;
Vector g_vPlayerVelocity;

/*
======================
AlertMessage

Print debug messages to console
======================
*/
void AlertMessage( ALERT_TYPE atype, const char *szFmt, ... )
{
	va_list		argptr;
	static char	string[1024];

	va_start (argptr, szFmt);
	vsprintf (string, szFmt,argptr);
	va_end (argptr);

	gEngfuncs.Con_Printf( "cl:  " );
	gEngfuncs.Con_Printf( string );
}

/*
=====================
HUD_PrepEntity

Links the raw entity to an entvars_s holder.  If a player is passed in as the owner, then
we set up the m_pPlayer field.
=====================
*/

void HUD_PrepEntityNamed( CBaseEntity *pEntity, CBasePlayer *pWeaponOwner, const char *debugName )
{
	const int localWpnsCapacity = (int)( sizeof( g_pWpns ) / sizeof( g_pWpns[0] ) );
	const int itemInfoCapacity = (int)( sizeof( CBasePlayerItem::ItemInfoArray ) / sizeof( CBasePlayerItem::ItemInfoArray[0] ) );

	PRED_RAW( "HUD_PrepEntity enter" );
	PRED_STR( "HUD_PrepEntity weapon label", debugName );
	PRED_PTR( "HUD_PrepEntity entity", pEntity );
	PRED_PTR( "HUD_PrepEntity owner", pWeaponOwner );
	PRED_INT( "HUD_PrepEntity num_ents_before", num_ents );

	memset( &ev[ num_ents ], 0, sizeof( entvars_t ) );
	pEntity->pev = &ev[ num_ents++ ];
	PRED_PTR( "HUD_PrepEntity pev", pEntity->pev );
	PRED_INT( "HUD_PrepEntity num_ents_after_alloc", num_ents );

#if defined(__ANDROID__) && defined(__aarch64__)
	if( g_cspb_hud_client_weapon_init && pWeaponOwner )
	{
		PRED_RAW( "HUD_PrepEntity skip Precache during HUD client weapon init android arm64 aggressive" );
		PRED_RAW( "HUD_PrepEntity skip Spawn during HUD client weapon init android arm64 aggressive" );
	}
	else
	{
		PRED_RAW( "HUD_PrepEntity before Precache" );
		pEntity->Precache();
		PRED_RAW( "HUD_PrepEntity after Precache" );
		PRED_RAW( "HUD_PrepEntity before Spawn" );
		pEntity->Spawn();
		PRED_RAW( "HUD_PrepEntity after Spawn" );
	}
#else
	PRED_RAW( "HUD_PrepEntity before Precache" );
	pEntity->Precache();
	PRED_RAW( "HUD_PrepEntity after Precache" );
	PRED_RAW( "HUD_PrepEntity before Spawn" );
	pEntity->Spawn();
	PRED_RAW( "HUD_PrepEntity after Spawn" );
#endif

	if ( pWeaponOwner )
	{
		ItemInfo info;
		memset( &info, 0, sizeof( ItemInfo ) );

		((CBasePlayerWeapon *)pEntity)->m_pPlayer = pWeaponOwner;

		PRED_RAW( "HUD_PrepEntity before GetItemInfo" );
		((CBasePlayerWeapon *)pEntity)->GetItemInfo( &info );
		PRED_RAW( "HUD_PrepEntity after GetItemInfo" );
		PRED_INT( "HUD_PrepEntity info.iId", info.iId );
		PRED_INT( "HUD_PrepEntity MAX_WEAPONS", MAX_WEAPONS );
		PRED_INT( "HUD_PrepEntity g_pWpns capacity", localWpnsCapacity );
		PRED_INT( "HUD_PrepEntity ItemInfoArray capacity", itemInfoCapacity );
		PRED_PTR( "HUD_PrepEntity cast weapon pointer", (CBasePlayerWeapon *)pEntity );
		PRED_PTR( "HUD_PrepEntity info.pszName", info.pszName );

		if ( info.iId < 0 || info.iId >= MAX_WEAPONS || info.iId >= localWpnsCapacity || info.iId >= itemInfoCapacity )
		{
			PRED_RAW( "HUD_PrepEntity invalid weapon id skip" );
			PRED_RAW( "HUD_PrepEntity before HUD_PrepEntity leave" );
			PRED_RAW( "HUD_PrepEntity leave" );
			return;
		}

#if defined(__ANDROID__) && defined(__aarch64__)
		if( g_cspb_hud_client_weapon_init && ( !info.pszName || !info.pszName[0] ))
		{
			PRED_RAW( "HUD_PrepEntity empty pszName skip ItemInfoArray registration during HUD client weapon init android arm64 diagnostic" );
			PRED_RAW( "HUD_PrepEntity before HUD_PrepEntity leave" );
			PRED_RAW( "HUD_PrepEntity leave" );
			return;
		}

		if( g_cspb_hud_client_weapon_init && info.iId == WEAPON_KNIFE )
		{
			PRED_RAW( "HUD_PrepEntity skip g_Knife registration during HUD client weapon init android arm64 diagnostic" );
			PRED_RAW( "HUD_PrepEntity before HUD_PrepEntity leave" );
			PRED_RAW( "HUD_PrepEntity leave" );
			return;
		}

		if( g_cspb_hud_client_weapon_init && ( ( debugName && !strcmp( debugName, "g_Flashbang" )) || info.iId == 25 ) )
		{
			PRED_RAW( "HUD_PrepEntity skip g_Flashbang registration during HUD client weapon init android arm64 diagnostic" );
			PRED_RAW( "HUD_PrepEntity before HUD_PrepEntity leave" );
			PRED_RAW( "HUD_PrepEntity leave" );
			return;
		}

		if( g_cspb_hud_client_weapon_init && s_cspb_hud_weapon_slot_used[ info.iId ] )
		{
			PRED_RAW( "HUD_PrepEntity duplicate weapon slot skip" );
			PRED_RAW( "HUD_PrepEntity before HUD_PrepEntity leave" );
			PRED_RAW( "HUD_PrepEntity leave" );
			return;
		}
#endif

		PRED_RAW( "HUD_PrepEntity before g_pWpns write" );
		g_pWpns[ info.iId ] = (CBasePlayerWeapon *)pEntity;
		PRED_RAW( "HUD_PrepEntity after g_pWpns write" );
		PRED_RAW( "HUD_PrepEntity before ItemInfoArray decision" );

#if defined(__ANDROID__) && defined(__aarch64__)
		if( g_cspb_hud_client_weapon_init && s_cspb_hud_weapon_slot_used[ info.iId ] )
		{
			PRED_RAW( "HUD_PrepEntity skip ItemInfoArray write duplicate slot during HUD client weapon init android arm64 diagnostic" );
		}
		else
#endif
		{
			PRED_RAW( "HUD_PrepEntity before ItemInfoArray write" );
			CBasePlayerItem::ItemInfoArray[ info.iId ] = info;
			PRED_RAW( "HUD_PrepEntity after ItemInfoArray write" );
		}

#if defined(__ANDROID__) && defined(__aarch64__)
		if( g_cspb_hud_client_weapon_init )
			s_cspb_hud_weapon_slot_used[ info.iId ] = true;
#endif
	}

	PRED_RAW( "HUD_PrepEntity before HUD_PrepEntity leave" );
	PRED_RAW( "HUD_PrepEntity leave" );
}

void HUD_PrepEntity( CBaseEntity *pEntity, CBasePlayer *pWeaponOwner )
{
	HUD_PrepEntityNamed( pEntity, pWeaponOwner, "(unknown)" );
}

/*
=====================
CBaseEntity :: Killed

If weapons code "kills" an entity, just set its effects to EF_NODRAW
=====================
*/
void CBaseEntity :: Killed( entvars_t *pevAttacker, int iGib )
{
	pev->effects |= EF_NODRAW;
}

/*
=====================
CBasePlayerWeapon :: DefaultReload
=====================
*/
BOOL CBasePlayerWeapon :: DefaultReload( int iClipSize, int iAnim, float fDelay, int body )
{
	if( !m_pPlayer->m_pActiveItem )
		return FALSE;

	if (m_pPlayer->m_rgAmmo[m_iPrimaryAmmoType] <= 0)
		return FALSE;

	int j = min(iClipSize - m_iClip, player.m_rgAmmo[m_iPrimaryAmmoType]);

	if (j == 0)
		return FALSE;

	m_pPlayer->m_flNextAttack = UTIL_WeaponTimeBase() + fDelay;

	//!!UNDONE -- reload sound goes here !!!
	SendWeaponAnim( iAnim, UseDecrement() );

	m_fInReload = TRUE;

	m_flTimeWeaponIdle = UTIL_WeaponTimeBase() + fDelay + 0.5f;
	return TRUE;
}

BOOL CBasePlayerWeapon :: DefaultReloadQuick( int iClipSize, int iAnim, float fDelay, int body )
{
	if( !m_pPlayer->m_pActiveItem )
		return FALSE;

	if (m_pPlayer->m_rgAmmo[m_iPrimaryAmmoType] <= 0)
		return FALSE;

	int j = min(iClipSize - m_iClip, player.m_rgAmmo[m_iPrimaryAmmoType]);

	if (j == 0)
		return FALSE;

	m_pPlayer->m_flNextAttack = UTIL_WeaponTimeBase() + fDelay;

	//!!UNDONE -- reload sound goes here !!!
	SendWeaponAnim( iAnim, UseDecrement() );

	m_fInReload = TRUE;

	m_flTimeWeaponIdle = UTIL_WeaponTimeBase() + fDelay + 0.5f;
	return TRUE;
}

/*
=====================
CBasePlayerWeapon :: CanDeploy
=====================
*/
BOOL CBasePlayerWeapon :: CanDeploy( void )
{
#if 0
	BOOL bHasAmmo = 0;

	if ( !pszAmmo1() )
	{
		// this weapon doesn't use ammo, can always deploy.
		return TRUE;
	}

	if ( pszAmmo1() )
	{
		bHasAmmo |= (m_pPlayer->m_rgAmmo[m_iPrimaryAmmoType] != 0);
	}
	if ( pszAmmo2() )
	{
		bHasAmmo |= (m_pPlayer->m_rgAmmo[m_iSecondaryAmmoType] != 0);
	}
	if (m_iClip > 0)
	{
		bHasAmmo |= 1;
	}
	if (!bHasAmmo)
	{
		return FALSE;
	}

	return TRUE;
#else
	return TRUE;
#endif
}
/*
=====================
CBasePlayer :: HasShield

=====================
*/
bool CBasePlayer::HasShield()
{
	return g_bHoldingShield;
}

/*
=====================
CBasePlayerWeapon::HasSecondaryAttack()

=====================
*/
bool CBasePlayerWeapon::HasSecondaryAttack()
{
	if (g_bHoldingShield == false)
	{
		if (m_iId == WEAPON_AK47 || m_iId ==  WEAPON_M3 || m_iId == WEAPON_DEAGLE || m_iId == WEAPON_P90 || m_iId == WEAPON_C4)
			return false;
	}

	return true;
}

void CBasePlayerWeapon::FireRemaining(int &shotsFired, float &shootTime, BOOL isGlock18)
{
	m_iClip--;

	if (m_iClip < 0)
	{
		m_iClip = 0;
		shotsFired = 3;
		shootTime = 0;
		return;
	}

	UTIL_MakeVectors(m_pPlayer->pev->v_angle + m_pPlayer->pev->punchangle);

	Vector vecDir;

	if (isGlock18)
	{
		vecDir = m_pPlayer->FireBullets3(m_pPlayer->GetGunPosition(), gpGlobals->v_forward, 0.05, 8192, 1, BULLET_PLAYER_9MM, 18, 0.9, m_pPlayer->pev, TRUE, m_pPlayer->random_seed);
		PLAYBACK_EVENT_FULL(FEV_NOTHOST, ENT(m_pPlayer->pev), m_usFireGlock18, 0, (float *)&g_vecZero, (float *)&g_vecZero, vecDir.x, vecDir.y, (int)(m_pPlayer->pev->punchangle.x * 10000), (int)(m_pPlayer->pev->punchangle.y * 10000), m_iClip != 0, FALSE);
		m_pPlayer->ammo_9mm--;
	}
	else
	{
		vecDir = m_pPlayer->FireBullets3(m_pPlayer->GetGunPosition(), gpGlobals->v_forward, m_fBurstSpread, 8192, 2, BULLET_PLAYER_556MM, 30, 0.96, m_pPlayer->pev, TRUE, m_pPlayer->random_seed);
		/*PLAYBACK_EVENT_FULL(FEV_NOTHOST, ENT(m_pPlayer->pev), m_usFireFamas, 0, (float *)&g_vecZero, (float *)&g_vecZero, vecDir.x, vecDir.y, (int)(m_pPlayer->pev->punchangle.x * 10000000), (int)(m_pPlayer->pev->punchangle.y * 10000000), m_iClip != 0, FALSE);*/
		m_pPlayer->ammo_556nato--;
	}

	m_pPlayer->pev->effects |= EF_MUZZLEFLASH;
#ifndef CLIENT_DLL
	m_pPlayer->SetAnimation(PLAYER_ATTACK1);
#endif
	shotsFired++;

	if (shotsFired == 3)
		shootTime = 0;
	else
		shootTime = gpGlobals->time + 0.1;
}

bool CBasePlayerWeapon::ShieldSecondaryFire(int up_anim, int down_anim)
{
	if (m_pPlayer->HasShield() == false)
		return false;

	if (m_iWeaponState & WPNSTATE_SHIELD_DRAWN)
	{
		m_iWeaponState &= ~WPNSTATE_SHIELD_DRAWN;
		SendWeaponAnim(down_anim, UseDecrement() != FALSE);
		strncpy(m_pPlayer->m_szAnimExtention, "shieldgun", sizeof(m_pPlayer->m_szAnimExtention));
		m_fMaxSpeed = 250;
		m_pPlayer->m_bShieldDrawn = false;
	}
	else
	{
		m_iWeaponState |= WPNSTATE_SHIELD_DRAWN;
		SendWeaponAnim(up_anim, UseDecrement() != FALSE);
		strncpy(m_pPlayer->m_szAnimExtention, "shielded", sizeof(m_pPlayer->m_szAnimExtention));
		m_fMaxSpeed = 180;
		m_pPlayer->m_bShieldDrawn = true;
	}

#ifndef CLIENT_DLL
	m_pPlayer->UpdateShieldCrosshair((m_iWeaponState & WPNSTATE_SHIELD_DRAWN) ? true : false);
	m_pPlayer->ResetMaxSpeed();
#endif
	m_flNextSecondaryAttack = UTIL_WeaponTimeBase() + 0.4;
	m_flNextPrimaryAttack = UTIL_WeaponTimeBase() + 0.4;
	m_flTimeWeaponIdle = UTIL_WeaponTimeBase() + 0.6;
	return true;
}

void CBasePlayerWeapon::KickBack(float up_base, float lateral_base, float up_modifier, float lateral_modifier, float up_max, float lateral_max, int direction_change)
{

}

void CBasePlayerWeapon::SetPlayerShieldAnim(void)
{
	if (m_pPlayer->HasShield() == true)
	{
		if (m_iWeaponState & WPNSTATE_SHIELD_DRAWN)
			strncpy(m_pPlayer->m_szAnimExtention, "shield", sizeof(m_pPlayer->m_szAnimExtention));
		else
			strncpy(m_pPlayer->m_szAnimExtention, "shieldgun", sizeof(m_pPlayer->m_szAnimExtention));
	}
}

void CBasePlayerWeapon::ResetPlayerShieldAnim(void)
{
	if (m_pPlayer->HasShield() == true)
	{
		if (m_iWeaponState & WPNSTATE_SHIELD_DRAWN)
			strncpy(m_pPlayer->m_szAnimExtention, "shieldgun", sizeof(m_pPlayer->m_szAnimExtention));
	}
}

/*
=====================
CBasePlayerWeapon :: DefaultDeploy

=====================
*/
BOOL CBasePlayerWeapon :: DefaultDeploy( const char *szViewModel, const char *szWeaponModel, int iAnim, const char *szAnimExt, int skiplocal )
{
	if ( !CanDeploy() )
		return FALSE;

	return TRUE;
}

/*
=====================
CBasePlayerWeapon :: PlayEmptySound

=====================
*/
BOOL CBasePlayerWeapon :: PlayEmptySound( void )
{
#if 0
	if (m_iPlayEmptySound)
	{
		switch (m_iId)
		{
		case WEAPON_USP:
		case WEAPON_GLOCK18:
		case WEAPON_DEAGLE:
			HUD_PlaySound("weapons/dryfire_pistol.wav", 0.8);
			break;
		default:
			HUD_PlaySound("weapons/dryfire_rifle.wav",  0.8);
			break;
		}
	}
#endif
	return 0;
}

/*
=====================
CBasePlayerWeapon :: ResetEmptySound

=====================
*/
void CBasePlayerWeapon :: ResetEmptySound( void )
{
	m_iPlayEmptySound = 1;
}

/*
=====================
CBasePlayerWeapon::Holster

Put away weapon
=====================
*/
void CBasePlayerWeapon::Holster( int skiplocal /* = 0 */ )
{
	m_fInReload = FALSE; // cancel any reload in progress.
	m_pPlayer->pev->viewmodel = 0;
}



/*
=====================
CBasePlayerWeapon::SendWeaponAnim

Animate weapon model
=====================
*/
void CBasePlayerWeapon::SendWeaponAnim( int iAnim, int skiplocal )
{
m_pPlayer->pev->weaponanim = iAnim;
HUD_SendWeaponAnim( iAnim, m_iId, 0, 0 );
}


void CBasePlayerWeapon::RetireWeapon()
{
	// TODO: Implement
	//UTIL_GetNextBestWeapon( m_pPlayer, this );
}

Vector CBaseEntity::FireBullets3 ( Vector vecSrc, Vector vecDirShooting, float flSpread, float flDistance, int iPenetration, int iBulletType, int iDamage, float flRangeModifier, entvars_t *pevAttacker, bool bPistol, int shared_rand )
{
	float x, y, z;

	if ( pevAttacker )
	{
		x = UTIL_SharedRandomFloat(shared_rand, -0.5, 0.5) + UTIL_SharedRandomFloat(shared_rand + 1, -0.5, 0.5);
		y = UTIL_SharedRandomFloat(shared_rand + 2, -0.5, 0.5) + UTIL_SharedRandomFloat(shared_rand + 3, -0.5, 0.5);
	}
	else
	{
		do
		{
			x = RANDOM_FLOAT(-0.5, 0.5) + RANDOM_FLOAT(-0.5, 0.5);
			y = RANDOM_FLOAT(-0.5, 0.5) + RANDOM_FLOAT(-0.5, 0.5);
			z = x * x + y * y;
		}
		while (z > 1);
	}

	return Vector(x * flSpread, y * flSpread, 0);
}
/*
=====================
CBasePlayerWeapon::ItemPostFrame

Handles weapon firing, reloading, etc.
=====================
*/
void CBasePlayerWeapon::ItemPostFrame( void )
{
	int button = m_pPlayer->pev->button;

	if (!HasSecondaryAttack())
		button &= ~IN_ATTACK2;

	if (m_flGlock18Shoot != 0)
	{
		m_iClip--;
		if( m_iClip < 0 )
		{
			m_iClip = m_iGlock18ShotsFired = 0;
		}
		FireRemaining(m_iGlock18ShotsFired, m_flGlock18Shoot, TRUE);
	}
	else if (gpGlobals->time > m_flFamasShoot && m_flFamasShoot != 0)
	{
		m_iClip--;
		if( m_iClip < 0 )
		{
			m_iClip = m_iFamasShotsFired = 0;
		}
		FireRemaining(m_iFamasShotsFired, m_flFamasShoot, FALSE);
	}

	if (m_flNextPrimaryAttack <= UTIL_WeaponTimeBase() )
	{
		if (m_pPlayer->m_bResumeZoom)
		{
			m_pPlayer->pev->fov = m_pPlayer->m_iFOV = m_pPlayer->m_iLastZoom;

			if (m_pPlayer->m_iFOV == m_pPlayer->m_iLastZoom)
			{
				m_pPlayer->m_bResumeZoom = false;
				// viewmodel hide is implemented elsewhere
			}
		}
	}

	if ( m_pPlayer->HasShield() )
	{
		if (m_fInReload && m_pPlayer->pev->button & IN_ATTACK2)
		{
			SecondaryAttack();
			m_pPlayer->pev->button &= ~IN_ATTACK2;
			m_fInReload = FALSE;
			m_pPlayer->m_flNextAttack = UTIL_WeaponTimeBase();
		}
	}

	if ((m_fInReload) && m_pPlayer->m_flNextAttack <= UTIL_WeaponTimeBase())
	{
		int j = min(iMaxClip() - m_iClip, m_pPlayer->m_rgAmmo[m_iPrimaryAmmoType]);

		m_iClip += j;
		m_pPlayer->m_rgAmmo[m_iPrimaryAmmoType] -= j;
		m_fInReload = FALSE;
	}

	if ((button & IN_ATTACK2) && m_flNextSecondaryAttack <= UTIL_WeaponTimeBase())
	{
		if (pszAmmo2() && !m_pPlayer->m_rgAmmo[SecondaryAmmoIndex()])
			m_fFireOnEmpty = TRUE;

		SecondaryAttack();
		m_pPlayer->pev->button &= ~IN_ATTACK2;
	}
	else if ((m_pPlayer->pev->button & IN_ATTACK) && m_flNextPrimaryAttack <= UTIL_WeaponTimeBase())
	{
		if ((!m_iClip && pszAmmo1()) || (iMaxClip() == WEAPON_NOCLIP && !m_pPlayer->m_rgAmmo[PrimaryAmmoIndex()]))
			m_fFireOnEmpty = TRUE;

		if (m_pPlayer->m_bCanShoot == true)
			PrimaryAttack();
	}
	else if (m_pPlayer->pev->button & IN_RELOAD && iMaxClip() != WEAPON_NOCLIP && !m_fInReload)
	{
		if (m_flNextPrimaryAttack < UTIL_WeaponTimeBase())
		{
			if (m_flFamasShoot == 0 && m_flGlock18Shoot == 0)
			{
				if (!(m_iWeaponState & WPNSTATE_SHIELD_DRAWN))
					Reload();
			}
		}
	}
	else if (!(button & (IN_ATTACK | IN_ATTACK2)))
	{
		if (m_bDelayFire == true)
		{
			m_bDelayFire = false;

			if (m_iShotsFired > 15)
				m_iShotsFired = 15;

			m_flDecreaseShotsFired = gpGlobals->time + 0.4;
		}

		m_fFireOnEmpty = FALSE;

		if (m_iId != WEAPON_USP && m_iId != WEAPON_GLOCK18 && m_iId != WEAPON_DEAGLE)
		{
			if (m_iShotsFired > 0)
			{
				if (gpGlobals->time > m_flDecreaseShotsFired)
				{
					m_iShotsFired--;
					m_flDecreaseShotsFired = gpGlobals->time + 0.0225;
				}
			}
		}
		else
			m_iShotsFired = 0;


		if (!(m_iWeaponState & WPNSTATE_SHIELD_DRAWN))
		{

			if (m_iClip == 0 && !(iFlags() & ITEM_FLAG_NOAUTORELOAD)
					&& m_flNextPrimaryAttack < UTIL_WeaponTimeBase())
			{
				if (m_flFamasShoot == 0 && m_flGlock18Shoot == 0)
				{
					Reload();
					return;
				}
			}
		}

		WeaponIdle();
		return;
	}
}

/*
=====================
CBasePlayer::SelectLastItem

=====================
*/
void CBasePlayer::SelectLastItem(void)
{
	if (!m_pLastItem)
	{
		return;
	}

	if ( m_pActiveItem && !m_pActiveItem->CanHolster() )
	{
		return;
	}

	if (m_pActiveItem)
		m_pActiveItem->Holster( );

	CBasePlayerItem *pTemp = m_pActiveItem;
	m_pActiveItem = m_pLastItem;
	m_pLastItem = pTemp;
	m_pActiveItem->Deploy( );
}

/*
=====================
CBasePlayer::Killed

=====================
*/
void CBasePlayer::Killed( entvars_t *pevAttacker, int iGib )
{
	// Holster weapon immediately, to allow it to cleanup
	if ( m_pActiveItem )
		 m_pActiveItem->Holster( );
}

/*
=====================
CBasePlayer::Spawn

=====================
*/
void CBasePlayer::Spawn( void )
{
	if (m_pActiveItem)
		m_pActiveItem->Deploy( );
}

Vector CBasePlayer::GetGunPosition()
{
	Vector origin = pev->origin;
	Vector view_ofs;

	gEngfuncs.pEventAPI->EV_LocalPlayerViewheight(view_ofs);

	return origin + view_ofs;
}

/*
=====================
UTIL_TraceLine

Don't actually trace, but act like the trace didn't hit anything.
=====================
*/
void UTIL_TraceLine( const Vector &vecStart, const Vector &vecEnd, IGNORE_MONSTERS igmon, edict_t *pentIgnore, TraceResult *ptr )
{
	memset( ptr, 0, sizeof( *ptr ) );
#if 0
	static float flLastFraction = 1.0f;

	if( g_runfuncs )
	{
		Vector vStart = vecStart, vEnd = vecEnd;
		pmtrace_t pmtrace;

		gEngfuncs.pEventAPI->EV_SetTraceHull( 0 );
		gEngfuncs.pEventAPI->EV_PlayerTrace( vStart, vEnd, 0, -1, &pmtrace );
		flLastFraction = ptr->flFraction = pmtrace.fraction;
		ptr->vecEndPos = pmtrace.endpos;
	}
	else
	{
		ptr->flFraction = flLastFraction;
	}
#else
	ptr->flFraction = 1.0f;
#endif
}

char UTIL_TextureHit(TraceResult *ptr, Vector vecSrc, Vector vecEnd)
{
	char chTextureType;
	float rgfl1[3], rgfl2[3];
	const char *pTextureName;
	char szbuffer[64];
	CBaseEntity *pEntity;

	if( ptr->pHit == NULL )
		return CHAR_TEX_FLESH;

	pEntity = CBaseEntity::Instance(ptr->pHit);

	if (pEntity && pEntity->Classify() != CLASS_NONE && pEntity->Classify() != CLASS_MACHINE)
		return CHAR_TEX_FLESH;

	vecSrc.CopyToArray(rgfl1);
	vecEnd.CopyToArray(rgfl2);

	if (pEntity)
		pTextureName = TRACE_TEXTURE(ENT(pEntity->pev), rgfl1, rgfl2);
	else
		pTextureName = TRACE_TEXTURE(ENT(0), rgfl1, rgfl2);

	if (pTextureName)
	{
		if (*pTextureName == '-' || *pTextureName == '+')
			pTextureName += 2;

		if (*pTextureName == '{' || *pTextureName == '!' || *pTextureName == '~' || *pTextureName == ' ')
			pTextureName++;

		strncpy(szbuffer, pTextureName, sizeof(szbuffer));
		szbuffer[CBTEXTURENAMEMAX - 1] = 0;
		chTextureType = PM_FindTextureType(szbuffer);
	}
	else
		chTextureType = 0;

	return chTextureType;
}

CBaseEntity *UTIL_PlayerByIndex(int playerIndex)
{
	CBaseEntity *pPlayer = NULL;

	if (playerIndex > 0 && playerIndex <= gpGlobals->maxClients)
	{
		edict_t *pPlayerEdict = INDEXENT(playerIndex);

		if (pPlayerEdict && !pPlayerEdict->free)
			pPlayer = CBaseEntity::Instance(pPlayerEdict);
	}

	return pPlayer;
}

void UTIL_MakeVectors( const Vector &vec )
{
	gEngfuncs.pfnAngleVectors( vec, gpGlobals->v_forward, gpGlobals->v_right, gpGlobals->v_up );
}


/*
=====================
CBasePlayerWeapon::PrintState

For debugging, print out state variables to log file
=====================
*/
/*void CBasePlayerWeapon::PrintState( void )
{
	COM_Log( "c:\\hl.log", "%.4f ", gpGlobals->time );
	COM_Log( "c:\\hl.log", "%.4f ", m_pPlayer->m_flNextAttack );
	COM_Log( "c:\\hl.log", "%.4f ", m_flNextPrimaryAttack );
	COM_Log( "c:\\hl.log", "%.4f ", m_flTimeWeaponIdle - gpGlobals->time);
	COM_Log( "c:\\hl.log", "%i ", m_iClip );
}*/

long RandomLong( long a, long b )
{
	return gEngfuncs.pfnRandomLong( a, b );
}

byte *HUD_LoadFileForMe( const char *name, int *pLength )
{
	return (byte *)gEngfuncs.COM_LoadFile( (char *)name, 5, pLength );
}

void HUD_FreeFile( void *buffer )
{
	gEngfuncs.COM_FreeFile( buffer );
}

/*
=====================
HUD_InitClientWeapons

Set up weapons, player and functions needed to run weapons code client-side.
=====================
*/
void HUD_InitClientWeapons( void )
{
	static int initialized = 0;
	static bool s_loggedInitAbi = false;

	PRED_RAW( "HUD_InitClientWeapons enter" );
	PRED_INT( "HUD_InitClientWeapons initialized", initialized );
	PRED_INT( "HUD_InitClientWeapons num_ents", num_ents );

	if ( initialized )
	{
		PRED_RAW( "HUD_InitClientWeapons already initialized return" );
		return;
	}

	initialized = 1;
	memset( s_cspb_hud_weapon_slot_used, 0, sizeof( s_cspb_hud_weapon_slot_used ) );

	if( !s_loggedInitAbi )
	{
		s_loggedInitAbi = true;
		PRED_INT( "HUD_InitClientWeapons MAX_WEAPONS", MAX_WEAPONS );
		PRED_INT( "HUD_InitClientWeapons sizeof local_state_t", (int)sizeof( local_state_t ));
		PRED_INT( "HUD_InitClientWeapons sizeof weapon_data_t", (int)sizeof( weapon_data_t ));
		PRED_INT( "HUD_InitClientWeapons sizeof clientdata_t", (int)sizeof( clientdata_t ));
		PRED_INT( "HUD_InitClientWeapons sizeof entity_state_t", (int)sizeof( entity_state_t ));
		PRED_INT( "HUD_InitClientWeapons sizeof usercmd_t", (int)sizeof( usercmd_t ));
	}

	// Set up pointer ( dummy object )
	gpGlobals = &Globals;

	// Fill in current time ( probably not needed )
	gpGlobals->time = gEngfuncs.GetClientTime();

	// Fake functions
	//g_engfuncs.pfnSetClientMaxspeed = HUD_SetMaxSpeed;

	// Handled locally
	g_engfuncs.pfnPlaybackEvent		= HUD_PlaybackEvent;
	g_engfuncs.pfnAlertMessage		= AlertMessage;
	g_engfuncs.pfnLoadFileForMe		= HUD_LoadFileForMe;
	g_engfuncs.pfnFreeFile			= HUD_FreeFile;

	// Safe stubs for client weapon precache calls
	static auto s_DummyPrecacheModel = [](const char *s) -> int { return 1; };
	static auto s_DummyPrecacheSound = [](const char *s) -> int { return 1; };
	g_engfuncs.pfnPrecacheModel     = +s_DummyPrecacheModel;
	g_engfuncs.pfnPrecacheSound     = +s_DummyPrecacheSound;

	// Pass through to engine
	g_engfuncs.pfnPrecacheEvent		= gEngfuncs.pfnPrecacheEvent;
	g_engfuncs.pfnRandomFloat		= gEngfuncs.pfnRandomFloat;
	g_engfuncs.pfnRandomLong		= RandomLong;

	// Allocate a slot for the local player
	PRED_RAW( "HUD_InitClientWeapons before HUD_PrepEntity player" );
	HUD_PrepEntityNamed( &player, NULL, "player" );
	PRED_RAW( "HUD_InitClientWeapons after HUD_PrepEntity player" );

#if defined(__ANDROID__) && defined(__aarch64__)
	g_cspb_hud_client_weapon_init = true;
	PRED_RAW( "HUD_InitClientWeapons aggressive client weapon init flag ON" );
#endif

	// Allocate slot(s) for each weapon that we are going to be predicting
	//HUD_PrepEntity( &g_P228, &player);
	PRED_RAW( "HUD_InitClientWeapons before HUD_PrepEntity g_SCOUT" );
	HUD_PrepEntityNamed( &g_SCOUT, &player, "g_SCOUT" );
	PRED_RAW( "HUD_InitClientWeapons after HUD_PrepEntity g_SCOUT" );
	PRED_RAW( "HUD_InitClientWeapons before HUD_PrepEntity g_HEGrenade" );
	HUD_PrepEntityNamed( &g_HEGrenade, &player, "g_HEGrenade" );
	PRED_RAW( "HUD_InitClientWeapons after HUD_PrepEntity g_HEGrenade" );
	//HUD_PrepEntity( &g_XM1014, &player);
	PRED_RAW( "HUD_InitClientWeapons before HUD_PrepEntity g_C4" );
	HUD_PrepEntityNamed( &g_C4, &player, "g_C4" );
	PRED_RAW( "HUD_InitClientWeapons after HUD_PrepEntity g_C4" );
	//HUD_PrepEntity( &g_MAC10, &player);
	PRED_RAW( "HUD_InitClientWeapons before HUD_PrepEntity g_AUG" );
	HUD_PrepEntityNamed( &g_AUG, &player, "g_AUG" );
	PRED_RAW( "HUD_InitClientWeapons after HUD_PrepEntity g_AUG" );
	PRED_RAW( "HUD_InitClientWeapons before HUD_PrepEntity g_SmokeGrenade" );
	HUD_PrepEntityNamed( &g_SmokeGrenade, &player, "g_SmokeGrenade" );
	PRED_RAW( "HUD_InitClientWeapons after HUD_PrepEntity g_SmokeGrenade" );
	//HUD_PrepEntity( &g_ELITE, &player);
	//HUD_PrepEntity( &g_FiveSeven, &player);
	//HUD_PrepEntity( &g_UMP45, &player);
	PRED_RAW( "HUD_InitClientWeapons before HUD_PrepEntity g_SG550" );
	HUD_PrepEntityNamed( &g_SG550, &player, "g_SG550" );
	PRED_RAW( "HUD_InitClientWeapons after HUD_PrepEntity g_SG550" );
	//HUD_PrepEntity( &g_Galil, &player);
	//HUD_PrepEntity( &g_Famas, &player);
	PRED_RAW( "HUD_InitClientWeapons before HUD_PrepEntity g_USP" );
	HUD_PrepEntityNamed( &g_USP, &player, "g_USP" );
	PRED_RAW( "HUD_InitClientWeapons after HUD_PrepEntity g_USP" );
	PRED_RAW( "HUD_InitClientWeapons before HUD_PrepEntity g_GLOCK18" );
	HUD_PrepEntityNamed( &g_GLOCK18, &player, "g_GLOCK18" );
	PRED_RAW( "HUD_InitClientWeapons after HUD_PrepEntity g_GLOCK18" );
	PRED_RAW( "HUD_InitClientWeapons before HUD_PrepEntity g_AWP" );
	HUD_PrepEntityNamed( &g_AWP, &player, "g_AWP" );
	PRED_RAW( "HUD_InitClientWeapons after HUD_PrepEntity g_AWP" );
	//HUD_PrepEntity( &g_MP5N, &player);
	//HUD_PrepEntity( &g_M249, &player);
	PRED_RAW( "HUD_InitClientWeapons before HUD_PrepEntity g_M4A1" );
	HUD_PrepEntityNamed( &g_M4A1, &player, "g_M4A1" );
	PRED_RAW( "HUD_InitClientWeapons after HUD_PrepEntity g_M4A1" );
	PRED_RAW( "HUD_InitClientWeapons before HUD_PrepEntity g_M3" );
	HUD_PrepEntityNamed( &g_M3, &player, "g_M3" );
	PRED_RAW( "HUD_InitClientWeapons after HUD_PrepEntity g_M3" );
	//HUD_PrepEntity( &g_TMP, &player);
	//HUD_PrepEntity( &g_G3SG1, &player);
	PRED_RAW( "HUD_InitClientWeapons before HUD_PrepEntity g_Flashbang" );
	HUD_PrepEntityNamed( &g_Flashbang, &player, "g_Flashbang" );
	PRED_RAW( "HUD_InitClientWeapons after HUD_PrepEntity g_Flashbang" );
	PRED_RAW( "HUD_InitClientWeapons before HUD_PrepEntity g_DEAGLE" );
	HUD_PrepEntityNamed( &g_DEAGLE, &player, "g_DEAGLE" );
	PRED_RAW( "HUD_InitClientWeapons after HUD_PrepEntity g_DEAGLE" );
	//HUD_PrepEntity( &g_SG552, &player);
	PRED_RAW( "HUD_InitClientWeapons before HUD_PrepEntity g_AK47" );
	HUD_PrepEntityNamed( &g_AK47, &player, "g_AK47" );
	PRED_RAW( "HUD_InitClientWeapons after HUD_PrepEntity g_AK47" );
	PRED_RAW( "HUD_InitClientWeapons before HUD_PrepEntity g_Knife" );
	HUD_PrepEntityNamed( &g_Knife, &player, "g_Knife" );
	PRED_RAW( "HUD_InitClientWeapons after HUD_PrepEntity g_Knife" );
	PRED_RAW( "HUD_InitClientWeapons before HUD_PrepEntity g_P90" );
	HUD_PrepEntityNamed( &g_P90, &player, "g_P90" );
	PRED_RAW( "HUD_InitClientWeapons after HUD_PrepEntity g_P90" );

#if defined(__ANDROID__) && defined(__aarch64__)
	g_cspb_hud_client_weapon_init = false;
	PRED_RAW( "HUD_InitClientWeapons aggressive client weapon init flag OFF" );
#endif

	PRED_RAW( "HUD_InitClientWeapons before BTEClientWeapons.PrepEntity" );
	BTEClientWeapons().PrepEntity(&player);
	PRED_RAW( "HUD_InitClientWeapons after BTEClientWeapons.PrepEntity" );
	PRED_RAW( "HUD_InitClientWeapons leave" );
}


int GetWeaponAccuracyFlags( int weaponid )
{
	int result = 0;

	if( weaponid <= WEAPON_P90 )
	{
		switch( weaponid )
		{
		case WEAPON_AUG:
		//case WEAPON_GALIL:
		case WEAPON_M249:
		//case WEAPON_SG552:
		case WEAPON_AK47:
		case WEAPON_P90:
			result = ACCURACY_AIR | ACCURACY_SPEED;
			break;
		//case WEAPON_P228:
		//case WEAPON_FIVESEVEN:
		case WEAPON_DEAGLE:
			result = ACCURACY_AIR | ACCURACY_SPEED | ACCURACY_DUCK;
			break;
		case WEAPON_GLOCK18:
			if( g_iWeaponFlags & WPNSTATE_GLOCK18_BURST_MODE)
			{
				result = ACCURACY_AIR | ACCURACY_SPEED | ACCURACY_DUCK;
			}
			else
			{
				result = ACCURACY_AIR | ACCURACY_SPEED | ACCURACY_DUCK | ACCURACY_MULTIPLY_BY_14_2;
			}
			break;
		case WEAPON_MAC10:
		case WEAPON_UMP45:
		case WEAPON_MP5N:
		case WEAPON_TMP:
			result = ACCURACY_AIR;
			break;
		case WEAPON_M4A1:
			if(g_iWeaponFlags & WPNSTATE_USP_SILENCED)
			{
				result = ACCURACY_AIR | ACCURACY_SPEED;
			}
			else
			{
				result = ACCURACY_AIR | ACCURACY_SPEED | ACCURACY_MULTIPLY_BY_14;
			}
			break;
		case WEAPON_FAMAS:
			if(g_iWeaponFlags & WPNSTATE_FAMAS_BURST_MODE)
			{
				result = ACCURACY_AIR | ACCURACY_SPEED;
			}
			else
			{
				result = ACCURACY_AIR | ACCURACY_SPEED | (1<<4);
			}
			break;
		case WEAPON_USP:
			if(g_iWeaponFlags & WPNSTATE_USP_SILENCED)
			{
				result = ACCURACY_AIR | ACCURACY_SPEED | ACCURACY_DUCK;
			}
			else
			{
				result = ACCURACY_AIR | ACCURACY_SPEED | ACCURACY_DUCK | ACCURACY_MULTIPLY_BY_14;
			}
			break;
		}
	}

	return result;
}


// Name says it!
// Override stupid Xash(or even GoldSrc?) bug with overwriting
// already predicted values, like maxspeed or punchangle vector
#define _CS16CLIENT_TAKE_PREDICTED_INFO_FOR_WEAPON_PREDICTION

#ifdef _CS16CLIENT_TAKE_PREDICTED_INFO_FOR_WEAPON_PREDICTION
#define STATE to
#else
#define STATE from
#endif

/*
=====================
HUD_WeaponsPostThink

Run Weapon firing code on client
=====================
*/
void HUD_WeaponsPostThink( local_state_s *from, local_state_s *to, usercmd_t *cmd, double time, unsigned int random_seed )
{
	int i;
	int buttonsChanged;
	CBasePlayerWeapon *pWeapon = NULL;
	CBasePlayerWeapon *pActiveBTEWeapon = NULL;
	static int lasthealth;
	static bool s_loggedPredictionAbi = false;
	int flags;

	PRED_RAW( "HUD_WeaponsPostThink enter" );
	PRED_PTR( "HUD_WeaponsPostThink from", from );
	PRED_PTR( "HUD_WeaponsPostThink to", to );
	PRED_PTR( "HUD_WeaponsPostThink cmd", cmd );
	PRED_INT( "HUD_WeaponsPostThink runfuncs", g_runfuncs );
	PRED_INT( "HUD_WeaponsPostThink time_ms", (int)( time * 1000.0 ) );
	PRED_U32( "HUD_WeaponsPostThink random_seed", random_seed );

	if( !s_loggedPredictionAbi )
	{
		s_loggedPredictionAbi = true;
		PRED_INT( "CSPB_PRED_ABI local_state_t sizeof", (int)sizeof( local_state_t ));
		PRED_INT( "CSPB_PRED_ABI usercmd_t sizeof", (int)sizeof( usercmd_t ));
		PRED_INT( "CSPB_PRED_ABI weapon_data_t sizeof", (int)sizeof( weapon_data_t ));
		PRED_INT( "CSPB_PRED_ABI clientdata_t sizeof", (int)sizeof( clientdata_t ));
		PRED_INT( "CSPB_PRED_ABI entity_state_t sizeof", (int)sizeof( entity_state_t ));
	}

	if( !from || !to || !cmd )
	{
		PRED_RAW( "HUD_WeaponsPostThink null input guard return" );
		return;
	}

	PRED_INT( "HUD_WeaponsPostThink from client.fov", (int)from->client.fov );
	PRED_INT( "HUD_WeaponsPostThink to client.fov", (int)to->client.fov );
	PRED_INT( "HUD_WeaponsPostThink from nextattack_ms", (int)( from->client.m_flNextAttack * 1000.0 ) );
	PRED_INT( "HUD_WeaponsPostThink to nextattack_ms", (int)( to->client.m_flNextAttack * 1000.0 ) );
	PRED_INT( "HUD_WeaponsPostThink from weaponmodel", from->playerstate.weaponmodel );
	PRED_INT( "HUD_WeaponsPostThink to weaponmodel", to->playerstate.weaponmodel );
	PRED_INT( "HUD_WeaponsPostThink from weaponanim", from->client.weaponanim );
	PRED_INT( "HUD_WeaponsPostThink to weaponanim", to->client.weaponanim );
	PRED_INT( "HUD_WeaponsPostThink active weapon id", from->client.m_iId );

#if defined(__ANDROID__) && defined(__aarch64__)
	if( from->client.m_iId <= 0 || from->client.m_iId >= MAX_WEAPONS )
	{
		PRED_RAW( "HUD_WeaponsPostThink skip weapon prediction: active weapon id not ready android arm64" );
		PRED_INT( "HUD_WeaponsPostThink skip active weapon id", from->client.m_iId );

		if( to )
		{
			to->client.m_iId = from->client.m_iId;
			to->client.fov = from->client.fov;
			to->client.weaponanim = from->client.weaponanim;
			to->client.m_flNextAttack = from->client.m_flNextAttack;
			to->client.viewmodel = from->client.viewmodel;
		}

		PRED_RAW( "HUD_WeaponsPostThink leave early no active weapon" );
		return;
	}
#endif

	PRED_RAW( "HUD_WeaponsPostThink before HUD_InitClientWeapons" );
	HUD_InitClientWeapons();
	PRED_RAW( "HUD_WeaponsPostThink after HUD_InitClientWeapons" );

	PRED_PTR( "HUD_WeaponsPostThink gpGlobals", gpGlobals );
	if( !gpGlobals )
	{
		PRED_RAW( "HUD_WeaponsPostThink gpGlobals null guard return" );
		return;
	}

	// Get current clock
	PRED_RAW( "HUD_WeaponsPostThink before gpGlobals->time" );
	gpGlobals->time = time;
	PRED_RAW( "HUD_WeaponsPostThink after gpGlobals->time" );

	// Fill in data based on selected weapon
	PRED_RAW( "HUD_WeaponsPostThink before active weapon switch" );
	switch ( from->client.m_iId )
	{
		//case WEAPON_P228:
			//pWeapon = &g_P228;
			//break;

		case WEAPON_SCOUT:
			pWeapon = &g_SCOUT;
			break;

		case WEAPON_HEGRENADE:
			pWeapon = &g_HEGrenade;
			break;

		//case WEAPON_XM1014:
			//pWeapon = &g_XM1014;
			//break;

		case WEAPON_C4:
			pWeapon = &g_C4;
			break;

		//case WEAPON_MAC10:
			//pWeapon = &g_MAC10;
			//break;

		case WEAPON_AUG:
			pWeapon = &g_AUG;
			break;

		case WEAPON_SMOKEGRENADE:
			pWeapon = &g_SmokeGrenade;
			break;

		//case WEAPON_ELITE:
			//pWeapon = &g_ELITE;
			//break;

		//case WEAPON_FIVESEVEN:
			//pWeapon = &g_FiveSeven;
			//break;

		//case WEAPON_UMP45:
			//pWeapon = &g_UMP45;
			//break;

		case WEAPON_SG550:
			pWeapon = &g_SG550;
			break;

		//case WEAPON_GALIL:
			//pWeapon = &g_Galil;
			//break;

		//case WEAPON_FAMAS:
			//pWeapon = &g_Famas;
			//break;

		case WEAPON_USP:
			pWeapon = &g_USP;
			break;

		case WEAPON_GLOCK18:
			pWeapon = &g_GLOCK18;
			break;

		case WEAPON_AWP:
			pWeapon = &g_AWP;
			break;

		//case WEAPON_MP5N:
			//pWeapon = &g_MP5N;
			//break;

		//case WEAPON_M249:
			//pWeapon = &g_M249;
			//break;

		case WEAPON_M3:
			pWeapon = &g_M3;
			break;

		case WEAPON_M4A1:
			pWeapon = &g_M4A1;
			break;

		//case WEAPON_TMP:
			//pWeapon = &g_TMP;
			//break;

		//case WEAPON_G3SG1:
			//pWeapon = &g_G3SG1;
			//break;

		case WEAPON_FLASHBANG:
			pWeapon = &g_Flashbang;
			break;

		case WEAPON_DEAGLE:
			pWeapon = &g_DEAGLE;
			break;

		//case WEAPON_SG552:
			//pWeapon = &g_SG552;
			//break;

		case WEAPON_AK47:
			pWeapon = &g_AK47;
			break;

		case WEAPON_KNIFE:
			pWeapon = &g_Knife;
			break;

		case WEAPON_P90:
			pWeapon = &g_P90;
			break;

		/*case WEAPON_NONE:
			break;

		case WEAPON_GLOCK:
		default:
			gEngfuncs.Con_Printf("VALVEWHY: Unknown Weapon %i is active.\n", from->client.m_iId );
			break;*/
	}
	PRED_PTR( "HUD_WeaponsPostThink switch pWeapon", pWeapon );
	PRED_RAW( "HUD_WeaponsPostThink after active weapon switch" );

	// if we have BTE weapon entity, use it.
	PRED_RAW( "HUD_WeaponsPostThink before BTE active weapon lookup" );
	pActiveBTEWeapon = BTEClientWeapons().GetActiveWeaponEntity();
	PRED_PTR( "HUD_WeaponsPostThink BTE active weapon", pActiveBTEWeapon );
	if (pActiveBTEWeapon)
		pWeapon = pActiveBTEWeapon;
	PRED_PTR( "HUD_WeaponsPostThink final pWeapon", pWeapon );
	PRED_RAW( "HUD_WeaponsPostThink after BTE active weapon lookup" );

	// Store pointer to our destination entity_state_t so we can get our origin, etc. from it
	//  for setting up events on the client
	PRED_RAW( "HUD_WeaponsPostThink before set g_finalstate" );
	g_finalstate = to;
	PRED_RAW( "HUD_WeaponsPostThink after set g_finalstate" );

	// If we are running events/etc. go ahead and see if we
	//  managed to die between last frame and this one
	// If so, run the appropriate player killed or spawn function
	if ( g_runfuncs )
	{
		PRED_RAW( "HUD_WeaponsPostThink before runfuncs death/spawn block" );
		if ( to->client.health <= 0 && lasthealth > 0 )
			player.Killed( NULL, 0 );
		else if ( to->client.health > 0 && lasthealth <= 0 )
			player.Spawn();

		lasthealth = to->client.health;
		PRED_RAW( "HUD_WeaponsPostThink after runfuncs death/spawn block" );
	}

	// We are not predicting the current weapon, just bow out here.
	if ( !pWeapon )
	{
		PRED_RAW( "HUD_WeaponsPostThink null pWeapon return" );
		return;
	}

	PRED_RAW( "HUD_WeaponsPostThink before weapon sync loop" );
	for ( i = 0; i < MAX_WEAPONS; i++ )
	{
		CBasePlayerWeapon *pCurrent = g_pWpns[ i ];
		PRED_INT( "HUD_WeaponsPostThink weapon sync i", i );
		PRED_PTR( "HUD_WeaponsPostThink weapon sync pCurrent", pCurrent );
		if ( !pCurrent )
		{
			PRED_RAW( "HUD_WeaponsPostThink weapon sync skip null" );
			continue;
		}

		weapon_data_t *pfrom = from->weapondata + i;
		PRED_PTR( "HUD_WeaponsPostThink weapon sync pfrom", pfrom );

		pCurrent->m_fInReload			= pfrom->m_fInReload;
		pCurrent->m_fInSpecialReload	= pfrom->m_fInSpecialReload;
		pCurrent->m_iClip				= pfrom->m_iClip;
		pCurrent->m_flNextPrimaryAttack	= pfrom->m_flNextPrimaryAttack;
		pCurrent->m_flNextSecondaryAttack = pfrom->m_flNextSecondaryAttack;
		pCurrent->m_flTimeWeaponIdle	= pfrom->m_flTimeWeaponIdle;
		pCurrent->m_flStartThrow		= pfrom->fuser2;
		pCurrent->m_flReleaseThrow		= pfrom->fuser3;
		pCurrent->m_iSwing				= pfrom->iuser1;
		pCurrent->m_iWeaponState		= pfrom->m_iWeaponState;
		pCurrent->m_flLastFire			= pfrom->m_fAimedDamage;
		pCurrent->m_iShotsFired			= pfrom->m_fInZoom;
		PRED_RAW( "HUD_WeaponsPostThink weapon sync copied" );
	}
	PRED_RAW( "HUD_WeaponsPostThink after weapon sync loop" );

	PRED_RAW( "HUD_WeaponsPostThink before ammo type block" );
	if( from->client.vuser4.x < 0 || from->client.vuser4.x > MAX_AMMO_TYPES )
		pWeapon->m_iPrimaryAmmoType = 0;
	else
	{
		pWeapon->m_iPrimaryAmmoType = (int)from->client.vuser4.x;
		player.m_rgAmmo[ pWeapon->m_iPrimaryAmmoType ]  = (int)from->client.vuser4.y;
	}
	PRED_INT( "HUD_WeaponsPostThink primary ammo type", pWeapon->m_iPrimaryAmmoType );
	PRED_RAW( "HUD_WeaponsPostThink after ammo type block" );


	g_iWeaponFlags = pWeapon->m_iWeaponState;

	// For random weapon events, use this seed to seed random # generator
	player.random_seed = random_seed;

	// Get old buttons from previous state.
	player.m_afButtonLast = from->playerstate.oldbuttons;
	PRED_RAW( "HUD_WeaponsPostThink after button state setup" );

	// Which buttsons chave changed
	buttonsChanged = (player.m_afButtonLast ^ cmd->buttons);	// These buttons have changed this frame

	// Debounced button codes for pressed/released
	// The changed ones still down are "pressed"
	player.m_afButtonPressed =  buttonsChanged & cmd->buttons;
	// The ones not down are "released"
	player.m_afButtonReleased = buttonsChanged & (~cmd->buttons);

	// Set player variables that weapons code might check/alter
	player.pev->button = cmd->buttons;

	player.pev->velocity = from->client.velocity;

	player.pev->deadflag   = from->client.deadflag;
	player.pev->waterlevel = from->client.waterlevel;
	player.pev->maxspeed   = STATE->client.maxspeed; //!!! Taking "to"
	player.pev->punchangle = STATE->client.punchangle; //!!! Taking "to"
	player.pev->fov        = from->client.fov;
	player.pev->weaponanim = from->client.weaponanim;
	player.pev->viewmodel  = from->client.viewmodel;
	player.m_flNextAttack  = from->client.m_flNextAttack;
	PRED_PTR( "HUD_WeaponsPostThink player.pev", player.pev );
	if( !player.pev )
	{
		PRED_RAW( "HUD_WeaponsPostThink player.pev null guard return" );
		g_finalstate = NULL;
		return;
	}

	g_iPlayerFlags    = player.pev->flags = from->client.flags;
	g_vPlayerVelocity = player.pev->velocity;
	g_flPlayerSpeed	  = player.pev->velocity.Length();
	PRED_RAW( "HUD_WeaponsPostThink after player pev state copy" );

	//Stores all our ammo info, so the client side weapons can use them.
	player.ammo_9mm			= from->client.ammo_nails;
	player.ammo_556nato		= from->client.ammo_cells;
	player.ammo_buckshot	= from->client.ammo_shells;
	player.ammo_556natobox	= from->client.ammo_rockets;
	player.ammo_762nato		= (int)from->client.vuser2.x;
	player.ammo_45acp		= (int)from->client.vuser2.y;
	player.ammo_50ae		= (int)from->client.vuser2.z;
	player.ammo_338mag		= (int)from->client.vuser3.x;
	player.ammo_57mm		= (int)from->client.vuser3.y;
	player.ammo_357sig		= (int)from->client.vuser3.z;
	PRED_RAW( "HUD_WeaponsPostThink after ammo copy" );

	PRED_RAW( "HUD_WeaponsPostThink before GetLocalPlayer" );
	cl_entity_t *pplayer = gEngfuncs.GetLocalPlayer();
	PRED_PTR( "HUD_WeaponsPostThink local player entity", pplayer );
	if( pplayer )
	{
		player.pev->origin = STATE->client.origin; //!!! Taking "to"
		player.pev->angles	= pplayer->angles;
		player.pev->v_angle = v_angles;
	}
	PRED_RAW( "HUD_WeaponsPostThink after GetLocalPlayer" );

	flags = from->client.iuser3;
	g_bHoldingKnife		= pWeapon->m_iId == WEAPON_KNIFE;
	player.m_bCanShoot	= (flags & PLAYER_CAN_SHOOT) != 0;
	g_iFreezeTimeOver	= !(flags & PLAYER_FREEZE_TIME_OVER);
	g_bInBombZone		= (flags & PLAYER_IN_BOMB_ZONE) != 0;
	g_bHoldingShield	= (flags & PLAYER_HOLDING_SHIELD) != 0;

	// Point to current weapon object
	if ( from->client.m_iId )
		player.m_pActiveItem = pWeapon;
	PRED_PTR( "HUD_WeaponsPostThink player active item", player.m_pActiveItem );

	// Don't go firing anything if we have died.
	// Or if we don't have a weapon model deployed
	if ( ( player.pev->deadflag != ( DEAD_DISCARDBODY + 1 ) ) &&
		 !CL_IsDead() && player.pev->viewmodel && !g_iUser1 )
	{
		PRED_RAW( "HUD_WeaponsPostThink before ItemPostFrame gate" );
		if( g_bHoldingKnife && pWeapon->m_iClientWeaponState &&
				player.pev->button & IN_FORWARD )
			player.m_flNextAttack = 0;
		else if( player.m_flNextAttack <= 0 )
		{
			PRED_RAW( "HUD_WeaponsPostThink before ItemPostFrame" );
			pWeapon->ItemPostFrame();
			PRED_RAW( "HUD_WeaponsPostThink after ItemPostFrame" );
		}
		PRED_RAW( "HUD_WeaponsPostThink after ItemPostFrame gate" );
	}

	// Assume that we are not going to switch weapons
	to->client.m_iId					= from->client.m_iId;
	PRED_RAW( "HUD_WeaponsPostThink after default weapon id copy" );

	// Now see if we issued a changeweapon command ( and we're not dead )
	if ( cmd->weaponselect && ( player.pev->deadflag != ( DEAD_DISCARDBODY + 1 ) ) )
	{
		PRED_INT( "HUD_WeaponsPostThink cmd weaponselect", cmd->weaponselect );
		if( cmd->weaponselect >= MAX_WEAPONS )
		{
			PRED_RAW( "HUD_WeaponsPostThink invalid weaponselect skip" );
		}
		else
		{
		// Switched to a different weapon?
			if ( from->weapondata[ cmd->weaponselect ].m_iId == cmd->weaponselect )
			{
				CBasePlayerWeapon *pNew = g_pWpns[ cmd->weaponselect ];
				PRED_PTR( "HUD_WeaponsPostThink switch pNew", pNew );
				if ( pNew && ( pNew != pWeapon ) )
				{
					// Put away old weapon
					if (player.m_pActiveItem)
					{
						PRED_RAW( "HUD_WeaponsPostThink before Holster" );
						player.m_pActiveItem->Holster( );
						PRED_RAW( "HUD_WeaponsPostThink after Holster" );
					}

					player.m_pLastItem = player.m_pActiveItem;
					player.m_pActiveItem = pNew;

					// Deploy new weapon
					if (player.m_pActiveItem)
					{
						PRED_RAW( "HUD_WeaponsPostThink before Deploy" );
						player.m_pActiveItem->Deploy( );
						PRED_RAW( "HUD_WeaponsPostThink after Deploy" );
					}

					// Update weapon id so we can predict things correctly.
					to->client.m_iId = cmd->weaponselect;
				}
			}
		}
	}
	PRED_RAW( "HUD_WeaponsPostThink after weapon switch block" );

	// Copy in results of prediction code
	PRED_RAW( "HUD_WeaponsPostThink before copy results" );
	to->client.viewmodel				= player.pev->viewmodel;
	to->client.fov						= player.pev->fov;
	to->client.weaponanim				= player.pev->weaponanim;
	to->client.m_flNextAttack			= player.m_flNextAttack;
	to->client.maxspeed					= player.pev->maxspeed;
	to->client.punchangle				= player.pev->punchangle;


	to->client.ammo_nails = player.ammo_9mm;
	to->client.ammo_cells = player.ammo_556nato;
	to->client.ammo_shells = player.ammo_buckshot;
	to->client.ammo_rockets = player.ammo_556natobox;
	to->client.vuser2.x = player.ammo_762nato;
	to->client.vuser2.y = player.ammo_45acp;
	to->client.vuser2.z = player.ammo_50ae;
	to->client.vuser3.x = player.ammo_338mag;
	to->client.vuser3.y = player.ammo_57mm;
	to->client.vuser3.z = player.ammo_357sig;
	to->client.iuser3 = flags;
	PRED_RAW( "HUD_WeaponsPostThink after copy results" );




	// Make sure that weapon animation matches what the game .dll is telling us
	//  over the wire ( fixes some animation glitches )
	if ( g_runfuncs && ( HUD_GetWeaponAnim() != to->client.weaponanim ) )
	{
		// Force a fixed anim down to viewmodel
		PRED_RAW( "HUD_WeaponsPostThink before HUD_SendWeaponAnim" );
		HUD_SendWeaponAnim( to->client.weaponanim, to->client.m_iId, 2, 1 );
		PRED_RAW( "HUD_WeaponsPostThink after HUD_SendWeaponAnim" );
	}

	if (pWeapon->m_iPrimaryAmmoType < MAX_AMMO_TYPES)
	{
		to->client.vuser4.x = pWeapon->m_iPrimaryAmmoType;
		to->client.vuser4.y = player.m_rgAmmo[ pWeapon->m_iPrimaryAmmoType ];
	}
	else
	{
		to->client.vuser4.x = -1.0;
		to->client.vuser4.y = 0;
	}
	PRED_RAW( "HUD_WeaponsPostThink after vuser4 block" );

	PRED_RAW( "HUD_WeaponsPostThink before weapon output loop" );
	for ( i = 0; i < MAX_WEAPONS; i++ )
	{
		CBasePlayerWeapon *pCurrent = g_pWpns[ i ];
		PRED_INT( "HUD_WeaponsPostThink weapon output i", i );
		PRED_PTR( "HUD_WeaponsPostThink weapon output pCurrent", pCurrent );

		weapon_data_t *pto = to->weapondata + i;
		PRED_PTR( "HUD_WeaponsPostThink weapon output pto", pto );

		if ( !pCurrent )
		{
			PRED_RAW( "HUD_WeaponsPostThink weapon output memset zero" );
			memset( pto, 0, sizeof( weapon_data_t ) );
			continue;
		}

		pto->m_iClip					= pCurrent->m_iClip;

		pto->m_flNextPrimaryAttack		= pCurrent->m_flNextPrimaryAttack;
		pto->m_flNextSecondaryAttack	= pCurrent->m_flNextSecondaryAttack;
		pto->m_flTimeWeaponIdle			= pCurrent->m_flTimeWeaponIdle;

		pto->m_fInReload				= pCurrent->m_fInReload;
		pto->m_fInSpecialReload			= pCurrent->m_fInSpecialReload;
		pto->m_flNextReload				= pCurrent->m_flNextReload;
		pto->fuser2						= pCurrent->m_flStartThrow;
		pto->fuser3						= pCurrent->m_flReleaseThrow;
		pto->iuser1						= pCurrent->m_iSwing;
		pto->m_iWeaponState				= pCurrent->m_iWeaponState;
		pto->m_fInZoom					= pCurrent->m_iShotsFired;
		pto->m_fAimedDamage				= pCurrent->m_flLastFire;

		// Decrement weapon counters, server does this at same time ( during post think, after doing everything else )
		pto->m_flNextReload				-= cmd->msec / 1000.0f;
		pto->m_fNextAimBonus			-= cmd->msec / 1000.0f;
		pto->m_flNextPrimaryAttack		-= cmd->msec / 1000.0f;
		pto->m_flNextSecondaryAttack	-= cmd->msec / 1000.0f;
		pto->m_flTimeWeaponIdle			-= cmd->msec / 1000.0f;


		if( pto->m_flPumpTime != -9999.0f )
		{
			pto->m_flPumpTime -= cmd->msec / 1000.0f;
			if( pto->m_flPumpTime < -1.0f )
				pto->m_flPumpTime = 1.0f;
		}

		if ( pto->m_fNextAimBonus < -1.0 )
		{
			pto->m_fNextAimBonus = -1.0;
		}

		if ( pto->m_flNextPrimaryAttack < -1.0 )
		{
			pto->m_flNextPrimaryAttack = -1.0;
		}

		if ( pto->m_flNextSecondaryAttack < -0.001 )
		{
			pto->m_flNextSecondaryAttack = -0.001;
		}

		if ( pto->m_flTimeWeaponIdle < -0.001 )
		{
			pto->m_flTimeWeaponIdle = -0.001;
		}

		if ( pto->m_flNextReload < -0.001 )
		{
			pto->m_flNextReload = -0.001;
		}

		/*if ( pto->fuser1 < -0.001 )
		{
			pto->fuser1 = -0.001;
		}*/
		PRED_RAW( "HUD_WeaponsPostThink weapon output copied" );
	}
	PRED_RAW( "HUD_WeaponsPostThink after weapon output loop" );

	// m_flNextAttack is now part of the weapons, but is part of the player instead
	to->client.m_flNextAttack -= cmd->msec / 1000.0f;
	if ( to->client.m_flNextAttack < -0.001 )
	{
		to->client.m_flNextAttack = -0.001;
	}
	PRED_RAW( "HUD_WeaponsPostThink after next attack clamp" );

	// Wipe it so we can't use it after this frame
	g_finalstate = NULL;
	PRED_RAW( "HUD_WeaponsPostThink leave" );
}

/*
=====================
HUD_PostRunCmd

Client calls this during prediction, after it has moved the player and updated any info changed into to->
time is the current client clock based on prediction
cmd is the command that caused the movement, etc
runfuncs is 1 if this is the first time we've predicted this command.  If so, sounds and effects should play, otherwise, they should
be ignored
=====================
*/
void DLLEXPORT HUD_PostRunCmd( local_state_t *from, local_state_t *to, struct usercmd_s *cmd, int runfuncs, double time, unsigned int random_seed )
{
	PRED_RAW( "HUD_PostRunCmd enter" );
	PRED_PTR( "HUD_PostRunCmd from", from );
	PRED_PTR( "HUD_PostRunCmd to", to );
	PRED_PTR( "HUD_PostRunCmd cmd", cmd );
	PRED_INT( "HUD_PostRunCmd runfuncs", runfuncs );
	PRED_INT( "HUD_PostRunCmd time_ms", (int)( time * 1000.0 ) );
	PRED_U32( "HUD_PostRunCmd random_seed", random_seed );

	g_runfuncs = runfuncs;
	PRED_RAW( "HUD_PostRunCmd after set g_runfuncs" );

	PRED_RAW( "HUD_PostRunCmd before HUD_WeaponsPostThink" );
	HUD_WeaponsPostThink( from, to, cmd, time, random_seed );
	PRED_RAW( "HUD_PostRunCmd after HUD_WeaponsPostThink" );
	PRED_RAW( "HUD_PostRunCmd before copy fov" );
	to->client.fov = g_lastFOV;
	PRED_RAW( "HUD_PostRunCmd after copy fov" );

	if ( g_runfuncs )
	{
		PRED_RAW( "HUD_PostRunCmd before runfuncs block" );
		g_gaitseq	= to->playerstate.gaitsequence;
		g_rseq		= to->playerstate.sequence;
		g_clang		= cmd->viewangles;
		g_clorg		= to->playerstate.origin;
		PRED_RAW( "HUD_PostRunCmd after runfuncs block" );
	}

	PRED_RAW( "HUD_PostRunCmd leave" );
}
