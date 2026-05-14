CSPB ANDROID V12.6 :
//What's new
-new animated kill
-kill frag anim
-corrected chain stopper
-weapon fixes
-Less recoil for dual
-other fixes

CSPB ANDROID V12.8 UNSTABLE :
//What's new
-bot improvement 
-reduce speed to match pb
-added mission failed and mission success sound
-character, team, and gamemode now saved from menu
-android 13 compatible
-weapon fixes
-working radio bot
-some code changes 
-etc

CSPB ANDROID V13.1 patch for V12.8 :
//What's new
-Fix some weapon
-Added piercing shot
-Added mass kill
-Added chain slugger
-Added zombie slayer kill sound
-Fixed oa93 cannot dual mode and other duals
-Announcement now only have 1 tga image animated inside code
-Fixed radio sound being cut when player use it
-Fixed scoreboard number bugs
-More correct announcement animation 
-Revert back speed to fix step sound

CSPB ANDROID V13.6 UPDATE :
//Update 
-Fixed throwable not equip
-Added shotgun tracer
-New simplified scoreboard
-More apk to choose (android 8/9/10/11/12/13/14)
-Weapon fixes
-Added bomb shot announcement 
-Added special gunner announcement 
-Fixed unbalanced player count
-More kill mark
-Medkit fix
-Fixed how chain slugger work 
-Announcement kill animation remake only using 1 tga each
-Added keyboard overlay use enable_keyboard_overlay 1 
-You can now edit inventory at match start see inv folder

CSPB ANDROID V14.8 :
//what new
-fixed unlimited bomb ammo on compound bow
-added new point every kill given 300points (no more using command on previous)
-added 8 total masks and hats
-added quick respawn item
-fixed more bomb mission that causes crash 
-fixed equip weapons on bomb mission 
-fixed ssg69 hand model
-added Bella Rangda character

CSPB ANDROID V16 :
//Feature 
-added test hud from latest pb
-added sequentially kill effect to make more clean
-added custom black sidebar scope using weapon_sight_"name weapon" 25-39
-added sniper custom scope using weapon_sight_"name weapon" 40-49
-added c4 timer hud
-added hit mark can be resize using hitmark_size command
-added healthbar hud can be disable using enable_healthbar_overlay 0 command

CSPB ANDROID V20 :
//Updates
-removed c hand (about 7163514 people complain because how hard it is to understand)
-fixed force closed when playing bomb mission 
-some rank fixes
-bot can use scope (testing)
-fixed radio slot cannot be selected
-fixed c4 exploded when you shoot at it from ct side
-fixed death sound when killed from headshot
-corrected behave player helmet
-when inventory is open the player will not spawn until inventory is close (dm)
-added sf shotgun 
-karambit re animation 
-fixed some muted radio sound
-added 10 melee classes (amok kukri base)
-added 40 new character classes
-character script currently uses hand body group and helmet body group 
-added event 6001 for melee hit in qc, it will hit depends on what frame you put 
Example:
{ event 6001 10 } on frame 10, the melee weapon will hit player/object
{ event 6001 20 } on frame 20, the melee weapon will hit player/object
added new script for melee

CSPB ANDROID patch v20.1:
//Updates
- fixed new melee classes did not register as slugger kill
- added mapconfig (gamma, overbright, etc) for each map, you can add (your map name).mapconfig.txt, it will exec when starting map
- More buffer overflow engine protection
- faster multiplayer lan connection
