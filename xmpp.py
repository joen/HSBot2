#!/usr/bin/python
# -*- coding: utf-8 -*-

import sleekxmpp
from time import sleep

import demo as c

class Jabber(sleekxmpp.ClientXMPP):
	logging.basicConfig(level=logging.ERROR)
	XMPP_CA_CERT_FILE = c.JCERT		#Setze Certificat fuer xmpp
	online = False

	def __init__(self):
		print("[init]")
		sleekxmpp.ClientXMPP.__init__(self, c.JUSER, c.JPASS)
		self.register_plugin('xep_0030') # Service Discovery
		self.register_plugin('xep_0045') # Multi-User Chat
		self.register_plugin('xep_0199') # XMPP Ping
		
	def run(self):
		while True:
			print("[run]")
			sleep(60)
			self.send_presence()
				
	def onDisc(self):
		print("[disconnect]")
		self.online = False
		while not self.online: 
			if self.connect():#use_ssl=True):
				self.process()
				self.online = True
				if g.input(15):
					g.output(11,0)
				else:
					g.output(11,1)
					
				self.add_event_handler("session_start", self.onStart)
				self.add_event_handler("groupchat_message", self.onMuc)
				self.add_event_handler("diconnected", self.onDisc)
				self.add_event_handler("groupchat_subject", self.onSubj)
			else:
				print('Verbindung fehlgeschlagen ... (warte 60 Sekunden)')
				for i in range(60):
					g.output(11,1)
					sleep(1)
					g.output(11,0)
					sleep(1)
				
	def onStart(self, event):
		print("[start]")
		self.get_roster()
		self.send_presence()
		self.plugin['xep_0045'].joinMUC(c.JROOM, c.JNICK,wait=True)		
		
	def onSubj(self,event):
		print("[subj]")
		
	def onMuc(self, msg):
		print("[init]"+ msg['mucnick'] +":"+ msg['body'])

		
	def sendTo(self,txt):
		self.send_message(mto=c.JROOM,mbody=txt,mtype='groupchat')
		
	def changeSubj(self,subj):
		if subj:
			self.TOPIC = str(subj)

		self.send_raw("<message from='"+c.JROOM+"/"+c.JNICK+"' id='lh2bs617' to='"+c.JROOM+"' type='groupchat'><subject>"+self.TOPIC+"</subject></message>")
	