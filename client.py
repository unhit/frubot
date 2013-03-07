class Client:
    def __init__(self, id):
	self.id = id
	self.name = "NULL"
	self.ip = "NULL"
	self.port = "NULL"
	self.team = "NULL"
	self.guid = "NULL"
	self.noticed = 1
	self.kills = 0
	self.rgb = "255,255,255"
	self.kills = 0
	self.deaths = 0
	self.caps = 0
	
    def show(self):
	print "name %s ip %s team %s guid %s" %(self.name, self.ip, self.team, self.guid)

    def coloredIrcNickname(self):
	if self.team == "1":
	    ret = "\x034" + self.name + "\x03"
	elif self.team == "2":
	    ret = "\x0312" + self.name + "\x03"
	elif self.team == "3":
	    ret = "\x039" + self.name + "\x03"
	else:
	    ret = "\x02" + self.name + "\x02"
	
	return ret
