import MySQLdb
import time

class Sql:
    def __init__(self, dbhost, dbuser, dbpass, dbname):
	self.dbhost = dbhost
	self.dbuser = dbuser
	self.dbpasswd = dbpass
	self.dbname = dbname
	    
    def	connect(self):
	self.db = MySQLdb.connect(self.dbhost, self.dbuser, self.dbpasswd, self.dbname)

    def disconnect(self):
	self.db.close()
	
    def checkState(self):
	try:
	    cursor = self.db.cursor()
	    cursor.execute('SELECT COUNT(*) FROM groups')
	    cursor.close()
	except MySQLdb.OperationalError:
	    print "DB need reconnect"
	    self.disconnect()
	    self.connect()
	    
    def getId(self, guid):
	self.checkState()
	cursor = self.db.cursor()
	cursor.execute("SELECT id FROM clients WHERE guid = '" + guid + "'")
	row = cursor.fetchone()
	cursor.close()
	return row[0]
	
    def getAliases(self, guid):
	self.checkState()
	id = self.getId(guid)
	cursor = self.db.cursor()
	cursor.execute("SELECT alias FROM aliases WHERE client_id = " + str(id))
	rows = cursor.fetchall()
	cursor.close()
	return rows

    def tempBan(self, cid, duration, nick):
	self.checkState()
	cursor = self.db.cursor()
	time_add = int(time.time())
	time_expire = time_add + int(duration*60.0*60.0)
	mins = int(duration*60.0)
	sql = "INSERT INTO penalties (type, client_id, duration, time_add, time_edit, time_expire, reason, ircnick) VALUES ('TempBan', " + str(cid) + ", " + str(mins) + ", " + str(time_add) + ", " + str(time_add) + ", " + str(time_expire) + ", 'Tempbanned from IRC', '" + nick + "')"
	cursor.execute(sql);
	cursor.close()

    def permBan(self, cid, reason, nick):
	self.checkState()
	cursor = self.db.cursor()
	time_add = int(time.time())
	time_expire = -1
	sql = "INSERT INTO penalties (type, client_id, duration, time_add, time_edit, time_expire, reason) "
	sql += "VALUES ('Ban', %s, 0, %s, %s, -1, \'%s\')" % (str(cid), str(time_add), str(time_add), reason)
	cursor.execute(sql)
	cursor.close()
	
    def search(self, query):
	self.checkState()
	cursor = self.db.cursor()
	cursor.execute("SELECT name, id FROM clients WHERE name LIKE '%%" + query + "%%' UNION SELECT alias, client_id FROM aliases WHERE alias LIKE '%%" + query + "%%'")
	print "search"
	rows = cursor.fetchall()
	print rows
	cursor.close()
	return rows

    def extInfo(self, cid):
	self.checkState()
	cursor = self.db.cursor()
	cursor.execute("SELECT ip, connections, guid, name FROM clients WHERE id = " + str(cid))
	row = cursor.fetchone()
	return row
