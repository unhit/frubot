import ConfigParser
import sys

class Config:
    ircServer = None
    ircChannel = None
    ircNick = None

    serverName = None
    serverAddr = None
    serverPort = None
    rconPassword = None
    logName = None
    
    adminPassword = None
    modPassword = None

    dbHost = None
    dbUser = None
    dbPass = None
    dbName = None
    
    ts3enabled = 0
    ts3host = None
    ts3port = None
    ts3user = None
    ts3pass = None

    geoEnabled = 0
    geoApiKey = None
       
    def __init__(self, filename):
	self.filename = filename
	
	try:
	    self.cfg = ConfigParser.ConfigParser()
	    self.cfg.read(self.filename)
	except ConfigParser.Error:
	    print "An error occurred while reading config file"
	    sys.exit(-1)
	    
    def read(self):
	try:
	    self._readCore()
	    self._readIrc()
	    self._readUrt()
	    self._readB3()
	    self._readTS3()
	    self._readGeo()
	except ConfigParser.NoSectionError:
	    print 'Cannot find required section'
	    sys.exit(-1)
	except ConfigParser.NoOptionError:
	    print 'Cannot find required option'
	    sys.exit(-1)
	except ConfigParser.Error:
	    print 'An error occurred while reading config file'
	    sys.exit(-1)
	    
    def _readCore(self):
	self.adminPassword = self.cfg.get('core', 'admin')
	self.modPassword = self.cfg.get('core', 'mod')
	
    def _readIrc(self):
	self.ircServer = self.cfg.get('irc', 'server')
	self.ircChannel = self.cfg.get('irc', 'channel')
	self.ircNick = self.cfg.get('irc', 'nick')
	
    def _readUrt(self):
	self.serverName = self.cfg.get('urt', 'name')
	self.serverAddr = self.cfg.get('urt', 'ip')
	self.serverPort = self.cfg.getint('urt', 'port')
	self.rconPassword = self.cfg.get('urt', 'rcon')
	self.logName = self.cfg.get('urt', 'log')
	
    def _readB3(self):
	self.dbHost = self.cfg.get('b3', 'host')
	self.dbUser = self.cfg.get('b3', 'user')
	self.dbPass = self.cfg.get('b3', 'pass')
	self.dbName = self.cfg.get('b3', 'name')
	
    def _readTS3(self):
	self.ts3enabled = self.cfg.getint('ts3', 'enabled')
	self.ts3host = self.cfg.get('ts3', 'host')
	self.ts3port = self.cfg.getint('ts3', 'port')
	self.ts3user = self.cfg.get('ts3', 'user')
	self.ts3pass = self.cfg.get('ts3', 'pass')

    def _readGeo(self):
	self.geoEnabled = self.cfg.getint('geo', 'enabled')
	self.geoApiKey = self.cfg.get('geo', 'apikey')
	
    def show(self):
	print "* IRC server: %s" % self.ircServer
	print "* IRC channel: %s" % self.ircChannel
	print "* IRC nick: %s" % self.ircNick
	print "* Server name: %s" % self.serverName
	print "* Server address: %s" % self.serverAddr
	print "* Server port: %s" % self.serverPort
	print "* RCON password: %s" % self.rconPassword
	print "* IRC admin password: %s" % self.adminPassword
	print "* IRC mod password: %s" % self.modPassword
	print "* Log file: %s" % self.logName
	print "* TS3 ([%s] %s:%s as %s)" % (self.ts3enabled, self.ts3host, self.ts3port, self.ts3user)
	print "* Geolocalization ([%s] [%s])" % (self.geoEnabled, self.geoApiKey)
