import socket
from threading import Thread

class TS3(Thread):
    host = None
    port = None
    login = None
    passwd = None
    sock = None
    irc = None
    target = None
    action = None
    arg = None
    
    def __init__(self, host, port, login, passwd, irc, target, action, arg):
	Thread.__init__(self)
	self.host = host
	self.port = port
	self.login = login
	self.passwd = passwd
	self.irc = irc
	self.target = target
	self.action = action
	self.arg = arg
	
    def connect(self):
	self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	self.sock.connect((self.host, self.port))
	
    def getList(self):
	self.ts3login()
	self.sock.send("clientlist\n")
	ret = 1
	data = ""
	
	while ret:
	    new_data = self.sock.recv(65536)
	    data = data + new_data
	    
	    if len(new_data) < 65536:
		ret = 0
	
	res = data.split("|")
	self.ts3logout()
	return res

    def getInfo(self, clid):
	self.ts3login()
	self.sock.send("clientinfo clid=" + clid + "\n")
	ret = 1
	data = ""
	
	while ret:
	    new_data = self.sock.recv(4096)
	    data = data + new_data
	    
	    if len(new_data) < 4096:
		ret = 0
	
	self.ts3logout()
	return data.split(" ")
	
    def ts3login(self):
	self.connect()
	self.sock.recv(1024)
	self.sock.recv(1024)
	self.sock.send("use 1\n")
	self.sock.recv(1024)
	self.sock.send("login " + self.login + " " + self.passwd + "\n")
	self.sock.recv(1024)
	
    def ts3logout(self):
	self.sock.send("logout\n")
	self.sock.recv(1024)
	self.sock.send("quit\n")
	self.sock.close()
	
    def run(self):
	if self.action == "list":
	    self.actionList()
	elif self.action == "info":
	    self.actionInfo()
	    
    def actionList(self):
	res = self.getList()
	output = "\x02*** TS3:\x02 "
	print res
	
	for r in res:
	    details = r.split(" ")
	    
	    try:
		nickname = details[3].split("client_nickname=")[1]
		clid = details[0].split("clid=")[1]
	    except:
		nickname = "\x02[ERROR]\x02"

	    if nickname.find("195.114.0.18") == -1:
		output = output + "(" + clid + ")" + nickname + " "

	self.irc.connection.privmsg(self.target, output);

    def actionInfo(self):
	res = self.getInfo(self.arg)
	output = "\x02*** TS3INFO: \x02 "
	info = {}
	
	for r in res:
	    ret = r.split("=", 1)
	    key = ret[0].replace("\n", "")
	    
	    if len(ret) == 2:
		val = ret[1].replace("\n", "")
	    else:
		val = "(undefined)"
		
	    info[key] = val
	
	output = output + info['client_nickname'] + " [" + info['client_platform'] + ", " + info['client_unique_identifier'] + ", " + info['client_version'] + ", " + info['connection_client_ip'] + ", " + info['client_country'] + "]"
	self.irc.connection.privmsg(self.target, output);
