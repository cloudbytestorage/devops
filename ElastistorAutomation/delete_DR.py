#!/usr/bin/env python
#title           :delete_DR.py
#description     :Test to delete DR VSM with expected results.
#author          :SWarnalatha
#date            :20170831
#version         :1
#usage           :python delete_DR.py
#notes           :
#python_version  :2.7
#==============================================================================

from GUIConfig import GuiConfig as const
from SSHConnection import SSHConnection
from WebUtils import WebUtils
import logging, time

def main():
    Url = const.url
    password = const.password
    username = const.username
    try:
        print ("Test begins")
        GUI = WebUtils()
        GUI.login_EC(Url, username, password)
        try:
            GUI.DR_Enable_Disable("Disable")
            print "DR transfer disabled successfully"
            time.sleep(30)
            GUI.deleteDR()
            print "DR VSM deleted sucessfully"
        except Exception as fi:
            print "Error: While deleting DR VSM ", str(fi)
            raise
    except Exception as e:
            print "Exception Occured: While logging into EC", str(e)

if __name__ == '__main__':
    main()

