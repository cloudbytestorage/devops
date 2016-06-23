import os
import json 
import subprocess
option=raw_input("Press 1 for mount or 2 for unmount\n")
directory=raw_input("Enter the directory name to be mounted or unmount\n")

if option=="1":

	ip=raw_input("Enter the tsm ipaddress\n")

	command = 'showmount -e '+ip+' |cut -d ":" -f 2|cut -d " " -f 1'

	#print "output of command - " +command

	link = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)

	ldata = link.stdout.readlines()
	#print "what is ldata"+str(ldata)+" - "+str(type(ldata))

	output, errors = link.communicate()

	#print "what is error"+str(errors)

	rco = link.returncode

	#print "print output = "+str(output)

	i=1

	for a in ldata:
		if a!='\n':
			folder = directory+str(i)
			dir=str(os.system("mkdir /"+folder))
		#print "print dir = "+str(dir)
		#print "print ip= "+str(ip)
		#print "print a = "+str(a)
        	#print "*******************"
        
	
			cmd="mount " +str(ip)+":"+a.strip(" \n\r\t")+" /"+folder+""
		#print "command for mounting = "+str(cmd)
			link=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
			ldata = link.stdout.readlines()


			output, errors = link.communicate()


			rco = link.returncode

		#print "print output = "+str(output)
			print"The NFS share :"+str(a)
			print"is mounted on Directory"+folder
	
        		i=i+1


elif option=="2":
	cmd="ls / |grep "+directory+"*"
	#print "command for listing directories = "+str(cmd)	
	link = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
	ldata=link.stdout.readlines()
	for a in ldata:
		os.system("umount /"+a+"")
		os.system("rm -rf /"+a+"")
		print "Unmounted and removed directory"+a
