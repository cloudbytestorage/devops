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

from SCM2.GUIConfig import GuiConfig as const
from SSHConnection import SSHConnection
from WebUtils import WebUtils
import Logging, time, os, sys

def main():
    Url = const.url
    password = const.password
    username = const.username
    filename = os.path.abspath(__file__)
    log = Logging.getLogger(filename, 'Migration_enable_disable')
    try:
        log.info("Test Resumability_Migration begins")
        GUI = WebUtils()
        #GUI.Enable_Flash()
        GUI.login_EC(Url, username, password)
        try:
            GUI.Create_MigrantVSM(bkp_ip=const.BKPIP)
        except Exception as j:
            print "Error: Exception occure while creating Migration", str(j)
            sys.exit(1)
        time.sleep(60)
        print "Waiting till schedule duration for Migration to begin"
        log.info("Waiting till schedule duration for Migration to begin")
        time.sleep(10)
        user = const.node_username
        pwd = const.node_password
        host1 = const.Node1_IP
        vsm_ip = const.VSM1Ip
        SSH = SSHConnection()
        output = SSH.cbdpctl_Migration(user,pwd,host1,vsm_ip)
        print output
        if output[0] == "transferring":
            try:
                GUI.Migration_Enable_Disable("Disable")
                log.info("Migration transfer disabled successfully")
                time.sleep(30)
                t = SSHConnection()
                t.createSSHConnection(host=host1, username=user, password=pwd)
                time.sleep(5)
                out = t.exec_cmd("jls")
                out1 = out.split()
                if vsm_ip in out1:
                    jls = out1.index(vsm_ip)
                    jls_id = int(out1[jls - 1])
                    time.sleep(20)
                    output = t.exec_cmd("jexec %s cbdpctl -c list" % jls_id)
                    if not output:
                        log.info("Pass: Verified that Migration transfer did not continued after disabling transfer")
                    else:
                        log.error("Fail: Migration transfer is still in-progress")
                t.close()
            except Exception as z:
                log.error("Error: Exception occured while disabling transfer"), str(z)
                raise
            try:
                time.sleep(10)
                log.info("Enabling Migration transfer to verify resumability")
                GUI.Migration_Enable_Disable("Enable")
                log.info("Migration transfer enabled successfully")
            except Exception as f:
                log.error("Error: Exception occured while enabling transfer"), str(f)
                raise
            time.sleep(50)
            out1 = SSH.cbdpctl_Migration(user,pwd,host1,vsm_ip)
            bytestransfered = out1[1]
            time.sleep(30)
            out2 = SSH.cbdpctl_Migration(user,pwd,host1,vsm_ip)
            cstatus = out2[0]
            cbytestransfered = out2[1]
            if cstatus == "transferring" and int(cbytestransfered) > int(bytestransfered):
                log.info("Pass: Migration transfer resumed successfully")
            elif cstatus == "uptodate":
                log.info("Pass: Migration resumed and completed successfully")
            else:
                log.error("Fail: Migration resume failed")
            time.sleep(2)
        elif output[0] == "uptodate":
            log.info("Base snapshot transfered")
        else:
            log.info("Failed to get DR status, please recheck")
        time.sleep(5)
        try:
            GUI.Migration_Enable_Disable("Disable")
            print "Migrant transfer disabled successfully"
            time.sleep(10)
            GUI.deleteMigrantVSM()
            print "Migrant VSM deleted sucessfully"
            time.sleep(2)
            GUI.close_browser()
        except Exception as fi:
            print "Error: While deleting Migrant VSM ", str(fi)
            raise
    except Exception as e:
        log.error("Exception Occured: While logging into EC")
        print str(e)
        sys.exit(1)

if __name__ == '__main__':
    main()
