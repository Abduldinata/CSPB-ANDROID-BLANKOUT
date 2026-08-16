
unsigned short UTIL_PrecacheEvent( int type, const char *s )
{
	if ( !s || !s[0] ) return 0;
	if ( UTIL_FileExists( s ) )
	{
		return (*g_engfuncs.pfnPrecacheEvent)( type, s );
	}
	CSPB_LOG_DIAG("[PRECACHE] WARNING: Event missing: %s - bypassed", s);
	return 0;
}
