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

import events

def cleanLine(line):
	line = line.split(':')[1:]
	line = ':'.join(line)[2:]
	line = line.split(' ')
	line = [_ for _ in line if _ != '']
	return line

def checkLine(line):
	if len(line) < 1:
		return True
	if line[0][-1] != ':': #It's not a function
		return True

def getEvent(line):
	line = cleanLine(line)
	if checkLine(line):
		return None
	func = line[0][:-1]
	args = line[1:]
	if func == 'ClientConnect':
		id = int(args[0])
		event = events.Event(events.EVT_CLIENT_CONNECT)
		event.id = id
	elif func == 'ClientDisconnect':
		id = int(args[0])
		event = events.Event(events.EVT_CLIENT_DISCONNECT)
		event.id = id
	elif func == 'ClientUserinfo':
		i = 0
		vars = {}
		id = int(args[0])
		args = ' '.join(args[1:])
		args = args.split('\\')[1:]
		while i < len(args):
			vars[args[i]] = args[i+1]
			i += 2
		event = events.Event(events.EVT_CLIENT_INFO)
		event.id = id
		event.vars = vars
	elif func == 'ClientUserinfoChanged':
		i = 0
		vars = {}
		id = int(args[0])
		args = ' '.join(args[1:])
		args = args.split('\\')
		if len(args) < 2:
			event = events.Event(events.EVT_UNKNOWN)
		else:
			while i < len(args):
				vars[args[i]] = args[i+1]
				i += 2
			event = events.Event(events.EVT_CLIENT_UPDATE)
			event.id = id
			event.vars = vars
	elif func == 'ClientBegin':
		id = int(args[0])
		event = events.Event(events.EVT_CLIENT_BEGIN)
		event.id = id
	elif func == 'InitGame':
		i = 0
		vars = {}
		args = ' '.join(args)
		args = args.split('\\')[1:]
		while i < len(args):
			vars[args[i]] = args[i+1]
			i += 2
		event = events.Event(events.EVT_GAME_START)
		event.vars = vars
	elif func == 'say': #  4:36 say: 0 {wwF*MathX}: yes !
		id = int(args[0])
		nick = args[1][:-1]
		message = ' '.join(args[2:])
		event = events.Event(events.EVT_CLIENT_SAY)
		event.id = id
		event.nick = nick
		event.message = message
	elif func == 'sayteam':
		id = int(args[0])
		nick = args[1][:-1]
		message = ' '.join(args[2:])
		event = events.Event(events.EVT_CLIENT_TEAMSAY)
		event.id = id
		event.nick = nick
		event.message = message
	elif func == 'saytell':
		id = int(args[0])
		receiver = int(args[1])
		nick = args[2][:-1]
		message = ' '.join(args[3:])
		event = events.Event(events.EVT_CLIENT_TELL)
		event.id = id
		event.receiver = receiver
		event.nick = nick
		event.message = message
	elif func == 'Warmup':
		event = events.Event(events.EVT_GAME_WARMUP)
	elif func == 'ShutdownGame':
		event = events.Event(events.EVT_GAME_STOP)
	elif func == 'InitRound':
		i = 0
		vars = {}
		args = ' '.join(args)
		args = args.split('\\')[1:]
		while i < len(args):
			vars[args[i]] = args[i+1]
			i += 2
		event = events.Event(events.EVT_GAME_ROUND_START)
		event.vars = vars
	elif func == 'SurvivorWinner':
		team = args[0]
		event = events.Event(events.EVT_GAME_SURVIVORWINNER)
		event.team = team
	elif func == 'Item':
		id = int(args[0])
		item = args[1]
		event = events.Event(events.EVT_CLIENT_ITEM)
		event.id = id
		event.item = item
	elif func == 'Kill':
		killer = int(args[0])
		dead = int(args[1])
		weap = int(args[2][:-1])
		event = events.Event(events.EVT_CLIENT_KILL)
		event.dead = dead
		event.killer = killer
		event.weap = weap
	elif func == 'Exit':
		message = ' '.join(args)
		event = events.Event(events.EVT_GAME_END)
		event.message = message
	else:
		event = events.Event(events.EVT_UNKNOWN)
	return event
