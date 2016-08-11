#!/usr/bin/env python
#-*- coding:utf-8 -*-

import re

def parseCode(codi):
	parse = ""
	premove = [':','*','/','?','"']
	if(codi.find("iso-8859-1")!=-1 or codi.find("ISO-8859-1")!=1):
		dict = {}
		dict['E0'] = chr(224)
		dict['E1'] = chr(225)
		dict['E8'] = chr(232)
		dict['E9'] = chr(233)
		dict['ED'] = chr(237)
		dict['EE'] = chr(238)
		dict['F2'] = chr(242)
		dict['F3'] = chr(243)
		dict['FA'] = chr(250)
		dict['FB'] = chr(251)
		dict['E7'] = chr(231)
		dict['C7'] = chr(199)
		dict['C0'] = chr(192)
		dict['C1'] = chr(193)
		dict['C8'] = chr(200)
		dict['C9'] = chr(201)
		dict['CC'] = chr(204)
		dict['CD'] = chr(205)
		dict['D2'] = chr(210)
		dict['D3'] = chr(211)
		dict['D9'] = chr(217)
		dict['DA'] = chr(218)
		for key in dict.keys():
			codi = codi.replace("="+key,dict[key])
	codi = codi.replace("iso-8859-1","")
	codi = codi.replace("ISO-8859-1","")
	codi = codi.replace("=?","")
	codi = codi.replace("?=","")
	codi = codi.replace("?Q?","")
	codi = codi.replace("?q?","")
	codi = codi.replace("?b?","")
	codi = codi.replace("?B?","")

	for char in premove:
		codi = codi.replace(char, "_")
	return codi

def slugify(value):
	"""
	Normalizes string, converts to lowercase, removes non-alpha characters,
	and converts spaces to hyphens.
	"""
	import unicodedata
	value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
	value = unicode(re.sub('[^\w\s-]', '', value).strip().lower()) 
	value = unicode(re.sub('[-\s]+', '-', value))

	return value