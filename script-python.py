#!/usr/bin/python

from lxml import etree
from subprocess import call
from os import listdir
import shutil
import os
import sys
import time
import glob
from copy import deepcopy

############## CONTEXT VARIABLES ###############

VMs = ['lb', 'c1', 's1', 's2', 's3','s4','s5']

############## CONTEXT VARIABLES ###############

############### AUXILIAR FUNCTIONS #############

def clean_the_pool():
	pool = listdir(os.getcwd())
	pool.remove('cdps-vm-base-p3.qcow2.bz2')
	pool.remove('cdps-vm-base-p3.qcow2')
	pool.remove('plantilla-vm-p3.xml')

	for dirt in pool:
		os.remove(dirt)

def seek_and_power_machines():
	os.chdir('machines')
	found_unpowered_machines = glob.glob('*.xml')
	found_unpowered_machines.remove('plantilla-vm-p3.xml')
	for machine in found_unpowered_machines:
		call(["sudo", "virsh", "create", machine])

def modifyXML(xml_path, vm_path, name):	
	xml_struct = etree.parse(xml_path)
	
	root_node = xml_struct.getroot()
	
	machinename = root_node.find('name')
	machinename.text = name
	
	disk_source = root_node.find('devices').find('disk').find('source')
	disk_source.set('file', os.getcwd() + "/" + name  + ".qcow2")

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
	
	clean_the_pool()

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

def configureNetVMs(number):
	for name in VMs:
		if not os.path.exists("../mnt/" + name):
			os.makedirs("../mnt/" + name)

		call(["sudo","vnx_mount_rootfs","-s","-r", name + ".qcow2", "../mnt/" + name])
		ip = ""
		ip1 = ""
		ip2 = ""
		if name == "s1":
			ip = "10.0.2.11"
		elif name == "s2":
			ip = "10.0.2.12"
		elif name == "s3":
			ip = "10.0.2.13"
		elif name == "s4":
			ip = "10.0.2.14"
		elif name == "s5":
			ip = "10.0.2.15"
		elif name == "c1":
			ip = "10.0.1.3"
		elif name == "lb":
			ip1 = "10.0.1.1"
			ip2 = "10.0.2.1"
		else:
			ip1 = ""
			ip2 = ""
		if name == "s1" or name == "s2" or name == "s3" or name == "s4" or name == "s5":	
			call(["sudo", "chmod", "+w", "/etc/network/interfaces"])
			file = open("../mnt/" + name + "etc/network/interfaces","a")
			arguments = ["address " + ip + "\n", "netmask 255.255.255.0\n", "gateway 10.0.2.1\n"]
			file.writelines(arguments)
			file.close()
		if name == "lb":
			file = open("../mnt/" + name + "etc/network/interfaces","a")
			call(["sudo", "chmod", "+w", "/etc/network/interfaces"])
			arguments = ["address " + ip1 + "\n", "netmask 255.255.255.0\n", "\n\n","auto eth1\n" "iface eth1 inet static\n", "address" + ip2 + "\n", "netmask 255.255.255.0"]
			file.writelines(arguments)
			file.close()
		if name == "c1":
			call(["sudo", "chmod", "+w", "/etc/network/interfaces"])
			file = open("../mnt/" + name + "etc/network/interfaces","a")
			arguments = ["address " + ip + "\n", "netmask 255.255.255.0\n", "gateway 10.0.2.1\n"]
			file.writelines(arguments)
			file.close()

		file_name = open("../mnt/" + name + "etc/hostname", "w")
		file_name.write(name)
		file_name.close()

		call(["sudo", "vnx_mount_rootfs", "-u", "../mnt" + name])

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
	configureNetVMs(len(VMs))	
		
def start():
	seek_and_power_machines()
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
	call(["sudo", "virsh", "destroy", "s1"])
	call(["sudo", "virsh", "destroy", "s2"])
	call(["sudo", "virsh", "destroy", "s3"])
	call(["sudo", "virsh", "destroy", "s4"])
	call(["sudo", "virsh", "destroy", "s5"])
	call(["sudo", "virsh", "destroy", "c1"])
	call(["sudo", "virsh", "destroy", "lb"])
	#os.chdir('machines')
	#call(['rm', 'lb*', 'c1*', 's*'], shell=True)
elif param1 == 'test':
	os.chdir('machines')

else:
	print 'Parametros no reconocidos' 

print("Finished in %s seconds" % (time.time() - start_time))
################ PROGRAM DEFINITION ################
