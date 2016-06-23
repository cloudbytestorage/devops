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

#localoutputdir='logs/output'
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
def createSFTPConnection(IP='localhost',user='root',paswd='test'):
    t = paramiko.Transport((IP,22)) 
    t.connect(username=user, password=paswd)
    sftp = paramiko.SFTPClient.from_transport(t) 
    return sftp

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
