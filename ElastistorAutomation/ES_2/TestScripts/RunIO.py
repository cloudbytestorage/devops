#!/usr/bin/env python
#title           :IO.py
#description     :Runs IO after connecting to Client on specified VSM's volumes
#author          :Sudarshan
#date            :20170818
#version         :1
#usage           :python IO.py
#notes           :
#python_version  :2.7
#==============================================================================

from ES_2.GUIConfig import GuiConfig as const
import Logging, time, os
from SSHConnection import SSHConnection

def main():
    vsmip = const.VSM1Ip
    clientip = const.hostIP
    filename = os.path.abspath(__file__)
    log = Logging.getLogger(filename, 'RunIO')
    try:
        log.info("Test RunIO begins")
        ssh = SSHConnection()
        ssh.createSSHConnection(clientip,username="root",password="test123")
        time.sleep(2)
        ssh.exec_cmd("umount 16.10.31.200:/CBUserNFSVol1")
        time.sleep(2)
        cmd = "python IORunner.py --vsms_ip %s" % vsmip
        print "Running IO"
        print "Waiting for IO to finish....."
        out = ssh.exec_cmd(cmd)
        if "Vdbench execution completed successfully" in out:
            log.info("IO ran successfully")
        else:
            log.error("IO error")
    except Exception as e:
        log.error("Exception Occured:TC: RunIO"),str(e)

if __name__ == '__main__':
    main()

