#!/usr/bin/env python
#title           :Networkloss_migration.py
#description     :Testing VSM Migration resumability incase of network loss while data is transferring.
#author          :Swarnalatha
#date            :20171213
#version         :1
#usage           :python Networkloss_migration.py
#notes           :
#python_version  :2.7
#==============================================================================

from SCM2.GUIConfig import GuiConfig as const
from SSHConnection import SSHConnection
from WebUtils import WebUtils
import Logging, time, sys, os
import pyping

def main():
    Url = const.url
    password = const.password
    username = const.username
    filename = os.path.abspath(__file__)
    log = Logging.getLogger(filename, 'Networkloss_DR')
    try:

        log.info("Testing resumability incase of networkloss")
        GUI = WebUtils()
        GUI.Enable_Flash()
        GUI.login_EC(Url, username, password)
        try:
            GUI.Create_MigrantVSM(bkp_ip=const.BKPIP)
            print "Migrant VSM created successfully"
        except Exception as j:
            print "Error: Exception occure while creating Migrant VSM", str(j)
        time.sleep(20)
        print "Waiting till schedule duration for Migrant to begin"
        #GUI.close_browser()
        time.sleep(80)
        user = const.node_username
        pwd = const.node_password
        host1 = const.Node1_IP
        vsm_ip = const.VSM1Ip
        SSH = SSHConnection()
        output = SSH.cbdpctl_Migration(user,pwd,host1,vsm_ip)
        print output
        if output[0] == "transferring":
            try:
                interface = const.interface
                t1 = SSHConnection()
                t1.createSSHConnection(host1,user,pwd)
                time.sleep(10)
                print "Making Vlan interface down to check resumability"
                t1.exec_cmd("ifconfig %s down" % interface)
                bkpip = const.BKPIP
                response = pyping.ping(bkpip)
                if response.ret_code == 0:
                    print("reachable")
                    log.error("Unable to bring down data network")
                else:
                    print("data network is down")
                    log.info("Data network is down")

                time.sleep(30)
                output = t1.cbdpctl_Migration(user,pwd,host1,vsm_ip)
                if output:
                    print "Fail: Migrant transfer is still running after Data N/W loss"
                    log.error("Fail: Migrant transfer is still running after Data N/W loss")
            except Exception as z:
                print "Pass: Migrant transfer did not continue after Data N/W loss"
                log.info("Pass: Migrant transfer did not continue after Data N/W loss")
            try:
                time.sleep(20)
                print  "Making vlan interface Up"
                log.info("Making vlan interface up")
                interface = const.interface
                t1 = SSHConnection()
                t1.createSSHConnection(host1, user, pwd)
                time.sleep(5)
                t1.exec_cmd("ifconfig %s up" % interface)
                print "vlan network is up"
                time.sleep(60)
                output = t1.cbdpctl_Migration(user, pwd, host1, vsm_ip)
                if output:
                    print "pass: Migrant transfer is continuied after making nw interface ip"
                    log.info("pass: Migrant transfer is continuied after making nw interface ip")
                    time.sleep(5)
                    try:
                        GUI.DR_Enable_Disable("Disable")
                        print "Migrant transfer disabled successfully"
                        time.sleep(10)
                        GUI.deleteMigrantVSM()
                        print "Migrant VSM deleted sucessfully"
                        time.sleep(2)
                        GUI.close_browser()
                    except Exception as fi:
                        print "Error: While deleting Migrant VSM "
                        print str(fi)
                        raise
            except Exception as z:
                print "fail: Migrant transfer did not continue after Data N/W UP", str(z)
                log.error("fail: Migrant transfer did not continue after Data N/W UP")
    except Exception as e:
        print "Exception Occured: While logging into EC", str(e)

if __name__ == '__main__':
    main()