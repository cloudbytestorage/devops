#######################################################################################################################
# Script Name : iscsi_io_runner_windows.py
# Description : Discover, create persistent devices, login into iSCSI targets, format drives & run I/O
# Args : Scipt takes TSM IPs as argument                                                                               
# Pre-Requisites :a) Run the configCreator.sh before running this script b) Place the script in the vdbench directory 
# Creation Date : 15/08/2016                                                                                          
# Modifications : None											               		
# Script Author : Karthik											      
#######################################################################################################################

import sys
import os
import argparse
import subprocess
import socket
import platform
import re
import time
import string

# creating object for argument parser
parser = argparse.ArgumentParser()

# assigning defination for required paramaters
parser.add_argument("--vsms_ip", nargs='+', help="give vsms ip with space separated as parameter")

# assigning required parameters to args
args = parser.parse_args()
vsms_ip = args.vsms_ip

#vsm_ip = sys.argv[1]
success_string = "The operation completed successfully"

# Function that uses inbuilt python routines to validate IP string
def IPvalidator(ip):
	try:
		socket.inet_aton(ip)
		return True
	except socket.error:
		return False

# Function that uses ping for min trials w/ with min time b/w attempts to determine connectivity
def ping(host):
	try:
		result = subprocess.check_output ("ping -n 1 -w 10 %s" %(host), shell=True)
		return True
	except subprocess.CalledProcessError as e:
		return False

# Function that creates the batch file fed to diskpart util for disk ops
def BatchCreator(DiskNumber, DiskName, DriveLetter):
	line1 = "select disk %s" %(DiskNumber)
	line2 = "online disk"
	line3 = "attributes disk clear readonly"
	line4 = "clean"
	line5 = "create partition primary"
	line6 = "format fs=ntfs label=%s quick" %(DiskName)
	line7 = "assign letter %s" %(DriveLetter)
	with open('disk.bat', 'w') as f:
		f.write("%s \n%s \n%s \n%s \n%s \n%s \n%s \n" %(line1, line2, line3, line4, line5, line6, line7))
		
# Function that execute the diskpart functions to prepare drive for I/O
def DiskPartUtil():
	try:
		diskpart_result = subprocess.check_output ("diskpart.exe /s disk.bat", shell=True)
		if "DiskPart successfully formatted the volume" in diskpart_result:
			print diskpart_result
		else:
			print "Diskpart operation failed on disk %s, please check LUN" %(num)
			exit()
			time.sleep(1)
	except subprocess.CalledProcessError as e:
		print "Diskpart operation failed on disk %s, please check LUN" %(num)
		
# Function that consructs the fsd elements in vdbench config file
def vdFSDCreator(disknum, dir):
	sdLine = 'fsd=fsd-%s,anchor=%s:/vdir,depth=1,width=1,files=1,size=2G' %(disknum, dir) + '\n'
	with open('vdConfigFile', 'a') as vd:
		vd.write("%s" %(sdLine))
		
def GetDriveNum(lineitem):
	diff = len(lineitem.split()[5]) - 18 # 18 is Typical length of \\.\PHYSICALDRIVE?  
	if diff > 0:
		indices = diff + 1 # indices will refer to the actual drive number digits
		numlist = []
		for i in range(1, indices + 1):
			numlist.insert(0, line.split()[5][-i])
		numval = ''.join(numlist)
		return numval
	else:
		numval = line.split()[5][17]
		return numval
		
		
#### START OF MAIN FUNCTION ####

for vsm_ip in vsms_ip:
	
	# IP validation
	ip_valid = IPvalidator(vsm_ip)
	if ip_valid is False:
		print "Invalid IP address %s, re-run with correct IP address" %(vsm_ip)
		exit()

	# Connectivity check	
	ping_check = ping(vsm_ip)
	if ping_check is False:
		print "VSM IP address %s is not reachable, ensure VSM is accessible" %(vsm_ip)
		exit()
	
	# Attempt addition on iSCSI portal groups - iterate for every IP provided
	try:
		DiscoveryResult = subprocess.check_output ("iscsicli.exe AddTargetPortal %s 3260" %(vsm_ip), shell=True, stderr=subprocess.STDOUT)
		print "Addition of target portal is successful"
	except subprocess.CalledProcessError as e:
		print "Unable to add target portal, check the VSM IP \n"
		exit()

# List all targets from above IPs		
try :
	TargetList = subprocess.check_output ("iscsicli.exe ListTargets | findstr iqn", shell=True).rsplit()
	print "Identified Targets. Target list : %s" %(TargetList)
except subprocess.CalledProcessError as e:
	print "No targets found, please check LUN accessibility"
	exit()

# Attempt persistent login into all listed targets (Add into favourite targets)
for i in TargetList:
	try:
		PersistentLoginResult = subprocess.check_output ("iscsicli.exe PersistentLoginTarget %s T * * * * * * * * * * * * * * * 0" %(i), shell=True)
		print "Persistent Login of target is successful"
	except subprocess.CalledProcessError as e:
		print "Persistent Login attempt failed, check the LUN status OR check if target is already logged in"
		exit()		
		
# Attempt to setup ITN with all persistent target devices, construct a connection.log to store session/connection details		
for j in TargetList:
	try:
		QLoginResult = subprocess.check_output ("iscsicli.exe QLoginTarget %s" %(j), shell=True)
		if str(success_string) in QLoginResult:
			iqnval = '\n' + "Volume : %s" %(j) + '\n'
			with open('connection.log', 'a') as file:
				file.writelines(iqnval)
			for line in QLoginResult.splitlines():
				if re.search('Session', line): # re.search returns some kind of "match status"
					sid = line.split()[3]
				if re.search('Connection', line):
					cid = line.split()[3]
			if sid:
				sidwrite = "session id : %s" %(sid) + '\n'
				with open('connection.log', 'a') as file:
					file.writelines(sidwrite)
			else:
				print "Unable to determine session id, check the login status of LUN"
				exit()
				
			if cid:
				cidwrite = "connection id : %s" %(cid) + '\n'
				with open('connection.log', 'a') as file:
					file.writelines(cidwrite)
			else:
				print "Unable to determine session id, check the login status of LUN"
				exit()
		else:
			print "Couldn't login into target, check LUN status"
			exit()
			
	except subprocess.CalledProcessError as e:
		print "Login attempt failed, check the LUN status OR check if target is already logged in"
		exit()
			
# Empty out previous/existing vdbench config files with same name
open('vdConfigFile', 'w').close()

# Initialize a master list that will contain disk #, Label & Drive letter 
CombinedDiskList = []

# D:68, E:69,...,Z:90
DriveLetterASCSII = 69 # Start Drive letter assignment from E:

# Sleep for a couple of seconds before listing drives
time.sleep(5)

# List set of existing disks post ITN establishment
DriveList = subprocess.check_output ("wmic diskdrive list brief | findStr CloudByt", shell=True)
for line in DriveList.splitlines():
	if re.search('CloudByt', line):
		print line
		IndividualList = []
		name = line.split()[1]
		#num = line.split()[5][17]
		num = GetDriveNum(line)
		IndividualList.append(num)
		IndividualList.append(name)
		IndividualList.append(chr(DriveLetterASCSII))
		DriveLetterASCSII = DriveLetterASCSII + 1 
		CombinedDiskList.append(IndividualList)
print CombinedDiskList


for item in CombinedDiskList:
	# Create disk.bat for disk num/label/letter combo
	BatchCreator(item[0], item[1], item[2])
	
	# Execute above disk.bat
	DiskOpsResult = DiskPartUtil()
	
	# Construct fsd for all formatted disks
	vdFSDCreator(item[0], item[2])

# Add fwd & rd once all fsds' are constructed	
wdLine = 'fwd=fwd1,fsd=fsd*,xfersize=4k,rdpct=50,fileio=random,threads=1'	
rdLine = 'rd=rd1,fwd=fwd*,elapsed=36000000000,interval=1,fwdrate=max,format=yes'
with open('vdConfigFile', 'a') as vd:
	vd.write("%s \n%s" %(wdLine, rdLine))

# Construct timestamp for vdbench output folder
stamp = time.ctime().replace(" ", "-").replace(":", "-")

# Initiate I/O by invoking vdbench
subprocess.call ("vdbench.bat -f vdConfigFile -o %s" %(stamp), shell=True)


	
		
		

	

	

	
	

	
	

	
	



