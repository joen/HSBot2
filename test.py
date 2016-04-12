#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib3

def website():
	ret = list()
	http = urllib3.PoolManager()
	r = http.request('GET', 'http://hackerspace-bielefeld.de/')
	if r.status == 200:
		data = r.data.split("\n")
		s = 0
		for d in data:
			d = d.strip()
			if s == 1 and d == "<hr>":
				break
			
			if s == 1 and d.startswith('<h3 class="entry-title">'):
				i_start = d.find(">",25)+1
				i_stop = d.find("<",i_start)
				j_start = d.find(">",i_stop)
				j_stop = d.find("<",j_start)
				i = d[i_start:i_stop]
				j = d[j_start:j_stop].split(', ')
				time = j[0].split(".")
				ret.append(time[2],time[1],time[0],i+" "+j[1])
				
				print (d[i_start:i_stop])
				#print (d)
			
			if s == 0 and d == "<h2>Anstehende Veranstaltungen</h2>":
				s=1
		return ret
	else:
		print("FEHLER")
		
website()
