#!/usr/bin/python
# -*- coding: utf-8 -*-

from time import localtime,time
from datetime import datetime as datetime
import urllib3
import config as c

#callback func für sorter
def timer(inp):
	return inp[0]*10000+inp[1]*100+inp[2]

# holt termine vom wordpress
def wordpress():
	ret = list()
	http = urllib3.PoolManager()
	r = http.request('GET', 'http://hackerspace-bielefeld.de/')
	if r.status == 200:
		data = r.data.split("\n")
		s = 0
		for d in data:
			d = d.strip()
			ee = d.split('</h3><h3 class="entry-title">')
			if s == 2: 
				try:
					for e in ee:
						i_start = e.find(">",25)+1
						i_stop = e.find("<",i_start)
						j_start = e.find(">",i_stop)+1
						j_stop = e.find("<",j_start)
						i = e[i_start:i_stop]
						j = e[j_start:j_stop].split(', ')
						time = j[0].split(".")
						ret.append([int(time[2]),int(time[1]),int(time[0]),i+" "+j[1]])
					break;
				except:
					pass
					
			if s == 1:
				s=2
			
			if s == 0 and d == "<h2>Anstehende Veranstaltungen</h2>":
				s=1
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
soon = localtime(time()+60*60*24*7)
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
	
with open (c.INFPATH+"/Termine.txt", "w") as myfile:
	myfile.truncate()
	myfile.write(wif)