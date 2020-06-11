#!/bin/python3
import hashlib
from cryptography.fernet import Fernet
from tinydb import TinyDB, Query
import datetime
import time

db = TinyDB('history.json')

def insertData(data, fileName):
	db.insert({'File': '{}'.format(str(fileName)),'Hash': '{}'.format(str(data)), 'Date/Time': str(datetime.datetime.now())})
	


def hashComputeMD5(fileName):
	
	hashComp = hashlib.md5()
	f = open("{}".format(str(fileName)), "rb")
	
	for c in iter(lambda: f.read(4096), b""):
		hashComp.update(c)
	print(hashComp.hexdigest())
	return hashComp.hexdigest()
	
	
q = Query()

def importantFiles():
	files = ['/etc/passwd','/etc/shadow']
	for f in files:
		print('The following file has the following hash: ')
		print('File: {}'.format(str(f)))
		print('Hash: ')
		hsh = hashComputeMD5(f)
		insertData(hsh, str(f))
		print('----------------------------------------------------')
	x = datetime.datetime.now()
	print('Computed at {}'.format(str(x)))
		
def searchDB():
	change = False
	hashList = []
	res = db.search(q.File == '/etc/passwd')
	print('Historic passwd Data - Last 10 entries: ')
	res = (res[-10:])
	for r in res:
		print(str(r))
		x = r.get("Hash")
		hashList.append(x)
	if hashList[-1] != hashList[-2]:
		print('Hash has changed since last scan...') 
		res = (res[-2:])
		print("Please See Below!")
		for r in res:
			print(str(r))
		
		
		
	
	print('-----------------------------------------------------------------------------')
	
	res = db.search(q.File == '/etc/shadow')
	print('Historic shadow Data - Last 10 entries: ')
	
	res = (res[-10:])
	for r in res:
		print(str(r))
		x = r.get("Hash")
		hashList.append(x)
	if hashList[-1] != hashList[-2]:
		print('Hash has changed since last scan...')
		res = (res[-2:])
		print("Please See Below!")
		for r in res:
			print(str(r))
		change = True

	if change == True:
		print("Email bit....")


		
		
	print('-----------------------------------------------------------------------------')


def main():
	con = True
	while con == True:
		try:
			print('Starting Scan...')
			time.sleep(3) 
			importantFiles()
			searchDB()
			time.sleep(120)
		except KeyboardInterrupt:
			print('Stopped and Quitting')
			con = False

main()
