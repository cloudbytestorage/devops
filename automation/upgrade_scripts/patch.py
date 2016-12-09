#!/usr/bin/python
import os
import json
import subprocess
import time
from datetime import datetime
import sys
from cbrequest import get_url, configFile, sendrequest, resultCollection, \
        get_apikey, executeCmd, sshToOtherClient, passCmdToPanic, \
        getControllerInfo

from haUtils import change_node_state, ping_machine
import logging

# Get necessary params and values from config file (conf.txt)
conf = configFile(sys.argv)

DEVMAN_IP = conf['host']
USER = conf['username']
PASSWORD = conf['password']

APIKEY = get_apikey(conf)
APIKEY = APIKEY[1]
STDURL = get_url(conf, APIKEY)

Setup = conf['setup']

EC1_IP = conf['EC1_IP']
EC1_Username = conf['EC1_Username']
EC1_Password = conf['EC1_Password']

Node1_IP = conf['Node1_IP']
Node1_Username = conf['Node1_Username']
Node1_Password = conf['Node1_Password']

Node2_IP = conf['Node2_IP']
Node2_Username = conf['Node2_Username']
Node2_Password = conf['Node2_Password']

BuildPath = conf['Build_Path']

# Clear the log file before execution starts

executeCmd('> /logs/automation_execution.log')

# Initialization for Logging location
tcName = sys.argv[0]
tcName = tcName.split('.py')[0]
logFile = tcName + '.log'
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',\
filename='logs/'+logFile,filemode='a',level=logging.DEBUG)


def gen_build_number(path):
	'''Function for genbuild dir'''
	return (path.split("/")[6].split("_")[2].split(".")[0])

def patch_dir_prepare(box_ip, box_user, box_pwd, num, path):
    package_name = path.split("/")[6]
   
   mkdir_cmd = 'mkdir /cbdir/patch%s' %(num)
    try:
        mkdir_result = sshToOtherClient(box_ip, box_user, box_pwd , mkdir_cmd)
        if mkdir_result != "":
            print mkdir_result
            exit()
        else:
            print "Created the patch directory"
    #except paramiko.ssh_exception.AuthenticationException as e:
    except: 
        print "Patch directory creation failed, verify credentials"
        exit()
   
   fetch_cmd = 'cd /cbdir/patch%s ; fetch %s' %(num, path)
    try:
        fetch_result = sshToOtherClient(box_ip, box_user, box_pwd, fetch_cmd)
        if (package_name in fetch_result) and ("Not Found" not in fetch_result):
            print "Downloaded the patch package"
        else:
            print fetch_result
            exit()
    except:
        print "Unable to fetch build from build server"
        exit()

    unzip_cmd = 'tar -zxvf %s' %(package_name)
    try:
        unzip_result = sshToOtherClient(box_ip, box_user, box_pwd, unzip_cmd)
        if "apply_patch.py" in unzip_result:
            print "Unzipped package"
        else:
            print unzip_result
            exit()
    except:
        print "Unable to unzip patch package"
        exit()

def apply_patch(ptype, box_ip, box_user, box_pwd, num):
    if ptype == 'ec':
        patch_application_cmd = 'cd /cbdir/patch%s ; python apply_patch.py -u1' %(num)
        result_string = "Patching for devman completed"
    elif ptype == 'nodeha':
        patch_application_cmd = 'cd /cbdir/patch%s ; python apply_patch.py -u2' %(num)
        result_string = "Patching for node ha completed"
    elif ptype == 'kernel':
        patch_application_cmd = 'cd /cbdir/patch%s ; python apply_patch.py -u3' %(num)
        result_string = "Patching kernel completed"
    try:
        patch_application_result = sshToOtherClient(box_ip, box_user, box_pwd, patch_application_cmd)
        if result_string in patch_application_result:
            print "%s patch has been completed successfully" %(ptype)
            else:
                print patch_application_result 
                exit()
    except:
        print "Unable to apply %s patch" %(ptype)
        exit()
    sshToOtherClient(box_ip, box_user, box_pwd, 'sync; sync; sync')

def bring_up_check(box_ip):
    node_online = True
    ping_result = ping_machine(node_ip)
    count = 1
    while ping_result[0] = 'FAILED':
        if count == 4:
            node_online = False
            break
        print "Box did not come up yet, sleeping for 5 more min"
        time.sleep(300)
        count = count + 1
        ping_result = ping_machine(node_ip)
    return (node_online)
        
def standalone_devman_upgrade(ec_ip, ec_user, ec_pwd, patchnum, patchpath):
    patch_dir_prepare(ec_ip, ec_user, ec_pwd, patchnum, patchpath)
    patch_type = 'ec'
    apply_patch(patch_type, ec_ip, ec_user, ec_pwd, patchnum)
    getControllerInfo(node_ip, node_pwd, 'reboot', 'reboot.txt')
    
    time.sleep(300)
    ec_up_status = bring_up_check(ec_ip)
    if ec_up_status == True:
        print "Devman patched and brought up"
    else:
        print "Could't bring up devman after patching, unable to proceed"
        exit()

def echa_devman_upgrade(ec_ip, ec_user, ec_pwd, patchnum, patchpath):
    patch_dir_prepare(ec_ip, ec_user, ec_pwd, patchnum, patchpath)
    patch_type = 'ec'
    apply_patch(patch_type, ec_ip, ec_user, ec_pwd, patchnum)

def node_upgrade(node_ip, node_user, node_pwd, patchnum, patchpath):
    patch_dir_prepare(node_ip, node_user, node_pwd, patchnum, patchpath)
    
    patch_type = 'nodeha'
    apply_patch(patch_type, node_ip, node_user, node_pwd, patchnum)

    passCmdToPanic(node_ip, node_pwd, 'sysctl kern.coredump_on_panic=0; sysctl debug.kdb.panic=1')
    
    time.sleep(300)
    
    node_up_status = bring_up_check(node_ip)
    
    if node_up_status == True:
        patch_type = 'kernel'
        apply_patch(patch_type, node_ip, node_user, node_pwd, patchnum)
        getControllerInfo(node_ip, node_pwd, 'reboot', 'reboot.txt')
    
        time.sleep(300)

        node_up_status = bring_up_check(node_ip)
        if node_up_status == True:
            time.sleep(30) #Grace period before state change
            available_state = change_node_state(STDURL, node_ip, 'available')
            if available_state == 'FAILED':
                print "failed to move node to available state, unable to proceed"
                exit()
            else:
                print "Node is available. Patch application on this node is Complete"

        else:
            print "box did not come up after 20 min, unable to proceed"
            exit()
    else:
        print "box did not come up after 20 min, unable to proceed"
        exit()


if __name__ == "__main__":
	BuildNum = gen_build_number(BuildPath)	
	if(Setup == "Node-HA"):
            standalone_devman_upgrade(EC1_IP, EC1_Username, EC1_Password, BuildNum, BuildPath)
	    node_upgrade(Node1_IP, Node1_Username, Node1_Password, BuildNum, BuildPath)	
	    node_upgrade(Node2_IP, Node2_Username, Node2_Password, BuildNum, BuildPath)	
	elif(setup == "EC-HA"):
            echa_devman_upgrade(Node1_IP, Node1_Username, Node1_Password, BuildNum, BuildPath)
            node_upgrade(Node1_IP, Node1_Username, Node1_Password, BuildNum, BuildPath)
            
            echa_devman_upgrade(Node1_IP, Node1_Username, Node1_Password, BuildNum, BuildPath)
            node_upgrade(Node2_IP, Node2_Username, Node2_Password, BuildNum, BuildPath)
	else:
            print "Provide the right setup type in the config file"

