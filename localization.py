from threading import Thread
import urllib

class Localization(Thread):
    def __init__(self, irc, ip, output, target):
	Thread.__init__(self)
    	self.irc = irc
	self.ip = ip
	self.output = output
	self.target = target
	
    def run(self):
	fp = urllib.urlopen("http://api.ipinfodb.com/v3/ip-city/?key=" + self.irc.cfg.geoApiKey + "&ip=" + self.ip.split(":")[0])
	ret = fp.readline()
	fp.close()
	country = ret.split(";")[4]
	state = ret.split(";")[5]
	city = ret.split(";")[6]
	
	if country == "":
	    country = "Unknown country"
	    
	if state == "":
	    state = "Unknown state"
	    
	if city == "":
	    city = "Unknown city"
	    
	self.output = self.output + " [" + country + ", " + state + ", " + city + "]"
	self.irc.connection.privmsg(self.target, self.output)