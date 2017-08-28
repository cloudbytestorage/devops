import paramiko
import os, time
from GUIConfig import GuiConfig as const


__SCRIPTDELAY__ = .5

class SSHConnection():
    def __init__(self):
        #self._host = host
        #self._username = username
        #self._password = password
        #self._timeout = 5
        #logging.debug('loading default config')
        self.connections = []
        self.filename = os.path.abspath(__file__)


    def createSSHConnection(self,host,username="",password=""):
        self._host = host
        self._username = username
        self._password = password
        self._timeout = 5
        from time   import sleep
        sshcon = paramiko.SSHClient()
        sshcon.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        rtn = sshcon.connect(self._host,username=self._username,password=self._password)
        print sshcon
        if sshcon:    # if login attempt returned True
            #self.prompt = self.conn.prompt
            print('Successfully logged into %s via ' % \
                (self._host))
        else:    # else login attempt returned False
            print('Unsuccessful login to %s via ' % \
                (self._host))

        sleep(__SCRIPTDELAY__)    # slow script down
        self.connections.append(sshcon)

    def exec_cmd(self, command):
        for conn in self.connections:
            print conn
            stdin, stdout, stderr = conn.exec_command(command)
            data = stdout.read()
            print data
            return data

    def cbdpctl_status(self):
        username = const.node_username
        password = const.node_password
        host = const.Node1_IP
        vsm_ip = const.VSM1Ip
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
            o1 = output.split('\n')
            Job = o1[0].split(':')[1]
            instance = o1[1].split(':')[1]
            command = ("jexec %s cbdpctl -c status -i %s -j %s" % (jls_id, instance, Job))
            time.sleep(2)
            validate = t.exec_cmd(command)
            out0 = validate.split('\n')
            status = out0[2].split()[1]
            bytes_transfered = out0[11].split()[1]
            completed = out0[13].split()[1]
            t.close()
            return status,bytes_transfered,completed

        else:
            print "VSM not found"

    def close(self):
        for conn in self.connections:
            conn.close()


def main():
    t = SSHConnection()
    out = t.cbdpctl_status()
    print out

if __name__ == '__main__':
    main()
