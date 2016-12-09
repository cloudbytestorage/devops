import json
import sys
import os
from time import ctime
from cbrequest import *
import subprocess

## Modify the Primary and Secondary IP and NIC and see if it updates the portal
''' Steps to the test case
       1) Create VSM
       2) Create iSCSI Volume
       3) Change or add the secondary IP and NIC interface
       4) To check if the same gets updated in istgt.conf '''

### Method to Validate IP 
def validate_ip(x):
    parts = x.split('.')
    if len(parts) != 4:
        return False
    for item in parts:
        if item.isdigit() == False:
            return False
        if not 0 <= int(item) <= 255:
            return False
    else:
        return True

###Method to Convert a string
def stringConverter(command):
    print command
    strToBeConverted = command.split('-')
    convertedStr = ''.join(str(x) for x in strToBeConverted)
    return convertedStr


###To Assign the arguments to the respective components

startTime = ctime()
if len(sys.argv) > 3:
    configurationFile = str(sys.argv[1])
    nicInterface = str(sys.argv[3])
    print configurationFile
    ip = sys.argv[2]
    if validate_ip(ip) == True:
        secondaryIpAddress = str(ip)
        config = configFile(sys.argv)
        stdurl = 'http://%s/client/api?apikey=%s&response=%s&'  %(config['host'], config['apikey'], config['response'])
    elif validate_ip(ip) == False:
        print "Enter valid IP"
        endTime = ctime()
        resultCollection("Adding and verifying SecondaryIpAddress to the VSM",["FAILED","ValidIPNotEntered"],startTime,endTime)
        exit()

else:
    print "Please enter the command correctly"
    print "The correct command would be:  python Script.py configFile.txt IPAddress nicInterface"
    endTime = ctime()
    resultCollection("Adding and verifying SecondaryIpAddress to the VSM",["FAILED","ProperArgumentsRequired"],startTime,endTime)
    exit()

##Not Required
'''
#config = configFile(sys.argv)
#stdurl = 'http://%s/client/api?apikey=%s&response=%s&'  %(config['host'], config['apikey'], config['response'])

##If required
'''
'''
## Create VSM
#print "\n............Creating VSM from the config file............\n"
#os.system("python Tsm.py smoketest.txt")

##Create iscsi volume
print "\n ...........Creating ISCSIVolume from the config file .....\n"
os.system("python ISCSIVolume.py smoketest.txt")


## To modify or give a different Secondary IP address

for x in range(1,int(config['Number_of_Nodes'])+1):
    querycommand = 'command=listController'
    resp_listController = sendrequest(stdurl,querycommand)
    data = json.loads(resp_listController.text)
    controllers = data['listControllerResponse']['controller']

    for controller in controllers:
        if controller['name'] == "%s" %(config['nodeName%d'%(x)]):
            controller_id = controller['id']
            #print "The controller id is ", controller_id
            break
'''
## Program to get tsm_id to update SecondaryIPAddress

#for x in range(1,int(config['Number_of_TSMs'])+1):
querycommand = 'command=listTsm&type=all'
resp_listTsm = sendrequest(stdurl,querycommand)
data = json.loads(resp_listTsm.text)
#print data
x = 1
tsms = data['listTsmResponse']['listTsm']
for tsm in tsms:
    if tsm['name'] == "%s" %(config['tsmName%d' %(x)]):
        tsm_id = tsm['id']
        tsmConvertedStr = stringConverter(tsm_id)
        #print "The tsm id is ", tsm_id
            
        querycommand = 'command=updateTsmSettings&tsmid=%s&secondaryipaddress=%s&subnet=8&secondaryinterface=%s' %(tsm_id,secondaryIpAddress,nicInterface)
        resplist = sendrequest(stdurl,querycommand)
        filesave("logs/AddSecondaryIpAndVerify.txt","w",resplist)
        querycommand = 'command=listTsmDNSSettings&tsmid=%s'%(tsm_id)
        resp_dnssetting = sendrequest(stdurl,querycommand)
        data = json.loads(resp_dnssetting.text)
        if not "errortext" in str(data):
            dnssettings = data['listTsmDnsSettingsResponse']['dnssettings']
            for dnssetting in dnssettings:
                dnssetting['secondaryipaddress'] = secondaryIpAddress
                dnssetting['secondaryinterface'] = nicInterface


            ### This Section takes the secondary ip from Controller and verifies it with the given IP to Confirm the change
            
            #command = 'scp -r %s:/tenants/%s/usr/local/etc/istgt/istgt.conf /mnt/' %(str(config['nodeIP%d' %(x)]), str(tsmConvertedStr))
            command1 = 'cat /tenants/%s/usr/local/etc/istgt/istgt.conf | grep %s' %(str(tsmConvertedStr),str(secondaryIpAddress))
            output = str(getControllerInfo('%s'%(config['nodeIP%d' %(x)]),'test',command1,'samplefile')).split(' ')[4].split(':')[0]
            endTime = ctime()

            if output == secondaryIpAddress:
                #print "True"
                errorstatus = str(data['listTsmDnsSettingsResponse']['dnssettings'])
                result = resultCollection("Adding and verifying SecondaryIpAddress",["PASSED",str("")],startTime,endTime)
                #print result

            else:
                #print "FALSE"
                errorstatus = str(data['listTsmDnsSettingsResponse']['dnssettings']['errortext'])
                resultCollection("Adding and verifying SecondaryIpAddress" %(secondaryIpAddress),["FAILED",errorstatus],startTime,endTime)
        else:
            endTime = ctime()
            print "result is FAILED"
            errorstatus = str(data['listTsmDnsSettingsResponse']['dnssettings']['errortext'])
            print "The SecondaryIpAddress addition failed with errorstatus"
            resultCollection("Adding and verifying SecondaryIpAddress to the VSM",["FAILED",errorstatus],startTime,endTime)
