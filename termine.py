#!/usr/bin/python
# -*- coding: utf-8 -*-

from time import localtime,time
import config as c

#callback func für sorter
def timer(inp):
	return inp[0]*10000+inp[1]*100+inp[2]

#list den abfall kalender
def abfall():
	with open (c.CACPATH+"/abfall.ics", "r") as myfile:
		r = list()
		data = myfile.readlines()
		n = len(data)
		i = 0
		while i<n:
			#print(i)
			if data[i].startswith("DTSTART;VALUE=DATE:"):
				zeile = data[i]
				datum = [int(zeile[19:23]),int(zeile[23:25]),int(zeile[25:27]),""]
				
				i=i+8
				zeile = data[i]
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

now = localtime()
soon = localtime(time()+60*60*24*7)
#print(now)
#print(soon)
for term in termine:
	#print(term)
	if(term[0] >= now.tm_year and term[0] <= soon.tm_year and term[1] >= now.tm_mon and term[1] <= soon.tm_mon and term[2] >= now.tm_mday and term[2] <= soon.tm_mday):
		gesiebt.append(term)

#print(gesiebt)
sortiert = sorted(gesiebt, key=timer)
#print(sortiert)
wif = ''
jetzt = [0,0,0]
for s in sortiert:
	if(not (s[0] == jetzt[0] and s[1] == jetzt[1] and s[2] == jetzt[2])):
		wif += "=== "+ str(s[2]) +"."+ str(s[1]) +". ===\n"
		jetzt[0] = s[0]
		jetzt[1] = s[1]
		jetzt[2] = s[2]
	
	wif += str(s[3]) +"\n"
	
with open (c.INFPATH+"/Termine.txt", "w") as myfile:
	myfile.truncate()
	myfile.write(wif)

 