#!/usr/bin/python
# -*- coding: utf-8 -*-
import json,os,thread,sys
from thread import start_new_thread as thread
from subprocess import call
from time import sleep,localtime
from Tkinter import *

import paho.mqtt.client as mossub
import paho.mqtt.publish as mospub

# Ports & URLs
NODERED = "http://127.0.0.1:1880"					#wohin wird die nodered anfrage geschickt

# Pfade
INFPATH = os.path.dirname(os.path.realpath(__file__)) +"/info"		#da wo die info txt files liegen
JCERT = os.path.dirname(os.path.realpath(__file__)) +"/xmpp.pem"	#Jabber Certificate

# Jabber Daten
JUSER = "bot@jabber.space.bi"						#bot anmeldename
JNICK = "HSBot"								#Bot anzeigename
JPASS = "PgDNDy70aeqU2w"						#bot Passwort
JROOM = "bot@chat.jabber.space.bi"					#bot raum
JDEBU = "debug@chat.jabber.space.bi"					#bot debug raum

#Telegram Daten
TOKEN = "164086266:AAGSMwxJQH2Tp1Odgeujmaaw7vPalj-noMc"			#Telegram Bot Token
TFILE = os.path.dirname(os.path.realpath(__file__)) +"/follower"	#eingetragene follower bei telegram

#MQTT Daten
MQTTSRV = "172.23.45.55"						#mqtt server
MQTTTOPI = "chat"							#mqtt chat topic
MQTTDEBU = "debug"							#mqtt debug topic

# GPIO Daten
INPINS = [8,10,11,12,13,15,16,18,21,22,23,24,26]
OUTPINS = []

def debugMsg(msg,fkt=''):
	pl = "["+str(fkt)+"]: "+str(msg)
	mospub.single(MQTTDEBU, payload=pl, hostname=MQTTSRV)

def sendMsg(msg,service='',nick=''):
	pass

def setTopic(tpc):
	pass
	
class MQTT():
	def __init__(self):
		client = mossub.Client()
		client.on_connect = self.on_connect
		client.on_message = self.on_message

		client.connect(MQTTSRV, 1883, 60)
		thread.start_new_thread(client.loop_forever,())

	def on_connect(self,client, userdata, flags, rc):
		print("MQTT Start: "+str(rc))
		client.subscribe(MQTTTOP)

	def on_message(self,client, userdata, msg):
		print("MQTT Msg: "+msg.topic+" "+str(msg.payload))
		sendMsg(str(msg.payload),'mqtt',"[MQTT]")
		
	def incMsg(msg,nick=''):
		pass

class GUI():
	f = Tk()
	h = f.winfo_screenheight()
	w = f.winfo_screenwidth()
	
	#Fenster
	f.title('HSBot2')
	f.geometry(str(w)+"x"+str(h)+"+0+0")
	f.wm_overrideredirect(True)
	f.resizable(False, False)
	f.config(bg="#000000")
	
	#Variablen
	ts = StringVar()
	ts.set("XX:XX")
	
	ti = StringVar()
	ti.set("Test")
	
	chat = Text(f,bg="#000000",fg="#ffffff",font=("Arial",32),bd=2,height=16,width=36)
	
	clock = Label(f,textvariable=ts,fg="#ffffff", bg="#000000", bd=2,font=("Arial",108),width=5)
	
	infoh = Label(f,textvariable=ti,fg="#ffffff", bg="#000000",font=("Arial",32))
	
	infot = Text(f,bg="#000000",fg="#ffffff",font=("Arial",24),bd=2,height=15,width=22)
	
	def __init__(self):
		# Chat
		self.chat.tag_add("all", "1.0", END)
		self.chat.tag_config("all",wrap=WORD)
		self.chat.grid(row=0,column=0,rowspan=3,sticky=NW)
		
		# Clock
		self.clock.grid(row=0,column=1,sticky=NE)
		
		# Info Header
		self.infoh.grid(row=1,column=1,sticky=S)
		
		# Info Text
		self.infot.grid(row=2,column=1,sticky=SE)
		self.f.rowconfigure(2, minsize=548)
		
		data = "Chatfenster"

		self.chat.insert(END, str(data) + "\n")
		self.chat.tag_add("all", "1.0", END)
		self.chat.see(END)
		self.chat.update()
		
		self.f.update_idletasks()
		
		while True:
			lt = localtime()
			self.ts.set("%02i:%02i" % (lt.tm_hour,lt.tm_min))
			self.f.update_idletasks()
			sleep(5)
	
	def getInfo(self):
		while True:
			infos = {}
			tmp = os.listdir(INFPATH)
			for i in tmp:
				if not i.startswith("."):
					with open (c.INFPATH+"/"+infos[curInfo]+".txt", "r") as myfile:
						data=myfile.readlines()
						infos[i[:-4]] = data
				
			for j in infos:
				ti.delete("1.0",tk.END)
				ti.insert(tk.END, "".join(infos[j]))
				titel.set(j)
				ti.update()
			sleep(10)
			curInfo = curInfo + 1
		
	def incMsg(msg,nick=''):
		if not nick == '':
			msg = nick+": "+msg
		#todo
		
thread(GUI,())
		
		
while True:
	print('tick')
	sleep(1)
	print('tack')
	sleep(1)