#!/usr/bin/python
# -*- coding: utf-8 -*-

from time import localtime,time
from datetime import datetime as datetime
import urllib3,json
import config as c

#callback func für sorter
def timer(inp):
	return inp[0]*10000+inp[1]*100+inp[2]

# holt termine vom wordpress
def wordpress():
	ret = list()
	http = urllib3.PoolManager()
	r = http.request('GET', 'https://blog.hackerspace-bielefeld.de/?plugin=all-in-one-event-calendar&controller=ai1ec_exporter_controller&action=export_events&xml=true')
	if r.status == 200:
		#data = json.loads(r.data)
		data = r.data.split("\n")
		n = len(data)
		i = 0
		while i<n:
			if data[i].startswith("<vevent>"):
				i=i+6
				while not data[i].startswith("<dtstart"):
					i=i+1
				s = data[i].find(">")
				datum = [int(data[i][s+1:s+5]),int(data[i][s+5:s+7]),int(data[i][s+7:s+9]),""]
				
				while not data[i].startswith("<summary>"):
					i=i+1
				datum[3] = data[i][9:-11]
				#print(datum)
				ret.append(datum)
			i=i+1
			

		print(ret)
		return ret
		
	else:
		print("FEHLER")	
	
#list den abfall kalender
def abfall():
	with open (c.CACPATH+"/abfall.ics", "r") as myfile:
		r = list()
		data = myfile.readlines()
		n = len(data)
		i = 0
		while i<n:
			if data[i].startswith("DTSTART;VALUE=DATE:"):
				zeile = data[i]
				datum = [int(zeile[19:23]),int(zeile[23:25]),int(zeile[25:27]),""]
				
				i=i+8
				zeile = data[i]
				#print(data[i])
				datum[3] = "Abfall: "+zeile[20:-2]
				r.append(datum)
				i=i+7
			else:
				i=i+1
		return r
		

#termin liste
termine = list()
gesiebt = list()
sortiert = list()
		
#termine einlesen
termine.extend(abfall())
termine.extend(wordpress())
#print(termine)
now = localtime()
soon = localtime(time()+60*60*24*14)
#print(now)
print(soon)
for term in termine:
	print(term)
	if((term[0] == now.tm_year and ((term[1] == now.tm_mon and term[2] >= now.tm_mday) or (term[1] > now.tm_mon))) or term[0] > now.tm_year) and ((term[0] == soon.tm_year and ((term[1] == soon.tm_mon and term[2] <= soon.tm_mday) or (term[1] < soon.tm_mon))) or term[0] < soon.tm_year):
		print("+")
		gesiebt.append(term)

#print(gesiebt)
sortiert = sorted(gesiebt, key=timer)
#print(sortiert)
wif = ''
jetzt = [0,0,0]
wday = ("Mo","Di","Mi","Do","Fr","Sa","So")

for s in sortiert:
	if(not (s[0] == jetzt[0] and s[1] == jetzt[1] and s[2] == jetzt[2])):
		w = datetime(s[0], s[1], s[2], 12, 0, 0, 0).weekday()
		wif += "=== "+ wday[w] +", "+ str(s[2]) +"."+ str(s[1]) +". ===\n"
		jetzt[0] = s[0]
		jetzt[1] = s[1]
		jetzt[2] = s[2]
	
	wif += str(s[3]) +"\n"
	
with open (c.INFPATH+"/TeRmInE.txt", "w") as myfile:
	myfile.truncate()
	myfile.write(wif)
