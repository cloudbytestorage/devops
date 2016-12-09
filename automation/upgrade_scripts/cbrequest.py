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
import logging
logging.basicConfig(format = '%(asctime)s %(message)s', filename = \
        'logs/automation_execution.log', filemode = 'a', level = logging.DEBUG)

#### Function(s) Declaration Begins
def get_apikey(conf):
    #m = md5.new()
    #m.update("%s" %(conf['password']))
    #md5_pwd =  m.hexdigest()
    stdurl_noapikey = 'https://%s/client/api?response=%s&' %(conf['host'], \
            'json')
    s = requests.session()
    payload = {'command': 'login', 'username': conf['username'], \
            'password': conf['password'], 'domain': '', 'response': 'json'}
    r = s.post(stdurl_noapikey, verify=False, data=payload)
    querystring = 'command=listUsers'
    r = s.get(stdurl_noapikey+querystring, verify=False)
    data = json.loads(r.text)
    if 'errorcode' in str(data):
        errormsg = str(data['listusersresponse']['errortext'])
        print errormsg
        result = ['FAILED', 'Not able to get apikey because: %s' %(errormsg)]
        return result
    if 'user' not in str(data):
        print 'There is no user, please create user and continue...'
        result = ['BLOCKED', 'There is no user, please create user and continue...']
        return result
    users = data["listusersresponse"]["user"]
    for user in users:
        if user['username'] == '%s' %conf['username'] and 'apikey' in str(user):
            user_id = user['id']
            apikey = user['apikey']
            result = ['PASSED', apikey]
        elif user['username'] == '%s' %conf['username']:
            user_id = user['id']
            querystring = 'command=registerUserKeys&id=%s' %(user_id)
            r = s.get(stdurl_noapikey+querystring, verify=False)
            data = json.loads(r.text)
            if 'errorcode' in str(data):
                errormsg = str(data["registeruserkeysresponse"]['errortext'])
                result = ['FAILED', 'Not able to generate apikey due to: %s' %(errormsg)]
                return result
            if 'apikey' in str(data):
                apikey = data["registeruserkeysresponse"]["userkeys"]["apikey"]
                result = ['PASSED', apikey]
            else:
                result = ['FAILED', 'Not able to generate apikey']
        return result

def getURL(config):
    stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(config['host'], config['apikey'], config['response'])
    return stdurl

#New get_url methosd for new configuration file
def get_url(conf, apikey):
    stdurl = 'https://%s/client/api?apikey=%s&response=%s&' %(conf['host'], apikey, 'json')
    return stdurl

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

def createScheduleSnapshot(config, bucket, name, retentioncopies, interval, type):
    ### here bucket can be a tsm dictionary or volume dictionary
    ### type is refer for vsm/tsm level local dp or volume level local dp
    if interval > 1:
        sch = 'minute=*/' + str(interval)
    else:
        sch = 'minute=*'
    if type == 'vsm':
        dataset_id = bucket['datasetid']
        tsm_id = bucket['id']
        querycommand = 'command=addLocalDPScheduler&day=*&fortype=tsm&hour=*&month=*&%s&week=*&status=enabled&retentioncopies=%s&tsmid=%s&name=%s&datasetid=%s' %(sch, retentioncopies, tsm_id, name, dataset_id)
    else:
        dataset_id = bucket['id']
        tsm_id = bucket['Tsmid']
        querycommand = 'command=addLocalDPScheduler&day=*&fortype=volume&hour=*&month=*&%s&week=*&status=enabled&retentioncopies=%s&tsmid=%s&name=%s&datasetid=%s' %(sch, retentioncopies, tsm_id, name, dataset_id)
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

def listLocalDPScheduler(config, id, level):
    # "level" means here tsm or volume
    # "id" it can be a tsm id or volume id
    stdurl = getURL(config)
    if level.lower() == 'vsm':
        id = 'tsmid=%s' %(id)
    elif level.lower() == 'volume':
        id = 'datasetid=%s' %(id)
    else:
        return('BLOCKED', 'Please give last parameter as vsm/volume')
    querycommand = 'command=listLocalDPScheduler&%s' %(id)
    respListLocalDP = sendrequest(stdurl, querycommand)
    filesave('logs/listLocalDP.txt', 'w', respListLocalDP)
    data = json.loads(respListLocalDP.text)
    if 'listLocalScheduler' in str(data['listLocalDPSResponse']):
        snapshots = data['listLocalDPSResponse']['listLocalScheduler']
        return('PASSED', snapshots)
    elif 'errorcode' in str(data['listLocalDPSResponse']):
        errormsg = data['listLocalDPSResponse']['errortext']
        return('FAILED', errormsg)
    else:
        return('BLOCKED', 'There is no schedule snapshot to list')

def deleteScheduleSnapshot(config, schSnpID):
    querycommand = 'command=deleteLocalDPScheduler&id=%s' %(schSnpID)
    stdurl = getURL(config)
    respDeleteSchSnp = sendrequest(stdurl, querycommand)
    filesave('logs/DeleteLocalDP.txt', 'w', respDeleteSchSnp)
    data = json.loads(respDeleteSchSnp.text)
    if 'errorcode' in str(data['deleteLocalDPSResponse']):
        print 'Not able to delete Schedule snapshot'
        errormsg = str(data['deleteLocalDPSResponse']['errortext'])
        return ('FAILED', errormsg)
    elif 'success' in str(data['deleteLocalDPSResponse']):
        print 'Successfully deleted schedule snapshot'
        return ('PASSED', '')
    else:
        print 'Something went wrong while deleting schedule snapshot'
        return ('BLOCKED', str(data['deleteLocalDPSResponse']))

def listVolume(config):
    stdurl = getURL(config)
    querycommand = 'command=listFileSystem'
    resplistVolumes = sendrequest(stdurl, querycommand)
    filesave('logs/listVolumes.txt', 'w', resplistVolumes)
    data = json.loads(resplistVolumes.text)
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

def listVolumeWithTSMId(config, tsm_id):
    stdurl = getURL(config)
    querycommand = 'command=listFileSystem&tsmid=%s' %(tsm_id)
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
    mountCheck = executeCmd('mount | grep %s' %(volume['mountPoint']))
    if mountCheck[0] == 'PASSED':
        umountResult = executeCmd('umount mount/%s' %(volume['mountPoint']))
        if umountResult[0] == 'PASSED':
            print 'Volume \"%s\" umounted successfully' %(volume['name'])
            return 'PASSED'
        else:
            print umountResult[1]
            print 'Volume \"%s\" failed to umount' %(volume['name'])
            return 'FAILED'
    else:
        print 'Volume \"%s\" is not mounted' %(volume['name'])
        return 'PASSED'

def umountVolume_new(volume):
    ### volume is a dictionary and it contains dataset's(volume) properties.
    mountCheck = executeCmd('mount | grep %s' %(volume['mountPoint']))
    if mountCheck[0] == 'PASSED':
        umountResult = executeCmd('umount mount/%s' %(volume['mountPoint']))
        if umountResult[0] == 'PASSED':
            print 'Volume \"%s\" umounted successfully' %(volume['name'])
            return ['PASSED', '']
        else:
            print umountResult[1]
            print 'Volume \"%s\" failed to umount' %(volume['name'])
            return ['FAILED', umountResult[1]]
    else:
        print 'Volume \"%s\" is not mounted' %(volume['name'])
        return ['PASSED', 'Volume is not mounted']

def umount_with_dir(mountpoint):
    ### mountpoint is mountpoint of mounted volume
    mountCheck = executeCmd('mount | grep %s' %(mountpoint))
    if mountCheck[0] == 'PASSED':
        umountResult = executeCmd('umount mount/%s' %(mountpoint))
        if umountResult[0] == 'PASSED':
            print 'Volume with mountpoint \"%s\" umounted...' %(mountpoint)
            return ['PASSED', '']
        else:
            print umountResult[1]
            print 'Volume with mountpoint \"%s\" failed to umount' %(mountpoint)
            return ['FAILED', umountResult[1]]
    else:
        print 'Volume with mountpoint \"%s\" is not mounted' %(mountpoint)
        return ['PASSED', 'Volume is not mounted']

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

def mountNFS_new(volume):
    ### volume is a dictionary and it contains dataset's(volume) properties. 
    ### create directory for mounting NFS volume
    executeCmd('mkdir -p mount/%s' %(volume['mountPoint']))
    ### Mount
    mountResult = executeCmd('mount -t nfs %s:/%s mount/%s' %(volume['TSMIPAddress'], volume['mountPoint'], volume['mountPoint']))
    if mountResult[0] == 'PASSED':
        print 'NFS volume \"%s\" mounted successfully' %(volume['name'])
        return ['PASSED', '']
    else:
        print 'NFS volume \"%s\" failed to mount' %(volume['name'])
        return ['FAILED', mountResult[1]]

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

##To mount an NFS volume with TCP/UDP protocol
def nfsMountPrtcl(prtcl, volume):
    ##here volume is a Dictionary
    logging.info('Inside mountPrtcl method..')
    logging.debug('creating a new directory for mounting at :%s', (volume['mountPoint']))
    mk = executeCmd('mkdir -p mount/%s' %(volume['mountPoint']))
    logging.debug('creating directory result:%s', mk)
    logging.info('executing mounting command')
    mountcmd = executeCmd('mount -o mountproto=%s,sync %s:/%s mount/%s'\
            %(prtcl, volume['TSMIPAddress'], volume['mountPoint'],\
            volume['mountPoint']))
    logging.debug('executing mounting command', mountcmd)
    output=executeCmd('mount | grep %s' %(volume['mountPoint']))
    logging.debug('mounting command result %s:', output)
    if output[0] ==  'PASSED':
        msg =  'NFS volume \"%s\" mounted successfully' %(volume['mountPoint'])
        mount_result = ['PASSED', msg]
        logging.debug('%s', msg)
        return mount_result
    else:
        msg =  'NFS volume \"%s\" failed to mount' %(volume['mountPoint'])
        mount_result = ['FAILED', msg]
        logging.error('%s', msg)
        return mount_result

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
        time.sleep(2);
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
        time.sleep(2);
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

def resultCollectionNew(testcase, value):
    f=open("results/result.csv","a")
    f.write(testcase)
    f.write(",")
    f.write(value[0])
    f.write(",")
    f.write(value[1])
    f.write("\n")
    return

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

def passCmdToController(ip, passwd, command):
    ssh.connect(ip, username="root", password=passwd, allow_agent = False)
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read()
    ssh.close()
    #print "Output Available: "+str(ip)+" path: "+outputfile
    return(output)

def passCmdToPanic(ip, passwd, command):
    ssh.connect(ip, username="root", password=passwd, allow_agent = False)
    stdin, stdout, stderr = ssh.exec_command(command)

def getControllerInfoAppend(ip, passwd, command, outputfile):
    ssh.connect(ip, username="root", password=passwd, allow_agent = False)
    stdin, stdout, stderr = ssh.exec_command(command)
    #print "Stdout = "+stdout.read()
    output = stdout.read()
    filesave1(outputfile, "a", output)
    ssh.close()
    #print "Output Available: "+str(ip)+" path: "+outputfile
    return(output)

def sshToOtherClient(ip, usrname, pwd, cmd):
    ssh.connect(ip, username=usrname, password=pwd, allow_agent = False)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    output = stdout.read()
    #print output
    error = stderr.read()
    #print error
    ssh.close()
    if not error and output:
        return output
    else:
       return error

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

def getoutput_with_error(command):
    print command
    link = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    ldata = link.stdout.readlines()
    output, errors = link.communicate()
    rco = link.returncode
    try:
         output = ldata
    except IndexError:
         output = ['null', str(errors)]
    return output

#anything to be replaced in a file
def replace_data(infile, old_data, new_data):
    f1 = open(infile,'r').read()
    f2 = open(infile,'w')
    m = f1.replace(old_data, new_data)
    f2.write(m)

def get_ntwInterfaceAndIP(ip_to_ping):
    #interfaces = getoutput("ifconfig -a| awk {'print $1'} | cut -d: -f1")
    #interfaces = map(str.rstrip, interfaces)
    interfaces = os.listdir('/sys/class/net/')
    for interface in interfaces:
        ping_by_interface = os.system(" ping -c 2 -I %s %s" %(interface, ip_to_ping))
        if ping_by_interface == 0:
            break
    else:
        result = ['FAILED', 'Not able to ping for given IP, make sure the ntw is configured']
        return result
    localClientIP = getoutput("ifconfig %s | grep 'inet ' | awk '{print $2}' "\
                         "| sed -e s/.*://" %interface)
    localClientIP = localClientIP[0].rstrip('\n')
    return ['PASSED', localClientIP]
