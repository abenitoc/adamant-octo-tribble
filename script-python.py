#!/usr/bin/python

from lxml import etree
from subprocess import call
import shutil
import os
import sys
import time
from copy import deepcopy

############## CONTEXT VARIABLES ###############

VMs = ['lb', 'c1', 's1', 's2', 's3','s4','s5']

############## CONTEXT VARIABLES ###############

############### AUXILIAR FUNCTIONS #############

def modifyXML(xml_path, vm_path, name):	
	xml_struct = etree.parse(xml_path)
	
	root_node = xml_struct.getroot()
	
	machinename = root_node.find('name')
	machinename.text = name
	
	disk_source = root_node.find('devices').find('disk').find('source')
	disk_source.set('file', "/mnt/tmp/" + name + "/" + name + ".qcow2")

	bridge_source =  root_node.find('devices').find('interface').find('source')	
	if name == "c1":
		bridge_source.set('bridge', "LAN2")
	else:
		bridge_source.set('bridge', "LAN1")
	
	if name == "lb":
		devices = root_node.find('devices')
		interface = devices.find('interface')
		interface2 = deepcopy(interface)
		interface2.find('source').set('bridge',"LAN2")
		devices.append(interface2)
	
	with open(xml_path, 'w') as fout:
		fout.write(etree.tostring(xml_struct).decode('utf-8'))
	

def relocateFiles():
	#Base Cases
	if not os.path.exists('machines'):
		os.makedirs('machines')
	
	os.chdir('machines')

	if not os.path.exists('machines/cdps-practica.qcow2'):	
		shutil.copy2('/mnt/vnx/repo/cdps-vm-base-p3.qcow2.bz2', os.getcwd())
		call(["bunzip2", "cdps-vm-base-p3.qcow2.bz2"])
	
	if not os.path.exists('machines/plantilla-vm-p3.xml'):
		shutil.copy2('/mnt/vnx/repo/plantilla-vm-p3.xml', os.getcwd())

def createVMs(number):
	#create images and all xmls and modififies
	for name in VMs:
		call(['qemu-img','create','-f','qcow2','-b','cdps-vm-base-p3.qcow2', name + '.qcow2' ])
		shutil.copy2('plantilla-vm-p3.xml', './' + name + '.xml')
		modifyXML(name + '.xml', name +'.qcow2', name  )			

	call(["sudo", "brctl", "addbr", "LAN1"])
	call(["sudo", "brctl", "addbr", "LAN2"])
	call(["sudo", "ifconfig", "LAN1", "up"])
	call(["sudo", "ifconfig", "LAN2","up"])	

def openVMs():
	print "n"	

############### AUXILIAR FUNCTIONS #############

################ MAIN FUNCTIONS ##############

def create(machines_number):
	relocateFiles()
	machines_erased = len(VMs) - (machines_number + 1)
	for i in range( 1, machines_erased ):
		del VMs[-1]
	
	createVMs(len(VMs))
			
def start():
	os.system("HOME=/mnt/tmp sudo virt-manager")			
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
		create(user_input)
		print 'Machines created'	
elif param1 == 'start': 
	start()
	print 'Machines started'	
elif param1 == 'stop':
	print 'stop'
elif param1 == 'destroy':
	os.chdir('machines')
	call(['rm', 'lb*', 'c1*', 's*'], shell=True)
else:
	print 'Parametros no reconocidos' 

print("Finished in %s seconds" % (time.time() - start_time))
################ PROGRAM DEFINITION ################
