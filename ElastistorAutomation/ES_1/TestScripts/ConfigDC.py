#!/usr/bin/env python
#title           :ConfigDC.py
#description     :Configure Data Center workflow.
#author          :Sudarshan
#date            :20170818
#version         :1
#usage           :python ConfigDC.py
#notes           :
#python_version  :2.7
#==============================================================================

from ES_1.GUIConfig import GuiConfig as const
from WebUtils import WebUtils
import Logging, time, sys, os

def main():
    Url = const.url
    password = const.password
    username = const.username
    try:
        filename = os.path.abspath(__file__)
        log = Logging.getLogger(filename, 'ConfigDC')
        log.info("Test ConfigDC begins")
        GUI = WebUtils()
        GUI.login_EC(Url, username, password)
        if True:
            GUI.Addsite(n=1,sitename=const.SiteName,location=const.Location)
            if True:
                GUI.Add_HA_Group(n=1,haname=const.HaGroupName,ip1=const.HaG_IP1,ip2=const.HaG_IP2)
                if True:
                    GUI.Add_Node(2, const.NodeName)
                    time.sleep(5)
                    if True:
                        GUI.Add_Account(const.AccountName,const.mailid,const.userpwd)
                        if True:
                            GUI.Add_VLAN(const.VLAN_ID,const.VLAN_Interface)
                            time.sleep(3)
                            if True:
                                GUI.Configure_DA(const.Disk_Enclosure_Name, 18)
                            GUI.close_browser()
                        else:
                            log.error("Failed to add account")
                    else:
                        log.error("Failed to add Node")
                else:
                    log.error("Failed to add HA Group")
            else:
                log.error("Failed to create Site")
        else:
            log.error("Failed to Login to EC ")
    except Exception as e:
        print "Exception Occured:TC: ConfigDC",str(e)
        raise

if __name__ == '__main__':
    main()

