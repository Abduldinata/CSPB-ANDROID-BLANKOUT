/*
kill_effect.cpp - Point Blank alerts implementation (V20 Modernized)
*/

#include "hud.h"
#include "triangleapi.h"
#include "r_efx.h"
#include "cl_util.h"
#include "draw_util.h"
#include "stdio.h"
#include "stdlib.h"
#include "math.h"
#include "parsemsg.h"
#include "eventscripts.h"
#include "const.h"
#include "entity_state.h"
#include "cl_entity.h"
#include "event_api.h"
#include "com_weapons.h"
#include "kill_effect.h"

static void R_InitTextureBillflx(UniqueTexture &tex, const char *relPath, const char *fallbackRelPath = nullptr)
{
	if (!relPath || !relPath[0])
		return;

	char fullPath[256];
	snprintf(fullPath, sizeof(fullPath), "gfx/billflx/%s", relPath);
	R_InitTexture(tex, fullPath);
	if (!tex && fallbackRelPath && fallbackRelPath[0])
	{
		snprintf(fullPath, sizeof(fullPath), "gfx/billflx/%s", fallbackRelPath);
		R_InitTexture(tex, fullPath);
	}
}

// --- Helper for Frag History ---
void CHudKillEffect::AddFragToHistory(int fragIndex) {
	const int kMaxFrags = 8;

	if (m_fragCount < kMaxFrags) {
		m_fragHistory[m_fragCount] = fragIndex;
		m_fragCount++;
	} else {
		for (int i = 0; i < kMaxFrags - 1; i++) {
			m_fragHistory[i] = m_fragHistory[i + 1];
		}
		m_fragHistory[kMaxFrags - 1] = fragIndex;
	}
}

// --- Combat Macro Declarations ---
DECLARE_MESSAGE(m_KillEffect, Add_point);
DECLARE_COMMAND(m_KillEffect, CommandActiveAdd_point);
DECLARE_MESSAGE(m_KillEffect, killframe);
DECLARE_COMMAND(m_KillEffect, CommandActivekillframe);
DECLARE_MESSAGE(m_KillEffect, killframeAnim);
DECLARE_COMMAND(m_KillEffect, CommandActivekillframeAnim);
DECLARE_MESSAGE(m_KillEffect, MissionComplete);
DECLARE_COMMAND(m_KillEffect, CommandActiveMissionComplete);
DECLARE_MESSAGE(m_KillEffect, Pointkill);
DECLARE_COMMAND(m_KillEffect, CommandActivePointkill);
DECLARE_MESSAGE(m_KillEffect, PiercingShot);
DECLARE_COMMAND(m_KillEffect, CommandActivePiercingShot);
DECLARE_MESSAGE(m_KillEffect, MassKill);
DECLARE_COMMAND(m_KillEffect, CommandActiveMassKill);
DECLARE_MESSAGE(m_KillEffect, Doublekill);
DECLARE_COMMAND(m_KillEffect, CommandActiveDoublekill);
DECLARE_MESSAGE(m_KillEffect, Triplekill);
DECLARE_COMMAND(m_KillEffect, CommandActiveTriplekill);
DECLARE_MESSAGE(m_KillEffect, Chainkiller);
DECLARE_COMMAND(m_KillEffect, CommandActiveChainkiller);
DECLARE_MESSAGE(m_KillEffect, HeadshotPoint);
DECLARE_COMMAND(m_KillEffect, CommandActiveHeadshotPoint);
DECLARE_MESSAGE(m_KillEffect, Headshot);
DECLARE_COMMAND(m_KillEffect, CommandActiveHeadshot);
DECLARE_MESSAGE(m_KillEffect, ChainHeadshot);
DECLARE_COMMAND(m_KillEffect, CommandActiveChainHeadshot);
DECLARE_MESSAGE(m_KillEffect, Helmet);
DECLARE_COMMAND(m_KillEffect, CommandActiveHelmet);
DECLARE_MESSAGE(m_KillEffect, Stopper);
DECLARE_COMMAND(m_KillEffect, CommandActiveStopper);
DECLARE_MESSAGE(m_KillEffect, Slugger);
DECLARE_COMMAND(m_KillEffect, CommandActiveSlugger);
DECLARE_MESSAGE(m_KillEffect, PointNumber);
DECLARE_COMMAND(m_KillEffect, CommandActivePointNumber);
DECLARE_MESSAGE(m_KillEffect, HitMarker);
DECLARE_COMMAND(m_KillEffect, CommandActiveHitMarker);
DECLARE_MESSAGE(m_KillEffect, HotKiller);
DECLARE_COMMAND(m_KillEffect, CommandActiveHotKiller);
DECLARE_MESSAGE(m_KillEffect, Nightmare);
DECLARE_COMMAND(m_KillEffect, CommandActiveNightmare);
DECLARE_COMMAND(m_KillEffect, CommandActiveassist);
DECLARE_MESSAGE(m_KillEffect, FragAnimKill);
DECLARE_COMMAND(m_KillEffect, CommandActiveFragAnimKill);
DECLARE_MESSAGE(m_KillEffect, FragAnimHs);
DECLARE_COMMAND(m_KillEffect, CommandActiveFragAnimHs);
DECLARE_MESSAGE(m_KillEffect, FragAnimStopper);
DECLARE_COMMAND(m_KillEffect, CommandActiveFragAnimStopper);
DECLARE_MESSAGE(m_KillEffect, FragAnimStopperHs);
DECLARE_COMMAND(m_KillEffect, CommandActiveFragAnimStopperHs);
DECLARE_MESSAGE(m_KillEffect, FragAnimBlue);
DECLARE_COMMAND(m_KillEffect, CommandActiveFragAnimBlue);
DECLARE_MESSAGE(m_KillEffect, FragAnimGold);
DECLARE_COMMAND(m_KillEffect, CommandActiveFragAnimGold);
DECLARE_MESSAGE(m_KillEffect, SpecialGunner);
DECLARE_COMMAND(m_KillEffect, CommandActiveSpecialGunner);
DECLARE_MESSAGE(m_KillEffect, BombShot);
DECLARE_COMMAND(m_KillEffect, CommandActiveBombShot);
DECLARE_MESSAGE(m_KillEffect, oneShot);
DECLARE_COMMAND(m_KillEffect, CommandActiveoneShot);
DECLARE_MESSAGE(m_KillEffect, OneshotEnable);
DECLARE_COMMAND(m_KillEffect, CommandActiveOneshotEnable);
DECLARE_MESSAGE(m_KillEffect, OneshotDisable);
DECLARE_COMMAND(m_KillEffect, CommandActiveOneshotDisable);

// --- Shop Macro Declarations ---
DECLARE_MESSAGE(m_KillEffect, buy_qc);
DECLARE_COMMAND(m_KillEffect, CommandActivebuy_qc);
DECLARE_MESSAGE(m_KillEffect, buy_megahp);
DECLARE_COMMAND(m_KillEffect, CommandActivebuy_megahp);
DECLARE_MESSAGE(m_KillEffect, buy_bpoint);
DECLARE_COMMAND(m_KillEffect, CommandActivebuy_bpoint);
DECLARE_MESSAGE(m_KillEffect, buy_qr);
DECLARE_COMMAND(m_KillEffect, CommandActivebuy_qr);
DECLARE_MESSAGE(m_KillEffect, buy_qrespawn);
DECLARE_COMMAND(m_KillEffect, CommandActivebuy_qrespawn);
DECLARE_MESSAGE(m_KillEffect, Unequip_mask);
DECLARE_COMMAND(m_KillEffect, CommandActiveUnequip_mask);
DECLARE_MESSAGE(m_KillEffect, Count_unit);
DECLARE_COMMAND(m_KillEffect, CommandActiveCount_unit);

DECLARE_MESSAGE(m_KillEffect, buy_mask_1); DECLARE_COMMAND(m_KillEffect, CommandActivebuy_mask_1);
DECLARE_MESSAGE(m_KillEffect, buy_mask_2); DECLARE_COMMAND(m_KillEffect, CommandActivebuy_mask_2);
DECLARE_MESSAGE(m_KillEffect, buy_mask_3); DECLARE_COMMAND(m_KillEffect, CommandActivebuy_mask_3);
DECLARE_MESSAGE(m_KillEffect, buy_mask_4); DECLARE_COMMAND(m_KillEffect, CommandActivebuy_mask_4);
DECLARE_MESSAGE(m_KillEffect, buy_mask_5); DECLARE_COMMAND(m_KillEffect, CommandActivebuy_mask_5);
DECLARE_MESSAGE(m_KillEffect, buy_mask_6); DECLARE_COMMAND(m_KillEffect, CommandActivebuy_mask_6);
DECLARE_MESSAGE(m_KillEffect, buy_mask_7); DECLARE_COMMAND(m_KillEffect, CommandActivebuy_mask_7);
DECLARE_MESSAGE(m_KillEffect, buy_mask_8); DECLARE_COMMAND(m_KillEffect, CommandActivebuy_mask_8);
DECLARE_MESSAGE(m_KillEffect, buy_mask_9); DECLARE_COMMAND(m_KillEffect, CommandActivebuy_mask_9);
DECLARE_MESSAGE(m_KillEffect, buy_mask_10); DECLARE_COMMAND(m_KillEffect, CommandActivebuy_mask_10);
DECLARE_MESSAGE(m_KillEffect, buy_mask_11); DECLARE_COMMAND(m_KillEffect, CommandActivebuy_mask_11);
DECLARE_MESSAGE(m_KillEffect, buy_mask_12); DECLARE_COMMAND(m_KillEffect, CommandActivebuy_mask_12);
DECLARE_MESSAGE(m_KillEffect, buy_mask_13); DECLARE_COMMAND(m_KillEffect, CommandActivebuy_mask_13);

// --- Combat Logic & Animation States ---
bool isPiercingShot, isMassKill, isDoublekill, isTriplekill, isChainkiller;
bool isHeadshot, isChainHeadshot, isHelmet, isStopper, isSlugger;
bool isHotKiller, isNightmare, isSpecialGunner, isBombShot;

float dis_PiercingShot, dis_MassKill, dis_Doublekill, dis_Triplekill, dis_Chainkiller;
float dis_Headshot, dis_ChainHeadshot, dis_Helmet, dis_Stopper, dis_Slugger;
float dis_HotKiller, dis_Nightmare, dis_SpecialGunner, dis_BombShot;

float KillDisplay() {
    if (isPiercingShot) dis_PiercingShot = 100.0f; else dis_PiercingShot = 0.0f;
    if (isMassKill) dis_MassKill = 100.0f; else dis_MassKill = 0.0f;
    if (isDoublekill) dis_Doublekill = 100.0f; else dis_Doublekill = 0.0f;
    if (isTriplekill) dis_Triplekill = 100.0f; else dis_Triplekill = 0.0f;
    if (isChainkiller) dis_Chainkiller = 100.0f; else dis_Chainkiller = 0.0f;
    if (isHeadshot) dis_Headshot = 100.0f; else dis_Headshot = 0.0f;
    if (isChainHeadshot) dis_ChainHeadshot = 100.0f; else dis_ChainHeadshot = 0.0f;
    if (isHelmet) dis_Helmet = 100.0f; else dis_Helmet = 0.0f;
    if (isStopper) dis_Stopper = 100.0f; else dis_Stopper = 0.0f;
    if (isSlugger) dis_Slugger = 100.0f; else dis_Slugger = 0.0f;
    if (isHotKiller) dis_HotKiller = 100.0f; else dis_HotKiller = 0.0f;
    if (isNightmare) dis_Nightmare = 100.0f; else dis_Nightmare = 0.0f;
    if (isSpecialGunner) dis_SpecialGunner = 100.0f; else dis_SpecialGunner = 0.0f;
    if (isBombShot) dis_BombShot = 100.0f; else dis_BombShot = 0.0f;
    
    return dis_PiercingShot + dis_MassKill + dis_Doublekill + dis_Triplekill + dis_Chainkiller + 
           dis_Headshot + dis_ChainHeadshot + dis_Helmet + dis_Stopper + dis_Slugger + 
           dis_HotKiller + dis_Nightmare + dis_SpecialGunner + dis_BombShot;
}

void CHudKillEffect::Reset(void) {
    if (gHUD.m_iIntermission) {
        isPiercingShot=isMassKill=isDoublekill=isTriplekill=isChainkiller=FALSE;
        isHeadshot=isChainHeadshot=isHelmet=isStopper=isSlugger=FALSE;
        isHotKiller=isNightmare=isSpecialGunner=isBombShot=FALSE;
        HotKiller_time = Nightmare_time = assist_time = oneShot_time = BombShot_time = SpecialGunner_time = 0;
        PiercingShot_time = MassKill_time = Chainkiller_time = Triplekill_time = Doublekill_time = 0;
        ChainHeadshot_time = Slugger_time = Stopper_time = Helmet_time = Headshot_time = 0;
        current_blood_frame = 0; last_frag_id = -1; is_blood_anim_active = false;
        m_center_anim_start_time = 0.0f;
        m_pending_frag_id = -1;
        m_pending_frag_added = false;
        m_active_announcement_tex = nullptr;
        m_fragCount = 0;
        m_queueHead = 0;
        m_queueTail = 0;
        m_queueCount = 0;
    }
}

void CHudKillEffect::EnqueueAnim(int fragId, UniqueTexture *pAnnTex, const char *szSound) {
    if (m_queueCount >= 16)
        return;
    FragQueueItem &item = m_animQueue[m_queueTail];
    item.fragId = fragId;
    item.pAnnTex = pAnnTex;
    if (szSound && szSound[0])
        strncpy(item.szSound, szSound, sizeof(item.szSound) - 1);
    else
        item.szSound[0] = 0;
    item.szSound[sizeof(item.szSound) - 1] = 0;
    m_queueTail = (m_queueTail + 1) % 16;
    m_queueCount++;
}

void CHudKillEffect::PlayNextQueuedAnim() {
    if (m_queueCount <= 0) {
        is_blood_anim_active = false;
        last_frag_id = -1;
        m_pending_frag_id = -1;
        m_pending_frag_added = false;
        m_active_announcement_tex = nullptr;
        return;
    }
    FragQueueItem item = m_animQueue[m_queueHead];
    m_queueHead = (m_queueHead + 1) % 16;
    m_queueCount--;

    is_blood_anim_active = true;
    current_blood_frame = 0;
    m_center_anim_start_time = (float)gEngfuncs.GetClientTime();
    if (m_center_anim_start_time <= 0.0f)
        m_center_anim_start_time = (float)gHUD.m_flTime;
    last_frag_id = item.fragId;
    m_pending_frag_id = item.fragId;
    m_pending_frag_added = false;
    m_active_announcement_tex = item.pAnnTex;

    if (item.szSound[0]) {
        gEngfuncs.pfnPlaySoundByName(item.szSound, 1.0f);
    }
}

// --- Combat Command Handlers ---
void CHudKillEffect::StartCenterAnim(int fragId, UniqueTexture *pAnnTex, const char *szSound)
{
    int effFragId = fragId;
    if (effFragId < 0)
        effFragId = (last_frag_id >= 0 ? last_frag_id : 0);
    if (effFragId < 0 || effFragId >= 32)
        effFragId = 0;
    if (!m_fraganim[effFragId])
        effFragId = (effFragId >= 6 && effFragId <= 17 && m_fraganim[6]) ? 6 : 0;

    is_blood_anim_active = true;
    current_blood_frame = 0;
    m_center_anim_start_time = (float)gEngfuncs.GetClientTime();
    if (m_center_anim_start_time <= 0.0f)
        m_center_anim_start_time = (float)gHUD.m_flTime;
    last_frag_id = effFragId;
    m_pending_frag_id = effFragId;
    m_pending_frag_added = false;
    m_active_announcement_tex = pAnnTex;

    if (szSound && szSound[0]) {
        gEngfuncs.pfnPlaySoundByName(szSound, 1.0f);
    }
}

void CHudKillEffect::UserCmd_CommandActivePointkill(void) {
    m_iConsecutiveHeadshots = 0;

    if (gHUD.mass_kill >= 2) {
        isMassKill = TRUE;
        MassKill_time = 100;
        int kCount = gHUD.mass_kill > 8 ? 8 : gHUD.mass_kill;
        int mkFragId = (kCount == 2 ? 6 : (12 + (kCount - 3)));
        ClientCmd("spk vox/mass.wav");
        StartCenterAnim(mkFragId, m_mass);
    } else if (gHUD.piercing_shot >= 2) {
        isPiercingShot = TRUE;
        PiercingShot_time = 100;
        int kCount = gHUD.piercing_shot > 8 ? 8 : gHUD.piercing_shot;
        int psFragId = 18 + (kCount - 2);
        ClientCmd("spk vox/piercing.wav");
        StartCenterAnim(psFragId, m_piercing);
    } else if (gHUD.bomb_shot) {
        isBombShot = TRUE;
        BombShot_time = 100;
        ClientCmd("spk vox/special_ann.wav");
        StartCenterAnim(26, &m_special[1]);
    } else if (gHUD.special_gunner) {
        isSpecialGunner = TRUE;
        SpecialGunner_time = 100;
        ClientCmd("spk vox/special_ann.wav");
        StartCenterAnim(25, &m_special[0]);
    } else if (gHUD.slugger_kill) {
        isSlugger = TRUE;
        Slugger_time = 100;
        ClientCmd("spk vox/chainslugger.wav");
        StartCenterAnim(5, m_chslugger);
    } else {
        StartCenterAnim(last_frag_id >= 0 ? last_frag_id : 0);
    }
}

void CHudKillEffect::UserCmd_CommandActiveHeadshotPoint(void) {
    m_iConsecutiveHeadshots++;

    if (m_iConsecutiveHeadshots >= 2) {
        isChainHeadshot = TRUE;
        ChainHeadshot_time = 100;
        ClientCmd("spk vox/chainHeadshot.wav");
        StartCenterAnim(last_frag_id >= 0 ? last_frag_id : 1, m_chheadshot);
    } else {
        isHeadshot = TRUE;
        Headshot_time = 100;
        ClientCmd("spk vox/headshot.wav");
        StartCenterAnim(last_frag_id >= 0 ? last_frag_id : 1, m_headshot);
    }
}

void CHudKillEffect::UserCmd_CommandActiveDoublekill(void) {
    m_iConsecutiveHeadshots = 0;
    isDoublekill = TRUE;
    Doublekill_time = 100;
    ClientCmd("spk vox/doublekill.wav");
    StartCenterAnim(last_frag_id >= 0 ? last_frag_id : 0, m_kill2);
}

void CHudKillEffect::UserCmd_CommandActiveTriplekill(void) {
    m_iConsecutiveHeadshots = 0;
    isTriplekill = TRUE;
    Triplekill_time = 100;
    ClientCmd("spk vox/triplekill.wav");
    StartCenterAnim(last_frag_id >= 0 ? last_frag_id : 0, m_kill3);
}

void CHudKillEffect::UserCmd_CommandActiveChainkiller(void) {
    m_iConsecutiveHeadshots = 0;
    isChainkiller = TRUE;
    Chainkiller_time = 100;
    ClientCmd("spk vox/chainkiller.wav");
    StartCenterAnim(last_frag_id >= 0 ? last_frag_id : 0, m_kill4);
}

void CHudKillEffect::UserCmd_CommandActiveHeadshot(void) {
    m_iConsecutiveHeadshots = 1;
    isHeadshot = TRUE;
    Headshot_time = 100;
    ClientCmd("spk vox/headshot.wav");
    StartCenterAnim(last_frag_id >= 0 ? last_frag_id : 1, m_headshot);
}

void CHudKillEffect::UserCmd_CommandActiveChainHeadshot(void) {
    m_iConsecutiveHeadshots++;
    isChainHeadshot = TRUE;
    ChainHeadshot_time = 100;
    ClientCmd("spk vox/chainHeadshot.wav");
    StartCenterAnim(last_frag_id >= 0 ? last_frag_id : 1, m_chheadshot);
}

void CHudKillEffect::UserCmd_CommandActiveStopper(void) {
    isStopper = TRUE;
    Stopper_time = 100;
    ClientCmd("spk vox/chainstopper.wav");
    StartCenterAnim(last_frag_id >= 0 ? last_frag_id : 2, m_stopper);
}

void CHudKillEffect::UserCmd_CommandActiveMissionComplete(void) { MissionComplete_time = 250; }
void CHudKillEffect::UserCmd_CommandActivekillframe(void) { killframe_time = 40; }
void CHudKillEffect::UserCmd_CommandActivekillframeAnim(void) { killframeAnim_time = 35; }
void CHudKillEffect::UserCmd_CommandActiveOneshotEnable(void) {}
void CHudKillEffect::UserCmd_CommandActiveOneshotDisable(void) {}

void CHudKillEffect::UserCmd_CommandActivePiercingShot(void) {
    isPiercingShot = TRUE;
    PiercingShot_time = 100;
    int kCount = (gHUD.piercing_shot >= 2 ? gHUD.piercing_shot : 2);
    if (kCount > 8) kCount = 8;
    int psFragId = 18 + (kCount - 2);
    ClientCmd("spk vox/piercing.wav");
    StartCenterAnim(psFragId, m_piercing);
}

void CHudKillEffect::UserCmd_CommandActiveMassKill(void) {
    isMassKill = TRUE;
    MassKill_time = 100;
    int kCount = (gHUD.mass_kill >= 2 ? gHUD.mass_kill : 2);
    if (kCount > 8) kCount = 8;
    int mkFragId = (kCount == 2 ? 6 : (12 + (kCount - 3)));
    ClientCmd("spk vox/mass.wav");
    StartCenterAnim(mkFragId, m_mass);
}

void CHudKillEffect::UserCmd_CommandActiveSlugger(void) {
    isSlugger = TRUE;
    Slugger_time = 100;
    ClientCmd("spk vox/chainslugger.wav");
    StartCenterAnim(5, m_chslugger);
}

void CHudKillEffect::UserCmd_CommandActivePointNumber(void) {}
void CHudKillEffect::UserCmd_CommandActiveHitMarker(void) {}

void CHudKillEffect::UserCmd_CommandActiveHotKiller(void) {
    isHotKiller = TRUE;
    HotKiller_time = 100;
    ClientCmd("spk vox/special_ann.wav");
    StartCenterAnim(3, m_hotkiller);
}

void CHudKillEffect::UserCmd_CommandActiveNightmare(void) {
    isNightmare = TRUE;
    Nightmare_time = 100;
    ClientCmd("spk vox/special_ann.wav");
    StartCenterAnim(4, m_nightmare);
}

void CHudKillEffect::UserCmd_CommandActiveassist(void) {
    assist_time = 80;
}

void CHudKillEffect::UserCmd_CommandActiveFragAnimKill(void) {
    if (!is_blood_anim_active) StartCenterAnim(0);
    else { last_frag_id = 0; m_pending_frag_id = 0; m_pending_frag_added = false; }
}
void CHudKillEffect::UserCmd_CommandActiveFragAnimHs(void) {
    if (!is_blood_anim_active) StartCenterAnim(1);
    else { last_frag_id = 1; m_pending_frag_id = 1; m_pending_frag_added = false; }
}
void CHudKillEffect::UserCmd_CommandActiveFragAnimStopper(void) {
    if (!is_blood_anim_active) StartCenterAnim(2);
    else { last_frag_id = 2; m_pending_frag_id = 2; m_pending_frag_added = false; }
}
void CHudKillEffect::UserCmd_CommandActiveFragAnimStopperHs(void) {
    if (!is_blood_anim_active) StartCenterAnim(7);
    else { last_frag_id = 7; m_pending_frag_id = 7; m_pending_frag_added = false; }
}
void CHudKillEffect::UserCmd_CommandActiveFragAnimBlue(void) {
    if (!is_blood_anim_active) StartCenterAnim(3);
    else { last_frag_id = 3; m_pending_frag_id = 3; m_pending_frag_added = false; }
}
void CHudKillEffect::UserCmd_CommandActiveFragAnimGold(void) {
    if (!is_blood_anim_active) StartCenterAnim(4);
    else { last_frag_id = 4; m_pending_frag_id = 4; m_pending_frag_added = false; }
}
void CHudKillEffect::UserCmd_CommandActiveSpecialGunner(void) {
    isSpecialGunner = TRUE;
    SpecialGunner_time = 100;
    ClientCmd("spk vox/special_ann.wav");
    StartCenterAnim(25, &m_special[0]);
}
void CHudKillEffect::UserCmd_CommandActiveBombShot(void) {
    isBombShot = TRUE;
    BombShot_time = 100;
    ClientCmd("spk vox/special_ann.wav");
    StartCenterAnim(26, &m_special[1]);
}
void CHudKillEffect::UserCmd_CommandActiveoneShot(void) {
    oneShot_time = 100;
    ClientCmd("spk vox/special_ann.wav");
    StartCenterAnim(27, &m_special[2]);
}
void CHudKillEffect::UserCmd_CommandActiveHelmet(void) {
    isHelmet = TRUE;
    Helmet_time = 100;
    gHUD.helmet_on = FALSE;

    int snd = rand() % 3;
    if (snd == 0) ClientCmd("spk vox/Helmet_Hit_Defence_1.wav");
    else if (snd == 1) ClientCmd("spk vox/Helmet_Hit_Defence_2.wav");
    else ClientCmd("spk vox/Helmet_Hit_Defence_3.wav");

    ClientCmd("spk vox/helmet.wav");
}

// --- MsgFunc Hooks ---
int CHudKillEffect::MsgFunc_Pointkill(const char *pszName, int iSize, void *pbuf) { UserCmd_CommandActivePointkill(); return 1; }
int CHudKillEffect::MsgFunc_HeadshotPoint(const char *pszName, int iSize, void *pbuf) { UserCmd_CommandActiveHeadshotPoint(); return 1; }
int CHudKillEffect::MsgFunc_Doublekill(const char *pszName, int iSize, void *pbuf) { UserCmd_CommandActiveDoublekill(); return 1; }
int CHudKillEffect::MsgFunc_Triplekill(const char *pszName, int iSize, void *pbuf) { UserCmd_CommandActiveTriplekill(); return 1; }
int CHudKillEffect::MsgFunc_Chainkiller(const char *pszName, int iSize, void *pbuf) { UserCmd_CommandActiveChainkiller(); return 1; }
int CHudKillEffect::MsgFunc_Headshot(const char *pszName, int iSize, void *pbuf) { UserCmd_CommandActiveHeadshot(); return 1; }
int CHudKillEffect::MsgFunc_ChainHeadshot(const char *pszName, int iSize, void *pbuf) { UserCmd_CommandActiveChainHeadshot(); return 1; }
int CHudKillEffect::MsgFunc_Stopper(const char *pszName, int iSize, void *pbuf) { UserCmd_CommandActiveStopper(); return 1; }
int CHudKillEffect::MsgFunc_Helmet(const char *pszName, int iSize, void *pbuf) { UserCmd_CommandActiveHelmet(); return 1; }
int CHudKillEffect::MsgFunc_Slugger(const char *pszName, int iSize, void *pbuf) { UserCmd_CommandActiveSlugger(); return 1; }
int CHudKillEffect::MsgFunc_Add_point(const char *pszName, int iSize, void *pbuf) { return 1; }
int CHudKillEffect::MsgFunc_killframe(const char *pszName, int iSize, void *pbuf) { UserCmd_CommandActivekillframe(); return 1; }
int CHudKillEffect::MsgFunc_killframeAnim(const char *pszName, int iSize, void *pbuf) { UserCmd_CommandActivekillframeAnim(); return 1; }
int CHudKillEffect::MsgFunc_MissionComplete(const char *pszName, int iSize, void *pbuf) { UserCmd_CommandActiveMissionComplete(); return 1; }
int CHudKillEffect::MsgFunc_PiercingShot(const char *pszName, int iSize, void *pbuf) { UserCmd_CommandActivePiercingShot(); return 1; }
int CHudKillEffect::MsgFunc_MassKill(const char *pszName, int iSize, void *pbuf) { UserCmd_CommandActiveMassKill(); return 1; }
int CHudKillEffect::MsgFunc_OneshotEnable(const char *pszName, int iSize, void *pbuf) { UserCmd_CommandActiveOneshotEnable(); return 1; }
int CHudKillEffect::MsgFunc_OneshotDisable(const char *pszName, int iSize, void *pbuf) { UserCmd_CommandActiveOneshotDisable(); return 1; }
int CHudKillEffect::MsgFunc_PointNumber(const char *pszName, int iSize, void *pbuf) { UserCmd_CommandActivePointNumber(); return 1; }
int CHudKillEffect::MsgFunc_HitMarker(const char *pszName, int iSize, void *pbuf) { UserCmd_CommandActiveHitMarker(); return 1; }
int CHudKillEffect::MsgFunc_HotKiller(const char *pszName, int iSize, void *pbuf) { UserCmd_CommandActiveHotKiller(); return 1; }
int CHudKillEffect::MsgFunc_Nightmare(const char *pszName, int iSize, void *pbuf) { UserCmd_CommandActiveNightmare(); return 1; }
int CHudKillEffect::MsgFunc_SpecialGunner(const char *pszName, int iSize, void *pbuf) { UserCmd_CommandActiveSpecialGunner(); return 1; }
int CHudKillEffect::MsgFunc_BombShot(const char *pszName, int iSize, void *pbuf) { UserCmd_CommandActiveBombShot(); return 1; }
int CHudKillEffect::MsgFunc_oneShot(const char *pszName, int iSize, void *pbuf) { UserCmd_CommandActiveoneShot(); return 1; }
int CHudKillEffect::MsgFunc_FragAnimKill(const char *pszName, int iSize, void *pbuf) { UserCmd_CommandActiveFragAnimKill(); return 1; }
int CHudKillEffect::MsgFunc_FragAnimHs(const char *pszName, int iSize, void *pbuf) { UserCmd_CommandActiveFragAnimHs(); return 1; }
int CHudKillEffect::MsgFunc_FragAnimStopper(const char *pszName, int iSize, void *pbuf) { UserCmd_CommandActiveFragAnimStopper(); return 1; }
int CHudKillEffect::MsgFunc_FragAnimStopperHs(const char *pszName, int iSize, void *pbuf) { UserCmd_CommandActiveFragAnimStopperHs(); return 1; }
int CHudKillEffect::MsgFunc_FragAnimBlue(const char *pszName, int iSize, void *pbuf) { UserCmd_CommandActiveFragAnimBlue(); return 1; }
int CHudKillEffect::MsgFunc_FragAnimGold(const char *pszName, int iSize, void *pbuf) { UserCmd_CommandActiveFragAnimGold(); return 1; }

// --- Global CVars ---
cvar_t *mission_kill, *mission_doublekill, *mission_triplekill, *mission_chainkiller;
cvar_t *mission_headshot, *mission_chainheadshot, *mission_slugger, *mission_masskill, *mission_piercingshot, *pb_point;

// --- Class Initialization ---
int CHudKillEffect::Init() {
    HOOK_MESSAGE(Add_point); HOOK_COMMAND("Add_point", CommandActiveAdd_point);
    HOOK_MESSAGE(Count_unit); HOOK_COMMAND("Count_unit", CommandActiveCount_unit);
    HOOK_MESSAGE(Unequip_mask); HOOK_COMMAND("Unequip_mask", CommandActiveUnequip_mask);
    HOOK_MESSAGE(buy_qc); HOOK_COMMAND("buy_qc", CommandActivebuy_qc);
    HOOK_MESSAGE(buy_megahp); HOOK_COMMAND("buy_megahp", CommandActivebuy_megahp);
    HOOK_MESSAGE(buy_bpoint); HOOK_COMMAND("buy_bpoint", CommandActivebuy_bpoint);
    HOOK_MESSAGE(buy_qr); HOOK_COMMAND("buy_qr", CommandActivebuy_qr);
    HOOK_MESSAGE(buy_qrespawn); HOOK_COMMAND("buy_qrespawn", CommandActivebuy_qrespawn);
    
    HOOK_MESSAGE(buy_mask_1); HOOK_COMMAND("buy_mask_1", CommandActivebuy_mask_1);
    HOOK_MESSAGE(buy_mask_2); HOOK_COMMAND("buy_mask_2", CommandActivebuy_mask_2);
    HOOK_MESSAGE(buy_mask_3); HOOK_COMMAND("buy_mask_3", CommandActivebuy_mask_3);
    HOOK_MESSAGE(buy_mask_4); HOOK_COMMAND("buy_mask_4", CommandActivebuy_mask_4);
    HOOK_MESSAGE(buy_mask_5); HOOK_COMMAND("buy_mask_5", CommandActivebuy_mask_5);
    HOOK_MESSAGE(buy_mask_6); HOOK_COMMAND("buy_mask_6", CommandActivebuy_mask_6);
    HOOK_MESSAGE(buy_mask_7); HOOK_COMMAND("buy_mask_7", CommandActivebuy_mask_7);
    HOOK_MESSAGE(buy_mask_8); HOOK_COMMAND("buy_mask_8", CommandActivebuy_mask_8);
    HOOK_MESSAGE(buy_mask_9); HOOK_COMMAND("buy_mask_9", CommandActivebuy_mask_9);
    HOOK_MESSAGE(buy_mask_10); HOOK_COMMAND("buy_mask_10", CommandActivebuy_mask_10);
    HOOK_MESSAGE(buy_mask_11); HOOK_COMMAND("buy_mask_11", CommandActivebuy_mask_11);
    HOOK_MESSAGE(buy_mask_12); HOOK_COMMAND("buy_mask_12", CommandActivebuy_mask_12);
    HOOK_MESSAGE(buy_mask_13); HOOK_COMMAND("buy_mask_13", CommandActivebuy_mask_13);

    HOOK_MESSAGE(killframe); HOOK_COMMAND("killframe", CommandActivekillframe);
    HOOK_MESSAGE(killframeAnim); HOOK_COMMAND("killframeAnim", CommandActivekillframeAnim);
    HOOK_MESSAGE(MissionComplete); HOOK_COMMAND("MissionComplete", CommandActiveMissionComplete);
    HOOK_MESSAGE(Pointkill); HOOK_COMMAND("Pointkill", CommandActivePointkill);
    HOOK_MESSAGE(PiercingShot); HOOK_COMMAND("PiercingShot", CommandActivePiercingShot);
    HOOK_MESSAGE(MassKill); HOOK_COMMAND("MassKill", CommandActiveMassKill);
    HOOK_MESSAGE(Doublekill); HOOK_COMMAND("Doublekill", CommandActiveDoublekill);
    HOOK_MESSAGE(Triplekill); HOOK_COMMAND("Triplekill", CommandActiveTriplekill);
    HOOK_MESSAGE(Chainkiller); HOOK_COMMAND("Chainkiller", CommandActiveChainkiller);
    HOOK_MESSAGE(HeadshotPoint); HOOK_COMMAND("HeadshotPoint", CommandActiveHeadshotPoint);
    HOOK_MESSAGE(Headshot); HOOK_COMMAND("Headshot", CommandActiveHeadshot);
    HOOK_MESSAGE(ChainHeadshot); HOOK_COMMAND("ChainHeadshot", CommandActiveChainHeadshot);
    HOOK_MESSAGE(Helmet); HOOK_COMMAND("Helmet", CommandActiveHelmet);
    HOOK_MESSAGE(Stopper); HOOK_COMMAND("Stopper", CommandActiveStopper);
    HOOK_MESSAGE(Slugger); HOOK_COMMAND("Slugger", CommandActiveSlugger);
    HOOK_MESSAGE(PointNumber); HOOK_COMMAND("PointNumber", CommandActivePointNumber);
    HOOK_MESSAGE(HitMarker); HOOK_COMMAND("HitMarker", CommandActiveHitMarker);
    HOOK_MESSAGE(HotKiller); HOOK_COMMAND("HotKiller", CommandActiveHotKiller);
    HOOK_MESSAGE(Nightmare); HOOK_COMMAND("Nightmare", CommandActiveNightmare);
    HOOK_COMMAND("assist", CommandActiveassist);
    HOOK_MESSAGE(FragAnimKill); HOOK_COMMAND("FragAnimKill", CommandActiveFragAnimKill);
    HOOK_MESSAGE(FragAnimHs); HOOK_COMMAND("FragAnimHs", CommandActiveFragAnimHs);
    HOOK_MESSAGE(FragAnimStopper); HOOK_COMMAND("FragAnimStopper", CommandActiveFragAnimStopper);
    HOOK_MESSAGE(FragAnimStopperHs); HOOK_COMMAND("FragAnimStopperHs", CommandActiveFragAnimStopperHs);
    HOOK_MESSAGE(FragAnimBlue); HOOK_COMMAND("FragAnimBlue", CommandActiveFragAnimBlue);
    HOOK_MESSAGE(FragAnimGold); HOOK_COMMAND("FragAnimGold", CommandActiveFragAnimGold);
    HOOK_MESSAGE(SpecialGunner); HOOK_COMMAND("SpecialGunner", CommandActiveSpecialGunner);
    HOOK_MESSAGE(BombShot); HOOK_COMMAND("BombShot", CommandActiveBombShot);
    HOOK_MESSAGE(oneShot); HOOK_COMMAND("oneShot", CommandActiveoneShot);
    HOOK_MESSAGE(OneshotEnable); HOOK_COMMAND("OneshotEnable", CommandActiveOneshotEnable);
    m_iFlags = HUD_DRAW;
    gHUD.AddHudElem(this);
    return 1;
}

int CHudKillEffect::VidInit() {
    m_iFlags = HUD_DRAW;
    R_InitTextureBillflx(m_killframe, "frame/frame.png");
    R_InitTextureBillflx(m_fraganim[0], "fraganim/Frag_Kill.png");
    R_InitTextureBillflx(m_fraganim[1], "fraganim/Frag_Headshot.png");
    R_InitTextureBillflx(m_fraganim[2], "fraganim/Frag_Stopper.png");
    R_InitTextureBillflx(m_fraganim[3], "fraganim/Frag_Blue_1.png");
    R_InitTextureBillflx(m_fraganim[4], "fraganim/Frag_Gold_1.png");
    R_InitTextureBillflx(m_fraganim[5], "fraganim/Frag_Melee.png");
    R_InitTextureBillflx(m_fraganim[6], "fraganim/Frag_Masskill2.png");
    R_InitTextureBillflx(m_fraganim[7], "fraganim/Frag_StopperHS.png");
    R_InitTextureBillflx(m_fraganim[8], "fraganim/Frag_Silver_1.png");
    R_InitTextureBillflx(m_fraganim[9], "fraganim/Frag_MeleeHS.png");
    R_InitTextureBillflx(m_fraganim[10], "fraganim/Frag_StopperMelee.png");
    R_InitTextureBillflx(m_fraganim[11], "fraganim/Frag_StopperMeleeHS.png");
    R_InitTextureBillflx(m_fraganim[12], "fraganim/Frag_Masskill3.png");
    R_InitTextureBillflx(m_fraganim[13], "fraganim/Frag_Masskill4.png");
    R_InitTextureBillflx(m_fraganim[14], "fraganim/Frag_Masskill5.png");
    R_InitTextureBillflx(m_fraganim[15], "fraganim/Frag_Masskill6.png");
    R_InitTextureBillflx(m_fraganim[16], "fraganim/Frag_Masskill7.png");
    R_InitTextureBillflx(m_fraganim[17], "fraganim/Frag_Masskill8.png");

    // Piercing and Special weapon animations (fallback to Kill icon if dedicated anim missing)
    for (int p = 18; p <= 27; p++) {
        R_InitTextureBillflx(m_fraganim[p], "fraganim/Frag_Kill.png");
    }
    
    // Separate Bottom Frag History Stars (Loaded from gfx/billflx/star/)
    R_InitTextureBillflx(m_star[0], "star/star_kill.png");
    R_InitTextureBillflx(m_star[1], "star/star_hs.png");
    R_InitTextureBillflx(m_star[2], "star/star_stopper.png");
    R_InitTextureBillflx(m_star[3], "star/star_blue.png");
    R_InitTextureBillflx(m_star[4], "star/star_gold.png");
    R_InitTextureBillflx(m_star[5], "star/star_melee.png");
    R_InitTextureBillflx(m_star[6], "star/star_masskill2.png", "star/star_masskill.png");
    R_InitTextureBillflx(m_star[7], "star/star_stopper_hs.png");
    R_InitTextureBillflx(m_star[8], "star/star_silver.png");
    R_InitTextureBillflx(m_star[9], "star/star_melee_hs.png");
    R_InitTextureBillflx(m_star[10], "star/star_stopper_melee.png", "star/star_stopper.png");
    R_InitTextureBillflx(m_star[11], "star/star_stopper_melee_hs.png", "star/star_stopper_hs.png");

    // MassKill 3..8 stars
    R_InitTextureBillflx(m_star[12], "star/star_masskill3.png");
    R_InitTextureBillflx(m_star[13], "star/star_masskill4.png");
    R_InitTextureBillflx(m_star[14], "star/star_masskill5.png");
    R_InitTextureBillflx(m_star[15], "star/star_masskill6.png");
    R_InitTextureBillflx(m_star[16], "star/star_masskill7.png");
    R_InitTextureBillflx(m_star[17], "star/star_masskill8.png");

    // Piercing Shot 2..8 stars
    R_InitTextureBillflx(m_star[18], "star/star_piercing2.png", "star/star_piercing.png");
    R_InitTextureBillflx(m_star[19], "star/star_piercing3.png", "star/star_piercing.png");
    R_InitTextureBillflx(m_star[20], "star/star_piercing4.png", "star/star_piercing.png");
    R_InitTextureBillflx(m_star[21], "star/star_piercing5.png", "star/star_piercing.png");
    R_InitTextureBillflx(m_star[22], "star/star_piercing6.png", "star/star_piercing.png");
    R_InitTextureBillflx(m_star[23], "star/star_piercing7.png", "star/star_piercing.png");
    R_InitTextureBillflx(m_star[24], "star/star_piercing8.png", "star/star_piercing.png");

    R_InitTextureBillflx(m_star[25], "star/star_sg.png");
    R_InitTextureBillflx(m_star[26], "star/star_bs.png");
    R_InitTextureBillflx(m_star[27], "star/star_oneshot.png");

    R_InitTextureBillflx(m_kill2[0], "announcement/double.png");
    R_InitTextureBillflx(m_kill3[0], "announcement/triple.png");
    R_InitTextureBillflx(m_kill4[0], "announcement/chkill.png");
    R_InitTextureBillflx(m_headshot[0], "announcement/hs.png");
    R_InitTextureBillflx(m_chheadshot[0], "announcement/chhs.png");
    R_InitTextureBillflx(m_chslugger[0], "announcement/chslug.png");
    R_InitTextureBillflx(m_stopper[0], "announcement/chstop.png");
    R_InitTextureBillflx(m_piercing[0], "announcement/piercing.png");
    R_InitTextureBillflx(m_mass[0], "announcement/masskill.png");
    R_InitTextureBillflx(m_hotkiller[0], "announcement/hotkill.png");
    R_InitTextureBillflx(m_nightmare[0], "announcement/night.png");
    R_InitTextureBillflx(m_special[0], "announcement/sg.png");
    R_InitTextureBillflx(m_special[1], "announcement/bs.png");
    R_InitTextureBillflx(m_special[2], "announcement/oneshot.png");
    R_InitTextureBillflx(m_helmet[0], "announcement/helmet.png");
    R_InitTextureBillflx(m_assist[0], "announcement/assist.png");
    
    mission_kill = CVAR_CREATE("billflxcrypted_mission_kill", "0", 0);
    pb_point = CVAR_CREATE("billflxencrypted_pb_points", "0", 0);
    
    m_fragCount = 0;
    return 1;
}

void CHudKillEffect::DrawFragRow() {
    if (m_fragCount <= 0)
        return;

    int starW = 32;
    int spacing = 36;
    int totalWidth = m_fragCount * spacing - (spacing - starW);
    int startX = ScreenWidth / 2 - totalWidth / 2;
    int finalY = ScreenHeight - 100;

    for (int i = 0; i < m_fragCount; i++) {
        int posX = startX + (i * spacing);
        int fId = m_fragHistory[i];
        if (fId < 0 || fId >= 32)
            fId = 0;
        
        UniqueTexture *pTex = (m_star[fId] ? &m_star[fId] : (m_fraganim[fId] ? &m_fraganim[fId] : &m_star[0]));
        if (!pTex || !(*pTex))
            continue;

        (*pTex)->Bind();
        gEngfuncs.pTriAPI->RenderMode(kRenderTransAlpha);
        gEngfuncs.pTriAPI->Brightness(1.0f);
        gEngfuncs.pTriAPI->Color4ub(255, 255, 255, 255);
        DrawUtils::Draw2DQuad(posX, finalY, posX + starW, finalY + starW);
    }
}

int CHudKillEffect::Draw(float flTime) {
    m_iFlags |= HUD_DRAW;

    // 1. Draw settled bottom star history row at all times
    DrawFragRow();
    
    // 2. Draw Active Kill Effect (Kill Frame + Center Frag Icon Pop + Glide to Star Row)
    if (is_blood_anim_active) {
        int centerX = ScreenWidth / 2;
        int centerY = ScreenHeight / 2 - 20;

        float elapsed = (m_center_anim_start_time > 0.0f) ? (flTime - m_center_anim_start_time) : 0.0f;
        if (elapsed < 0.0f) elapsed = 0.0f;

        const float kTotalDuration = 1.15f;
        const float kGlideStart = 0.50f;
        const float kGlideEnd = 1.00f;

        if (elapsed < kTotalDuration) {
            // A. KILL FRAME ANIMATION: Square frame centered behind frag icon
            if (m_killframe && elapsed < 0.85f) {
                float frameScale = 1.0f;
                float frameAlpha = 255.0f;

                if (elapsed < 0.12f) {
                    float p = elapsed / 0.12f;
                    frameScale = 1.30f - p * 0.30f;
                } else if (elapsed >= kGlideStart) {
                    float p = (elapsed - kGlideStart) / (0.85f - kGlideStart);
                    if (p > 1.0f) p = 1.0f;
                    frameAlpha = 255.0f * (1.0f - p);
                }

                float baseFrameSize = 88.0f * frameScale;

                m_killframe->Bind();
                gEngfuncs.pTriAPI->RenderMode(kRenderTransAlpha);
                gEngfuncs.pTriAPI->Brightness(1.0f);
                gEngfuncs.pTriAPI->Color4ub(255, 255, 255, (int)frameAlpha);
                DrawUtils::Draw2DQuad((int)(centerX - baseFrameSize / 2.0f), (int)(centerY - baseFrameSize / 2.0f),
                                      (int)(centerX + baseFrameSize / 2.0f), (int)(centerY + baseFrameSize / 2.0f));
            }

            // B. CENTER FRAG ICON ANIMATION
            int activeFragId = last_frag_id;
            if (activeFragId < 0 || activeFragId >= 32 || !m_fraganim[activeFragId])
                activeFragId = 0;

            if (m_fraganim[activeFragId]) {
                float curX = (float)centerX;
                float curY = (float)centerY;
                float curW = 60.0f;
                float curH = 60.0f;
                float fragAlpha = 255.0f;

                if (elapsed < 0.12f) {
                    float p = elapsed / 0.12f;
                    float scale = 1.30f - p * 0.30f;
                    curW *= scale;
                    curH *= scale;
                } else if (elapsed >= kGlideStart) {
                    float p = (elapsed - kGlideStart) / (kGlideEnd - kGlideStart);
                    if (p > 1.0f) p = 1.0f;
                    float smoothP = p * p * (3.0f - 2.0f * p);

                    int starW = 32;
                    int spacing = 36;
                    int rowStartX = ScreenWidth / 2 - ((m_fragCount < 8 ? (m_fragCount + 1) : 8) * spacing - (spacing - starW)) / 2;
                    int finalY = ScreenHeight - 100;
                    float targetX = (float)(rowStartX + (m_fragCount < 8 ? m_fragCount : 7) * spacing + starW / 2);
                    float targetY = (float)(finalY + starW / 2);

                    curX = (float)centerX + (targetX - (float)centerX) * smoothP;
                    curY = (float)centerY + (targetY - (float)centerY) * smoothP;
                    curW = 60.0f + (32.0f - 60.0f) * smoothP;
                    curH = 60.0f + (32.0f - 60.0f) * smoothP;

                    if (p >= 0.95f && !m_pending_frag_added && m_pending_frag_id >= 0) {
                        AddFragToHistory(m_pending_frag_id);
                        m_pending_frag_added = true;
                    }
                }

                if (!m_pending_frag_added) {
                    m_fraganim[activeFragId]->Bind();
                    gEngfuncs.pTriAPI->RenderMode(kRenderTransAlpha);
                    gEngfuncs.pTriAPI->Brightness(1.0f);
                    gEngfuncs.pTriAPI->Color4ub(255, 255, 255, (int)fragAlpha);
                    DrawUtils::Draw2DQuad((int)(curX - curW / 2.0f), (int)(curY - curH / 2.0f),
                                          (int)(curX + curW / 2.0f), (int)(curY + curH / 2.0f));
                }
            }
        } else {
            if (!m_pending_frag_added && m_pending_frag_id >= 0) {
                AddFragToHistory(m_pending_frag_id);
                m_pending_frag_added = true;
            }
            if (m_queueCount > 0) {
                PlayNextQueuedAnim();
            } else {
                is_blood_anim_active = false;
                last_frag_id = -1;
                m_pending_frag_id = -1;
                m_pending_frag_added = false;
                m_active_announcement_tex = nullptr;
            }
        }
    }

    // 3. ANNOUNCEMENT BANNER ANIMATION (Bill's priority cascade)
    UniqueTexture *announcement = NULL;
    long *timer = NULL;
    if (HotKiller_time > 0) { announcement = m_hotkiller; timer = &HotKiller_time; }
    else if (Nightmare_time > 0) { announcement = m_nightmare; timer = &Nightmare_time; }
    else if (assist_time > 0) { announcement = m_assist; timer = &assist_time; }
    else if (oneShot_time > 0) { announcement = &m_special[2]; timer = &oneShot_time; }
    else if (BombShot_time > 0) { announcement = &m_special[1]; timer = &BombShot_time; }
    else if (SpecialGunner_time > 0) { announcement = &m_special[0]; timer = &SpecialGunner_time; }
    else if (PiercingShot_time > 0) { announcement = m_piercing; timer = &PiercingShot_time; }
    else if (MassKill_time > 0) { announcement = m_mass; timer = &MassKill_time; }
    else if (Chainkiller_time > 0) { announcement = m_kill4; timer = &Chainkiller_time; }
    else if (Triplekill_time > 0) { announcement = m_kill3; timer = &Triplekill_time; }
    else if (Doublekill_time > 0) { announcement = m_kill2; timer = &Doublekill_time; }
    else if (ChainHeadshot_time > 0) { announcement = m_chheadshot; timer = &ChainHeadshot_time; }
    else if (Slugger_time > 0) { announcement = m_chslugger; timer = &Slugger_time; }
    else if (Stopper_time > 0) { announcement = m_stopper; timer = &Stopper_time; }
    else if (Helmet_time > 0) { announcement = m_helmet; timer = &Helmet_time; }
    else if (Headshot_time > 0) { announcement = m_headshot; timer = &Headshot_time; }
    else if (m_active_announcement_tex && m_active_announcement_tex[0]) { announcement = m_active_announcement_tex; }

    if (announcement && announcement[0]) {
        int cx = ScreenWidth / 2;
        int cy = ScreenHeight / 2 - 90;
        float alpha = 255.0f;
        if (timer) {
            alpha = (*timer < 20) ? (*timer / 20.0f) * 255.0f : 255.0f;
            *timer -= 1;
        }
        announcement[0]->Bind();
        gEngfuncs.pTriAPI->RenderMode(kRenderTransAlpha);
        gEngfuncs.pTriAPI->Brightness(1.0f);
        gEngfuncs.pTriAPI->Color4ub(255, 255, 255, (int)alpha);
        DrawUtils::Draw2DQuad(cx - 150, cy - 35, cx + 150, cy + 35);
    }

    return 1;
}

// --- SHOP FUNCTIONS ---
void CHudKillEffect::UserCmd_CommandActiveUnequip_mask(void)
{
ClientCmd("billflxcrypted_item_mask 0");
}

void CHudKillEffect::UserCmd_CommandActiveCount_unit(void)
{
/*if (gHUD.item_QuickDeploy->value == 1)
{
gHUD.unit_item_QuickDeploy->value -= 1;
gEngfuncs.Cvar_SetValue( "billflxcrypted_unit_quickdeploy", gHUD.unit_item_QuickDeploy->value);
}
if (gHUD.item_QuickReload->value == 1)
{
gHUD.unit_item_QuickReload->value -= 1;
gEngfuncs.Cvar_SetValue( "billflxcrypted_unit_quickreload", gHUD.unit_item_QuickReload->value);
}*/
}

void CHudKillEffect::UserCmd_CommandActiveAdd_point(void)
{
pb_point->value += 300;
gEngfuncs.Cvar_SetValue( "billflxencrypted_pb_points", pb_point->value);
}

void CHudKillEffect::UserCmd_CommandActivebuy_qrespawn(void)
{
ClientCmd("billflxcrypted_item_qrespawn 1");
ClientCmd("exec touch/notice; touch_addbutton \"notice_bg2\" \"#SUCCESS\" \"\" 0.360000 0.555870 0.660000 0.684148 255 255 255 214 4; play media/PB_15ver_Equip_on.wav");
}

void CHudKillEffect::UserCmd_CommandActivebuy_qc(void)
{
ClientCmd("billflxcrypted_quickdeploy_enable 1; billflxcrypted_bought_quickdeploy 1");
ClientCmd("exec touch/notice; touch_addbutton \"notice_bg2\" \"#SUCCESS\" \"\" 0.360000 0.555870 0.660000 0.684148 255 255 255 214 4; play media/PB_15ver_Equip_on.wav");
}

void CHudKillEffect::UserCmd_CommandActivebuy_qr(void)
{
ClientCmd("billflxcrypted_quickreload_enable 1; billflxcrypted_bought_quickreload 1");
ClientCmd("exec touch/notice; touch_addbutton \"notice_bg2\" \"#SUCCESS\" \"\" 0.360000 0.555870 0.660000 0.684148 255 255 255 214 4; play media/PB_15ver_Equip_on.wav");
}

void CHudKillEffect::UserCmd_CommandActivebuy_megahp(void)
{
ClientCmd("billflxcrypted_megahp_enable 1; billflxcrypted_bought_megahp 1");
ClientCmd("exec touch/notice; touch_addbutton \"notice_bg2\" \"#SUCCESS\" \"\" 0.360000 0.555870 0.660000 0.684148 255 255 255 214 4; play media/PB_15ver_Equip_on.wav");
}

void CHudKillEffect::UserCmd_CommandActivebuy_bpoint(void)
{
if (pb_point->value >= 0)
{
switch (Com_RandomLong(1, 20))
{
case 1: pb_point->value += 20000; break;
case 2: pb_point->value += 5000; break;
case 3: pb_point->value += 20000; break;
default: pb_point->value += 1000; break;
}
gEngfuncs.Cvar_SetValue( "billflxencrypted_pb_points", pb_point->value);
ClientCmd("exec touch/notice; touch_addbutton \"notice_bg2\" \"#POINTS GIVEN\" \"\" 0.360000 0.555870 0.660000 0.684148 255 255 255 214 4; play media/PB_15ver_Equip_on.wav");
}
}

// MsgFuncs for Shop
int CHudKillEffect::MsgFunc_buy_qc(const char *pszName, int iSize, void *pbuf ) { return 1; }
int CHudKillEffect::MsgFunc_buy_qrespawn(const char *pszName, int iSize, void *pbuf ) { return 1; }
int CHudKillEffect::MsgFunc_buy_megahp(const char *pszName, int iSize, void *pbuf ) { return 1; }
int CHudKillEffect::MsgFunc_buy_bpoint(const char *pszName, int iSize, void *pbuf ) { return 1; }
int CHudKillEffect::MsgFunc_buy_qr(const char *pszName, int iSize, void *pbuf ) { return 1; }
int CHudKillEffect::MsgFunc_Unequip_mask(const char *pszName, int iSize, void *pbuf ) { return 1; }
int CHudKillEffect::MsgFunc_Count_unit(const char *pszName, int iSize, void *pbuf ) { return 1; }

// Mask Functions
void CHudKillEffect::UserCmd_CommandActivebuy_mask_1(void) { ClientCmd("billflxcrypted_item_mask 1"); }
void CHudKillEffect::UserCmd_CommandActivebuy_mask_2(void) { ClientCmd("billflxcrypted_item_mask 2"); }
void CHudKillEffect::UserCmd_CommandActivebuy_mask_3(void) { ClientCmd("billflxcrypted_item_mask 3"); }
void CHudKillEffect::UserCmd_CommandActivebuy_mask_4(void) { ClientCmd("billflxcrypted_item_mask 4"); }
void CHudKillEffect::UserCmd_CommandActivebuy_mask_5(void) { ClientCmd("billflxcrypted_item_mask 5"); }
void CHudKillEffect::UserCmd_CommandActivebuy_mask_6(void) { ClientCmd("billflxcrypted_item_mask 6"); }
void CHudKillEffect::UserCmd_CommandActivebuy_mask_7(void) { ClientCmd("billflxcrypted_item_mask 7"); }
void CHudKillEffect::UserCmd_CommandActivebuy_mask_8(void) { ClientCmd("billflxcrypted_item_mask 8"); }
void CHudKillEffect::UserCmd_CommandActivebuy_mask_9(void) { ClientCmd("billflxcrypted_item_mask 9"); }
void CHudKillEffect::UserCmd_CommandActivebuy_mask_10(void) { ClientCmd("billflxcrypted_item_mask 10"); }
void CHudKillEffect::UserCmd_CommandActivebuy_mask_11(void) { ClientCmd("billflxcrypted_item_mask 11"); }
void CHudKillEffect::UserCmd_CommandActivebuy_mask_12(void) { ClientCmd("billflxcrypted_item_mask 12"); }
void CHudKillEffect::UserCmd_CommandActivebuy_mask_13(void) { ClientCmd("billflxcrypted_item_mask 13"); }

int CHudKillEffect::MsgFunc_buy_mask_1(const char *pszName, int iSize, void *pbuf ) { return 1; }
int CHudKillEffect::MsgFunc_buy_mask_2(const char *pszName, int iSize, void *pbuf ) { return 1; }
int CHudKillEffect::MsgFunc_buy_mask_3(const char *pszName, int iSize, void *pbuf ) { return 1; }
int CHudKillEffect::MsgFunc_buy_mask_4(const char *pszName, int iSize, void *pbuf ) { return 1; }
int CHudKillEffect::MsgFunc_buy_mask_5(const char *pszName, int iSize, void *pbuf ) { return 1; }
int CHudKillEffect::MsgFunc_buy_mask_6(const char *pszName, int iSize, void *pbuf ) { return 1; }
int CHudKillEffect::MsgFunc_buy_mask_7(const char *pszName, int iSize, void *pbuf ) { return 1; }
int CHudKillEffect::MsgFunc_buy_mask_8(const char *pszName, int iSize, void *pbuf ) { return 1; }
int CHudKillEffect::MsgFunc_buy_mask_9(const char *pszName, int iSize, void *pbuf ) { return 1; }
int CHudKillEffect::MsgFunc_buy_mask_10(const char *pszName, int iSize, void *pbuf ) { return 1; }
int CHudKillEffect::MsgFunc_buy_mask_11(const char *pszName, int iSize, void *pbuf ) { return 1; }
int CHudKillEffect::MsgFunc_buy_mask_12(const char *pszName, int iSize, void *pbuf ) { return 1; }
int CHudKillEffect::MsgFunc_buy_mask_13(const char *pszName, int iSize, void *pbuf ) { return 1; }
