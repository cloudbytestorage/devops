import sys
import logging
from cbrequest import executeCmd, sshToOtherClient, getControllerInfo, putFileToController, sshToRemoteClient

CLIENT1_IP = '20.10.26.12'
CLIENT1_USER = 'root'
CLIENT1_PASSWORD = 'test123'
CLIENT_NFS_MOUNT_PNT = '/mnt/nfsnew'
OUTPUT_FILE1 = '/mnt/opfile1'
OUTPUT_FILE2 = '/mnt/opfile2'


mkdir_cmd = 'mkdir %s', CLIENT_NFS_MOUNT_PNT
#mount_cmd = 'mount -o mountproto=tcp,sync 20.10.199.189:/Account1DontDeleteVolume %s', CLIENT_NFS_MOUNT_PNT

mkdir_result = getControllerInfo(CLIENT1_IP, CLIENT1_PASSWORD, mkdir_cmd, OUTPUT_FILE1)
print "mkdir_result"

#mount_result = sshToOtherClient(CLIENT1_IP, CLIENT1_USER, CLIENT1_PASSWORD, mount_cmd)
#mount_result = getControllerInfo(CLIENT1_IP, CLIENT1_PASSWORD, mount_cmd, OUTPUT_FILE2)
#print "mount_result"

#src_file = 'FileCreateReadModifyWriteDelete.sh'
#dst_file = src_file
#dst_file = '/home/workload.sh'
#file_transfer_result = putFileToController(CLIENT1_IP, CLIENT1_PASSWORD, src_file, dst_file)
#print file_transfer_result


#result = sshToOtherClient(CLIENT1_IP, CLIENT1_USER, CLIENT1_PASSWORD, 'ls' )
#print result
