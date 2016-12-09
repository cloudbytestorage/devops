import json
import sys
from time import ctime
from cbrequest import  configFile, resultCollection, executeCmd, getControllerInfo, createSFTPConnection, putFileToController

config = configFile(sys.argv);
IP="ESXIP"
passwd="ESXPASSWORD"
for x in range(1, int(config['Number_of_VMs'])+1):
    executeCmd('> temp/createrdm.sh')
    executeCmd('cat sample/createrdm.sh >> temp/createrdm.sh')
    vmname = "%s" %(config['vmName%d'%(x)])
    datastore = "%s" %(config['datastoreName%d'%(x)])
    vmpassword = "%s" %(config['vmPassword%d'%(x)])
    executeCmd('sed -i s/VMNAME/%s/g temp/createrdm.sh' % vmname)
    executeCmd('sed -i s/DATASTORE/%s/g temp/createrdm.sh' % datastore)
    executeCmd('sed -i s/VMLFILE/vmlfile%d/g temp/createrdm.sh'%(x))
    output = putFileToController(IP, passwd, "temp/createrdm.sh", "/vmfs/volumes/%s/%s/createrdm.sh" % (datastore, vmname))
    print output
    cmd = getControllerInfo(IP, passwd,"cp /autofolder/vmlfile%d /vmfs/volumes/%s/%s/vmlfile%d" % (x, datastore, vmname, x),"vmlfile.txt")
    print cmd
    cmd = getControllerInfo(IP, passwd,"sh -x /vmfs/volumes/%s/%s/createrdm.sh"% (datastore, vmname),"rdmfile.txt")
    print cmd


