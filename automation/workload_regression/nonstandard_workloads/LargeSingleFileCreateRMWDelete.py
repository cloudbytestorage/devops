import sys
import logging
from time import ctime
from subprocess import call

script_name = sys.argv[0]
mount_point = sys.argv[1]
FileDir = 'a'
location = '%s/%s' %(mount_point, FileDir)

test_log = '/root/LargeSingleFileCreateRMWDelete.log'

FileSize = 460 #in GB
ddBlockSize = 1 # in M
ddCountValue = FileSize * 1024 / ddBlockSize
bSize = '%sM' %(ddBlockSize)

def CreateFiles(loc, bs, count):
    call ("dd if=/dev/urandom of=%s/file bs=%s count=%s" %(loc, bs, count), shell=True)

def ReadFiles(loc, bs, count):
    call ("dd if=%s/file of=/dev/null bs=%s count=%s" %(loc, bs, count), shell=True)

def ModifyWriteFiles(loc, bs, count):
    call ("dd if=/dev/urandom of=%s/file bs=%s count=%s conv=notrunc" %(loc, bs, count/2), shell=True)

def DeleteFiles(loc):
    call ("rm -rf %s/*" %(loc), shell=True)

def Create():
    call ("mkdir -p %s/%s" %(mount_point, FileDir), shell=True)
    CreateFiles(location, bSize, ddCountValue)
    call ("echo 'FILES CREATED' > %s" %(test_log), shell=True)

def ReadModifyWrite():
    ReadFiles(location, ddBlockSize, ddCountValue)
    ModifyWriteFiles(location, bSize, ddCountValue)
    call ("echo 'FILES READ MODIFIED WRITTEN' >> %s" %(test_log), shell=True)

def Delete():
    DeleteFiles(location)
    call ("echo 'FILES DELETED' >> %s" %(test_log), shell=True)

Create()
ReadModifyWrite()
Delete()








    



