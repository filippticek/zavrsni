#!/usr/bin/python3

from tinydb import TinyDB
import sys


db = TinyDB('db.json')
print ("To stop inserting write Q:")
print ("Input UID:")

for line in sys.stdin:
	if line.rstrip() == 'Q':
		exit()
	else:
		db.insert({'uid': line.rstrip()})

	print ("Input UID:")
