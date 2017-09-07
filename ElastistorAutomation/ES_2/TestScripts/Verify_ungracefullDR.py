from ES_2.GUIConfig import GuiConfig as const
from SSHConnection import SSHConnection
from WebUtils import WebUtils
import time, sys, Logging, os

def main():
    Url = const.url
    password = const.password
    username = const.username
    filename = os.path.abspath(__file__)
    log = Logging.getLogger(filename, 'UngracefullHA_DR')
    try:
        user = const.node_username
        pwd = const.node_password
        host2 = const.Node2_IP
        vsm_ip = const.VSM1Ip
        SSH = SSHConnection()
        time.sleep(130)
        out1 = SSH.cbdpctl_status(user, pwd, host2, vsm_ip)
        print out1
        bytestransfered = out1[1]
        time.sleep(50)
        out2 = SSH.cbdpctl_status(user, pwd, host2, vsm_ip)
        print out2
        cstatus = out2[0]
        cbytestransfered = out2[1]
        if cstatus == "transferring" and int(cbytestransfered) > int(bytestransfered):
            print "Pass: DR transfer resumed successfully"
            log.info("Pass: DR transfer resumed successfully")
        elif cstatus == "uptodate":
            print "Pass: DR resumed and completed successfully"
            log.info("Pass: DR resumed and completed successfully")
        else:
            print "Fail: DR resume failed"
            log.error("Fail: DR resume failed")
        time.sleep(60)
        GUI = WebUtils()
        GUI.login_EC(Url,username,password)
        GUI.HA_Maintenance(1,"Maintenance")
        if True:
            log.info("Moved Node to available state")
        else:
            log.warning("Move the Node to available state")
    except Exception as e:
        log.error("Exception:TC: Verify ungracefullDR"),str(e)
if __name__ == '__main__':
    main()
