import sys
import logging
from time import ctime, sleep
from subprocess import call, check_output
import os

script_name = sys.argv[0]
server_ip = sys.argv[1]
share_loc = sys.argv[2]
mount_point = sys.argv[3]

test_log = '/root/NFSMetaDataStress.log' 

No2kFiles=10
No4kFiles=10
No8kFiles=10
No16kFiles=10
No32kFiles=10

dir_recursive = ['a', 'b', 'c', 'd']

iterations = 5

def mount(server_ip, share_loc, mount_point):
    
    #FSINFO, PATHCONF
    call ("mount -o mountproto=tcp,sync %s:/%s %s" %(server_ip, share_loc, mount_point), shell=True)
    
    mount_result = check_output ("df -h | grep %s" %(share_loc), shell=True)
    if '%s' %(share_loc) in str(mount_result):
        print "Volume is mounted successfully"
    else:
        print "Volume is not mounted successfully"

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
        
        #CREATE, WRITE, ACCESS, LOOKUP, SETATTR
        call ("dd if=/dev/urandom of=%s/file%s-%s bs=%s count=4" %(location, FileSize, i, ddBlockSize), shell=True) 

        #SYMLINK 
        call ("ln -s %s/file%s-%s %s/linktofile%s-%s" %(location, FileSize, i, location, FileSize, i), shell=True)

        #GETATTR, ACCESS, READDIRPLUS 
        call ("ls -liatrR %s" %(location), shell=True) 
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
        
        #FSTAT
        path = '%s/file%s-%s' %(location, FileSize, i)
        print path
        fd = os.open(path, os.O_RDWR) 
        print "FD is %s" %(fd) 
        os.fstatvfs(fd)
        os.close(fd)
        sleep(1) 

        #GETATTR, ACCESS, READ 
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
         
         #WRITE, ACCESS, SETATTR, GETATTR
         call ("dd if=/dev/urandom of=%s/file%s-%s bs=%s count=2 conv=notrunc" %(location, FileSize, i, ddBlockSize), shell=True)

         #GETATTR, ACCESS, READDIRPLUS 
         call ("ls -liatrR %s" %(location), shell=True)

         i = i + 1

def DeleteFiles(FileSize, location):
        
        #GETATTR, ACCESS 
        list = check_output("ls %s/linktofile%s*" %(location, FileSize), shell=True )
        list = str(list)
        links = list.split()
        
        #UNLINK 
        for l in links:
            call ("unlink %s" %(l), shell=True)
            print "unlinked %s", l
        
        #REMOVE, GETATTR, ACCESS 
        call ("rm -rf %s/file%s*" %(location, FileSize), shell=True)
        
        #GETATTR, ACCESS, READDIRPLUS 
        call ("ls -liatrR %s" %(location), shell=True)

def CreateWithLinks(dir_list):
    for x in dir_list:
        
        #MKDIR, ACCESS, READDIRPLUS 
        call ("mkdir -p %s/%s" %(mount_point, x), shell=True)
        
        for y in dir_list:
            
            #MKDIR, ACCESS, READDIRPLUS 
            call ("mkdir -p %s/%s/%s%s" %(mount_point, x, x, y), shell=True)
            
            loc = '%s/%s/%s%s' %(mount_point, x, x, y )
            CreateFiles('2k', loc)
            CreateFiles('4k', loc)
            CreateFiles('8k', loc)
            CreateFiles('16k', loc)
            CreateFiles('32k', loc)

    #FLUSH CACHE
    call ("echo 3 > /proc/sys/vm/drop_caches", shell=True)
    
    call ("echo 'FILES CREATED WITH LINKS' >> %s" %(test_log), shell=True)
    
    #GETATTR, ACCESS, READDIRPLUS
    call ("ls -liatrR %s" %(mount_point), shell=True)
    call ("echo 'FILES LISTED AFTER CREATION - ls' >> %s" %(test_log), shell=True)
    
    #GETATTR, ACCESS
    call ("du -kh %s" %(mount_point), shell=True)
    call ("echo 'SPACE CONSUMPTION AFTER CREATION CHECKED - du' >> %s" %(test_log), shell=True)

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
    
    #GETATTR, ACCESS, READDIRPLUS
    call ("ls -liatrR %s" %(mount_point), shell=True)
    call ("echo 'FILES LISTED AFTER MODIFICATION' >> %s" %(test_log), shell=True)
    
    #GETATTR, ACCESS
    call ("du -kh %s" %(mount_point), shell=True)
    call ("echo 'SPACE CONSUMPTION AFTER MODIFY CHECKED - du' >> %s" %(test_log), shell=True)

def UnlinkAndDelete(dir_list):
    for x in dir_list:
        for y in dir_list:
            loc = '%s/%s/%s%s' %(mount_point, x, x, y )
            DeleteFiles('2k', loc)
            DeleteFiles('4k', loc)
            DeleteFiles('8k', loc)
            DeleteFiles('16k', loc)
            DeleteFiles('32k', loc)
    
    call ("echo 'FILES DELETED' >> %s" %(test_log), shell=True)
    
    #RMDIR
    call ("rm -rf %s/*" %(mount_point), shell=True)
    call ("echo 'DIRS DELETED' >> %s" %(test_log), shell=True)


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

def mountUmountLoop():
    it = 1
    while (it <= iterations):
        mount(server_ip, share_loc, mount_point)
        sleep(5)
        #umount(server_ip, share_loc, mount_point)
        UMain(mount_point)
        it = it + 1

def main():
    mountUmountLoop()
    mount(server_ip, share_loc, mount_point)
    CreateWithLinks(dir_recursive)
    ReadModifyWrite(dir_recursive)
    UnlinkAndDelete(dir_recursive)
    #umount(server_ip, share_loc, mount_point)
    UMain(mount_point)

main()




        

    









    


            

    

    




