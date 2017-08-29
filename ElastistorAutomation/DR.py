#!/usr/bin/env python
#title           :DisableEnable.py
#description     :Test DR enable and disable condition with expected results.
#author          :Sudarshan
#date            :20170818
#version         :1
#usage           :python DisableEnable.py
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
            GUI.Create_DR(name=const.DRName, bkp_ip=const.BKPIP)
            print "DR created successfully"
        except Exception as j:
            print "Error: Exception occure while creating DR", str(j)
        time.sleep(20)
        print "Waiting till schedule duration for DR to begin"
        time.sleep(90)
        SSH = SSHConnection()
        output = SSH.cbdpctl_status()
        print output
        if output[0] == "transferring":
            #print "Sudarshan"
            username = const.node_username
            password = const.node_password
            host = const.Node1_IP
            vsm_ip = const.VSM1Ip
            try:
                GUI.DR_Enable_Disable("Disable")
                print "DR transfer disabled successfully"
                time.sleep(30)
                t = SSHConnection()
                t.createSSHConnection(host=host, username=username, password=password)
                time.sleep(5)
                out = t.exec_cmd("jls")
                out1 = out.split()
                if vsm_ip in out1:
                    jls = out1.index(vsm_ip)
                    jls_id = int(out1[jls - 1])
                    time.sleep(2)
                    output = t.exec_cmd("jexec %s cbdpctl -c list" % jls_id)
                    while output:
                        time.sleep(10)
                        output1 = t.exec_cmd("jexec %s cbdpctl -c list" % jls_id)
                        if not output1:
                            print "Pass: Verified that DR transfer did not continued after disabling transfer"
                        else:
                            print "Fail: DR transfer is still in-progress"
                    print "Pass: Verified that DR transfer did not continued after disabling transfer"
                t.close()
            except Exception as z:
                print "Error: Exception occured while disabling transfer", str(z)
                raise
            try:
                time.sleep(10)
                print "Enabling DR transfer to verify resumability"
                GUI.DR_Enable_Disable("Enable")
                print "DR transfer enabled successfully"
            except Exception as f:
                print "Error: Exception occured while enabling transfer", str(f)
                raise
            time.sleep(60)
            out1 = SSH.cbdpctl_status()
            print out1
            bytestransfered = out1[1]
            completed = out1[2]
            time.sleep(100)
            out2 = SSH.cbdpctl_status()
            print out2
            cstatus = out2[0]
            cbytestransfered = out2[1]
            ccompleted = out2[2]
            if cstatus == "transferring" and int(cbytestransfered) > int(bytestransfered):
                print "Pass: DR transfer resumed successfully"
            elif cstatus == "uptodate":
                print "Pass: DR resumed and completed successfully"
            else:
                print "Fail: DR resume failed"
            time.sleep(2)
            GUI.close_browser()

        elif output[1] == "uptodate":
            print "Base snapshot transfered"
        else:
            print "Failed to get DR status, please recheck"

    except Exception as e:
        print "Exception Occured: While logging into EC", str(e)

if __name__ == '__main__':
    main()

