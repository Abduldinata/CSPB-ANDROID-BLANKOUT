import re

with open('jni/cl_dll/hud/modern/hud_radar_modern.cpp', 'r') as f:
    text = f.read()

bad_chunk = '''		HSPRITE hspr2 = 0;
		int scale = 8;
		float scale2 = 0.75;

		if (i == idx)
		{
		}
		else
		{
			if (g_PlayerExtraInfo[i].teamnumber == g_iTeamNumber)
			{
				if (g_iTeamNumber == TEAM_TERRORIST)
				{
					r = 255;
					g = 255;
					b = 255;
					hspr = m_hsprPlayerRed;

					if (g_PlayerExtraInfo[i].has_c4)
						hspr = m_hsprPlayerC4;
				}
				else if (g_iTeamNumber == TEAM_CT)
				{
					r = 255;
					g = 255;
					b = 255;
					hspr = m_hsprPlayerBlue;

					if (g_PlayerExtraInfo[i].vip)
						hspr = m_hsprPlayerVIP;
				}
			}
		}

		int rx, ry;
		float yaw = 0;

		if (i != 32)
		{
			if (hspr == 0)
				continue;

			cl_entity_t *ent = gEngfuncs.GetEntityByIndex(i);
			vec3_t *origin;
			bool valid;

			if (!IsValidEntity(ent))
			{
				valid = false;
				origin = &g_PlayerExtraInfo[i].origin;
			}'''

good_chunk = '''		}
		//glDisable(GL_SCISSOR_TEST);
		// if (g_iXash)
			// gRenderAPI.GL_Scissor(0, 0, 0, 0, 0);
	}

	DrawUtils::DrawOutlinedRect(sx / gHUD.m_flScale, sy / gHUD.m_flScale, wide / gHUD.m_flScale, tall / gHUD.m_flScale, 0, 0, 0, 255);

	DrawUtils::DrawOutlinedRect2(sx / gHUD.m_flScale, sy / gHUD.m_flScale, wide / gHUD.m_flScale, tall / gHUD.m_flScale + 40, 0, 0, 0, 200);

if (m_player) {
    gRenderAPI.GL_SelectTexture( 0 );
    gRenderAPI.GL_Bind(0, m_player);
    gEngfuncs.pTriAPI->Color4ub(255, 255, 255, 255);
    gEngfuncs.pTriAPI->RenderMode( kRenderTransAlpha );
    DrawUtils::Draw2DQuad(sx / 2, sy, wide, tall - TrueHeight / -70 ); 
}

int syy = 282;
int iLength, iHeight;

//map name
if (strlen(g_szLocation))
{
		gEngfuncs.pfnDrawSetTextColor(255, 255, 255);
		gEngfuncs.pfnDrawConsoleStringLen(g_szLocation, &iLength, &iHeight);
		gEngfuncs.pfnDrawConsoleString(64 - iLength / 1.8, tall / 1.03+ iHeight, g_szLocation);
}

	// TODO : localization

	gEngfuncs.pTriAPI->RenderMode(kRenderTransAdd);
	gEngfuncs.pTriAPI->Color4f(1, 0.62745f, 0, 1.0f);

	struct model_s* model = (struct model_s*)gEngfuncs.GetSpritePointer(m_hsprCamera);
	gEngfuncs.pTriAPI->SpriteTexture(model, 0);
	
	float cameraScale = 2;
	int cameraWide = gEngfuncs.pfnSPR_Width(m_hsprCamera, 0) * cameraScale;
	int cameraHeight = gEngfuncs.pfnSPR_Height(m_hsprCamera, 0) * cameraScale;

	gEngfuncs.pTriAPI->Begin(TRI_TRIANGLES);
	gEngfuncs.pTriAPI->TexCoord2f(1, 1);
	gEngfuncs.pTriAPI->Vertex3f(wide / 2 + cameraWide * 0.7, tall / 2 - cameraHeight * 0.7, 0);
	gEngfuncs.pTriAPI->TexCoord2f(0, 0);
	gEngfuncs.pTriAPI->Vertex3f(wide / 2 - cameraWide * 0.7, tall / 2 - cameraHeight * 0.7, 0);
	gEngfuncs.pTriAPI->TexCoord2f(0, 1);
	gEngfuncs.pTriAPI->Vertex3f(wide / 2, tall / 2, 0);
	gEngfuncs.pTriAPI->End();

	gEngfuncs.pTriAPI->RenderMode(kRenderTransAlpha);

	float flTime = gHUD.m_flTime;

	char szTeamName[MAX_TEAM_NAME];
	strcpy(szTeamName, g_PlayerExtraInfo[idx].teamname);

	for (int i = 0; i < MAX_CLIENTS + 1; i++)
	{
		if (i != 32 && (!g_PlayerInfoList[i].name || !g_PlayerInfoList[i].name[0]))
			continue;

		if (strcmp(szTeamName, g_PlayerExtraInfo[i].teamname) || g_PlayerExtraInfo[i].dead)
			continue;

		int r, g, b;
		HSPRITE hspr = 0;
		HSPRITE hspr2 = 0;
		int scale = 8;
		float scale2 = 0.75;

		if (i == idx)
		{
		}
		else
		{
			if (g_PlayerExtraInfo[i].teamnumber == g_iTeamNumber)
			{
				if (g_iTeamNumber == TEAM_TERRORIST)
				{
					r = 255;
					g = 255;
					b = 255;
					hspr = m_hsprPlayerRed;

					if (g_PlayerExtraInfo[i].has_c4)
						hspr = m_hsprPlayerC4;
				}
				else if (g_iTeamNumber == TEAM_CT)
				{
					r = 255;
					g = 255;
					b = 255;
					hspr = m_hsprPlayerBlue;

					if (g_PlayerExtraInfo[i].vip)
						hspr = m_hsprPlayerVIP;
				}
			}
		}

		int rx, ry;
		float yaw = 0;

		if (i != 32)
		{
			if (hspr == 0)
				continue;

			cl_entity_t *ent = gEngfuncs.GetEntityByIndex(i);
			vec3_t *origin;
			bool valid;

			if (!IsValidEntity(ent))
			{
				valid = false;
				origin = &g_PlayerExtraInfo[i].origin;
			}'''

text = text.replace(bad_chunk, good_chunk)
with open('jni/cl_dll/hud/modern/hud_radar_modern.cpp', 'w') as f:
    f.write(text)
print("Done")
