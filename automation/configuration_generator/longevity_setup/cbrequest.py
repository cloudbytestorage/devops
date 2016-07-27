import json
import requests
import md5
import fileinput
import subprocess
import time
import datetime
import paramiko
import os
import getpass
import sys

#### Function(s) Declaration Begins

def getURL(config):
    stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
    print stdurl
    return stdurl

#def enableDisableNFS()

def enabledDisableCIFS(config, vol_id, operation):
    stdurl = getURL(config)
    if operation.lower() == 'true':
        operation = 'true'
    else:
        operation = 'false'
    querycommand = 'command=updateFileSystem&cifsenabled=%s&id=%s' %(operation, vol_id)
    resp_enableCifs = sendrequest(stdurl, querycommand)
    filesave('logs/enabledCifs.txt', 'w', resp_enableCifs)
    data = json.loads(resp_enableCifs.text)
    if not 'errorecode' in data['updatefilesystemresponse']:
        print 'enable cifs \"%s\" on volume is successful' %(operation)
        result = ['PASSED', 'enable cifs %s on volume is successful' %(operation)]
        return result
    else:
        print 'enable cifs \"%s\" on volume is failed' %(operation)
        errormsg = data['updatefilesystemresponse']['errortext']
        result = ['FAILED', errormsg]
        return result


def createScheduleSnpVSM(config, tsm, name, retentioncopies, interval):
    dataset_id = tsm['datasetid']
    tsm_id = tsm['id']
    querycommand = 'command=addLocalDPScheduler&day=*&fortype=tsm&hour=*&month=*&minute=*/%s&week=*&status=enabled&retentioncopies=%s&tsmid=%s&name=%s&datasetid=%s' %(interval, retentioncopies, tsm_id, name, dataset_id)
    stdurl = getURL(config)
    resp_addLocalDPScheduler = sendrequest(stdurl, querycommand)
    filesave('logs/addLocalDPScheduler.txt', 'w', resp_addLocalDPScheduler)
    data = json.loads(resp_addLocalDPScheduler.text)
    print '\n' + querycommand + '\n'
    if not 'errorcode' in data['addLocalDPSchedulerResponse']:
        result = ['PASSED', '']
        return result
    else:
        errormsg = data['addLocalDPSchedulerResponse']['errortext']
        result = ['FAILED', errormsg]
        return result

#def deleteScheduleSnpVSM(tsm, name):
#    tsm_id = tsm['id']

def listVolume(config):
    stdurl = getURL(config)
    querycommand = 'command=listFileSystem'
    resp_listVolumes = sendrequest(stdurl, querycommand)
    filesave('logs/listVolumes.txt', 'w', resp_listVolumes)
    data = json.loads(resp_listVolumes.text)
    if 'filesystem' in str(data['listFilesystemResponse']):
        volumes = data['listFilesystemResponse']['filesystem']
        result = ['PASSED', volumes]
        return result
    elif not 'errorcode' in str(data['listFilesystemResponse']):
        print 'There is no volume'
        result = ['BLOCKED', 'There is no volume to list']
        return result
    else:
        errormsg = str(data['listFilesystemResponse']['errortext'])
        result = ['FAILED', errormsg]
        return result

def listTSM(config):
    querycommand = 'command=listTsm&type=all'
    stdurl = getURL(config)
    resp_listTsm = sendrequest(stdurl, querycommand)
    filesave('logs/listTsm.txt', 'w', resp_listTsm)
    data = json.loads(resp_listTsm.text)
    if not 'errorcode' in data['listTsmResponse']:
        if 'listTsm' in data['listTsmResponse']:
            tsms = data['listTsmResponse']['listTsm']
            result = ['PASSED', tsms]
            return result
        else:
            result = ['BLOCKED', 'There is no VSMs']
            return result
    else:
        errormsg = str(data['listTsmResponse']['errortext'])
        print 'Not able to list VSMs due to: ' + errormsg
        result = ['FAILED', errormsg]
        return result

def umountVolume(volume):
    ### volume is a dictionary and it contains dataset's(volume) properties.
    ### umount
    mountCheck = executeCmd('mount | grep %s' %(volume['mountPoint']))
    if mountCheck[0] == 'PASSED':
        umountResult = executeCmd('umount mount/%s' %(volume['mountPoint']))
        if umountResult[0] == 'PASSED':
            print 'Volume \"%s\" umounted successfully' %(volume['name'])
            return 'PASSED'
        else:
            print 'Volume \"%s\" failed to umount' %(volume['name'])
            return 'FAILED'
    else:
        print 'Volume \"%s\" is not mounted' %(volume['name'])
        return 'PASSED'

def mountNFS(volume):
    ### volume is a dictionary and it contains dataset's(volume) properties. 
    ### create directory for mounting NFS volume
    executeCmd('mkdir -p mount/%s' %(volume['mountPoint']))
    ### Mount
    mountResult = executeCmd('mount -t nfs %s:/%s mount/%s' %(volume['TSMIPAddress'], volume['mountPoint'], volume['mountPoint']))
    if mountResult[0] == 'PASSED':
        print 'NFS volume \"%s\" mounted successfully' %(volume['name'])
        return 'PASSED'
    else:
        print 'NFS volume \"%s\" failed to mount' %(volume['name'])
        return 'FAILED'

def mountCIFS(volume):
    ### volume is a dictionary and it contains dataset's(volume) properties.
    ### create directory for mounting CIFS volume
    executeCmd('mkdir -p mount/%s' %(volume['mountPoint']))
    ### Mount
    mountResult = executeCmd(' mount -t cifs //%s/%s mount/%s -o username=%suser -o password=%suser' %(volume['TSMIPAddress'], volume['mountPoint'], volume['mountPoint'], volume['AccountName'], volume['AccountName']))
    if mountResult[0] == 'PASSED':
        print 'CIFS volume \"%s\" mounted successfully' %(volume['name'])
        return 'PASSED'
    else:
        print 'CIFS volume \"%s\" failed to mount' %(volume['name'])
        return 'FAILED'

def sendrequest(url, querystring): 
    print url+querystring
    response = requests.get(
      url+querystring, verify=False
    )   
    return(response);

def filesave(loglocation,permission,content):
    f=open(loglocation,permission) 
    f.write(content.text)
    f.close()
    return;

def filesave1(loglocation,permission,content):
    f=open(loglocation,permission) 
    f.write(content)
    f.close()
    return;

def timetrack(event):
    f=open("results/config_creation_result.csv","a")
    f.write(event)
    f.write("--")
    time = datetime.datetime.now()
    f.write(str(time))
    f.write("\n")
    f.close()
    return;

def queryAsyncJobResult(url, jobid):
    tcdesc = ""
    tcoutput = "NotSure"
    querycommand = 'command=queryAsyncJobResult&jobId=%s' %(jobid)
    check_queryAsyncJobStatus = sendrequest(url, querycommand)
    data = json.loads(check_queryAsyncJobStatus.text)
    status = data["queryasyncjobresultresponse"]["jobstatus"]
    filesave("logs/queryAsyncJobResult.txt","w",check_queryAsyncJobStatus)
    if status == 0:
        print "Processing ..."
        print status
        time.sleep(10);
        return queryAsyncJobResult(url, jobid);
    else:
        if not "errortext" in str(data):
            tcdesc = ""
            tcoutput = "PASSED"
            return(tcoutput, str(tcdesc));
        else:
            print "Error in creating %s" %(data["queryasyncjobresultresponse"]["jobresult"]["errortext"])
            tcdesc = data["queryasyncjobresultresponse"]["jobresult"]["errortext"]
            tcoutput = "FAILED"
            return(tcoutput, str(tcdesc));
    print tcoutput
    print tcdesc
    return(tcoutput, str(tcdesc));

def queryAsyncJobResultNegative(url, jobid):
    tcdesc = ""
    tcoutput = "NotSure"
    querycommand = 'command=queryAsyncJobResult&jobId=%s' %(jobid)
    check_queryAsyncJobStatus = sendrequest(url, querycommand)
    data = json.loads(check_queryAsyncJobStatus.text)
    status = data["queryasyncjobresultresponse"]["jobstatus"]
    filesave("logs/queryAsyncJobResult.txt","w",check_queryAsyncJobStatus)
    if status == 0:
        print "Processing ..."
        print status
        time.sleep(10);
        return queryAsyncJobResultNegative(url, jobid);
    else:
        if not "errortext" in str(data):
            tcdesc = ""
            tcoutput = "FAILED"
            return(tcoutput, str(tcdesc));
        else:
            print "Error in creating %s" %(data["queryasyncjobresultresponse"]["jobresult"]["errortext"])
            tcdesc = data["queryasyncjobresultresponse"]["jobresult"]["errortext"]
            tcoutput = "PASSED"
            return(tcoutput, str(tcdesc));
    print tcoutput
    print tcdesc
    return(tcoutput, str(tcdesc));


def configFile(conf):
    if len(conf) > 1:
        configfile = str(conf[1])
    else:
        configfile = 'config.txt'
    config = {}
    with open('%s' %(configfile)) as cfg:
       config = json.load(cfg)
    cfg.close()
    return(config)

def configFileName(conf):
    if len(conf) > 1:
        configfile = str(conf[1])
    else:
        configfile = 'config.txt'
    return(configfile)


def executeCmd(command):
    print command
    link = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    ldata = link.stdout.readlines()
    output, errors = link.communicate()
    rco = link.returncode
    if rco != 0:
        return "FAILED", str(errors)
    return "PASSED", ""; 


def executeCmdStatus(command):
    print command
    link = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    ldata = link.stdout.readlines()
    output, errors = link.communicate()
    rco = link.returncode
    return rco

def executeCmdNegative(command):
    print command
    link = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    ldata = link.stdout.readlines()
    output, errors = link.communicate()
    rco = link.returncode
    if rco != 0:
        return "PASSED", str(errors)
    return "FAILED", ""; 

def resultCollection(testcase,value,startTime,endTime):
    f=open("results/result.csv","a")
    f.write(startTime)
    f.write(",")
    f.write(testcase)
    f.write(",")
    f.write(value[0])
    f.write(",")
    f.write(value[1])
    f.write(",")
    f.write(endTime)
    f.write("\n")
    return;

#localoutputdir='logs/output'
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
def createSFTPConnection(IP='localhost',user='root',paswd='test'):
    t = paramiko.Transport((IP,22)) 
    t.connect(username=user, password=paswd)
    sftp = paramiko.SFTPClient.from_transport(t) 
    #sftp = paramiko.SSHClient.from_transport(t) 
    return sftp

def putFileToController(ip, passwd, src_file, dst_file):
    print ip
    print passwd
    ssh.connect(ip, username="root", password=passwd, allow_agent = False)
    sftp=createSFTPConnection(ip,'root',passwd)
    sftp.put(src_file, dst_file)#,callback=none)
    sftp.close()

def getFileToController(ip, passwd, src_file, dst_file):
    print ip
    print passwd
    ssh.connect(ip, username="root", password=passwd, allow_agent = False)
    sftp=createSFTPConnection(ip,'root',passwd)
    sftp.get(src_file, dst_file)#,callback=none)
    sftp.close()

def getControllerInfo(ip, passwd, command, outputfile):
    ssh.connect(ip, username="root", password=passwd, allow_agent = False)
    stdin, stdout, stderr = ssh.exec_command(command)
    #print "Stdout = "+stdout.read()
    output = stdout.read()
    filesave1(outputfile, "w", output)
    ssh.close()
    #print "Output Available: "+str(ip)+" path: "+outputfile
    return(output)

def getControllerInfoAppend(ip, passwd, command, outputfile):
    ssh.connect(ip, username="root", password=passwd, allow_agent = False)
    stdin, stdout, stderr = ssh.exec_command(command)
    #print "Stdout = "+stdout.read()
    output = stdout.read()
    filesave1(outputfile, "a", output)
    ssh.close()
    #print "Output Available: "+str(ip)+" path: "+outputfile
    return(output)




def getoutput(command):
    print command
    link = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    ldata = link.stdout.readlines()
    output, errors = link.communicate()
    rco = link.returncode
    try:
         output = ldata
    except IndexError:
         output = 'null'
    return output


#### Function(s) Declartion Ends
