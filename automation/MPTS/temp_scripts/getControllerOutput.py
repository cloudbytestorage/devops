#!/usr/local/bin/python
import paramiko
import os
import subprocess
import getpass
import sys
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, executeCmd, filesave1

config = configFile(sys.argv);
localoutputdir='logs/output'
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


def createSFTPConnection(IP='localhost',user='root',paswd='test'):
    t = paramiko.Transport((IP,22)) 
    t.connect(username=user, password=paswd)
    sftp = paramiko.SFTPClient.from_transport(t) 
    return sftp

def getControllerInfo(ip, passwd, command):
    ssh.connect(ip, username="root", password=passwd, allow_agent = False)
    stdin, stdout, stderr = ssh.exec_command(command)
    #print "Stdout = "+stdout.read()
    output = stdout.read()
    filesave1(localoutputdir+"/myoutputfile.txt", "w", output)
    ssh.close()
    print "Output Available: "+str(ip)+" path: "+localoutputdir

if __name__=='__main__':
    if os.path.exists(localoutputdir):
        os.system("rm -rf "+localoutputdir) 
        os.system("mkdir "+localoutputdir)
    else: 
        os.system("mkdir "+localoutputdir)
    for i in range (1, 2):
        try:
            IP = "20.10.68.20"
            passwd = "test"
            program = "ip_get.sh"
            command = "zpool list"
            getControllerInfo(IP, passwd, command)
        except Exception, ex:
            print("An Unknown exception occured: "+ str(ex))
            print("pls check controller: "+str(IP)+" is pingable")



