#!/usr/bin/python

from lxml import etree
from subprocess import call
import shutil
import os
import sys
import time

############### AUXILIAR FUNCTIONS #############

def relocateXML(name):
	if not os.path.exists('machines'):
		os.makedirs('machines')

	shutil.copy2('/mnt/vnx/repo/plantilla-vm-p3.xml','machines/'+ name + '.xml')

############### AUXILIAR FUNCTIONS #############

################ MAIN FUNCTIONS ##############

def create():
	relocateXML('nueva')


################ MAIN FUNCTIONS ##############

################ PROGRAM DEFINITION ################
start_time = time.time()

param1 = sys.argv[1]

#parse $1 python
if param1 == 'create':
	create()
	print 'Machines succesfully created'	
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

print("Finished in %s seconds" % (time.time() - start_time))
################ PROGRAM DEFINITION ################
