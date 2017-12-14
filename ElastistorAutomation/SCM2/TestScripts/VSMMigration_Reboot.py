#!/usr/bin/env python
#title           :VSMMigration_Reboot.py
#description     :Test Ungracefull HA for VSM Migration.
#author          :Swarnalatha
#date            :20171207
#version         :1
#usage           :python VSMMigration.py
#notes           :
#python_version  :2.7
#==============================================================================

from SCM2.GUIConfig import GuiConfig as const
from SSHConnection import SSHConnection
from WebUtils import WebUtils
import time, sys, Logging, os

def main():
    Url = const.url
    password = const.password
    username = const.username
    filename = os.path.abspath(__file__)
    log = Logging.getLogger(filename, 'Ungracefull_VSM_Migration')
    try:
        log.info("Test UngracefullHA_VSM_Migration begins")
        GUI = WebUtils()
        #GUI.Enable_Flash()
        GUI.login_EC(Url, username, password)
        time.sleep(5)
        try:
            GUI.Create_MigrantVSM(bkp_ip=const.BKPIP)
        except Exception as j:
            print "Error: Exception occure while creating VSM Migration", str(j)
            raise
        time.sleep(20)
        GUI.close_browser()
        print "Waiting till schedule duration for migrant transfer to begin"
        log.info("Waiting till schedule duration formigrant transfer to begin")
        user = const.node_username
        pwd = const.node_password
        host1 = const.Node1_IP
        vsm_ip = const.VSM1Ip
        time.sleep(80)
        SSH = SSHConnection()
        output = SSH.cbdpctl_Migration(user,pwd,host1,vsm_ip)
        print output
        if output[0] == "transferring":
            try:
                SSH.createSSHConnection(host1,user,pwd)
                time.sleep(2)
                SSH.exec_cmd("reboot > /dev/null &")
                if True:
                    print "Rebooting Node1"
                    log.info("Rebooting Node for ungracefull HA")
                else:
                    print "Failed to Reboot Node1"
                    log.error("Failed to Reboot Node")
            except Exception as f:
                print "Error: SSH Connection ", str(f)
                raise
        else:
            print "Fail:Migrant transfer did not started after schedule duration"
            log.error("Fail:Migrant transfer did not started after schedule duration")

    except Exception as e:
        print "Exception Occured:TC: UngracefullHA_VSM_Migration", str(e)
        log.error("Exception Occured:TC: UngracefullHA_VSM_Migration")

if __name__ == '__main__':
    main()

