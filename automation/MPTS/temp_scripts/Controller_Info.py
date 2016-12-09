#!/usr/local/bin/python
import paramiko
import os
import subprocess
import getpass
sourcedir='sample'
targetdir='logs'
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


def createSFTPConnection(IP='localhost',user='root',paswd='test'):
    t = paramiko.Transport((IP,22)) 
    t.connect(username=user, password=paswd)
    sftp = paramiko.SFTPClient.from_transport(t) 
    return sftp

def getControllerInfo(ip,passwd):
    ssh.connect(ip, username="root", password=passwd, allow_agent = False)
#    i, o, e = ssh.exec_command("sed -i -e 's/root/#root/g' /etc/ftpusers") # example command
#    s = e.read()
#    if s: # an error occurred
#        raise RuntimeError, s
#    result = o.read()
    sftp=createSFTPConnection(ip,'root',passwd)
    sftp.put("ip_get.sh","/tmp/ip_get.sh",callback=None)
    sftp.close()
    ssh.exec_command("/bin/sh /tmp/ip_get.sh")
    sftp=createSFTPConnection(ip,'root',passwd)
    sftp.get("/tmp/ifconfig_output","logs/if_config_output",callback=None)
    sftp.close()
    print "SuccesFully Info from: "+str(ip)+" path: "+targetdir

if __name__=='__main__':
    if os.path.exists(targetdir):
        os.system("rm -rf "+targetdir) 
        os.system("mkdir "+targetdir)
    else: 
        os.system("mkdir "+targetdir)
    for i in range (1, 2):
        try:
            IP = "20.10.68.10"
            passwd = "test"
            getControllerInfo(IP,passwd)
        except Exception, ex:
            print("An Unknown exception occured: "+ str(ex))
            print("pls check controller: "+str(IP)+" is pingable")

ssh.close()
exit()


