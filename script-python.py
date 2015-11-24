#!/usr/bin/python

from lxml import etree
from subprocess import call
import shutil
import os
import sys
import time

############### AUXILIAR FUNCTIONS #############

def modifyXML(xml_path, vm_path, name, interface):	
	xml_struct = etree.parse(path)
	
	root_node = xml_struct.getroot()
	
	machinename = root_node.find('name')
	machinename.text = name
	
	disk_sourcefile = root.find('devices').find('disk').find('source')
	disk_sourcefile.text = vm_path 
	bridge_sourcefile =  root.find('devices').find('interface').find('source')	
	bridge_source.text = interface

	print etree.tostring(xml_struct, pretty_print=True)
	

def relocateXML(name):
	#Base Cases
	if not os.path.exists('machines'):
		os.makedirs('machines')

	if not os.file.exists('machines/cdps-practica.qcow2'):
		shutil.call("bunzip /mnt/vnx/repo/cdps-vm-base3.bcow2.tar.gz .")
	
	
	shutil.copy2('/mnt/vnx/repo/plantilla-vm-p3.xml','machines/'+ name + '.xml')

def openVMs():
	print "n"	

############### AUXILIAR FUNCTIONS #############

################ MAIN FUNCTIONS ##############

def create(machines_number):
	for 1..machines_number
	relocateXML()	

################ MAIN FUNCTIONS ##############

################ PROGRAM DEFINITION ################

start_time = time.time()
if len(sys.argv) > 1:
	param1 = sys.argv[1]
else:
	param1 = 'notcorrect'

#parse $1 python
if param1 == 'create':
	user_input = input("How many VMs do you want to create (1 by default): ")
	if user_input >= 1 and user_input <= 5:
		create()
		print 'Machines succesfully created'	
elif param1 == 'start': 
	print 'start'
elif param1 == 'stop':
	print 'stop'
elif param1 == 'destroy':
	print 'l'
else:
	print 'Parametros no reconocidos' 

print("Finished in %s seconds" % (time.time() - start_time))
################ PROGRAM DEFINITION ################
