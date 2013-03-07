#! /usr/bin/env python
#
# frubot is a gateway between Urban Terror server and IRC.
# It is based on example program delivered with irclib.py written by
# Joel Rosdahl <joel@rosdahl.net>
#
# events.py, rcon.py and parser.py are borrowed from Kiwi Bot written by
# Mathieu "MathX" Xhonneux
#
# Thank you!
#
# This program is free without restrictions; do anything you like with
# it.
#
# fruk <tm@ols.vectranet.pl>

import irclib
import sys
import re
import time
from reader import Reader
from messages import Message
from ts3 import TS3
from localization import Localization
from demo import Demo
import rcon
import client
import socket
import commands
import sql
import config

VERSION = "2013-03-07"

class IRCCat(irclib.SimpleIRCClient):
    reader = None
    cfg = None
    m = None
    currentMap = "(waiting for new round)"
    nextMap = "None"
    
    def __init__(self, target, rcon, cfg):
        irclib.SimpleIRCClient.__init__(self)
        self.target = target
        self.rcon = rcon
	self.admins = {}
	self.reader = None
	self.m = Message()
	self.cfg = cfg
	self.db = sql.Sql(self.cfg.dbHost, self.cfg.dbUser, self.cfg.dbPass, self.cfg.dbName)
	
	try:
	    self.db.connect()
	except:
	    print "Could not connect to database."
	    sys.exit(-1)
	    
    def on_welcome(self, connection, event):
        if irclib.is_channel(self.target):
    	    print "*** Joining channel %s" % self.target
            connection.join(self.target)
    	    self.connection.privmsg(self.target, "[frubot " + VERSION + "] \x02Running on " + self.cfg.serverName + "\x02")
    	    self.rcon.send("say \"^8[^1frubot ^2" + VERSION + "^8]^7 [^1init^7] Running on " + self.cfg.serverName + "\"")

    def on_kick(self, connection, event):
	if event.arguments()[0] == self.cfg.ircNick and irclib.is_channel(self.target):
	    self.connection.join(self.target)

    def on_disconnect(self, connection, event):
        sys.exit(0)

    def on_part(self, connection, event):
	try:
	    del self.admins[event.source()]
	except:
	    pass
	
    def on_quit(self, connection, event):
	try:
	    del self.admins[event.source()]
	except:
	    pass

    def on_privmsg(self, connection, event):
	source = event.source()
	nick = source.split('!')[0]
	args = event.arguments()
	
	if args[0] == self.cfg.adminPassword:
	    self.admins[event.source()] = 'admin'
	    self.connection.privmsg(nick, self.m.MSG_ADMIN_LOGIN_PM)
	    self.connection.privmsg(self.target, self.m.MSG_ADMIN_LOGIN % (nick))
	elif args[0] == self.cfg.modPassword:
	    self.admins[event.source()] = 'mod'
	    self.connection.privmsg(nick, self.m.MSG_MOD_LOGIN_PM)
	    self.connection.privmsg(self.target, self.m.MSG_MOD_LOGIN % (nick))
	elif args[0] == "logout":
	    try:
		del self.admins[event.source()]
		self.connection.privmsg(self.target, self.m.MSG_ADMIN_LOGOUT % (nick))
	    except:
		pass
		
    def on_pubmsg(self, connection, event):
	source = event.source()
	nick = source.split('!')[0]
	args = event.arguments()
	message = args[0].split(' ')
	
	if message[0] == '!!' and len(message) > 1:
	    try:
		if self.admins[event.source()] == 'admin':
		    command = "say \"^8(^1IRC:^5@^2" + nick + "^8)^7 " + ' '.join(message[1:]) + "\""
		elif self.admins[event.source()] == 'mod':
		    command = "say \"^8(^1IRC:^5+^2" + nick + "^8)^7 " + ' '.join(message[1:]) + "\""
		    
		self.rcon.send(command)
	    except:
		#command = "say \"^8(^1IRC:^2" + nick + "^8)^7 " + ' '.join(message[1:]) + "\""
		self.connection.privmsg(self.target, self.m.MSG_ERR_ADMIN_PRIV)
		
	elif message[0][0] == '@' and len(message[0]) > 1 and len(message) > 1:
	    if message[0][1:].isdigit():
		cid = message[0].split("@")[1]
		output = "tell " + cid + " \"^8(^1IRC:^2" + nick + "^8)^7 " + ' '.join(message[1:]) + "\""
		self.rcon.send(output)
	elif message[0] == '!bigtext' and len(message) > 1:
	    command = "bigtext \"" + ' '.join(message[1:]) + "\""
	    self.rcon.send(command)
	elif message[0] == '!kick' and len(message) > 1:
	    try:
		if self.admins[event.source()] == 'admin':
		    try:
			c = self.getClientObject(message[1])
			self.rcon.send("kick " + message[1])
			self.connection.privmsg(self.target, self.m.MSG_RCON_KICK % (nick, c.coloredIrcNickname())) 
		    except:
			self.connection.privmsg(self.target, self.m.MSG_ERR_CID)
	    except KeyError:
		self.connection.privmsg(self.target, self.m.MSG_ERR_ADMIN)
	elif message[0] == '!slap' and len(message) > 1:
	    try:
		if self.admins[event.source()] == 'admin':
		    try:
			c = self.getClientObject(message[1])
			self.rcon.send("slap " + message[1])    
			self.connection.privmsg(self.target, self.m.MSG_RCON_SLAP % (nick, c.coloredIrcNickname()))
		    except:
			self.connection.privmsg(self.target, self.m.MSG_ERR_CID)
	    except KeyError:
		self.connection.privmsg(self.target, self.m.MSG_ERR_ADMIN)
	elif message[0] == '!nuke' and len(message) > 1:
	    try:
		if self.admins[event.source()] == 'admin':
		    try:
			c = self.getClientObject(message[1])
			self.rcon.send("nuke " + message[1])
			self.connection.privmsg(self.target, self.m.MSG_RCON_NUKE % (nick, c.coloredIrcNickname()))
		    except:
			self.connection.privmsg(self.target, self.m.MSG_ERR_CID)
	    except KeyError:
		self.connection.privmsg(self.target, self.m.MSG_ERR_ADMIN)
	elif message[0] == '!mute' and len(message) > 1:
	    try:
		if self.admins[event.source()] == 'admin':
		    try:
			c = self.getClientObject(message[1])
			self.rcon.send("mute " + message[1])
			self.connection.privmsg(self.target, self.m.MSG_RCON_MUTE % (nick, c.coloredIrcNickname()))
		    except:
			self.connection.privmsg(self.target, self.m.MSG_ERR_CID)
	    except KeyError:
		self.connection.privmsg(self.target, self.m.MSG_ERR_ADMIN)
	elif message[0] == '!nextmap' and len(message) > 1:
	    try:
		if self.admins[event.source()] == 'admin':
		    self.rcon.send("g_nextmap " + message[1])
		    self.connection.privmsg(self.target, self.m.MSG_RCON_NEXTMAP % (message[1]))
	    except KeyError:
		self.connection.privmsg(self.target, self.m.MSG_ERR_ADMIN)
	elif message[0] == '!map':
	    if len(message) > 1:
		try:
	    	    if self.admins[event.source()] == 'admin':
	        	self.rcon.send("map " + message[1])
	        	self.connection.privmsg(self.target, self.m.MSG_RCON_MAP %(nick, message[1]))
		except KeyError:
	        	self.connection.privmsg(self.target, self.m.MSG_ERR_ADMIN)
	    else:
		self.connection.privmsg(self.target, self.m.MSG_CURR_MAP %(self.currentMap))
	elif message[0] == "!shuffle":
	    try:
		if self.admins[event.source()] == 'admin':
		    self.rcon.send("shuffleteams")
		    self.connection.privmsg(self.target, self.m.MSG_RCON_SHUFFLE % (nick))
	    except KeyError:
		self.connection.privmsg(self.target, self.m.MSG_ERR_ADMIN)
	elif message[0] == '!force' and len(message) > 3:
	    try:
		if self.admins[event.source()] == 'admin':
		    try:
			c = self.getClientObject(message[1])
			self.rcon.send("forcecvar " + message[1] + " " + message[2] + " " + ''.join(message[3:]))
			self.connection.privmsg(self.target, self.m.MSG_RCON_FORCECVAR % (nick, message[2], ''.join(message[3:]), c.coloredIrcNickname()))
		    except:
			self.connection.privmsg(self.target, self.m.MSG_ERR_CID)
	    except KeyError:
		self.connection.privmsg(self.target, self.m.MSG_ERR_ADMIN)
	elif message[0] == '!list':
	    if self.reader != None:
		output = (self.m.MSG_LIST % (len(self.reader.clients), self.currentMap)) + " "
		
		for key, c in self.reader.clients.iteritems():
		    output = output + "(" + str(key) + ")" + c.coloredIrcNickname() + " "
		    
		self.connection.privmsg(self.target, output)
	    else:
		self.connection.privmsg(self.target, self.m.MSG_ERR_OBJECT)
	elif message[0] == '!ts3' and self.cfg.ts3enabled:
	    try:
		ts3client = TS3(self.cfg.ts3host, self.cfg.ts3port, self.cfg.ts3user, self.cfg.ts3pass, self, self.target, "list", "")
		ts3client.start()
	    except:
		self.connection.privmsg(self.target, self.m.MSG_ERR_GENERAL)
	elif message[0] == '!ts3info' and len(message) > 1 and self.cfg.ts3enabled:
	    try:
		ts3client = TS3(self.cfg.ts3host, self.cfg.ts3port, self.cfg.ts3user, self.cfg.ts3pass, self, self.target, "info", message[1])
		ts3client.start()
	    except:
		self.connection.privmsg(self.target, self.m.MSG_ERR_GENERAL)
	elif message[0] == '!ban' and len(message) > 1:
	    if self.reader != None:
		try:
		    if self.admins[event.source()] == 'admin':
			try:
			    c = self.getClientObject(message[1])
			    self.rcon.send("addIP " + c.ip)
			    self.rcon.send("kick " + message[1])
			    self.connection.privmsg(self.target, self.m.MSG_RCON_BAN % (nick, c.coloredIrcNickname(), c.ip))
			except:
			    self.connection.privmsg(self.target, self.m.MSG_ERR_CID)
		except KeyError:
		    self.connection.privmsg(self.target, self.m.MSG_ERR_ADMIN)
	elif (message[0] == '!banguid' or message[0] == '!permban') and len(message) > 2:
	    if self.reader != None:
		try:
		    if self.admins[event.source()] == 'admin':
			try:
			    c = client.Client(-1)
			    
			    if message[1][0] == "#":
				ext_id = message[1].split("#")[1]
				ret = self.db.extInfo(int(ext_id))
				c.guid = ret[2]
				c.name = ret[3]
				c.ip = ret[0]
			    else:
				c = self.getClientObject(message[1])
				
			    guid = c.guid
			    reason = ' '.join(message[2:])
			    id = self.db.getId(c.guid)
			    
			    try:
				self.db.permBan(id, reason, nick)
			    except:
				self.connection.privmsg(self.target, self.m.MSG_ERR_DB)
				
			    self.rcon.send("addIP " + c.ip)
			    self.rcon.send("kick " + message[1])
			    self.connection.privmsg(self.target, self.m.MSG_RCON_BANGUID % (nick, c.coloredIrcNickname(), c.guid, c.ip, reason))
			except:
			    self.connection.privmsg(self.target, self.m.MSG_ERR_CID)
		except:
		    self.connection.privmsg(self.target, self.m.MSG_ERR_ADMIN)
	elif message[0] == '!search' and len(message) > 1:
	    try:
		if self.admins[event.source()] == 'admin':
		    try:
			if len(message[1]) >= 3 and message[1].isalnum():
			    results = self.db.search(message[1])
			    output = self.m.MSG_SEARCH % (message[1]) + " "
			
			    if len(results) > 40:
				output = output + self.m.MSG_ERR_SEARCH_RES
			    else:
				for result in results:
				    output = output + "(\x02#" + str(result[1]) + "\x02)" + result[0] + " "
			else:
			    output = self.m.MSG_ERR_SEARCH
			    	
			self.connection.privmsg(self.target, output)
		    except:
			print sys.exc_info()
			self.connection.privmsg(self.target, self.m.MSG_ERR_DB)
	    except:
		self.connection.privmsg(self.target, self.m.MSG_ERR_ADMIN)
	elif message[0] == '!tempban' and len(message) > 2:
	    try:
		if self.admins[event.source()] == 'admin':
		    try:
			c = client.Client(-1)
			c = self.getClientObject(message[1])
			id = self.db.getId(c.guid)
			duration = float(message[2])
			
			if duration > 0.0:
			    self.db.tempBan(id, duration, nick)
			    self.rcon.send("kick " + message[1])
			    self.connection.privmsg(self.target, self.m.MSG_RCON_TEMPBAN % (nick, c.coloredIrcNickname(), str(duration)))
		    except:
			self.connection.privmsg(self.target, self.m.MSG_ERR_DB)
	    except:
		self.connection.privmsg(self.target, self.m.MSG_ERR_ADMIN)
	elif message[0] == '!extinfo' and len(message) > 1:
	    try:
		if self.admins[event.source()] == 'admin':
		    try:
			ret = self.db.extInfo(int(message[1]))
			
			try:
			    (ip_ptr, alias, addr) = socket.gethostbyaddr(ret[0])
			    added = " [" + ip_ptr + "]"
			except:
			    added = ""
			    
			output = self.m.MSG_EXTINFO % (message[1], ret[3], ret[0], added, ret[2], str(ret[1]))
			self.connection.privmsg(self.target, output)
		    except:
			print sys.exc_info()
			self.connection.privmsg(self.target, self.m.MSG_ERR_DB)
	    except:
		self.connection.privmsg(self.target, self.m.MSG_ERR_ADMIN)
	elif message[0] == '!aliases' or message[0] == '!alias' and len(message) > 1:
	    if self.reader != None:
		try:
		    if self.admins[event.source()] == 'mod' or self.admins[event.source()] == 'admin':
			try:
			    c = client.Client(-1)
			    
			    if message[1][0] == "#":
				ext_id = message[1].split("#")[1]
				ret = self.db.extInfo(int(ext_id))
				c.guid = ret[2]
				c.name = ret[3]
				c.ip = ret[0]
			    else:
				c = self.reader.clients[int(message[1])]
			
			    guid = c.guid
		    
			    try:
				aliases = self.db.getAliases(guid)
				output = self.m.MSG_ALIASES % (c.coloredIrcNickname()) + " "
			
				if len(aliases) == 0:
				    output = output + "None"
				    self.connection.privmsg(self.target, output)
				else:
				    i = 0
				    for alias in aliases:
					output = output + alias[0] + " "
					i = i + 1
					if i == 10:
					    self.connection.privmsg(self.target, output)
					    i = 0
					    output = self.m.MSG_ALIASES % (c.coloredIrcNickname()) + " "
					    time.sleep(1.0)
				    
				    if i != 0:
					self.connection.privmsg(self.target, output)
			    except:
				print sys.exc_info()
				self.connection.privmsg(self.target, self.m.MSG_ERR_DB)
			except:
			    self.connection.privmsg(self.target, self.m.MSG_ERR_CID)
		except:
		    self.connection.privmsg(self.target, self.m.MSG_ERR_ADMIN_MOD)
	    else:
		self.connection.privmsg(self.target, self.m.MSG_ERR_OBJECT)
	elif message[0] == '!info' and len(message) > 1:
	    if self.reader != None:
		try:
		    if self.admins[event.source()] == 'admin' or self.admins[event.source()] == 'mod':
			try:
			    c = client.Client(-1)
			    c = self.reader.clients[int(message[1])]
			    output = self.m.MSG_INFO + " " + c.coloredIrcNickname() + " "
			    ip = c.ip.split(':')[0]
			    try:
				(ip_ptr, alias, addr) = socket.gethostbyaddr(ip)
				added = " [" + ip_ptr + "]"
			    except:
				print sys.exc_info()
				added = ""
			
			    output = output + "(" + c.ip + added + ", " + c.guid + ")"
			    
			    if self.cfg.geoEnabled:
				loc = Localization(self, c.ip, output, self.target)
				loc.start()
			    else:
				self.connection.privmsg(self.target, output)
			except:
			    self.connection.privmsg(self.target, self.m.MSG_ERR_CID)
		except:
		    self.connection.privmsg(self.target, self.m.MSG_ERR_ADMIN_MOD)
	    else:
		self.connection.privmsg(self.target, self.m.MSG_ERR_OBJECT)
	elif message[0] == '!demo' and len(message) > 1:
	    if self.reader != None:
		try:
		    if self.admins[event.source()] == 'admin' or self.admins[event.source()] == 'mod':
			try:
			    if len(message) >= 3:
				try:
				    duration = int(message[2])
				except:
				    duration = 1
			    else:
				duration = 1
				
			    c = client.Client(-1)
			    c = self.reader.clients[int(message[1])]
			    output = self.m.MSG_DEMO + c.coloredIrcNickname()
			    d = Demo(self, self.rcon, output, self.target, duration, c.id)
			    d.start()
			except:
			    self.connection.privmsg(self.target, self.m.MSG_ERR_CID)
		except:
		    self.connection.privmsg(self.target, self.m.MSG_ERR_ADMIN_MOD)
	    else:
		self.connection.privmsg(self.target, self.m.MSG_ERR_OBJECT)
	elif message[0] == '!stamina' and len(message) > 2:
	    if self.reader != None:
		try:
		    if self.admins[event.source()] == 'admin':
			try:
			    c = self.getClientObject(message[1])

			    output = self.m.MSG_RCON_STAMINA % (c.coloredIrcNickname(), message[2])
	
			    self.rcon.send("stamina " + message[1] + " " + message[2])
			    self.connection.privmsg(self.target, output);
			except:
			    self.connection.privmsg(self.target, self.m.MSG_ERR_CID);
		except:
		    self.connection.privmsg(self.target, self.m.MSG_ERR_ADMIN);
	    else:
		self.connection.privmsg(self.target, self.m.MSG_ERR_OBJECT);
	elif message[0] == '!wj' and len(message) > 2:
	    if self.reader != None:
		try:
		    if self.admins[event.source()] == 'admin':
			try:
			    c = self.getClientObject(message[1])

			    output = self.m.MSG_RCON_WJ % (c.coloredIrcNickname(), message[2])
	
			    self.rcon.send("walljumps " + message[1] + " " + message[2])
			    self.connection.privmsg(self.target, output);
			except:
			    self.connection.privmsg(self.target, self.m.MSG_ERR_CID);
		except:
		    self.connection.privmsg(self.target, self.m.MSG_ERR_ADMIN);
	    else:
		self.connection.privmsg(self.target, self.m.MSG_ERR_OBJECT);
	elif message[0] == '!damage' and len(message) > 3:
	    if self.reader != None:
		try:
		    if self.admins[event.source()] == 'admin':
			try:
			    c = self.getClientObject(message[1])
			    
			    if message[2] == 'source' or message[2] == 'target':
				output = self.m.MSG_RCON_DAMAGE % (c.coloredIrcNickname(), message[2], message[3])
	
				self.rcon.send("damage " + message[1] + " " + message[2] + " " + message[3])
				self.connection.privmsg(self.target, output);
			    else:
				self.connection.privmsg(self.target, self.m.MSG_ERR_PARAMS);
			except:
			    self.connection.privmsg(self.target, self.m.MSG_ERR_CID);
		except:
		    self.connection.privmsg(self.target, self.m.MSG_ERR_ADMIN);
	    else:
		self.connection.privmsg(self.target, self.m.MSG_ERR_OBJECT);
		
# buggy! triggered on every public ACTION			
#    def on_ctcp(self, connection, event):
#	self.connection.ctcp_reply(event.source().split('!')[0], "VERSION frubot " + VERSION + " (UrT <-> IRC gateway) by fruk")
	
    def on_nicknameinuse(self, connection, event):
	print "ERROR: Nickname already in use. Trying different one..."
	self.cfg.ircNick = self.cfg.ircNick + "_"
	print self.cfg.ircServer
	print self.cfg.ircNick
	self.connection.connect(self.cfg.ircServer.split(":")[0], self.cfg.ircServer.split(":")[1], self.cfg.ircNick)
	
    def disconnect(self, message):
	self.connection.disconnect(message)

    def getClientObject(self, cid):
	c = client.Client(-1)
	c = self.reader.clients[int(cid)]
	return c
	
    def setCurrentMap(self, mapname):
	self.currentMap = mapname

    def setNextMap(self, mapname):
	self.nextMap = mapname
		
def main():
    if len(sys.argv) != 2:
        print "Usage: frubot <config>"
        sys.exit(1)

    cfg = config.Config(sys.argv[1])
    cfg.read()
    cfg.show()
    
    s = cfg.ircServer.split(":", 1)
    server = s[0]
    if len(s) == 2:
        try:
            port = int(s[1])
        except ValueError:
            print "Error: Erroneous port."
            sys.exit(1)
    else:
        port = 6667
    nickname = cfg.ircNick
    initnickname = nickname
    target = cfg.ircChannel

    while True:
	try:
	    r = rcon.rcon(cfg.serverAddr, int(cfg.serverPort), cfg.rconPassword)
	    c = IRCCat(target, r, cfg)
	    print "*** Connecting to %s:%d as %s" % (server, port, nickname)
    	    c.connect(server, port, nickname)
    	    
    	    print "*** Opening logs"
	    reader = Reader(cfg.logName, c, target)
	    reader.start()
	    time.sleep(1.0)
	    c.start()
	
	except irclib.ServerConnectionError:
	    print "Could not connect to server"
	    reader.disable()
	except irclib.ServerNotConnectedError:
	    print "Reconnecting in 10 secs"
	    reader.disable()
	    time.sleep(10.0)
	except KeyboardInterrupt:
	    print "*!* Interrupted by keyboard! Waiting for threads..."
	    reader.disable()
	    c.disconnect("[frubot] kthxbai :(")
	    sys.exit(0)
	except:
	    print sys.exc_info()[:2]
	    print "Restarting ..."
	    
	    if nickname != initnickname:
		nickname = initnickname
	    else:
		nickname = nickname + "_"
		
	    cfg.ircNick = nickname
	    reader.disable()
	    time.sleep(10.0)
		
if __name__ == "__main__":
    main()
