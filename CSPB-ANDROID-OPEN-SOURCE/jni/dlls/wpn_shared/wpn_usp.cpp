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

#include "extdll.h"
#include "util.h"
#include "cbase.h"
#include "player.h"
#include "weapons.h"
#include "wpn_usp.h"
#include "../model_helper.h"

#if defined(__ANDROID__)
#include <android/log.h>
#define USP_PRED_TAG "CSPB_PRED"
#define USP_RAW(msg) __android_log_write( ANDROID_LOG_INFO, USP_PRED_TAG, msg )
#define USP_STR(label, v) __android_log_print( ANDROID_LOG_INFO, USP_PRED_TAG, "%s=%s", label, (v) ? (v) : "(null)" )
#define USP_INT(label, v) __android_log_print( ANDROID_LOG_INFO, USP_PRED_TAG, "%s=%d", label, (int)(v) )
#else
#define USP_RAW(msg)
#define USP_STR(label, v)
#define USP_INT(label, v)
#endif

static const char *USP_ResolveSoundPath( const char *preferred, const char *fallback )
{
	if( preferred && FileExists( preferred ))
		return preferred;
	if( fallback && FileExists( fallback ))
		return fallback;
	return NULL;
}

static void USP_PrecacheSoundTrace( const char *preferred, const char *fallback = NULL )
{
	const char *resolved = USP_ResolveSoundPath( preferred, fallback );
	USP_STR( "USP Precache sound requested", preferred );
	USP_STR( "USP Precache sound resolved", resolved );
	if( !resolved )
	{
		USP_RAW( "USP Precache sound missing skip" );
		return;
	}
	PRECACHE_SOUND( resolved );
}

static unsigned short USP_PrecacheEventTrace( int type, const char *path )
{
	USP_STR( "USP Precache event requested", path );
	if( !path || !FileExists( path ))
	{
		USP_RAW( "USP Precache event missing skip" );
		return 0;
	}
	return PRECACHE_EVENT( type, path );
}

enum usp_e
{
	USP_IDLE,
	USP_SHOOT,
	USP_SHOOT2,
	USP_SHOOT3,
	USP_SHOOT_EMPTY,
	USP_RELOAD,
	USP_DRAW,
	RUN, 
DAMAGE, 
JUMP,
ANIM1,
ANIM2,
ANIM3,
ANIM4,
ANIM5
};

enum usp_shield_e
{
	USP_SHIELD_IDLE,
	USP_SHIELD_SHOOT1,
	USP_SHIELD_SHOOT2,
	USP_SHIELD_SHOOT_EMPTY,
	USP_SHIELD_RELOAD,
	USP_SHIELD_DRAW,
	USP_SHIELD_UP_IDLE,
	USP_SHIELD_UP,
	USP_SHIELD_DOWN
};

LINK_ENTITY_TO_CLASS(weapon_usp, CUSP)

void CUSP::Spawn(void)
{
	pev->classname = MAKE_STRING("weapon_usp");

	Precache();
	m_iId = WEAPON_USP;
	SET_MODEL(ENT(pev), RESOLVE_CSPB_FIREARM_WORLD_MODEL("models/w_usp.mdl"));

	m_iDefaultAmmo = USP_DEFAULT_GIVE;
	m_flAccuracy = 0.92;
	m_iWeaponState &= ~WPNSTATE_SHIELD_DRAWN;

	FallInit();
}

void CUSP::Precache(void)
{
	USP_RAW( "USP Precache enter" );

	USP_RAW( "USP Precache before model v_k5" );
	USP_STR( "USP Precache model path", "models/billflx/v_k5.mdl" );
	PRECACHE_MODEL("models/billflx/v_k5.mdl");
	USP_RAW( "USP Precache after model v_k5" );

	USP_RAW( "USP Precache before model p_k5" );
	USP_STR( "USP Precache model path", "models/p_k5.mdl" );
	PRECACHE_MODEL("models/p_k5.mdl");
	USP_RAW( "USP Precache after model p_k5" );

	USP_RAW( "USP Precache before model shield v_shield_usp" );
	USP_STR( "USP Precache model path", "models/shield/v_shield_usp.mdl" );
	if( FileExists( "models/shield/v_shield_usp.mdl" ))
	{
		SAFE_PRECACHE_MODEL("models/shield/v_shield_usp.mdl");
	}
	else
	{
		USP_RAW( "USP Precache skip missing shield model models/shield/v_shield_usp.mdl" );
	}
	USP_RAW( "USP Precache after model shield v_shield_usp" );

	USP_RAW( "USP Precache before sound k5-1" );
	USP_PrecacheSoundTrace( "weapons/k5-1.wav" );
	USP_RAW( "USP Precache after sound k5-1" );

	USP_RAW( "USP Precache before sound usp2" );
	USP_PrecacheSoundTrace( "weapons/usp2.wav", "weapons/usp-2.wav" );
	USP_RAW( "USP Precache after sound usp2" );

	USP_RAW( "USP Precache before sound usp_unsil-1" );
	USP_PrecacheSoundTrace( "weapons/usp_unsil-1.wav" );
	USP_RAW( "USP Precache after sound usp_unsil-1" );

	USP_RAW( "USP Precache before sound usp_clipout" );
	USP_PrecacheSoundTrace( "weapons/usp_clipout.wav" );
	USP_RAW( "USP Precache after sound usp_clipout" );

	USP_RAW( "USP Precache before sound usp_clipin" );
	USP_PrecacheSoundTrace( "weapons/usp_clipin.wav" );
	USP_RAW( "USP Precache after sound usp_clipin" );

	USP_RAW( "USP Precache before sound usp_silencer_on" );
	USP_PrecacheSoundTrace( "weapons/usp_silencer_on.wav" );
	USP_RAW( "USP Precache after sound usp_silencer_on" );

	USP_RAW( "USP Precache before sound usp_silencer_off" );
	USP_PrecacheSoundTrace( "weapons/usp_silencer_off.wav" );
	USP_RAW( "USP Precache after sound usp_silencer_off" );

	USP_RAW( "USP Precache before sound usp_sliderelease" );
	USP_PrecacheSoundTrace( "weapons/usp_sliderelease.wav" );
	USP_RAW( "USP Precache after sound usp_sliderelease" );

	USP_RAW( "USP Precache before sound usp_slideback" );
	USP_PrecacheSoundTrace( "weapons/usp_slideback.wav" );
	USP_RAW( "USP Precache after sound usp_slideback" );

	USP_RAW( "USP Precache before model pshell" );
	USP_STR( "USP Precache model path", "models/pshell.mdl" );
	m_iShell = PRECACHE_MODEL("models/pshell.mdl");
	USP_INT( "USP Precache m_iShell", m_iShell );
	USP_RAW( "USP Precache after model pshell" );

	USP_RAW( "USP Precache before event usp.sc" );
	m_usFireUSP = USP_PrecacheEventTrace( 1, "events/usp.sc" );
	USP_INT( "USP Precache m_usFireUSP", m_usFireUSP );
	USP_RAW( "USP Precache after event usp.sc" );
	USP_RAW( "USP Precache leave" );
}

int CUSP::GetItemInfo(ItemInfo *p)
{
	p->pszName = STRING(pev->classname);
	p->pszAmmo1 = "45acp";
	p->iMaxAmmo1 = MAX_AMMO_45ACP;
	p->pszAmmo2 = NULL;
	p->iMaxAmmo2 = -1;
	p->iMaxClip = USP_MAX_CLIP;
	p->iSlot = 1;
	p->iPosition = 4;
	p->iId = WEAPON_USP;
	p->iFlags = 0;
	p->iWeight = USP_WEIGHT;

	return 1;
}


BOOL CUSP::Deploy(void)
{

   m_iWeaponState &= ~WPNSTATE_SHIELD_DRAWN;
   m_flAccuracy = 0.92f;
   m_fMaxSpeed = 250.0f;
   m_pPlayer->m_bShieldDrawn = false;

return DefaultDeploy("models/billflx/v_k5.mdl", "models/p_k5.mdl", USP_DRAW, "onehanded", 0);
}

void CUSP::QuickDeploy()
{
SendWeaponAnim(ANIM2, 0);
m_flNextPrimaryAttack = m_pPlayer->m_flNextAttack = UTIL_WeaponTimeBase() + 0.3;
m_flNextSecondaryAttack = UTIL_WeaponTimeBase() + 0.3;
}

void CUSP::SecondaryAttack(void)
{
	
;
}


void CUSP::PrimaryAttack(void)
{
	
		if (!FBitSet(m_pPlayer->pev->flags, FL_ONGROUND))
			USPFire((1.3) * (1 - m_flAccuracy), 0.225, FALSE);
		else if (m_pPlayer->pev->velocity.Length2D() > 0)
			USPFire((0.25) * (1 - m_flAccuracy), 0.225, FALSE);
		else if (FBitSet(m_pPlayer->pev->flags, FL_DUCKING))
			USPFire((0.125) * (1 - m_flAccuracy), 0.225, FALSE);
		else
			USPFire((0.15) * (1 - m_flAccuracy), 0.225, FALSE);
	
}

void CUSP::USPFire(float flSpread, float flCycleTime, BOOL fUseAutoAim)
{
	flCycleTime -= 0.075;
	m_iShotsFired++;

	if (m_iShotsFired > 1)
		return;

	if (m_flLastFire)
	{
		m_flAccuracy -= (0.3 - (gpGlobals->time - m_flLastFire)) * 0.275;

		if (m_flAccuracy > 0.92)
			m_flAccuracy = 0.92;
		else if (m_flAccuracy < 0.6)
			m_flAccuracy = 0.6;
	}

	m_flLastFire = gpGlobals->time;

	if (m_iClip <= 0)
	{
		if (m_fFireOnEmpty)
		{
			PlayEmptySound();
			m_flNextPrimaryAttack = UTIL_WeaponTimeBase() + 0.2;
		}

		return;
	}

	m_iClip--;
#ifndef CLIENT_DLL
	m_pPlayer->SetAnimation(PLAYER_ATTACK1);
#endif

	m_pPlayer->m_iWeaponVolume = BIG_EXPLOSION_VOLUME;
	m_pPlayer->m_iWeaponFlash = DIM_GUN_FLASH;

	UTIL_MakeVectors(m_pPlayer->pev->v_angle + m_pPlayer->pev->punchangle);

	if (!(m_iWeaponState & WPNSTATE_USP_SILENCED))
		m_pPlayer->pev->effects |= EF_MUZZLEFLASH;

	int iDamage = (m_iWeaponState & WPNSTATE_USP_SILENCED) ? 30 : 34;
	Vector vecDir = FireBullets3(m_pPlayer->GetGunPosition(), gpGlobals->v_forward, flSpread, 4096, 1, BULLET_PLAYER_45ACP, iDamage, 0.79, m_pPlayer->pev, TRUE, m_pPlayer->random_seed);

Vector vecSrc = m_pPlayer->GetGunPosition();
UTIL_MakeVectors(m_pPlayer->pev->v_angle);
	Vector vecEnd = vecSrc + gpGlobals->v_forward * 2000;

EMIT_SOUND(ENT(m_pPlayer->pev), CHAN_WEAPON, "weapons/k5-1.wav", VOL_NORM, ATTN_NORM);



if (m_iClip > 0)
{
SendWeaponAnim(USP_SHOOT, 0);
}
else if (m_iClip == 0)
{
SendWeaponAnim(USP_IDLE, 0);
}

	int flags;
#ifdef CLIENT_WEAPONS
	flags = FEV_NOTHOST;
#else
	flags = 0;
#endif

	PLAYBACK_EVENT_FULL(flags, ENT(m_pPlayer->pev),m_usFireUSP, 0, (float *)&g_vecZero, (float *)&g_vecZero, vecDir.x, vecDir.y, (int)(m_pPlayer->pev->punchangle.x * 100), 0, m_iClip != 0, m_iWeaponState & WPNSTATE_USP_SILENCED);
	m_flNextPrimaryAttack = m_flNextSecondaryAttack = UTIL_WeaponTimeBase() + flCycleTime;
#ifndef CLIENT_DLL
	if (!m_iClip && m_pPlayer->m_rgAmmo[m_iPrimaryAmmoType] <= 0)
		m_pPlayer->SetSuitUpdate("!HEV_AMO0", FALSE, 0);
#endif
	m_flTimeWeaponIdle = UTIL_WeaponTimeBase() + 2;
	m_pPlayer->pev->punchangle.x -= 2;
	ResetPlayerShieldAnim();
}

void CUSP::Reload(void)
{
if (m_pPlayer->ammo_45acp <= 0)
		return;
if (m_iClip == USP_MAX_CLIP)
return;
	

	if (DefaultReload(USP_MAX_CLIP, NULL, 2.2))
	{
#ifndef CLIENT_DLL
		m_pPlayer->SetAnimation(PLAYER_RELOAD);
#endif
		m_flAccuracy = 0.9;

	}
SendWeaponAnim(USP_RELOAD, 0);
}

void CUSP::QuickReload()
{
if (m_pPlayer->ammo_45acp <= 0)
		return;
if (m_iClip == USP_MAX_CLIP)
return;
	

	if (DefaultReloadQuick(USP_MAX_CLIP, NULL, 1.2))
	{
#ifndef CLIENT_DLL
		m_pPlayer->SetAnimation(PLAYER_RELOAD);
#endif
		m_flAccuracy = 0.9;
SendWeaponAnim(ANIM3, 0);
}
}

void CUSP::WeaponIdle(void)
{
	ResetEmptySound();
	m_pPlayer->GetAutoaimVector(AUTOAIM_10DEGREES);

	if (m_flTimeWeaponIdle > UTIL_WeaponTimeBase())
		return;
	{
		if (m_pPlayer->pev->button & IN_JUMP)
		{
			//if ()
			{
				SendWeaponAnim(JUMP, UseDecrement() != FALSE); 
			
				//m_flTimeWeaponIdle = gpGlobals->time;
				m_flTimeWeaponIdle = UTIL_WeaponTimeBase() + 0.75;
				return;
			}
			//else if (m_flNextRunIdle <= gpGlobals->time)
			{
				//SendWeaponAnim(ANIM_RUN_IDLE, UseDecrement() != FALSE);
				//m_flTimeWeaponIdle = gpGlobals->time + 0.57;
			}
			//m_flTimeWeaponIdle = gpGlobals->time;
		}
		//else
		{
			//if ()
			{
				//SendWeaponAnim(ANIM_RUN_END, UseDecrement() != FALSE);
			
				//m_flTimeWeaponIdle = gpGlobals->time;
				//m_flTimeWeaponIdle = UTIL_WeaponTimeBase() + 0.60;
				//return;
			}
			//else if( m_flNextRunEnd<= gpGlobals->time)
			{
				SendWeaponAnim(USP_IDLE, UseDecrement() != FALSE);
				//m_flTimeWeaponIdle = gpGlobals->time + 0.60;
			}
			//m_flNextRunIdle = gpGlobals->time;
		}
	}
}

void CUSP::ResetRunIdle()
{
	//pev->iuser2 = 1;
	m_flTimeWeaponIdle = gpGlobals->time;
}
