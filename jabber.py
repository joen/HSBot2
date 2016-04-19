#!/usr/bin/python
# -*- coding: utf-8 -*-
import json,os,thread,sys,logging,socket,json
from thread import start_new_thread as thread
from subprocess import call
from time import sleep,localtime,time
from Tkinter import *
from random import randint


import paho.mqtt.publish as mospub

import sleekxmpp


import config as c

# diese wartet auf Chat befehle und reagiert
class Befehle():
	def __init__(self):
		print "Befehle aktiviert"
		
	def befehl(self,nick,msg):
		FNAME = "./cache/pony.flv"
		b = str(msg).split(" ",1)
		b[0] = b[0].lower()
		
		# if b[0] == ':ponies':
			# if os.path.isfile(FNAME) :
				# starttime = randint(0,38)*10
				# stoptime = starttime+10
			
				# call(["vlc","--no-audio","--play-and-exit","--start-time="+str(starttime),"--stop-time="+str(stoptime),"--quiet","-f",FNAME])

			# else:
				# m.chat("404 File nicht gefunden")
				
		if b[0] == ':toast':
			jabber.sendTo(nick +" mag Toast")
			thread(self.toast,(b[1],10))
		elif b[0] == ':countdown':
			thread(self.countdown,(b[1],))
	
	def toast(self,msg,time):
		global toast
		
		mospub.single(c.MQTTTOPTOUT, payload=msg, hostname=c.MQTTSRV)
		data = json.dumps({'type':'toast','msg':msg,'time':time})
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect(('127.0.0.1', 2550))
		s.sendall(data)
		s.close()
		
	def countdown(self,timecode):
		time = str(timecode).split(":")
		l = len(time)
		m = 0
		if(l == 3):
			m = l[0]*3600+l[1]*60+l[2]
		elif(l == 2):
			m = l[0]*60+l[1]
		elif(l == 1):
			m = l[0]
		
		toast.grid_remove()
		if m > 0:
			toast.grid(row=0,column=0)
			while m > 0:
				to.set(str(m))
				toast.grid(row=0,column=0)
				sleep(1)
				m=m-1
			to.set("TIMEOUT")
			sleep(5)
			toast.grid_remove()

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
		data = json.dumps({'type':'chat','msg':c.JNICK +': '+ txt})
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect(('127.0.0.1', 2550))
		s.sendall(data)
		s.close()
		
	def sendPrivate(self,nick,text):
		self.send_message(mto=c.JROOM+"/"+nick,mbody=txt,mtype='groupchat')
		
	def changeSubj(self,subj):
		if subj:
			self.TOPIC = str(subj)

		self.send_raw("<message from='"+c.JROOM+"/"+c.JNICK+"' id='lh2bs617' to='"+c.JROOM+"' type='groupchat'><subject>"+self.TOPIC+"</subject></message>")
		
	def muc(self, msg):
		try:
			if msg['mucnick'] != c.JNICK and msg['from'].bare.startswith(c.JROOM):
				if msg['body'].startswith(':'):
					b.befehl(msg['mucnick'],msg['body'])
					
				data = json.dumps({'type':'chat','msg':msg['mucnick'] +': '+ msg['body']})
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.connect(('127.0.0.1', 2550))
				s.sendall(data)
				s.close()
		except:
			pass
			
b = Befehle()

			
jabber = Jabber()
jabber.run()