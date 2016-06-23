import json
import sys
import fileinput
from time import ctime
import time
from cbrequest import configFile, executeCmd, executeCmdNegative, resultCollection, sendrequest, filesave, configFileName, getControllerInfo, getControllerInfoAppend, createSFTPConnection, putFileToController

print 'Starting'

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

if len(sys.argv) < 5:
    print bcolors.WARNING + "python mapNfsDatadtoreToVM.py config.txt vm_number vm_name datastore_name" + bcolors.ENDC
    exit()
config = configFile(sys.argv);

vm_number = int(sys.argv[2])
vm_name = sys.argv[3]
datastore_name = sys.argv[4]
esxip = 'ESXIP'
passwd = 'ESXPASSWORD'
number_of_volume = int('NOOFVOLUMES')
#esxip = '20.10.49.1'
#passwd = 'test123'
#number_of_volume = 10

###vmid=`ssh root@20.10.49.1 vim-cmd vmsvc/getallvms | grep CentOS | awk '{print $1}'`
cmd1 = 'date +%d%h%y%H%M%S'
date = getControllerInfo(esxip, passwd, cmd1, "getdate.txt")
cmd2 = 'vim-cmd  vmsvc/getallvms > /vmfs/volumes/%s/%s/vimid_list_backup_%s' %(datastore_name, vm_name, date)
getControllerInfo(esxip, passwd, cmd2, "backup_of_vms.txt")
cmd3 = 'vim-cmd vmsvc/getallvms | grep " %s " | awk \'{print $1}\'' %(vm_name)
vm_id = getControllerInfo(esxip, passwd, cmd3, "getvmid.txt")
vm_id = vm_id.rstrip("\n")
print vm_id
#exit()
cmd4 = 'vim-cmd vmsvc/power.off %s' %(vm_id)
getControllerInfo(esxip, passwd, cmd4, "vmpoweroff.txt")

cmd4  = 'cat /vmfs/volumes/%s/%s/%s.vmx | grep scsi0.virtualDev | cut -d "=" -f 2' %(datastore_name, vm_name, vm_name)
virtualdev = getControllerInfo(esxip, passwd, cmd4, "get_virtualdev.txt")

str1 = 'scsi1.virtualDev ='
str1 = str1 + "%s" %(virtualdev)
executeCmd('cp sample/scsiController1.txt scsiController1.txt')
f = open('scsiController1.txt', 'a')
f.write(str1)
f.close()

str2 = 'scsi2.virtualDev ='
str2 = str2 + "%s" %(virtualdev)
executeCmd('cp sample/scsiController2.txt scsiController2.txt')
f = open('scsiController2.txt', 'a')
f.write(str2)
f.close()

str3 = 'scsi3.virtualDev ='
str3 = str3 + "%s" %(virtualdev)
executeCmd('cp sample/scsiController3.txt scsiController3.txt')
f = open('scsiController3.txt', 'a')
f.write(str3)
f.close()

cmd5 = 'cp /vmfs/volumes/%s/%s/%s.vmx /vmfs/volumes/%s/%s/%s.backup_%s' %(datastore_name, vm_name, vm_name, datastore_name, vm_name, vm_name, date)
getControllerInfo(esxip, passwd, cmd5, "backup_of.vmx_file.txt")
#creating directory for scsi controllers
result = getControllerInfo(esxip, passwd,"mkdir scsiControllers","scsicontrollers.txt")
print result
result = putFileToController(esxip, passwd, "scsiController1.txt", "/scsiControllers/scsiController1.txt")
print result
result = putFileToController(esxip, passwd, "scsiController2.txt", "/scsiControllers/scsiController2.txt")
print result
result = putFileToController(esxip, passwd, "scsiController3.txt", "/scsiControllers/scsiController3.txt")
print result

controllerID = 0
portNo = 0
if vm_number == 1:
    start_nfs_range = 1
else:
    start_nfs_range = int((((vm_number - 1) * number_of_volume) + 1 ))

for x in range(start_nfs_range, (start_nfs_range + number_of_volume)):
        startTime = ctime()
        #if tsmip ==  "%s" %(config['volIPAddress%d' %(x)]):
        portNo += 1
        if portNo == 7:
            continue
        try:
            size = "%s" %(config['volQuotasize%d' %(x)])
            print size
        except:
            print 'not enough volumes to add to VM'
            cmd12 = 'vim-cmd vmsvc/power.on %s' %(vm_id)
            getControllerInfo(esxip, passwd, cmd12, "vmpoweron.txt")
            continue

        if 'M' in size:
            size = (int(size.split('M')[0])) * 1000
        elif 'G' in size:
            size = (int(size.split('G')[0])) * 1000000
        elif 'T' in size:
            size = (int(size.split('T')[0])) * 1000000000
        #print size
        #exit()

        cmd5 = 'vim-cmd vmsvc/device.diskadd %s %s %s %s %s' %(vm_id, size, controllerID, portNo, config['volDatasetname%d' %(x)])
        getControllerInfo(esxip, passwd, cmd5, "map_nfs_disk_to_vm.txt")
        print cmd5
        if portNo == 15 and controllerID == 0:
            controllerID = 1
            portNo = -1
            cmd6  = 'cat /scsiControllers/scsiController1.txt >> /vmfs/volumes/%s/%s/%s.vmx' %(datastore_name, vm_name, vm_name)
            getControllerInfo(esxip, passwd, cmd6, "copyscsicontroller1.txt")
            cmd7 = 'vim-cmd vmsvc/reload %s' %(vm_id)
            getControllerInfo(esxip, passwd, cmd7, "reload1.txt")
        if portNo == 15 and controllerID == 1:
            controllerID = 2
            portNo = -1
            cmd8  = 'cat /scsiControllers/scsiController2.txt >> /vmfs/volumes/%s/%s/%s.vmx' %(datastore_name, vm_name, vm_name)
            getControllerInfo(esxip, passwd, cmd8, "copyscsicontroller2.txt")
            cmd9 = 'vim-cmd vmsvc/reload %s' %(vm_id)
            getControllerInfo(esxip, passwd, cmd9, "reload2.txt")
        if portNo == 15 and controllerID == 2:
            controllerID = 3
            portNo = 0
            cmd10  = 'cat /scsiControllers/scsiController3.txt >> /vmfs/volumes/%s/%s/%s.vmx' %(datastore_name, vm_name, vm_name)
            getControllerInfo(esxip, passwd, cmd10, "copyscsicontroller3.txt")
            cmd11 = 'vim-cmd vmsvc/reload %s' %(vm_id)
            getControllerInfo(esxip, passwd, cmd11, "reload3.txt")

cmd12 = 'vim-cmd vmsvc/power.on %s' %(vm_id)
getControllerInfo(esxip, passwd, cmd12, "vmpoweron.txt")
