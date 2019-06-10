#!/usr/bin/python3 
from http.server import HTTPServer, BaseHTTPRequestHandler
from tinydb import TinyDB, Query
from datetime import datetime
import socket

HOST_NAME = '192.168.7.191'
PORT_NUMBER = 80


class Server(BaseHTTPRequestHandler):
	def do_GET(self):
		command = handle_nfc(self.path)

		if command is 'Open':
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write("<ORBIT>\nGRNT=05\nUI=820432\n\n</ORBIT>".encode("utf-8"))

		elif command is 'Close':
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write("<ORBIT>\nDENY=05\nUI=A00332\n\n</ORBIT>".encode("utf-8"))

		elif command is 'PING':
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write("<ORBIT>RLY=1\nUI=000000\n\n</ORBIT>".encode("utf-8"))

		return

def handle_nfc(url):
	uid_len, uid = get_uid(url)
	print ('Uid_len:', uid_len)
	print ('Uid:', uid)
	if uid_len is not False:
		Uid = Query()
		if db.search(Uid.uid == uid):
			print ("%s Door opening. UID: %s" % (str(datetime.now()), uid))
			return 'Open'
		else:
			print("%s Unauthorized access. UID: %s" % (str(datetime.now()), uid))
			return 'Close'
	else:
		return 'PING'

def get_uid(url):
	if "ulen" in url:
		uid_len = int(url[url.find("ulen") + 5])
		uid_start = int(url.find("uid")) + 4
		uid = url[uid_start:(uid_start + uid_len * 2)]
		return (uid_len, uid)
	else:
		return (False, False)
try:
	server = HTTPServer((HOST_NAME, PORT_NUMBER), Server)
	print ("%s Started httpserver on port %d" % (str(datetime.now()), PORT_NUMBER))
	db = TinyDB('db.json')

	server.serve_forever()

except KeyboardInterrupt:
	print ('^C received, shutting down the web server')
	server.socket.close()

