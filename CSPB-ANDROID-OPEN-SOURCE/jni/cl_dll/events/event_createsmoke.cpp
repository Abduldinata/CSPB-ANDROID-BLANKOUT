/*
*
*    This program is free software; you can redistribute it and/or modify it
*    under the terms of the GNU General Public License as published by the
*    Free Software Foundation; either version 2 of the License, or (at
*    your option) any later version.
*
*    This program is distributed in the hope that it will be useful, but
*    WITHOUT ANY WARRANTY; without even the implied warranty of
*    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
*    General Public License for more details.
*
*    You should have received a copy of the GNU General Public License
*    along with this program; if not, write to the Free Software Foundation,
*    Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
*
*    In addition, as a special exception, the author gives permission to
*    link the code of this program with the Half-Life Game Engine ("HL
*    Engine") and Modified Game Libraries ("MODs") developed by Valve,
*    L.L.C ("Valve").  You must obey the GNU General Public License in all
*    respects for all of the code used other than the HL Engine and MODs
*    from Valve.  If you modify this file, you may extend this exception
*    to your version of the file, but you are not obligated to do so.  If
*    you do not wish to do so, delete this exception statement from your
*    version.
*
*/
#include "events.h"

#include "com_model.h"

#define SMOKE_CLOUDS 20

void EV_Smoke_FadeOut( struct tempent_s *te, float frametime, float currenttime )
{
	if( te->entity.curstate.renderamt > 0 && currenttime >= te->entity.curstate.fuser3 )
	{
		te->entity.curstate.renderamt = 255.0f - (currenttime - te->entity.curstate.fuser3) * te->entity.baseline.renderamt ;
		if( te->entity.curstate.renderamt < 0 ) te->entity.curstate.renderamt = 0;
	}
	EV_CS16Client_KillEveryRound( te, frametime, currenttime );
}


void EV_CreateSmoke(event_args_s *args)
{
	TEMPENTITY *pTemp;

	int iModelIndex = gEngfuncs.pEventAPI->EV_FindModelIndex("sprites/gas_puff_01.spr");
	if (!iModelIndex)
		iModelIndex = g_iBlackSmoke;
	if (!iModelIndex)
		iModelIndex = gEngfuncs.pEventAPI->EV_FindModelIndex("sprites/black_smoke4.spr");
	if (!iModelIndex)
		iModelIndex = gEngfuncs.pEventAPI->EV_FindModelIndex("sprites/wall_puff1.spr");

	if (!iModelIndex)
		return;

	if (!args->bparam2) //first explosion
	{
		for (int i = 0; i < SMOKE_CLOUDS; i++)
		{
			// randomize smoke cloud position
			Vector org = args->origin;
			org.x += Com_RandomFloat(-100.0f, 100.0f);
			org.y += Com_RandomFloat(-100.0f, 100.0f);
			org.z += 30;

			pTemp = gEngfuncs.pEfxAPI->R_DefaultSprite(org, iModelIndex, 10.0f);
			if (pTemp)
			{
				// don't die when animation is ended
				pTemp->flags |= (FTENT_SPRANIMATELOOP | FTENT_COLLIDEWORLD | FTENT_CLIENTCUSTOM);
				pTemp->die = gEngfuncs.GetClientTime() + 30.0f;
				pTemp->callback = EV_Smoke_FadeOut;
				pTemp->entity.curstate.fuser3 = gEngfuncs.GetClientTime() + 15.0f; // start fading after 15 sec
				pTemp->entity.curstate.fuser4 = gEngfuncs.GetClientTime(); // entity creation time

				pTemp->entity.curstate.renderamt = 250;
				pTemp->entity.curstate.rendermode = kRenderTransAlpha;
				pTemp->entity.curstate.rendercolor.r = Com_RandomLong(210, 230);
				pTemp->entity.curstate.rendercolor.g = Com_RandomLong(210, 230);
				pTemp->entity.curstate.rendercolor.b = Com_RandomLong(210, 230);
				pTemp->entity.curstate.scale = 5.0f;

				// make it move slowly
				pTemp->entity.baseline.origin.x = Com_RandomLong(-5, 5);
				pTemp->entity.baseline.origin.y = Com_RandomLong(-5, 5);
				pTemp->entity.baseline.renderamt = 18;
			}
		}
	}
	else // second and other
	{
		int iSecModel = g_iBlackSmoke ? g_iBlackSmoke : iModelIndex;
		pTemp = gEngfuncs.pEfxAPI->R_DefaultSprite(args->origin, iSecModel, 6.0f);

		if (pTemp)
		{
			pTemp->flags |= (FTENT_CLIENTCUSTOM | FTENT_COLLIDEWORLD);
			pTemp->callback = EV_CS16Client_KillEveryRound;
			pTemp->entity.curstate.fuser4 = gEngfuncs.GetClientTime();

			pTemp->entity.curstate.rendermode = kRenderTransAlpha;
			pTemp->entity.curstate.renderfx = kRenderFxNone;
			pTemp->entity.curstate.rendercolor.r = Com_RandomLong(210, 230);
			pTemp->entity.curstate.rendercolor.g = Com_RandomLong(210, 230);
			pTemp->entity.curstate.rendercolor.b = Com_RandomLong(210, 230);
			pTemp->entity.curstate.renderamt = Com_RandomLong(180, 200);

			pTemp->entity.baseline.origin[0] = Com_RandomLong(10, 30);
		}
	}
}
