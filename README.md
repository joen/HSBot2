dies soll in absehbarer zukunft infobeamer, spacestatus und chatbot ersetzen

wir brauchen
	apt-get install python python-tk python-sleekxmpp ssh mc nano wget python-pip git
	pip install python-telegram-bot
	pip install paho-mqtt
	apt-get install vlc
lighttpd installieren
	sudo apt-get install lighttpd php5 php5-cgi php5-common php-pear php5-sqlite php5-dev sqlite3
	sudo lighty-enable-mod fastcgi 
	sudo lighty-enable-mod fastcgi-php
	service lighttpd force-reload	
mit 
	git clone https://github.com/electronicfreak/HSBot
die daten holen
	
	nano /etc/lighttpd/lighttpd.conf
dann den ordner und groupname = pi anpassen
	sudo service lighttpd force-reload


aus example.config.py eine example.py fertig machen (pw eintragen)

LXDE installieren
	apt-get install lightdm
LXDE sich automatisch einloggen lassen
	nano /etc/lightdm/lightdm.conf
die zeile 
	autologin-user= 
einkommentieren und gewünschten user eintragen 

FERTIG 
----------------------------------------

webserver howto
https://www.scandio.de/2012/11/setting-up-a-lightweight-webserver-with-lighttpd-php5-and-sqlite3/
	
	
temperatur fühler:
https://www.raspberrypi.org/forums/viewtopic.php?f=37&t=30325

wiki:
https://wiki.hackerspace.bi/Garuda


