#!/usr/bin/env python
#-*- coding:utf-8 -*-

import imaplib
import argparse
import os
import datetime
import shutil
import email
import re
from email.parser import HeaderParser
import email.Header
from email.Header import decode_header
from functions import slugify
import json
import uuid


argparser = argparse.ArgumentParser(description="Dump a IMAP folder into .eml files", )
argparser.add_argument('-s', dest='host', help="IMAP host, like imap.gmail.com", required=True)
argparser.add_argument('-u', dest='username', help="Compte IMAP del Usuari", required=True)
argparser.add_argument('-p', dest='password', help="Password IMAP del Usuari", required=True)
argparser.add_argument('-r', dest='remote_folder', help="Origen de la copia (Directori Base dels correus). Per defecte: INBOX", default='INBOX')
argparser.add_argument('-l', dest='local_folder', help="Path de desti de la copia (per defecte, actual)", required=True)
argparser.add_argument('-sd', dest='start_date', help="Date Range Start. To select by date emails who will be backed up", default=None)
argparser.add_argument('-ed', dest='end_date', help="Date Range End. By default, NOW", default=datetime.datetime.now())
argparser.add_argument('-d', dest='delete_destination', help="If true, destination folder will be wiped!", default='false')
args = argparser.parse_args()

print args

connection = imaplib.IMAP4_SSL(args.host)
connection.login(args.username, args.password)
connection.select(args.remote_folder)

print 'Connected'

if os.path.exists(args.local_folder) and os.path.isabs(args.local_folder):
	if(args.delete_destination.lower() == 'true'):
		print 'INFO: Option -d detected!'
		confirm = raw_input('WARNING: This path and subcontent will be deleted: %s - Are you sure? (s/n): ' % os.path.join(args.local_folder,args.username))
		if confirm.lower() == 's':
			shutil.rmtree(os.path.join(args.local_folder,args.username))

mbtyp, mailboxes = connection.list()

backup_name = uuid.uuid4().hex
backup_mail_list = {}
backup_info = {
	"name": backup_name,
	"mailaccount": args.username,
	"backup_date": datetime.datetime.now(),
}

print backup_info

for mbox in mailboxes:
	mb = mbox.split('"')
	actual_folder = mb[3:4][0]
	
	actual_folder_str = os.path.join(args.local_folder, args.username)
	print actual_folder_str
	actual_folder_str = os.path.join(actual_folder_str,actual_folder.replace('.','/'))
	
	print actual_folder_str
	#Creem Directoris de l'estructura
	if not os.path.exists(actual_folder_str):
		print 'path not exist'
		os.makedirs(actual_folder_str)

	connection.select(actual_folder)

	print 'Folder: %s' % actual_folder

	typ, data = connection.search(None, 'ALL')
	for num in data[0].split():
		typ, data = connection.fetch(num, '(RFC822)')
		styp, sdata = connection.fetch(num, '(BODY[HEADER])')
		header_data = sdata[0][1]
		parser = HeaderParser()
		msg = parser.parsestr(header_data)
		dh = decode_header(msg.get('subject'))
		default_charset = 'ASCII'
		try:
			subject = ''.join([ unicode(t[0], t[1] or default_charset) for t in dh ])
			subject = slugify(subject)
			if subject is None:
				subject = ''
		except:
			subject = ''

		f = open('%s/%s.%s.eml' %(actual_folder_str, num, subject), 'w')
		print >> f, data[0][1]