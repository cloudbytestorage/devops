import sys
import os
import json
import logging
import subprocess
from time import ctime
import time
from cbrequest import executeCmd, getoutput

#make sure the standard file is present in templates folder to run vdbench

##To Execute vdbench
def excecute_vdbench(volume):
    ##volume is dictionary
    logging.info('.....inside excecute_vdbench method....')
    logging.info(' overwriting the file fileconfig with std path')
    executeCmd('yes | cp -rf vdbench/templates/fileconfig vdbench/fileconfig')
    output = getoutput('mount | grep %s | awk \'{print $3}\'' %(volume['mountPoint']))
    old_str = 'mountDirectory'
    new_str = output[0].rstrip('\n')
    path = 'vdbench12/fileconfig'
    logging.info('Replacing the std path with volume mountpoint')
    res = executeCmd("sed -i 's/%s/%s/' %s " %(old_str.replace('/', '\/'),\
            new_str.replace('/', '\/'), path ))
    logging.info('executing vdbench command')
    out = os.system('./vdbench/vdbench -f vdbench/fileconfig -o vdbench/output &')
    logging.debug('vdbench command result:%s', out)

###execute vdbench by passing sample file
def executeVdbenchFile(volume, vdbfile):
    ##volume is dictionary
    logging.info('.....inside excecute_vdbench method....')
    logging.info(' overwriting the file fileconfig with std path')
    executeCmd('yes | cp -rf vdbench/templates/%s vdbench/%s' %(vdbfile, volume['name']))
    output = getoutput('mount | grep %s | awk \'{print $3}\'' %(volume['mountPoint']))
    old_str = 'mountDirectory'
    new_str = output[0].rstrip('\n')
    path = 'vdbench/%s' %volume['name']
    logging.info('Replacing the std path with volume mountpoint')
    res = executeCmd("sed -i 's/%s/%s/' %s " %(old_str.replace('/', '\/'), new_str.replace('/', '\/'), path ))
    logging.info('executing vdbench....')
    out = os.system('./vdbench/vdbench -f vdbench/%s -o vdbench/output &' %volume['name'])
    #out = os.system('./vdbench12/vdbench -f vdbench12/fileconfig &')
    return out

##for more mountpoint within a single file
def writingVDBfile(x, volume):
    output = getoutput('mount | grep %s | awk \'{print $3}\'' %(volume['mountPoint']))
    old_str = 'mountDirectory%s' %x
    new_str = output[0].rstrip('\n')
    path = 'vdbench/%s' %vdbNewFile
    logging.info('Replacing the std path with volume mountpoint')
    res = executeCmd("sed -i 's/%s/%s/' %s " %(old_str.replace('/', '\/'), new_str.replace('/', '\/'), path ))

###vdbFile - name of the vdbench file that is running
def is_vdbench_alive(vdbFile):
    pidCheck = os.popen("ps -eo pid,command | grep './vdbench/vdbench "\
            "-f vdbench/%s -o vdbench/output' | grep -v grep | "\
            "awk '{print $1}'" %(vdbFile)).read().rstrip('\n')
    return pidCheck

###get vdbench pid and will check till process completes
##vdbfile = name of file to run vdbench
def vdbench_pid(vdbfile):
    while True:
        pidCheck = os.popen("ps -eo pid,command | grep './vdbench/vdbench "\
                "-f vdbench/%s -o vdbench/output' | grep -v grep | "\
                "awk '{print $1}'" %vdbfile).read().rstrip('\n')
        if not pidCheck:
            break
        else:
            continue
    return pidCheck

def kill_vdbench():
    logging.debug('inside kill_vdbench...')
    pid = getoutput('ps -aux |grep vdbench |awk \'{print $2}\'')
    logging.debug('vdbench process going to be killed...: %s', pid)
    processlist =[]
    for process in pid:
        p1 = process.rstrip('\n')
        processlist.append(p1)
    #print processlist
    logging.debug('vdbench process ids...: %s', processlist)
    cmd = 'kill -9'
    for proc in processlist:
        cmd = cmd + ' %s' %(proc)
       # print proc
    res = executeCmd(cmd)
    #print res
    if res[0] == 'PASSED' or 'No such process' in str(res[1]):
        print 'vdbench process is killed'
        logging.debug('vdbench process are killed')
    else:
        print 'vdbench process are not killed'
        logging.debug('one or more vdbench process is not killed, Error: %s', \
                res[1])

##process_name : process you want to search and kill the process
def kill_process(process_name):
    logging.debug('inside kill_process...')
    pid = getoutput('ps -aux |grep %s |awk \'{print $2}\'' %(process_name))
    logging.debug('process going to be killed...: %s', pid)
    processlist =[]
    for process in pid:
        p1 = process.rstrip('\n')
        processlist.append(p1)
    #print processlist
    logging.debug('%s process ids...: %s', process_name, processlist)
    cmd = 'kill -9'
    for proc in processlist:
        cmd = cmd + ' %s' %(proc)
    res = executeCmd(cmd)
    if res[0] == 'PASSED' or 'No such process' in str(res[1]):
        print 'process is killed'
        logging.debug('process are killed')
    else:
        print 'process are not killed'
        logging.debug('one or more process is not killed, Error: %s', \
                res[1])
