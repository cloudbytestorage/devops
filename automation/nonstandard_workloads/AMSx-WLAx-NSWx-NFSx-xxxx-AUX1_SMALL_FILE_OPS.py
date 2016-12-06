import sys
import logging
from time import ctime
from subprocess import call

script_name = sys.argv[0]
mount_point = sys.argv[1]

# File into which completion of important fileops are logged

test_log = '/root/FileCreateReadModifyWriteDelete.log' 

# Total file no : 16 * (No2kFiles+No4kFiles+No8kFiles+No16kFiles+No32kFiles)

No2kFiles=50 
No4kFiles=50 
No8kFiles=50 
No16kFiles=50 
No32kFiles=50

# Total dir no : square {length(dir_recursive)}

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
            #call ("cd %s/%s/%s%s" %(mount_point, x, x, y), shell=True)
            loc = '%s/%s/%s%s' %(mount_point, x, x, y )
            CreateFiles('2k', loc)
            CreateFiles('4k', loc)
            CreateFiles('8k', loc)
            CreateFiles('16k', loc)
            CreateFiles('32k', loc)
    
    #FLUSH CACHE
    call ("echo 3 > /proc/sys/vm/drop_caches", shell=True)
    
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

Create(dir_recursive)
#ReadModifyWrite(dir_recursive)
#Delete(dir_recursive)










    


            

    

    




