import sys
import logging
from time import ctime, sleep
from subprocess import call, check_output
import os

script_name = sys.argv[0]
mount_point = sys.argv[1]
print mount_point

test_log = '/root/FileCreateReadModifyWriteDelete.log' 

No2kFiles=50
No4kFiles=50
No8kFiles=50
No16kFiles=50
No32kFiles=50

dir_recursive = ['a', 'b', 'c', 'd']

def CreateFiles(FileSize, location):
    if FileSize == '2k':
        NumFiles = No2kFiles
        ddBlockSize = 512
    elif FileSize == '4k':
        NumFiles = No4kFiles 
        ddBlockSize = '1k'
    elif FileSize == '8k':
        NumFiles = No8kFiles 
        ddBlockSize = '2k'
    elif FileSize == '16k':
        NumFiles = No16kFiles
        ddBlockSize = '4k'
    elif FileSize == '32k':
        NumFiles = No32kFiles
        ddBlockSize = '8k'
    i = 1
    while (i <= NumFiles):
        call ("dd if=/dev/urandom of=%s/file%s-%s bs=%s count=4" %(location, FileSize, i, ddBlockSize), shell=True)
        i = i + 1
    
def ReadFiles(FileSize, location):
    if FileSize == '2k':
        NumFiles = No2kFiles
        ddBlockSize = 512
    elif FileSize == '4k':
        NumFiles = No4kFiles
        ddBlockSize = '1k'
    elif FileSize == '8k':
        NumFiles = No8kFiles
        ddBlockSize = '2k'
    elif FileSize == '16k':
        NumFiles = No16kFiles
        ddBlockSize = '4k'
    elif FileSize == '32k':
        NumFiles = No32kFiles
        ddBlockSize = '8k'
    else:
        print "Nonsense"
    i = 1
    while (i <= NumFiles):
        call ("dd if=%s/file%s-%s of=/dev/null bs=%s count=4" %(location, FileSize, i, ddBlockSize), shell=True)
        i = i + 1

def ModifyWriteFiles(FileSize, location):
    if FileSize == '2k':
        NumFiles = No2kFiles
        ddBlockSize = 512
    elif FileSize == '4k':
        NumFiles = No4kFiles
        ddBlockSize = '1k'
    elif FileSize == '8k':
        NumFiles = No8kFiles
        ddBlockSize = '2k'
    elif FileSize == '16k':
         NumFiles = No16kFiles
         ddBlockSize = '4k'
    elif FileSize == '32k':
        NumFiles = No32kFiles
        ddBlockSize = '8k'
    else:
        print "Nonsense"
    i = 1
    while (i <= NumFiles):
         call ("dd if=/dev/urandom of=%s/file%s-%s bs=%s count=2 conv=notrunc" %(location, FileSize, i, ddBlockSize), shell=True)
         i = i + 1

def DeleteFiles(FileSize, location):
    if FileSize == '2k':
        call ("rm -rf %s/file%s*" %(location, FileSize), shell=True)
    elif FileSize == '4k':
        call ("rm -rf %s/file%s*" %(location, FileSize), shell=True)
    elif FileSize == '8k':
        call ("rm -rf %s/file%s*" %(location, FileSize), shell=True)
    elif FileSize == '16k':
        call ("rm -rf %s/file%s*" %(location, FileSize), shell=True)
    elif FileSize == '32k':
        call ("rm -rf %s/file%s*" %(location, FileSize), shell=True)
    else:
        print "Nonsense"

def Create(dir_list):
    for x in dir_list:
        call ("mkdir -p %s/%s" %(mount_point, x), shell=True)
        for y in dir_list:
            call ("mkdir -p %s/%s/%s%s" %(mount_point, x, x, y), shell=True)
            loc = '%s/%s/%s%s' %(mount_point, x, x, y )
            CreateFiles('2k', loc)
            CreateFiles('4k', loc)
            CreateFiles('8k', loc)
            CreateFiles('16k', loc)
            CreateFiles('32k', loc)
    call ("echo 'FILES CREATED' > %s" %(test_log), shell=True)

def ReadModifyWrite(dir_list):
    for x in dir_list:
        for y in dir_list:
            loc = '%s/%s/%s%s' %(mount_point, x, x, y )
            ReadFiles('2k', loc)
            ReadFiles('8k', loc)
            ReadFiles('16k', loc)
            ModifyWriteFiles('4k', loc)
            ModifyWriteFiles('32k', loc)
    call ("echo 'FILES READ MODIFIED WRITTEN' >> %s" %(test_log), shell=True)

def Delete(dir_list):
    for x in dir_list:
        for y in dir_list:
            loc = '%s/%s/%s%s' %(mount_point, x, x, y )
            DeleteFiles('2k', loc)
            DeleteFiles('4k', loc)
            DeleteFiles('8k', loc)
            DeleteFiles('16k', loc)
            DeleteFiles('32k', loc)
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
    #Create(dir_recursive)
    #ReadModifyWrite(dir_recursive)
    Delete(dir_recursive)
    Umain(mount_point)

main()







    


            

    

    




