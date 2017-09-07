#!/usr/bin/env python
#title           :StorageConfig.py
#description     :Workflow to create Pools, VSM and Volume configuration.
#author          :Sudarshan
#date            :20170818
#version         :1
#usage           :python StorageConfig.py
#notes           :
#python_version  :2.7
#==============================================================================

from GUIConfig import GuiConfig as const
from WebUtils import WebUtils
import Logging, time, os
from SSHConnection import SSHConnection


def main():
    filename = os.path.abspath(__file__)
    log = Logging.getLogger(filename, 'ActivateDR')
    log.info("Test ActivateDR begins")
    try:
        GUI = WebUtils()
        Url = const.url
        password = const.password
        username = const.username
        GUI.login_EC(Url, username, password)
        time.sleep(5)
        GUI.HA_Maintenance(1, "Maintenance")
        time.sleep(20)
        t = SSHConnection()
        user = const.node_username
        pwd = const.node_password
        host = const.Node1_IP
        vsm_ip = const.VSM1Ip
        out = t.cbdpctl_status(user, pwd, host, vsm_ip)
        if out[0] == "uptodate":
            GUI.Activate_DR(const.BackupVSMIP)
            time.sleep(2)
            GUI.close_browser()
        else:
            log.error("DR transfer is not uptodate")
    except Exception as e:
        log.error("Exception: TC: ActivateDR"), str(e)
if __name__ == '__main__':
    main()




