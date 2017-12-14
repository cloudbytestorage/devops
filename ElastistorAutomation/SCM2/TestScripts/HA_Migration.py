#------------------------------------------------------------------------------
#!/usr/bin/env python
#title           :HA_DR.py
#description     :Testing Resumability incase of Gracefull HA.
#note            :These methods are written using EC of P5 1.4.0.1089 build.
#author          :Swarnalatha
#date            :2017/12/4
#version         :1
#usage           :python HA_Migration.py
#notes           :
#python_version  :2.7.12
#==============================================================================
from SCM2.GUIConfig import GuiConfig as const
from SSHConnection import SSHConnection
from WebUtils import WebUtils
import time, os, Logging

def main():

    Url = const.url
    password = const.password
    username = const.username
    filename = os.path.abspath(__file__)
    log = Logging.getLogger(filename, 'HA_Migration')
    try:
        log.info("Testing resumability incase of gracefull HA")
        GUI = WebUtils()
        GUI.Enable_Flash()
        GUI.login_EC(Url, username, password)

        try:

            GUI.Create_MigrantVSM(bkp_ip=const.BKPIP)
            print "Migrant VSM created successfully"
        except Exception as j:

            print "Error: Exception occure while creating Migrant VSM", str(j)
        time.sleep(10)
        print "Waiting till schedule duration for MIgration to begin"
        user = const.node_username
        pwd = const.node_password
        host1 = const.Node1_IP
        host2 = const.Node2_IP
        vsm_ip = const.VSM1Ip
        time.sleep(10)
        SSH = SSHConnection()
        output = SSH.cbdpctl_Migration(user,pwd,host1,vsm_ip)
        if output[0] == "transferring":
            try:
                GUI.HA_Maintenance(1, "available")
                time.sleep(100)
                output = GUI.Maintenance_table_info()
                if not "...Error" in output[1]:
                    print "Moved Node to maintenance Successfully"
                    log.info("Moved Node to maintenance Successfully")
                else:
                    print "Error in moving to maintenance"
            except Exception as f:
                print "Error: While moving node to maintenance ", str(f)
                log.error("Error: While moving node to maintenance")
                raise

            time.sleep(30)
            out1 = SSH.cbdpctl_Migration(user,pwd,host2,vsm_ip)
            print out1
            bytestransfered = out1[1]
            time.sleep(100)
            out2 = SSH.cbdpctl_Migration(user,pwd,host2,vsm_ip)
            print out2
            cstatus = out2[0]
            cbytestransfered = out2[1]
            if cstatus == "transferring" or int(cbytestransfered) > int(bytestransfered):
                print "Pass: Migration transfer resumed successfully"
                log.info("Pass: Migration transfer resumed successfully")
            elif cstatus == "uptodate":
                    print "Pass: Migration resumed and completed successfully"
                    log.info("Pass: Migration transfer resumed successfully")
            else:
                    print "Fail: Migration resume failed"
                    log.error("Fail: Migration resume failed")
            time.sleep(2)
            GUI.HA_Maintenance(1, "maintenance")
            time.sleep(100)
            if True:
                print "Node moved back to Available successfully"
                log.info("Node moved back to Available successfully")
                time.sleep(30)
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
                print "Exception Occured: While logging into EC"
                print str(e)


if __name__ == '__main__':
    main()

