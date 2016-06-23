import json
import requests
import md5
import fileinput
import subprocess
import time
import datetime
import paramiko
import os
import getpass
import sys
import logging
from cbrequest import executeCmd, sshToOtherClient, getControllerInfo

CLIENT1_IP = '20.10.26.12'
CLIENT1_USER = 'root'
CLIENT1_PASSWORD = 'test123'
CLIENT_NFS_MOUNT_PNT = '/mnt/nfstest'
NFS_DATASET_MNT_PT = 'AccNFS1'

mkdir_cmd = 'mkdir %s' %(CLIENT_NFS_MOUNT_PNT)
#mount_cmd = 'mount -o mountproto=tcp,sync %s:/%s %s' %(CLIENT_NFS_MOUNT_PNT, NFS_DATASET_MNT_PT, CLIENT_NFS_MOUNT_PNT)
#print mount_cmd
#exit()
#output = getControllerInfo('20.10.94.62', 'test@321', 'mkdir /mnt/mardan', 'abc.txt')
#print output
#mkdir_result = sshToOtherClient('20.10.26.12', 'root', 'test123', 'mkdir /mnt/nfstest')
#print mkdir_result

#mount_result = sshToOtherClient(CLIENT1_IP, CLIENT1_USER, CLIENT1_PASSWORD, 'df -h | grep sdm')
mount_result = sshToOtherClient(CLIENT1_IP, CLIENT1_USER, CLIENT1_PASSWORD, 'ls')
print mount_result

'''
client = SSHClient()
client.load_system_host_keys()
client.connect('ssh.example.com')
stdin, stdout, stderr = client.exec_command('ls -l')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect(CLIENT1_IP, username=CLIENT1_USER, password=CLIENT1_PASSWORD)
stdin, stdout, stderr = ssh.exec_command(mkdir_cmd)
output = stdout.read()
error = stderr.read()
ssh.close()
print output 
print error
'''

