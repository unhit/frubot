#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Kiwi Bot
#Copyright (C) 2009 Mathieu "MathX" Xhonneux

#This program is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 2 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License along
#with this program; if not, write to the Free Software Foundation, Inc.,
#51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import socket, time, re, sys

class rcon:
	def __init__(self, ip, port, rcon):
		self.ip, self.port, self.rcon = ip, port, rcon
		self.sending = True
		self.connection = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		self.lastAction = time.time()
		self.prefix = '\xFF'*4
		self.floodlimit = 0.75
		try:
			self.connection.connect((ip,port))
		except socket.gaierror:
			sys.exit(0)
	def send(self, command):
		if self.sending:
			query = self.prefix+'rcon %s %s'%(self.rcon, command)
			while time.time() < self.lastAction+self.floodlimit:
				time.sleep(0.01)
			self.lastAction = time.time()
			self.connection.send(query)
			self.connection.settimeout(5)
			try:
				response = self.connection.recv(2**14)[10:-1]
				if response == 'No rconpassword set on the server.' or response == 'Bad rconpassword.':
					sys.exit(0)
				else:
					response = self.unparse(response)
			except socket.timeout:
				response = ''
			return response
		return ''
	def unparse(self, string):
		return re.sub(r'\^[0-9a-z]', '', string)