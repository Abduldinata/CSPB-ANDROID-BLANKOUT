/*
Copyright (C) 1997-2001 Id Software, Inc.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

*/

#include "Framework.h"
#include "keydefs.h"
#include "Bitmap.h"
#include "Field.h"
#include "CheckBox.h"
#include "SpinControl.h"
#include "PicButton.h"
#include "Table.h"
#include "Action.h"
#include "YesNoMessageBox.h"
#include "StringArrayModel.h"
#include "Table.h"

#define ART_BANNER		"gfx/shell/head_creategame"

struct map_t
{
	char name[CS_SIZE];
	char desc[CS_SIZE];
};

static const char *g_GameModeLabels[] =
{
	"TDM / Deathmatch",
	"Bomb/Eliminate",
	"Sniper Mode",
	"Shotgun Mode",
	"Knife Mode"
};

static const char *g_GameModeValues[] =
{
	"tdm",
	"none",
	"sniper",
	"sg",
	"knife"
};

static const char *g_BlueCharacterLabels[] =
{
	"AcidPool (Blue Team)",
	"KeenEyes (Blue Team)",
	"Leopard (Blue Team)",
	"Hide (Blue Team)",
	"JudyChou (Blue Team)"
};

static const char *g_RedCharacterLabels[] =
{
	"RedBull (Red Team)",
	"Tarantula (Red Team)",
	"DFox (Red Team)",
	"Viper (Red Team)",
	"RicaLopez (Red Team)"
};

static const char *g_CharacterValues[] =
{
	"1",
	"2",
	"3",
	"4",
	"5"
};

static const char *g_StartTeamLabels[] =
{
	"Blue Team",
	"Red Team"
};

static const char *g_StartTeamValues[] =
{
	"blue",
	"red"
};

enum
{
	CREATEGAME_DEFAULT_MODE = 0,
	CREATEGAME_DEFAULT_BLUE_CHARACTER = 0,
	CREATEGAME_DEFAULT_RED_CHARACTER = 0,
	CREATEGAME_DEFAULT_START_TEAM = 1
};

static int UI_FindChoiceIndex( const char *value, const char *const *values, int count, int fallback = 0 )
{
	if( !value || !value[0] )
		return fallback;

	for( int i = 0; i < count; ++i )
	{
		if( !strcmp( value, values[i] ))
			return i;
	}

	return fallback;
}

static int UI_FindGameModeIndex( const char *value )
{
	if( !value || !value[0] )
		return CREATEGAME_DEFAULT_MODE;

	if( !strcmp( value, "0" ) || !strcmp( value, "1" ) || !strcmp( value, "tdm" ))
		return 0;
	if( !strcmp( value, "2" ) || !strcmp( value, "original" ) || !strcmp( value, "none" ))
		return 1;
	if( !strcmp( value, "3" ) || !strcmp( value, "sniper" ) || !strcmp( value, "sniperb" ))
		return 2;
	if( !strcmp( value, "sg" ) || !strcmp( value, "sgb" ))
		return 3;
	if( !strcmp( value, "4" ) || !strcmp( value, "5" ) || !strcmp( value, "knife" ) || !strcmp( value, "knifeB" ))
		return 4;

	return CREATEGAME_DEFAULT_MODE;
}

static int UI_FindStartTeamIndex( const char *value )
{
	if( !value || !value[0] )
		return CREATEGAME_DEFAULT_START_TEAM;

	if( !strcmp( value, "blue" ) || !strcmp( value, "ct" ) || !strcmp( value, "2" ))
		return 0;
	if( !strcmp( value, "red" ) || !strcmp( value, "tr" ) || !strcmp( value, "1" ))
		return 1;

	return CREATEGAME_DEFAULT_START_TEAM;
}

static const char *UI_GetPBTeamSelectValue( int startTeamIndex )
{
	return startTeamIndex == 0 ? "2" : "1";
}

class CMenuCreateGame;

class CMenuMapListModel : public CMenuBaseModel, public CUtlVector<map_t>
{
public:
	explicit CMenuMapListModel( CMenuCreateGame *p ) : parent( p ) {}

	void Update() override;
	int GetColumns() const override { return 2; }
	int GetRows() const override { return Count(); }
	bool IsCellTextWrapped( int, int ) override { return false; }

	bool IsValidIndex( int line ) const
	{
		return line >= 0 && line < Count();
	}

	const char *GetCellText( int line, int column ) override
	{
		if( line < 0 || line >= Count() )
			return NULL;

		switch( column )
		{
		case 0: return Element( line ).name;
		case 1: return Element( line ).desc;
		default: return NULL;
		}
	}

	CMenuCreateGame *parent;
};

class CMenuCreateGame : public CMenuFramework
{
public:
	CMenuCreateGame() :
		CMenuFramework( "CMenuCreateGame" ),
		mapsListModel( this ),
		gameModeModel( g_GameModeLabels, sizeof( g_GameModeLabels ) / sizeof( g_GameModeLabels[0] )),
		startTeamModel( g_StartTeamLabels, sizeof( g_StartTeamLabels ) / sizeof( g_StartTeamLabels[0] )),
		blueCharacterModel( g_BlueCharacterLabels, sizeof( g_BlueCharacterLabels ) / sizeof( g_BlueCharacterLabels[0] )),
		redCharacterModel( g_RedCharacterLabels, sizeof( g_RedCharacterLabels ) / sizeof( g_RedCharacterLabels[0] ))
	{}

	static void Begin( CMenuBaseItem *pSelf, void *pExtra );

	void Show() override;
	void Reload() override;
	void SaveCvars();
	void ApplyStoredMapSelection();

	CMenuField maxClients;
	CMenuField hostName;
	CMenuField password;
	CMenuField botQuota;
	CMenuSpinControl gameMode;
	CMenuSpinControl startTeam;
	CMenuSpinControl blueCharacter;
	CMenuSpinControl redCharacter;
	CMenuCheckBox nat;
	CMenuYesNoMessageBox msgBox;
	CMenuTable mapsList;
	CMenuMapListModel mapsListModel;
	CStringArrayModel gameModeModel;
	CStringArrayModel startTeamModel;
	CStringArrayModel blueCharacterModel;
	CStringArrayModel redCharacterModel;
	CMenuPicButton *done;

private:
	void _Init() override;
	void _VidInit() override;
};

static int UI_FindMapIndexByName( CMenuMapListModel &model, const char *value )
{
	if( !value || !value[0] )
		return 0;

	for( int i = 0; i < model.GetRows(); ++i )
	{
		if( !strcmp( model[i].name, value ))
			return i;
	}

	return 0;
}

void CMenuCreateGame::Begin( CMenuBaseItem *pSelf, void *pExtra )
{
	CMenuCreateGame *menu = (CMenuCreateGame *)pSelf->Parent();
	int item = menu->mapsList.GetCurrentIndex();
	if( !menu->mapsListModel.IsValidIndex( item ))
		return;

	if( item == 0 )
		item = EngFuncs::RandomLong( 1, menu->mapsListModel.GetRows() - 1 );

	const char *mapName = menu->mapsListModel[item].name;

	if( !EngFuncs::IsMapValid( mapName ))
		return;

	if( EngFuncs::GetCvarFloat( "host_serverstate" ))
	{
		if( EngFuncs::GetCvarFloat( "maxplayers" ) == 1.0f )
			EngFuncs::HostEndGame( "end of the game" );
		else
			EngFuncs::HostEndGame( "starting new server" );
	}

	EngFuncs::CvarSetValue( "deathmatch", 1.0f );
	menu->SaveCvars();
	UI_SaveScriptConfig();
	UI_ApplyServerSettings();

	EngFuncs::PlayBackgroundTrack( NULL, NULL );

	char cmd[1024];

	// Server-side game rules already execute lservercfg during listen server startup.
	// Re-executing it here from the menu adds duplicate config work right before map load.
	menu->maxClients.WriteCvar();

	const int startTeamIndex = (int)menu->startTeam.GetCurrentValue();
	const int blueCharacterIndex = (int)menu->blueCharacter.GetCurrentValue();
	const int redCharacterIndex = (int)menu->redCharacter.GetCurrentValue();
	const int modeIndex = (int)menu->gameMode.GetCurrentValue();
	const int botQuota = atoi( menu->botQuota.GetBuffer() );
	const char *pbTeamSelectValue = UI_GetPBTeamSelectValue( startTeamIndex );
	const char *pbBlueSelectValue = g_CharacterValues[blueCharacterIndex];
	const char *pbRedSelectValue = g_CharacterValues[redCharacterIndex];

	EngFuncs::CvarSetString( "pb_start_team", g_StartTeamValues[startTeamIndex] );
	EngFuncs::CvarSetString( "pb_user_char_blue", g_CharacterValues[blueCharacterIndex] );
	EngFuncs::CvarSetString( "pb_user_char_red", g_CharacterValues[redCharacterIndex] );
	EngFuncs::CvarSetString( "pb_selected_map", mapName );
	EngFuncs::CvarSetString( "pbteamselect", pbTeamSelectValue );
	EngFuncs::CvarSetString( "pbblueselect", pbBlueSelectValue );
	EngFuncs::CvarSetString( "pbredselect", pbRedSelectValue );
	EngFuncs::CvarSetString( "mp_gamemode", g_GameModeValues[modeIndex] );
	EngFuncs::CvarSetValue( "bot_quota", botQuota );

	char cmd2[256];
	Com_EscapeCommand( cmd2, mapName, sizeof( cmd2 ));
	Con_Printf( "[CREATEGAME] launch=connectionprogress marker=1 map=%s maxplayers=%s bot_quota=%i start_team=%s blue=%s red=%s mode=%s mp_consistency=0\n",
		mapName,
		menu->maxClients.GetBuffer(),
		botQuota,
		g_StartTeamValues[startTeamIndex],
		g_CharacterValues[blueCharacterIndex],
		g_CharacterValues[redCharacterIndex],
		g_GameModeValues[modeIndex] );
	snprintf( cmd, sizeof( cmd ),
		"cspb_local_creategame_start 1;disconnect;menu_connectionprogress localserver;wait;wait;wait;maxplayers %i;mp_consistency 0;pb_start_team %s;pb_user_char_blue %s;pb_user_char_red %s;pb_selected_map %s;pb_active_blue_class %s;pb_active_red_class %s;pbteamselect %s;pbblueselect %s;pbredselect %s;mp_gamemode %s;pb_active_mode %s;bot_quota %i;map %s\n",
		atoi( menu->maxClients.GetBuffer() ),
		g_StartTeamValues[startTeamIndex],
		g_CharacterValues[blueCharacterIndex],
		g_CharacterValues[redCharacterIndex],
		cmd2,
		g_CharacterValues[blueCharacterIndex],
		g_CharacterValues[redCharacterIndex],
		pbTeamSelectValue,
		pbBlueSelectValue,
		pbRedSelectValue,
		g_GameModeValues[modeIndex],
		g_GameModeValues[modeIndex],
		botQuota,
		cmd2 );
	EngFuncs::ClientCmd( false, cmd );
}

void CMenuMapListModel::Update()
{
	char *afile;

	if( !uiStatic.needMapListUpdate )
		return;

	RemoveAll();

	if( !EngFuncs::CreateMapsList( true ) || ( afile = (char *)EngFuncs::COM_LoadFile( "maps.lst", NULL )) == NULL )
	{
		parent->done->SetGrayed( true );
		Con_Printf( "Cmd_GetMapsList: can't open maps.lst\n" );
		return;
	}

	{
		map_t map;
		Q_strncpy( map.name, L( "GameUI_RandomMap" ), sizeof( map.name ));
		Q_strncpy( map.desc, "", sizeof( map.desc ));
		AddToTail( map );
	}

	char *pfile = afile;
	char token[1024];

	while(( pfile = EngFuncs::COM_ParseFile( pfile, token, sizeof( token ))) != NULL )
	{
		map_t map;
		Q_strncpy( map.name, token, sizeof( map.name ));

		if(( pfile = EngFuncs::COM_ParseFile( pfile, token, sizeof( token ))) == NULL )
		{
			Q_strncpy( map.desc, map.name, sizeof( map.desc ));
			AddToTail( map );
			break;
		}

		Q_strncpy( map.desc, token, sizeof( map.desc ));
		AddToTail( map );
	}

	EngFuncs::COM_FreeFile( afile );
	parent->done->SetGrayed( Count() == 0 );
	uiStatic.needMapListUpdate = false;
}

void CMenuCreateGame::_Init()
{
	uiStatic.needMapListUpdate = true;

	banner.SetPicture( ART_BANNER );
	AddItem( banner );

	nat.szName = L( "Use NAT Bypass instead of direct mode" );
	nat.bChecked = true;
	nat.LinkCvar( "sv_nat" );

	done = AddButton( "DONE", "", PC_DONE, Begin );
	done->onReleasedClActive = msgBox.MakeOpenEvent();

	mapsList.SetCharSize( QM_SMALLFONT );
	mapsList.SetupColumn( 0, L( "GameUI_Map" ), 0.5f );
	mapsList.SetupColumn( 1, L( "Title" ), 0.5f );
	mapsList.SetModel( &mapsListModel );

	hostName.szName = "Host Name:";
	hostName.iMaxLength = 31;
	hostName.eTextAlignment = QM_CENTER;
	SET_EVENT_MULTI( hostName.onCvarGet,
	{
		CMenuField *self = (CMenuField *)pSelf;
		const char *val = UI_GetScriptCvar( self->CvarName() );
		self->SetBuffer( val && val[0] ? val : "CSPB Server" );
	});
	hostName.LinkCvar( "hostname" );

	maxClients.iMaxLength = 3;
	maxClients.bNumbersOnly = true;
	maxClients.szName = "Max Players:";
	SET_EVENT_MULTI( maxClients.onChanged,
	{
		CMenuField *self = (CMenuField *)pSelf;
		const char *buf = self->GetBuffer();
		if( buf[0] == 0 ) return;

		int players = atoi( buf );
		if( players <= 1 )
			self->SetBuffer( "2" );
		else if( players > 32 )
			self->SetBuffer( "32" );
	});
	SET_EVENT_MULTI( maxClients.onCvarGet,
	{
		CMenuField *self = (CMenuField *)pSelf;
		const char *val = UI_GetScriptCvar( self->CvarName() );
		self->SetBuffer( val );

		const char *buf = self->GetBuffer();
		int players = atoi( buf );
		if( players <= 1 )
			self->SetBuffer( "16" );
		else if( players > 32 )
			self->SetBuffer( "32" );
	});
	maxClients.LinkCvar( "maxplayers" );

	password.szName = "Password:";
	password.iMaxLength = 16;
	password.eTextAlignment = QM_CENTER;
	password.bHideInput = true;
	SET_EVENT_MULTI( password.onCvarGet,
	{
		CMenuField *self = (CMenuField *)pSelf;
		self->SetBuffer( UI_GetScriptCvar( self->CvarName() ));
	});
	password.LinkCvar( "sv_password" );

	botQuota.iMaxLength = 2;
	botQuota.bNumbersOnly = true;
	botQuota.szName = "Bot Quota:";
	SET_EVENT_MULTI( botQuota.onChanged,
	{
		CMenuField *self = (CMenuField *)pSelf;
		const char *buf = self->GetBuffer();
		if( buf[0] == 0 ) return;

		int quota = atoi( buf );
		if( quota < 0 )
			self->SetBuffer( "0" );
		else if( quota > 31 )
			self->SetBuffer( "31" );
	});
	SET_EVENT_MULTI( botQuota.onCvarGet,
	{
		CMenuField *self = (CMenuField *)pSelf;
		const char *val = UI_GetScriptCvar( self->CvarName() );
		self->SetBuffer( val && val[0] ? val : "10" );
	});
	botQuota.LinkCvar( "bot_quota" );

	gameMode.SetNameAndStatus( "Select Mode:", "Select the multiplayer ruleset used when the map starts" );
	gameMode.Setup( &gameModeModel );

	startTeam.SetNameAndStatus( "Select Team:", "Choose the team that should be active when the server starts" );
	startTeam.Setup( &startTeamModel );

	redCharacter.SetNameAndStatus( "Red Character:", "Choose the Red team class used by the server and bots" );
	redCharacter.Setup( &redCharacterModel );

	blueCharacter.SetNameAndStatus( "Blue Character:", "Choose the Blue team class used by the server and bots" );
	blueCharacter.Setup( &blueCharacterModel );

	msgBox.onPositive = Begin;
	msgBox.SetMessage( L( "Starting a new game will exit any current game, OK to exit?" ));
	msgBox.Link( this );

	AddButton( L( "GameUI_Cancel" ), NULL, PC_CANCEL, VoidCb( &CMenuCreateGame::Hide ));
	AddItem( startTeam );
	AddItem( gameMode );
	AddItem( redCharacter );
	AddItem( blueCharacter );
	AddItem( hostName );
	AddItem( maxClients );
	AddItem( password );
	AddItem( botQuota );
	AddItem( nat );
	AddItem( mapsList );
}

void CMenuCreateGame::_VidInit()
{
	nat.SetCoord( 72, 640 );
	if( !EngFuncs::GetCvarFloat( "public" ))
		nat.Hide();
	else nat.Show();

	startTeam.SetRect( 575, 56, 340, 32 );
	gameMode.SetRect( 575, 118, 340, 32 );
	redCharacter.SetRect( 575, 180, 340, 32 );
	blueCharacter.SetRect( 575, 242, 340, 32 );

	hostName.SetRect( 350, 255, 205, 32 );
	maxClients.SetRect( 350, 335, 205, 32 );
	password.SetRect( 350, 415, 205, 32 );
	botQuota.SetRect( 350, 495, 205, 32 );

	mapsList.SetRect( 575, 304, 390, 346 );
}

void CMenuCreateGame::Show()
{
	UI_LoadScriptConfig();

	if( !UI_GetScriptCvar( "mp_gamemode" )[0] )
		UI_SetScriptCvar( "mp_gamemode", g_GameModeValues[CREATEGAME_DEFAULT_MODE] );
	if( !UI_GetScriptCvar( "pb_start_team" )[0] )
		UI_SetScriptCvar( "pb_start_team", g_StartTeamValues[CREATEGAME_DEFAULT_START_TEAM] );
	if( !UI_GetScriptCvar( "pb_user_char_blue" )[0] )
		UI_SetScriptCvar( "pb_user_char_blue", g_CharacterValues[CREATEGAME_DEFAULT_BLUE_CHARACTER] );
	if( !UI_GetScriptCvar( "pb_user_char_red" )[0] )
		UI_SetScriptCvar( "pb_user_char_red", g_CharacterValues[CREATEGAME_DEFAULT_RED_CHARACTER] );
	if( !UI_GetScriptCvar( "pbteamselect" )[0] )
		UI_SetScriptCvar( "pbteamselect", UI_GetPBTeamSelectValue( CREATEGAME_DEFAULT_START_TEAM ));
	if( !UI_GetScriptCvar( "pbblueselect" )[0] )
		UI_SetScriptCvar( "pbblueselect", g_CharacterValues[CREATEGAME_DEFAULT_BLUE_CHARACTER] );
	if( !UI_GetScriptCvar( "pbredselect" )[0] )
		UI_SetScriptCvar( "pbredselect", g_CharacterValues[CREATEGAME_DEFAULT_RED_CHARACTER] );

	hostName.UpdateCvar( true );
	maxClients.UpdateCvar( true );
	password.UpdateCvar( true );
	botQuota.UpdateCvar( true );
	nat.UpdateCvar( true );
	gameMode.SetCurrentValue( (float)UI_FindGameModeIndex( UI_GetScriptCvar( "mp_gamemode" )));
	startTeam.SetCurrentValue( (float)UI_FindStartTeamIndex( UI_GetScriptCvar( "pb_start_team" )));
	redCharacter.SetCurrentValue( (float)UI_FindChoiceIndex( UI_GetScriptCvar( "pb_user_char_red" ), g_CharacterValues, sizeof( g_CharacterValues ) / sizeof( g_CharacterValues[0] ), CREATEGAME_DEFAULT_RED_CHARACTER ));
	blueCharacter.SetCurrentValue( (float)UI_FindChoiceIndex( UI_GetScriptCvar( "pb_user_char_blue" ), g_CharacterValues, sizeof( g_CharacterValues ) / sizeof( g_CharacterValues[0] ), CREATEGAME_DEFAULT_BLUE_CHARACTER ));
	ApplyStoredMapSelection();

	CMenuBaseWindow::Show();
}

void CMenuCreateGame::SaveCvars()
{
	hostName.WriteCvar();
	maxClients.WriteCvar();
	password.WriteCvar();
	botQuota.WriteCvar();

	UI_SetScriptCvar( "hostname", hostName.GetBuffer() );
	UI_SetScriptCvar( "maxplayers", maxClients.GetBuffer() );
	UI_SetScriptCvar( "sv_password", password.GetBuffer() );
	UI_SetScriptCvar( "bot_quota", botQuota.GetBuffer() );
	UI_SetScriptCvar( "mp_gamemode", g_GameModeValues[(int)gameMode.GetCurrentValue()] );
	UI_SetScriptCvar( "pb_start_team", g_StartTeamValues[(int)startTeam.GetCurrentValue()] );
	UI_SetScriptCvar( "pb_user_char_blue", g_CharacterValues[(int)blueCharacter.GetCurrentValue()] );
	UI_SetScriptCvar( "pb_user_char_red", g_CharacterValues[(int)redCharacter.GetCurrentValue()] );
	UI_SetScriptCvar( "pbteamselect", UI_GetPBTeamSelectValue((int)startTeam.GetCurrentValue() ));
	UI_SetScriptCvar( "pbblueselect", g_CharacterValues[(int)blueCharacter.GetCurrentValue()] );
	UI_SetScriptCvar( "pbredselect", g_CharacterValues[(int)redCharacter.GetCurrentValue()] );
	if( mapsListModel.IsValidIndex( mapsList.GetCurrentIndex() ))
		UI_SetScriptCvar( "pb_selected_map", mapsListModel[mapsList.GetCurrentIndex()].name );

	EngFuncs::CvarSetString( "hostname", hostName.GetBuffer() );
	EngFuncs::CvarSetString( "sv_password", password.GetBuffer() );
	EngFuncs::CvarSetValue( "maxplayers", atoi( maxClients.GetBuffer() ));
	EngFuncs::CvarSetValue( "bot_quota", atoi( botQuota.GetBuffer() ));
	EngFuncs::CvarSetString( "mp_gamemode", g_GameModeValues[(int)gameMode.GetCurrentValue()] );
	EngFuncs::CvarSetString( "pb_start_team", g_StartTeamValues[(int)startTeam.GetCurrentValue()] );
	EngFuncs::CvarSetString( "pb_user_char_blue", g_CharacterValues[(int)blueCharacter.GetCurrentValue()] );
	EngFuncs::CvarSetString( "pb_user_char_red", g_CharacterValues[(int)redCharacter.GetCurrentValue()] );
	EngFuncs::CvarSetString( "pbteamselect", UI_GetPBTeamSelectValue((int)startTeam.GetCurrentValue() ));
	EngFuncs::CvarSetString( "pbblueselect", g_CharacterValues[(int)blueCharacter.GetCurrentValue()] );
	EngFuncs::CvarSetString( "pbredselect", g_CharacterValues[(int)redCharacter.GetCurrentValue()] );

	EngFuncs::CvarSetValue( "sv_nat", EngFuncs::GetCvarFloat( "public" ) ? nat.bChecked : 0 );
}

void CMenuCreateGame::Reload()
{
	mapsListModel.Update();
	ApplyStoredMapSelection();
}

void CMenuCreateGame::ApplyStoredMapSelection()
{
	if( mapsListModel.GetRows() <= 0 )
		return;

	const char *savedMap = UI_GetScriptCvar( "pb_selected_map" );
	mapsList.SetCurrentIndex( UI_FindMapIndexByName( mapsListModel, savedMap ));
}

ADD_MENU( menu_creategame, CMenuCreateGame, UI_CreateGame_Menu );
