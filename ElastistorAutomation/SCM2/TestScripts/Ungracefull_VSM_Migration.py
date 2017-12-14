#!/usr/bin/env python
#title           :Verify_ungracefull_VSM_Migration.py
#description     :This script is run to verify ungracefull HA during VSM Migration.
#author          :Swarnalatha
#date            :20171207
#version         :1
#usage           :python Verify_ungracefull_VSM_Migration.py
#notes           :
#python_version  :2.7
#==============================================================================

from SCM2.GUIConfig import GuiConfig as const
from SSHConnection import SSHConnection
import time, sys, Logging, os

def main():
    filename = os.path.abspath(__file__)
    log = Logging.getLogger(filename, 'Ungracefull_VSM_Migration')
    try:
        user = const.node_username
        pwd = const.node_password
        host2 = const.Node2_IP
        vsm_ip = const.VSM1Ip
        SSH = SSHConnection()
        time.sleep(10)
        out1 = SSH.cbdpctl_Migration(user, pwd, host2, vsm_ip)
        print out1
        bytestransfered = out1[1]
        time.sleep(60)
        out2 = SSH.cbdpctl_Migration(user, pwd, host2, vsm_ip)
        print out2
        cstatus = out2[0]
        cbytestransfered = out2[1]
        if cstatus == "transferring" or int(cbytestransfered) > int(bytestransfered):
            print "Pass: VSM Migration transfer resumed successfully"
            log.info("Pass: VSM Migration transfer resumed successfully")
        elif cstatus == "uptodate":
            print "Pass: VSM migration transfer resumed and completed successfully"
            log.info("Pass: VSM migration transfer resumed and completed successfully")
        else:
            print "Fail: VSM Migration resume failed"
            log.error("Fail: VSM Migration resume failed")

    except Exception as e:
        log.error("Exception:TC: Verify ungracefull_VSM_MIgration", str(e))

if __name__ == '__main__':
    main()