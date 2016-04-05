#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

# Ports & URLs
NODERED = "http://127.0.0.1:1880"					#wohin wird die nodered anfrage geschickt

# Pfade
INFPATH = os.path.dirname(os.path.realpath(__file__)) +"/info"		#da wo die info txt files liegen
JCERT = os.path.dirname(os.path.realpath(__file__)) +"/xmpp.pem"	#Jabber Certificate

# Jabber Daten
JUSER = "bot@jabber.space.bi"						#bot anmeldename
JNICK = "HSBot"								#Bot anzeigename
JPASS = "PgDNDy70aeqU2w"						#bot Passwort
JROOM = "hsb@chat.jabber.space.bi"					#bot raum

#Telegram Daten
TOKEN = "164086266:AAGSMwxJQH2Tp1Odgeujmaaw7vPalj-noMc"			#Telegram Bot Token
TFILE = os.path.dirname(os.path.realpath(__file__)) +"/cache/telegram-follower"	#eingetragene follower bei telegram

#MQTT Daten
MQTTSRV = "172.23.45.55"						#mqtt server
MQTTTOPI = "chat"							#mqtt chat topic
MQTTDEBU = "debug"							#mqtt debug topic

# GPIO Daten
INPINS = [8,10,11,12,13,15,16,18,21,22,23,24,26]
OUTPINS = []
