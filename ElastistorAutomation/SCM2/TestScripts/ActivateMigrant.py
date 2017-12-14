#!/usr/bin/env python
#title           :ActivateMigrant.py
#description     :Workflow to activate migrant VSM.
#author          :Swarnalatha
#date            :20171212
#version         :1
#usage           :python ActivateMigrant.py
#notes           :
#python_version  :2.7
#==============================================================================

from SCM2.GUIConfig import GuiConfig as const
from WebUtils import WebUtils
import Logging, time, os
from SSHConnection import SSHConnection


def main():
    filename = os.path.abspath(__file__)
    log = Logging.getLogger(filename, 'ActivateDR')
    log.info("Test ActivateDR begins")
    try:

        #GUI.HA_Maintenance(1, "maintenance")
        time.sleep(20)
        t = SSHConnection()
        user = const.node_username
        pwd = const.node_password
        host = const.Node1_IP
        vsm_ip = const.VSM1Ip
        out = t.cbdpctl_Migration(user, pwd, host, vsm_ip)
        print out[1], "Sud"

        if out[0] == "uptodate":
            GUI = WebUtils()
            Url = const.url
            password = const.password
            username = const.username
            GUI.login_EC(Url, username, password)
            time.sleep(5)
            GUI.Activate_MigrantVSM(const.BackupVSMIP)
            time.sleep(2)

        else:
            log.error("Migrant transfer is not uptodate")
    except Exception as e:
        log.error("Exception: TC: Activate migrant"), str(e)
if __name__ == '__main__':
    main()
