#!/usr/bin/python
# -*- coding: utf-8 -*-
import json,os,thread,sys,logging,socket,json
from thread import start_new_thread as thread
from subprocess import call
from time import sleep,localtime,time
from Tkinter import *
from random import randint

import sleekxmpp


import config as c

class Jabber(sleekxmpp.ClientXMPP):
	logging.basicConfig(level=logging.DEBUG)
	XMPP_CA_CERT_FILE = c.JCERT		#Setze Certificat fuer xmpp
	auto_reconnect = True

	def __init__(self):
		print("[init]")
		sleekxmpp.ClientXMPP.__init__(self, c.JUSER, c.JPASS)
		self.register_plugin('xep_0030') # Service Discovery
		self.register_plugin('xep_0045') # Multi-User Chat
		self.register_plugin('xep_0199') # XMPP Ping
		
	def run(self):
		self.newSession()
		while True:
			print("[run] ")
			#if (self.online + 65) < time():
				#self.disconnect()
				#sleep(5)
				#self.newSession()
			#else:
			sleep(30)
			
			self.send_presence()
				#io.blink_start(2,0.5)
				
	def newSession(self): 
		while not self.connect():
			sleep(0.1)
		print('[newSession] 1')
		self.process()
		print('[newSession] 2')
		# print('[newSession] 3')
		# if g.input(15):
			# print('[newSession] 4')
			# g.output(11,0)
		# else:
			# print('[newSession] 5')
			# g.output(11,1)
			
		self.add_event_handler("session_start", self.onStart)
		self.add_event_handler("groupchat_message", self.muc)
		self.add_event_handler("diconnected", self.newSession)
		#self.add_event_handler("groupchat_subject", self.onSubj)
		self.add_event_handler("presence_available",self.onPresence)
				
	def onStart(self, event):
		print('[start]')
		self.get_roster()
		self.send_presence()
		self.plugin['xep_0045'].joinMUC(c.JROOM, c.JNICK,wait=True)		
		
	def onPresence(self,event):
		print('[presence]'+str(event['from'].bare))
		if event['from'].bare == c.JUSER:
			#io.blink_stop()
			print('[timeup]'+ str(time()))
			
		
	def onSubj(self,event):
		if not event["muc"]["nick"] == c.JNICK:
			self.changeSubj(False)
		
	def sendTo(self,txt):
		print("[XMPP] "+str(txt))
		self.send_message(mto=c.JROOM,mbody=txt,mtype='groupchat')
		
	def sendPrivate(self,nick,text):
		self.send_message(mto=c.JROOM+"/"+nick,mbody=txt,mtype='groupchat')
		
	def changeSubj(self,subj):
		if subj:
			self.TOPIC = str(subj)

		self.send_raw("<message from='"+c.JROOM+"/"+c.JNICK+"' id='lh2bs617' to='"+c.JROOM+"' type='groupchat'><subject>"+self.TOPIC+"</subject></message>")
		
	def muc(self, msg):
		try:
			if msg['mucnick'] != c.JNICK and msg['from'].bare.startswith(c.JROOM):
				data = json.dumps({'type':'chat','msg':msg['mucnick'] +': '+ msg['body']})
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.connect(('127.0.0.1', 2550))
				s.sendall(data)
				s.close()
		except:
			pass
jabber = Jabber()
jabber.run()