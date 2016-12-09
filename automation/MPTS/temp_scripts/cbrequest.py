import json
import requests
import md5
import fileinput
import subprocess
import time
import datetime

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
    querycommand = 'command=queryAsyncJobResult&jobId=%s' %(jobid)
    check_queryAsyncJobStatus = sendrequest(url, querycommand)
    data = json.loads(check_queryAsyncJobStatus.text)
    status = data["queryasyncjobresultresponse"]["jobstatus"]
    filesave("logs/queryAsyncJobResult.txt","w",check_queryAsyncJobStatus)
    if status == 0 :
        print "Processing ..."
        time.sleep(2);
        queryAsyncJobResult(url, jobid);
    else  :
        #print "status : "
        return ;

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

def resultCollection(testcase,value):
    f=open("results/result.csv","a")
    f.write(testcase)
    f.write(",")
    f.write(value[0])
    f.write(",")
    f.write(value[1])
    f.write("\n")
    return;

#### Function(s) Declartion Ends
