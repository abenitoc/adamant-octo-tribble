#!/usr/bin/python

from lxml import etree
from subprocess import call
import shutil
import os
import sys

param1 = sys.argv[1]

#parse $1 python
if param1 == 'create':
	print 'n'	
elif param1 == 'start': 
	xml_path = "plantilla-vm-p3.xml"
	xml_struct = etree.parse(xml_path)
	print etree.tostring(xml_struct, pretty_print=True)
elif param1 == 'stop':
	print 'stop'
elif param1 == 'destroy':
	print 'l'
else:
	print 'Parametros no reconocidos' 
