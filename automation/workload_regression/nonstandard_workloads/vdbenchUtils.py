import sys
import os
import json
import logging
import subprocess
from time import ctime
import time
from cbrequest import executeCmd, getoutput

#make sure the standard file is present in templates folder to run vdbench

def executeVdbench(confFile, outputFile):
    logging.info('.....inside excecute_vdbench method....')
    logging.info('executing vdbench command')
    out = os.system('./vdbench/vdbench -f vdbench/%s -o vdbench/%s ' 
            %(confFile, outputFile))
    return

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

def createRunTimeConfig(confFile, userValues):
    # confFile is a template for creating config file
    # userValues is a directory, that contains new values to... 
    # ...updated in config file

    FIRSTELEMENT = 0
    EQUALOPERATOR = '='
    QUOMAOPERATOR = ','
   
    # removing the dummy text file if it exits
    os.system('rm -rf dummyConfFile.txt')
    
    # Opening source file(template)
    with open(confFile, "r") as sourceFile:
        for line in sourceFile:
        
            # creating a dummy file for newly updated values
            with open("dummyConfFile.txt", "a") as dummyFile:

                # making sure no empty line procede further
                if not line.strip():
                    continue
                
                # converting the line into a list, and will get only one value
                line = line.split()

                # In above code we converted whole line in a list with single element
                # getting the only present element from the list
                line = str(line[FIRSTELEMENT])

                # splitting all the values by "," from the above string and getting list 
                line = line.split(QUOMAOPERATOR)
                
                # proceding all the elements of the list
                newLine = []
                for element in line:
                    
                    # splitting elements by "=" into a sub list
                    subList = element.split(EQUALOPERATOR)
                    
                    # matching all the values with the user given values and updating the same
                    if subList[0] in userValues:
                        subList[1] = userValues[subList[0]]
                    
                    newLine.append(subList[0] + EQUALOPERATOR + subList[1])
                
                newLine = ','.join(newLine) + "\n"

                # writing newly created newLine into dummyFile
                dummyFile.write(str(newLine))

    # once dummy file is generated successfully, 
    # updating source file with the latest values
    with open("dummyConfFile.txt") as df:
        with open(confFile, "w") as sf:
            for line in df:
                sf.write(line)
