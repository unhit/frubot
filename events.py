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

class Events:
	def __init__(self):
		self.allEvents = (
		'EVT_START',
		'EVT_STOP',
		'EVT_UNKNOWN',
		'EVT_CLIENT_SAY',
		'EVT_CLIENT_TEAMSAY',
		'EVT_CLIENT_TELL',
		'EVT_CLIENT_CONNECT',
		'EVT_CLIENT_INFO',
		'EVT_CLIENT_DISCONNECT',
		'EVT_CLIENT_UPDATE',
		'EVT_CLIENT_KILL',
		'EVT_CLIENT_DAMAGE',
		'EVT_CLIENT_ITEM',
		'EVT_CLIENT_BEGIN',
		'EVT_GAME_ROUND_START',
		'EVT_GAME_ROUND_END',
		'EVT_GAME_WARMUP',
		'EVT_GAME_END',
		'EVT_GAME_SCORE',
		'EVT_GAME_START',
		'EVT_GAME_STOP',
		'EVT_GAME_SURVIVORWINNER'
		)
		i = 0
		g = globals()
		for event in self.allEvents:
			g[event] = i
			i += 1

class Event:
	def __init__(self,type):
		self.type = type

events = Events()
