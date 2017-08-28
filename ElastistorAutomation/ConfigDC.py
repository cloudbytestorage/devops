#!/usr/bin/env python
#title           :SeleniumEC.py
#description     :Workflow to create Site, HA Group and Nodes configuration.
#author          :Sudarshan
#date            :20170818
#version         :1
#usage           :python SeleniumEC.py
#notes           :
#python_version  :2.7
#==============================================================================

from GUIConfig import GuiConfig as const
from WebUtils import WebUtils
import logging, time
from datetime import datetime

def main():
    Url = const.url
    password = const.password
    username = const.username
    try:
        print ("Test begins")
        GUI = WebUtils()
        GUI.login_EC(Url, username, password)
        if True:
            print ("Info: Successfully Logged into EC")
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
                            GUI.close_browser()
                        else:
                            print "Error: Failed to create VLAN"
                    else:
                        print ("Error: Failed to add account")
                else:
                    print ("Error: Failed to add Node")
            else:
                print ("Error: Failed to create HA Group")
        else:
            print ("Error: Failed to add Site")
    except Exception as e:
        print "Exception Occured:",str(e)

if __name__ == '__main__':
    main()

