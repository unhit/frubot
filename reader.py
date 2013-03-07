import sys
import time
import re
from threading import Thread
import events
import parser
import client
import socket
import irclib

class Reader(Thread):
    def __init__(self, filename, irc, target):
	Thread.__init__(self)
	self.filename = filename
	self.irc = irc
	self.target = target
	self.clients = {}
	self.irc.reader = self
	
    def run(self):
	self.is_running = True
	self.f = open(self.filename, 'r')
	self.f.seek(0, 2)

	while self.is_running:
	    line = self.readline()

	    try:
		event = parser.getEvent(line)

		# client object is created here
		if event.type == events.EVT_CLIENT_CONNECT:
		    self.clients[event.id] = client.Client(event.id)
		    self.clients[event.id].noticed = 0
		    print "Client connected: %d" % self.clients[event.id].id
		    """
		    output = "forcecvar " + str(event.id) + " cg_rgb \"" + self.clients[event.id].rgb + "\""
		    self.irc.rcon.send(output)                                                
		    """
		# delete client object
		elif event.type == events.EVT_CLIENT_DISCONNECT:
		    print "Client disconnected: %d" % self.clients[event.id].id
		    """
		    output = "\x02*** QUIT:\x02 " + self.clients[event.id].coloredIrcNickname()
		    self.irc.connection.privmsg(self.target, output)
		    """
		    del self.clients[event.id]
		# someone killed someone
		elif event.type == events.EVT_CLIENT_KILL:
		    """
		    if self.clients[event.dead].team != self.clients[event.killer].team:
			self.clients[event.killer].kills = self.clients[event.killer].kills + 1
			rgb = self.clients[event.killer].rgb.split(",")
			r = int(rgb[0])
			g = int(rgb[1])
			b = int(rgb[2])
			
			if r > 11:
			    r = r - 10
			    g = g - 10
			    b = b - 10
			    
			rgb = str(r) + "," + str(g) + "," + str(b)
			self.clients[event.killer].rgb = rgb
			output = "forcecvar " + str(event.killer) + " cg_rgb \"" + self.clients[event.killer].rgb + "\""
			self.irc.rcon.send(output)
		    """
		# client sent connection string, we get ip, name, guid and so on
		elif event.type == events.EVT_CLIENT_INFO:
		    print "Client info: %d" % self.clients[event.id].id
		    self.clients[event.id].ip = event.vars['ip'].split(":")[0]
		    self.clients[event.id].port = event.vars['ip'].split(":")[1]
		    self.clients[event.id].name = event.vars['name']
		    self.clients[event.id].guid = event.vars['cl_guid']
		    
		    """
		    banInfo = self.irc.db.getBanByGuid(self.clients[event.id].guid)
		    if banInfo != None:
			guid = banInfo[1]
			banType = banInfo[2]
			source = banInfo[3]
			target = banInfo[4]
			desc = banInfo[6]
			
			if banType == "ban":
			    output = self.irc.m.MSG_RCON_AUTOKICK % (self.clients[event.id].name, target, guid, self.clients[event.id].ip, desc, source)
			    self.irc.rcon.send("addIP " + str(self.clients[event.id].ip))
			    self.irc.rcon.send("kick " + str(self.clients[event.id].id))
			elif banType == "lag":
			    output = self.irc.m.MSG_RCON_AUTOLAG % (self.clients[event.id].name, target, guid, self.clients[event.id].ip, desc, source)
			    self.irc.rcon.send("forcecvar " + str(self.clients[event.id].id) + " rate 1000")
			    
			self.irc.connection.privmsg(self.target, output)
		    """
		    
		    # find HAX! :<
		    if self.clients[event.id].port == "1337" or self.clients[event.id].guid.find("kemfew") != -1:
			output = "\x034,15Possible hacker detected:\x03 (" + str(event.id) + ")\x02" + event.vars['name'] + "\x02 " + event.vars['ip'] + " " + event.vars['cl_guid']
			self.irc.rcon.send("addIP " + str(self.clients[event.id].ip))
			self.irc.rcon.send("kick " + str(self.clients[event.id].id))
			self.irc.connection.privmsg(self.target, output)
		# client update - most usually changed his team
		elif event.type == events.EVT_CLIENT_UPDATE:
		    print "Client update: %d" % self.clients[event.id].id
		    self.clients[event.id].team = event.vars['t']
		# client said smth
		elif event.type == events.EVT_CLIENT_SAY or event.type == events.EVT_CLIENT_TEAMSAY:
		    print "Client say: %d" % event.id
		    if event.type == events.EVT_CLIENT_TEAMSAY:
			output = "<" + str(event.id)+ ":team:"
		    else:
			output = "<" + str(event.id) + ":"
		
		    try:
			if self.clients[event.id].team == "1":
			    output = output + "\x034" + event.nick + "\x03> " + event.message
			elif self.clients[event.id].team == "2":
			    output = output + "\x0312" + event.nick + "\x03> " + event.message   
			elif self.clients[event.id].team == "3":
			    output = output + "\x039" + event.nick + "\x03> " + event.message
		    except KeyError: 
			output = output + "\x02" + event.nick + "\x02> " + event.message
			
		    self.irc.connection.privmsg(self.target, output)
		# new round has started
		elif event.type == events.EVT_GAME_ROUND_START:
		    output = self.irc.m.MSG_NEW_ROUND % (event.vars['mapname'])
		    self.irc.setCurrentMap(event.vars['mapname'])
		    self.irc.connection.privmsg(self.target, output)
	    except KeyError:
		print "KeyError: wait for map reload"
	    except irclib.ServerNotConnectedError:
		print "Reader lost connection to the server"
		self.is_running = False
	    except ValueError:
		print "ValueError: error while converting types"
		self.irc.connection.privmsg(self.target, self.irc.m.MSG_ERR_CONV)
	    except:
		print "Reader exc:"
		print sys.exc_info()
		
	    time.sleep(0.001)	# we don't want to consume cpu too much
	self.f.close()
	    
    def readline(self):
	while 1:
	    line = self.f.readline()
	    if line:
		break
	    time.sleep(0.001)
	if line[-1] != '\n':
	    newline = self.readline()
	    if newline:
		line += newline
	return re.sub(r'\^[0-9a-z]', '', line.strip())  
	
    def disable(self):
	self.is_running = False
