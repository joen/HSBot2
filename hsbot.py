#!/usr/bin/python
# -*- coding: utf-8 -*-
import json,os,thread,sys,logging,socket,json
from thread import start_new_thread as thread
from subprocess import call
from time import sleep,localtime,time
from Tkinter import *
from random import randint,randrange

import sleekxmpp
from optparse import OptionParser

import RPi.GPIO as g
#import GPdummy as g

import paho.mqtt.client as mossub
import paho.mqtt.publish as mospub

import config as c

lastStatus = 0 # wann das letzte mal der space status geändert wurde
prioToast = False # wenn ein prioritäts Toast da ist werden sachen wie countdown ausgeblendet
lastTrain = 0 #letzter Zeug

#gpio einstellungen
g.setwarnings(False)
g.setmode(g.BOARD)

# erkennt und verteilt befehle weiter
def befehl(nick,msg):
	FNAME = "./cache/pony.flv"
	b = str(msg).split(" ",1)
	b[0] = b[0].lower()
	
	if len(b) == 2:
		param = b[1]
	else:
		param = '';
	#try:
	if True:
		if b[0] == ':ponies':
			jabber.sendTo("[PONIES] Ponies sind grad Feiern")
		elif b[0] == ':toast':
			jabber.sendTo("[TOAST] "+ nick +" mag Toast")
			thread(makeToast,(param,10))
		elif b[0] == ':trains':
			makeTrains(nick)
		elif b[0] == ':countdown':
			thread(makeCountdown,(nick,param))	
	#except:
	#	pass
	
def makeTrains(nick):
	global lastTrain
	global jabber
	
	print("TRAINS")

	if lastTrain < (time()-300):
		lastTrain = time()
		jabber.sendTo("[TRAIN] "+ nick +" mag Züge")
	else:
		antw = ("Zug hat verspätung."
		, "Zug macht Pause."
		, "Zug hat keine Lust."
		, "Im Zug ist die Heizung ausgefallen."
		, "Zugtüren lassen sich nicht schließen."
		, "Zug heute in umgekehrter Reihenfolge."
		, "Zug heute abweichend von Gleis 2 auf Gleis 238."
		, "Zugbeleuchtung wurde auf halbdunkel gestellt,damit wir noch genug strom für die Klimaanlagen haben."
		, "Bitte stellen sie keine Gepäckstücke vor die Türen, diese dienen dem Zugpersonal als Fluchtweg."
		, "Sehr geehrte Fahrgäste, heute bekommen sie für ihr Geld 20Minuten mehr Fahrzeit geboten."
		, "Sollten sie auf der Suche nach Wagen 9 sein, den haben wir heute ganz geschickt zwischen Wagen 5 und 6 versteckt."
		, "Weitere Informationen entnehmen sie bitte dem Zugpersonal."
		, "Bitte nehmen sie Ihre Regenschirme wieder mit. Die Bahn hat mittlerweile ausreichend."
		, "Im gesamten Zug herrscht absolutes Nichtraucherverbot.")

		jabber.sendTo("[TRAIN] "+ antw[randrange(0,len(antw))])
	
# zeigt den countdown mit low prio (bedeutet, wenn tost kommt wird der countdown ausgesetzt)
def makeCountdown(nick,timecode):
	global toast
	global prioToast

	time = str(timecode).split(":")
	l = len(time)
	m = 0
	if(l == 3):
		m = int(time[0])*3600+int(time[1])*60+int(time[2])
	elif(l == 2):
		m = int(time[0])*60+int(time[1])
	elif(l == 1):
		m = int(time[0])
	
	#toast.grid_remove()
	if m > 0:
		while m > 0:
			if not prioToast:
				toast.grid(row=0,column=0)
				to.set(str(m))
			sleep(1)
			print("[COUNTDOWN] "+ str(m))
			m=m-1
		jabber.sendTo("[COUNTDOWN] @"+nick +" Dein Countdown ist abgelaufen.")
		toast.grid_remove()

#sendet toast an display
def makeToast(msg,time):
	global toast
	global to
	global prioToast
	
	
	prioToast = True
	mospub.single(c.MQTTTOPTOUT, payload=msg, hostname=c.MQTTSRV)
	to.set(str(msg))
	toast.grid(row=0,column=0)
	sleep(time)
	toast.grid_remove()
	prioToast = False

#sendet zurück welchen Status der Space grade hat	
def makeStatus():
	if g.input(15):
		jabber.sendTo("[STATUS] Der Space ist aktuell geschlossen.")
	else:
		jabber.sendTo("[STATUS] Der Space ist aktuell geöffnet.")
		
def setTopic(tpc):
	pass
	
#def incMsg(msg,nick=''):
#	if not nick == '':
#		msg = nick+": "+msg
	#todo

# schliebs ne nachricht über mqtt topic debug
def debugMsg(msg,fkt='DEBUG'):
	pl = "["+str(fkt)+"]: "+str(msg)
	mospub.single(c.MQTTDEBU, payload=pl, hostname=c.MQTTSRV)

#mosquito Klasse
class MQTT():
	client = mossub.Client()
	
	def __init__(self):
		self.client = mossub.Client()
		self.client.on_connect = self.on_connect
		self.client.on_message = self.on_message

		self.client.connect(c.MQTTSRV, 1883, 60)
		
	def run(self):
		while True:
			self.client.loop_forever()

	def on_connect(self,client, userdata, flags, rc):
		print("MQTT Start: "+str(rc))
		self.client.subscribe(c.MQTTTOPI)
		self.client.subscribe(c.MQTTTOPT)

	def on_message(self,client, userdata, msg):
		print("MQTT Msg: "+msg.topic+" "+str(msg.payload))
		if(msg.topic == 'toast'):
			makeToast(msg.payload,10)
		
		if(msg.topic == 'chat'):
			sendMsg("[MQTT]: "+str(msg.payload))
		
	def incMsg(msg,nick=''):
		pass

# xmpp klasse
class Jabber(sleekxmpp.ClientXMPP):
	logging.basicConfig(level=logging.ERROR)
	XMPP_CA_CERT_FILE = c.JCERT		#Setze Certificat fuer xmpp
	auto_reconnect = True

	def __init__(self):
		sleekxmpp.ClientXMPP.__init__(self, c.JUSER, c.JPASS)
		self.register_plugin('xep_0030') # Service Discovery
		self.register_plugin('xep_0045') # Multi-User Chat
		self.register_plugin('xep_0199') # XMPP Ping
		
	def run(self):
		self.newSession()
		while True:
			sleep(30)
			self.send_presence()
				
	def newSession(self): 
		while not self.connect():
			sleep(0.1)
		self.process()

			
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
		sendMsg(c.JNICK +": "+ txt)
		
	def sendPrivate(self,nick,text):
		self.send_message(mto=c.JROOM+"/"+nick,mbody=txt,mtype='groupchat')
		
	def changeSubj(self,subj):
		if subj:
			self.TOPIC = str(subj)

		self.send_raw("<message from='"+c.JROOM+"/"+c.JNICK+"' id='lh2bs617' to='"+c.JROOM+"' type='groupchat'><subject>"+self.TOPIC+"</subject></message>")
		
	def muc(self, msg):
		#try:
			if msg['mucnick'] != c.JNICK and msg['from'].bare.startswith(c.JROOM):	
				sendMsg(msg['mucnick']+': '+msg['body'])
				if msg['body'].startswith(':'):
					befehl(msg['mucnick'],msg['body'])
		#except:
			pass
			
# diese klasse überwacht alle GPIO ports und reagiert nach wunsch
class IOPorts():
	blinking = False

	def __init__(self):
		g.setup(11, g.OUT) #Botlampe
		g.setup(15, g.IN, pull_up_down=g.PUD_UP) #Botschalter Hi=off
		
		g.add_event_detect(15, g.BOTH, callback=self.makeSpaceStatus, bouncetime=300)
	
	def blinking(self,interval,ratio):
		while self.blinking:
			a = interval*ratio
			b = interval-a
			g.output(11,1)
			sleep(a)
			g.output(11,0)
			sleep(b)
		
	def blink_start(self,interval,ratio=0.5):
		self.blinking = True
		thread(self.blinking,(interval,ratio))

	def blink_stop(self):
		self.blinking = False
	
	def makeSpaceStatus(self,ch):
		if g.input(15):
			#monitor on 
			call(["./monitor.sh","off"])
			sleep(5)
			
			# spacestatus close
			call(['curl','-d status=close', "https://hackerspace-bielefeld.de/spacestatus/spacestatus.php"])
			
			# port 15 off
			g.output(11,0)
			
			
			# in chat schreiben, dass spcae geschlossen
			sendMsg("--- Der Space ist nun geschlossen.")
			debugMsg("Space geschlossen")
		else:
			#monitor on 
			call(["./monitor.sh","on"])
			# etwas show
			#jabber.disconnect()
			g.output(11,1)
			sleep(0.1)
			g.output(11,0)
			sleep(0.1)
			g.output(11,1)
			sleep(0.1)
			g.output(11,0)
			sleep(0.1)
			g.output(11,1)
			sleep(0.1)
			g.output(11,0)
			sleep(0.1)
			g.output(11,1)
			sleep(0.1)
			g.output(11,0)
			sleep(0.1)
			g.output(11,1)
			sleep(0.1)
			g.output(11,0)
			sleep(0.1)
			g.output(11,1)
			sleep(0.1)
			g.output(11,0)
			sleep(0.1)
			g.output(11,1)
			sleep(0.1)
			g.output(11,0)
			sleep(0.1)
			g.output(11,1)
			sleep(0.1)
			g.output(11,0)
			sleep(0.1)
			g.output(11,1)
			sleep(0.1)
			g.output(11,0)
			sleep(0.1)
			g.output(11,1)
			sleep(0.1)
			g.output(11,0)
			sleep(0.1)
			g.output(11,1)
			sleep(0.1)
			g.output(11,0)
			sleep(0.1)
			g.output(11,1)
			sleep(0.1)
			g.output(11,0)
			sleep(0.1)
			
			
			#jabber.newSession()
			# spacestatus open
			call(['curl','-d status=open', "https://hackerspace-bielefeld.de/spacestatus/spacestatus.php"])
			
			# port 11 on
			g.output(11,1)
			
			sleep(5)
			# in chat schreiben, dass space offen
			sendMsg("--- Der Space ist nun geffnet.")
			debugMsg("Space offen")
		lastStatus = time() #TODO

# GUI anlegen
f = Tk()
h = f.winfo_screenheight()
w = f.winfo_screenwidth()

#Fenster
f.title('HSBot2')
f.geometry(str(w)+"x"+str(h)+"+0+0")
f.wm_overrideredirect(True)
f.resizable(False, False)
f.config(bg="#000000")

# Label-Variablen
ts = StringVar()
ts.set("XX:XX")

ti = StringVar()
ti.set("------------")

to = StringVar()
to.set("TOAST")

#Textfelder
chat = Text(f,bg="#000000",fg="#ffffff",font=("Arial",32),bd=2,height=20,width=29)
clock = Label(f,textvariable=ts,fg="#ffffff", bg="#000000", bd=2,font=("Arial",108),width=5)
infoh = Label(f,textvariable=ti,fg="#ffffff", bg="#000000",font=("Arial",32))
infot = Text(f,bg="#000000",fg="#ffffff",font=("Arial",24),bd=2,height=19,width=22)	
toast = Label(f,textvariable=to,fg="#ffffff", bg="#000000", bd=2,font=("Arial",108),width=8)

chat.tag_add("all", "1.0", END)
chat.tag_config("all",wrap=WORD)
chat.grid(row=0,column=0,rowspan=3,sticky=NW)

# Clock
clock.grid(row=0,column=1,sticky=NE)

# Info Header
infoh.grid(row=1,column=1,sticky=S)

# Info Text
infot.tag_config("all",wrap=WORD)
infot.grid(row=2,column=1,sticky=SE)
f.rowconfigure(2, minsize=548)

data = "Chatfenster"

# sorgt fr die uhr
def getClock():
	global ts
	while True:
		lt = localtime()
		ts.set("%02i:%02i" % (lt.tm_hour,lt.tm_min))
		#f.update_idletasks()
		sleep(5)

# cycelt infos durch
def getInfo():
	global infot 
	global infoh
	while True:
		infos = {}
		tmp = os.listdir(c.INFPATH)
		for i in tmp:
			if not i.startswith(".") and i.endswith('.txt'):
				with open (c.INFPATH+"/"+i, "r") as myfile:
					data="".join(myfile.readlines())
					infos[i[:-4]] = data
			
		for j in infos:
			infot.delete("1.0",END)
			infot.insert(END, infos[j])
			infot.tag_add("all", "1.0", END)
			ti.set(j)
			infot.update()
			sleep(10)
	
#sendet nachricht an display	
def sendMsg(msg):
	global chat
	chat.insert(END, msg + "\n")
	chat.tag_add("all", "1.0", END)
	chat.see(END)
	chat.update()
	f.update_idletasks()
	
io = IOPorts()
	
thread(getClock,())
thread(getInfo,())

mqtt = MQTT()
jabber = Jabber()
thread(jabber.run,())
thread(mqtt.run,())




mainloop()
