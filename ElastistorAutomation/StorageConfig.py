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
import Logging, time

def main():
    Url = const.url
    password = const.password
    username = const.username

    try:
        print ("Test begins")
        GUI = WebUtils()
        GUI.login_EC(Url, username, password)
        if True:
            print ("Successfully Logged into EC")
            try:
                GUI.Configure_DA(const.Disk_Enclosure_Name,18)
                print "Disk Array Configured successfully"
            except Exception as e:
                print "Error: Exception occured while configuring Disk Array"
                return False
            try:
                time.sleep(10)
                GUI.Add_Pools(1, const.NodeName+str(1), const.Pool1, const.R5, 3)
                time.sleep(5)
                GUI.Add_Pools(1, const.NodeName+str(2), const.Pool2, const.R6, 4)
                if True:
                    GUI.Add_VSMS(const.VSM1Name, 1, capacity=1, ip=const.VSM1Ip)
                    time.sleep(5)
                    GUI.Add_VSMS(const.VSM2Name, 2, capacity=1, ip=const.VSM2Ip)
                    if True:
                        GUI.Add_NCFS_Volume(1, "NFSVol1",100, "NFS", const.NFSClientIP)
                        time.sleep(2)
                        GUI.Add_NCFS_Volume(2, "NFSVol2",100, "NFS", const.NFSClientIP)
                        time.sleep(2)
                        GUI.close_browser()
                    else:
                        print ("Error: Failed to add Volumes")
                else:
                    print ("Error: Failed to create VSMs")
            except Exception as f:
                print "Exception Occured: adding pools", str(f)

    except Exception as e:
        print "Exception Occured: While logging to EC",str(e)

if __name__ == '__main__':
    main()

