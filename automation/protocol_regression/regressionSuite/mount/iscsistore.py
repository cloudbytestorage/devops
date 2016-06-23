import sys
import os
import subprocess
#ADD DATASTORE

def iscsidatastore(IP,storename,iscsihba):
  cmd='esxcli iscsi adapter discovery sendtarget add --address='+str(IP)+':3260 --adapter='+iscsihba[0].strip("\n\t\r")+''
  login = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
  iscsilogin=login.stdout.readlines()
  cmd1='esxcfg-rescan '+iscsihba[0].strip("\n\t\r")+''
  res = subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
  rescanhba=res.stdout.readlines()
  print "ISCSI datastore created successfully"
#DELETE DATASTORE  

def deletestore(IP,storename,iscsihba):
  cmd='esxcli iscsi adapter target portal list |grep '+str(IP)+' |cut -d " " -f 3'
  link1 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
  ldata = link1.stdout.readlines()
  for a in ldata:
     cmd1='esxcli iscsi adapter discovery statictarget remove -A='+iscsihba[0].strip("\n\t\r")+' -a='+str(IP)+':3260 -n='+str(a).strip("\n\t\r")+''
     tar = subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
     staticremove = tar.stdout.readlines()
       
     cmd2='esxcli iscsi adapter discovery sendtarget remove --address='+str(IP)+':3260 -A='+iscsihba[0].strip("\n\t\r")+''
     #print cmd2
     dynamic = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
     stat= dynamic.stdout.readlines()
     
     resc='esxcfg-rescan '+iscsihba[0].strip("\n\t\r")+''
     #print resc
     res1 = subprocess.Popen(resc, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
     rescanhba=res1.stdout.readlines()
  print "ISCSI datastore deleted successfully"

if __name__ == "__main__":
   adapterlist = 'esxcli iscsi adapter list |grep vm |cut -d " " -f 1'
   link = subprocess.Popen(adapterlist, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
   iscsihba = link.stdout.readlines()
   
   choice=raw_input("Enter your choice 1 for creating datastore or ENTER for deleting datastore\n")
   if choice:
    iscsidatastore(sys.argv[1],sys.argv[2],iscsihba)
   else:
    deletestore(sys.argv[1],sys.argv[2],iscsihba)                        
