#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import socket
import json
import requests

HOST_NAME = '192.168.7.191'
PORT_NUMBER = 80

SUPERVISOR_ADDRESS = "http://localhost:8080/reader"

class Server(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		self.wfile.write("<ORBIT>\nUI=a00000\n\n</ORBIT>".encode("utf-8"))
		handle_nfc(self.path)
		return

def handle_nfc(url):
	uid_len, uid = get_uid(url)
	print ('Uid_len:', uid_len)
	print ('Uid:', uid)
	if uid_len is not False:
		send_response(uid_len, uid)

def send_response(uid_len, uid):
	response = json.dumps({'reader': 'NFC', 'id': uid})
	requests.post(SUPERVISOR_ADDRESS, data=response)

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
	print ('Started httpserver on port ' , PORT_NUMBER)

	server.serve_forever()

except KeyboardInterrupt:
	print ('^C received, shutting down the web server')
	server.socket.close()

