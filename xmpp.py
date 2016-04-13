#!/usr/bin/python
# -*- coding: utf-8 -*-

import sleekxmpp,logging
from time import sleep,time

import config as c

class Jabber(sleekxmpp.ClientXMPP):
	logging.basicConfig(level=logging.ERROR)
	XMPP_CA_CERT_FILE = c.JCERT		#Setze Certificat fuer xmpp
	online = time()

	def __init__(self):
		#print("[init]")
		sleekxmpp.ClientXMPP.__init__(self, c.JUSER, c.JPASS)
		self.register_plugin('xep_0030') # Service Discovery
		self.register_plugin('xep_0045') # Multi-User Chat
		self.register_plugin('xep_0199') # XMPP Ping
		
	def run(self):
		self.onDisc()
		while True:
			print("[run] "+ str(self.online))
			if (self.online + 65) < time():
				self.onDisc()
			else:
				sleep(30)
				self.send_presence()
				
	def onDisc(self):
		print("[disconnect]")
		while not self.online: 
			if self.connect():#use_ssl=True):
				self.process()
				self.online = time()
					
				self.add_event_handler("session_start", self.onStart)
				self.add_event_handler("groupchat_message", self.onMuc)
				self.add_event_handler("diconnected", self.onDisc)
				self.add_event_handler("groupchat_subject", self.onSubj)
				self.add_event_handler("presence_available",self.onPresence)
			else:
				print('Verbindung fehlgeschlagen ... (warte 10 Sekunden)')
			sleep(10)
				
	def onPresence(self,event):
		print('[presence]'+str(event['from'].bare))
		if event['from'].bare == c.JUSER:
			print('[timeup]'+ str(time()))
			self.online = time()

	def onStart(self, event):
		print("[start]")
		self.get_roster()
		self.send_presence()
		self.plugin['xep_0045'].joinMUC(c.JROOM, c.JNICK,wait=True)		
		
	def onSubj(self,event):
		print("[subj]")
		
	def onMuc(self, msg):
		print("[muc]"+ msg['mucnick'] +":"+ msg['body'])

		
	def sendTo(self,txt):
		self.send_message(mto=c.JROOM,mbody=txt,mtype='groupchat')
		
	def changeSubj(self,subj):
		if subj:
			self.TOPIC = str(subj)

		self.send_raw("<message from='"+c.JROOM+"/"+c.JNICK+"' id='lh2bs617' to='"+c.JROOM+"' type='groupchat'><subject>"+self.TOPIC+"</subject></message>")
	
jabber = Jabber()
jabber.run()
