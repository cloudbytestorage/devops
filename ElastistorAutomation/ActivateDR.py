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
import logging, time
from SSHConnection import SSHConnection


def main():
    GUI = WebUtils()
    t = SSHConnection()
    out = t.cbdpctl_status()
    if out[0] == "uptodate":
        Url = const.url
        password = const.password
        username = const.username
        GUI.login_EC(Url, username, password)
        time.sleep(5)
        GUI.Activate_DR(const.BackupVSMIP)
        time.sleep(2)
        GUI.close_browser()
    else:
        print "DR transfer is not uptodate"
if __name__ == '__main__':
    main()




