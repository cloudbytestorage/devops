#------------------------------------------------------------------------------
#!/usr/bin/env python
#title           :HA_DR.py
#description     :Testing Resumability incase of Gracefull HA.
#note            :These methods are written using EC of P5 1.4.0.1089 build.
#author          :Swarnalatha
#date            :2017/07/29
#version         :1
#usage           :python WebUtils.py
#notes           :
#python_version  :2.7.12
#==============================================================================
from GUIConfig import GuiConfig as const
from SSHConnection import SSHConnection
from WebUtils import WebUtils
import time, os, Logging



def main():

    Url = const.url
    password = const.password
    username = const.username
    filename = os.path.abspath(__file__)
    log = Logging.getLogger(filename, 'HA_DR')
    try:
        log.info("Testing resumability incase of gracefull HA")
        GUI = WebUtils()
        GUI.Enable_Flash()
        GUI.login_EC(Url, username, password)
        try:
            GUI.Create_DR(name=const.DRName, bkp_ip=const.BKPIP)
            print "DR created successfully"
        except Exception as j:
            print "Error: Exception occure while creating DR", str(j)
        time.sleep(20)
        print "Waiting till schedule duration for DR to begin"
        user = const.node_username
        pwd = const.node_password
        host1 = const.Node1_IP
        host2 = const.Node2_IP
        vsm_ip = const.VSM1Ip
        time.sleep(90)
        SSH = SSHConnection()
        output = SSH.cbdpctl_status(user,pwd,host1,vsm_ip)
        #print output
        if output[0] == "transferring":
            try:
                GUI.HA_Maintenance(1, "Available")
                time.sleep(30)
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
            out1 = SSH.cbdpctl_status(user,pwd,host2,vsm_ip)
            print out1
            bytestransfered = out1[1]
            completed = out1[2]
            time.sleep(100)
            out2 = SSH.cbdpctl_status(user,pwd,host2,vsm_ip)
            print out2
            cstatus = out2[0]
            cbytestransfered = out2[1]
            ccompleted = out2[2]
            if cstatus == "transferring" and int(cbytestransfered) > int(bytestransfered):
                print "Pass: DR transfer resumed successfully"
                log.info("Pass: DR transfer resumed successfully")
            elif cstatus == "uptodate":
                    print "Pass: DR resumed and completed successfully"
                    log.info("Pass: DR transfer resumed successfully")
            else:
                    print "Fail: DR resume failed"
                    log.error("Fail: DR resume failed")
            time.sleep(2)
            GUI.HA_Maintenance(1, "Maintenance")
            if True:
                print "Node moved back to Available successfully"
                log.info("Node moved back to Available successfully")

    except Exception as e:
                print "Exception Occured: While logging into EC", str(e)


if __name__ == '__main__':
    main()



