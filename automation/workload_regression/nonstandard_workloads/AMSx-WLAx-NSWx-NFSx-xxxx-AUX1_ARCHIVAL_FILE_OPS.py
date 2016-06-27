import sys
import logging
from time import ctime, sleep
from subprocess import call, check_output
import os

script_name = sys.argv[0]
mount_point_1 = sys.argv[1]
mount_point_2 = sys.argv[2]

FileDir = 'a'
location = '%s/%s' %(mount_point_1, FileDir)
backup_location = '%s' %(mount_point_2) 
test_log = '/root/Archival.log'

FileSize = 20 #in GB
ddBlockSize = 1 # in M
ddCountValue = FileSize * 1024 / ddBlockSize
bSize = '%sM' %(ddBlockSize)

NumFiles = 2
iterations = 5

def CreateFiles(loc, bs, count):
    c = 1
    while (c <= NumFiles):
        call ("dd if=/dev/urandom of=%s/file%s bs=%s count=%s" %(loc, c, bs, count), shell=True)
        c = c + 1

def ReadFiles(loc, bs, count):
    c = 1
    while (c <= NumFiles):
        call ("dd if=%s/file%s of=/dev/null bs=%s count=%s" %(loc, c, bs, count), shell=True)
        c = c + 1

def ModifyWriteFiles(loc, bs, count):
    c = 1
    while (c <= NumFiles):
        call ("dd if=/dev/urandom of=%s/file%s bs=%s count=%s conv=notrunc" %(loc, c, bs, count/2), shell=True)
        c = c + 1

def ArchiveFiles(backuploc, directory, timestamp, mnt):
    call ("cd %s;tar -cvzf %s_%s.tgz %s;mv *.tgz %s" %(mnt, directory, timestamp, directory, backuploc), shell=True)

def DeleteFiles(loc):
    call ("rm -rf %s/*" %(loc), shell=True)

def Create():
    call ("mkdir -p %s/%s" %(mount_point_1, FileDir), shell=True)
    CreateFiles(location, bSize, ddCountValue)
    
    #FLUSH CACHE
    call ("echo 3 > /proc/sys/vm/drop_caches", shell=True)

    call ("echo 'FILES CREATED' > %s" %(test_log), shell=True)

def ReadModifyWrite():
    ReadFiles(location, ddBlockSize, ddCountValue)
    ModifyWriteFiles(location, bSize, ddCountValue)
    call ("echo 'FILES READ MODIFIED WRITTEN' >> %s" %(test_log), shell=True)

def Archive():
    stamp = ctime()
    stamp = stamp.replace(" ", "_" )
    stamp = stamp.replace(":", "_" )
    ArchiveFiles(backup_location, FileDir, stamp, mount_point_1)
    call ("echo 'FILE DIR ARCHIVED' >> %s" %(test_log), shell=True)

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
    i = 1
    while (i <= iterations):
        ReadModifyWrite()
        Archive()
        i = i + 1
    Delete()
    Umain(mount_point_1)
    Umain(mount_point_2)

main()





    



