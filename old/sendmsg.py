#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket,json,sys

print(sys.argv[1])
data = json.dumps({'type':'chat','msg':sys.argv[1]})
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 2550))
s.sendall(data)
s.close()