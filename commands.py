# it's just a draft class...

class Commands:
    allCommands = None
        
    def __init__(self):
	self.allCommands = (
	    (
		"CMD_SAY",
		"!! <message>",
		"Send \x02message\x02 to the server"
	    ),
	    (
		"CMD_SAY_PRIV",
		"@<n> <message>",
		"Send \x02message\x02 to client ID \x02n\x02 privately"
	    ),
	    (
		"CMD_BIGTEXT",
		"!bigtext <message>",
		"Show \x02message\x02 on center of the screen"
	    ),
	    (
		"CMD_KICK",
		"!kick <n>",
		"Kick client ID \x02n\x02"
	    ),
	    (
		"CMD_SLAP",
		"!slap <n>",
		"Slap client ID \x02n\x02"
	    ),
	    (
		"CMD_NUKE",
		"!nuke <n>",
		"Nuke client ID \x02n\x02"
	    ),
	    (
		"CMD_MUTE",
		"!mute <n>",
		"Mute client ID \x02n\x02"
	    ),
	    (
		"CMD_NEXTMAP",
		"!nextmap <map>",
		"Set g_nextmap to \x02map\x02"
	    ),
	    (
		"CMD_MAP",
		"!map <map>",
		"Change current map to \x02map\x02"
	    ),
	    (
		"CMD_SHUFFLE",
		"!shuffle",
		"Shuffle teams"
	    ),
	    (
		"CMD_FORCE",
		"!force <n> <cvar> <value>",
		"Force any client variable \x02cvar\x02 to be \x02value\x02 for client ID \x02n\x02 (requires Rambetter's forcecvar.patch applied)"
	    ),
	    (
		"CMD_LIST",
		"!list",
		"List players on the server"
	    ),
	    (
		"CMD_BAN",
		"!ban <n>",
		"Ban client ID \x02n\x02 (IP only)"
	    ),
	    (
		"CMD_BANGUID",
		"!banguid <n> <reason>",
		"Ban client ID \x02n\x02 with a \x02reason\x02 (both IP and GUID)"
	    ),
	    (
		"CMD_SEARCH",
		"!search <string>",
		"Look for player in database - returns DBID (database ID) prefixed with #"
	    ),
	    (
		"CMD_EXTINFO",
		"!extinfo <#dbid>",
		"Show extended information about client database ID \x02dbid\x02"
	    ),
	    (
		"CMD_ALIASES",
		"!aliases <n | #dbid>",
		"Show player's aliases (client ID or database ID respectively)"
	    ),
	    (
		"CMD_INFO",
		"!info <n>",
		"Show connection details about client ID \x02n\x02"
	    ),
	    (
		"CMD_HELP",
		"!help [command]",
		"Show help text about \x02command\x02"
	    ))
	    
	g = globals()
	for cmd in self.allCommands:
	    (key, params, desc) = cmd
	    g[key] = (params, desc)

    def getAll(self):
	return self.allCommands
	
commands = Commands()
