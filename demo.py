from threading import Thread
import time

class Demo(Thread):
    def __init__(self, irc, rcon, output, target, duration, cid):
	Thread.__init__(self)
    	self.irc = irc
    	self.rcon = rcon;
	self.output = output
	self.target = target
	self.duration = duration
	self.cid = cid
	
    def run(self):
	self.rcon.send("startserverdemo " + str(self.cid))
	self.irc.connection.privmsg(self.target, self.output + " has started (" + str(self.duration) + " minute(s))")
	time.sleep(60.0 * self.duration);
	self.rcon.send("stopserverdemo " + str(self.cid))
	self.irc.connection.privmsg(self.target, self.output + " has stopped after " + str(self.duration) + " minute(s)")
