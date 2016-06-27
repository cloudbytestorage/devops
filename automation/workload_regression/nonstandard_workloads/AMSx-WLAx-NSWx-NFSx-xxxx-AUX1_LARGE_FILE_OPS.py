import sys
import logging
from time import ctime, sleep
from subprocess import call, check_output
import os

script_name = sys.argv[0]
mount_point = sys.argv[1]
FileDir = 'a'
location = '%s/%s' %(mount_point, FileDir)

test_log = '/root/LargeSingleFileCreateRMWDelete.log'

FileSize = 20 #in GB
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
    
    #FLUSH CACHE
    call ("echo 3 > /proc/sys/vm/drop_caches", shell=True)

    call ("echo 'FILES CREATED' > %s" %(test_log), shell=True)

def ReadModifyWrite():
    ReadFiles(location, ddBlockSize, ddCountValue)
    ModifyWriteFiles(location, bSize, ddCountValue)
    call ("echo 'FILES READ MODIFIED WRITTEN' >> %s" %(test_log), shell=True)

def Delete():
    DeleteFiles(location)
    call ("echo 'FILES DELETED' >> %s" %(test_log), shell=True)

def umount(mnt_pt):
    res = call ("umount %s" %(mnt_pt), shell=True)
    return res

def lazyumount(mnt_pt):
    call ("umount -l %s" %(mnt_pt), shell=True)

def checkMountUser(mnt_pt):
    res = check_output ("lsof %s | awk '{print $2}' | grep -v 'PID'" %(mnt_pt), shell=True)
    list = str(res)
    pidlist = list.split()
    return pidlist

def killer(processes):
    for x in processes:
        call ("kill -9 %s" %(x), shell=True)
        sleep(5)

def UMain(path):
    result = umount(path)
    if int(result) == 0:
        print "unmounted volume successfully"
    elif int(result) == 16:
        print "umount response is EBUSY"
        processlist = checkMountUser(path)
        print "Processes using mount point are %s" %(processlist)
        print "Attempting Kill of above processes..."
        killer(processlist)
        print "Attempting umount now.."
        newresult = umount(path)
        if int(newresult) == 0:
            print "unmounted volume successfully NOW"
        elif int(newresult) == 16:
            print "Attempting lazy umount"
            lazyumount(path)
            print "lazy-umounted volume successfully"

def main():
    Create()
    ReadModifyWrite()
    Delete()
    UMain(mount_point)

main()





    



