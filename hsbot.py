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
	
def incMsg(msg,nick=''):
	if not nick == '':
		msg = nick+": "+msg
	#todo
	
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


f = Tk()
h = f.winfo_screenheight()
w = f.winfo_screenwidth()/6*5

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
ti.set("------------")

chat = Text(f,bg="#000000",fg="#ffffff",font=("Arial",32),bd=2,height=16,width=36)

clock = Label(f,textvariable=ts,fg="#ffffff", bg="#000000", bd=2,font=("Arial",108),width=5)

infoh = Label(f,textvariable=ti,fg="#ffffff", bg="#000000",font=("Arial",32))

infot = Text(f,bg="#000000",fg="#ffffff",font=("Arial",24),bd=2,height=15,width=22)
	

chat.tag_add("all", "1.0", END)
chat.tag_config("all",wrap=WORD)
chat.grid(row=0,column=0,rowspan=3,sticky=NW)

# Clock
clock.grid(row=0,column=1,sticky=NE)

# Info Header
infoh.grid(row=1,column=1,sticky=S)

# Info Text
infot.grid(row=2,column=1,sticky=SE)
f.rowconfigure(2, minsize=548)

data = "Chatfenster"

chat.insert(END, str(data) + "\n")
chat.tag_add("all", "1.0", END)
chat.see(END)
chat.update()

f.update_idletasks()

def getClock():
	#global f,ts
	while True:
		lt = localtime()
		ts.set("%02i:%02i" % (lt.tm_hour,lt.tm_min))
		f.update_idletasks()
		sleep(5)

def getInfo():
	while True:
		infos = {}
		tmp = os.listdir(INFPATH)
		for i in tmp:
			if not i.startswith(".") and i.endswith('.txt'):
				print(i)
				with open (INFPATH+"/"+i, "r") as myfile:
					data=myfile.readlines()
					infos[i[:-4]] = data
			
		for j in infos:
			infot.delete("1.0",END)
			infot.insert(END, "".join(infos[j]))
			ti.set(j)
			infot.update()
			sleep(1)

thread(getClock,())
thread(getInfo,())

mainloop()
