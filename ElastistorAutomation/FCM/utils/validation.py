import paramiko
import os, time

__SCRIPTDELAY__ = .5

class SSHConnection():
    def __init__(self,host,username="",password=""):
        self._host = host
        self._username = username
        self._password = password
        self._timeout = 5
        #logging.debug('loading default config')
        self.connections = []
        self.filename = os.path.abspath(__file__)


    def createSSHConnection(self):
        #import time.sleep as sleep
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

    def close(self):
        for conn in self.connections:
            conn.close()


def main():
    username = "root"
    password = "test"
    host = "20.10.31.31"
    vsm_ip = "16.10.92.203"
    mount_point = "Accounthij1234567890CB1Abcdefghi"
    filename = os.path.abspath(__file__)

    t = SSHConnection(host=host, username=username, password=password)
    t.createSSHConnection()
    time.sleep(5)
    out = t.exec_cmd("jls")
    out1 = out.split()
    if vsm_ip in out1:
        jls = out1.index("16.10.92.203")
        jls_id = int(out1[jls-1])
        output = t.exec_cmd("jexec %s /%s/.zfs/snapshot" % (jls_id, mount_point))
        o1 = output.split('\n')
        print o1[0]
        validate = t.exec_cmd("jexec %s /%s/.zfs/snapshot/%s" % (jls_id, mount_point,o1[0]))
        error = "Input/Output Error"
        if error in validate:
            print "IO error occured"
        else:
            print "Able to access .zfs mount point"
    else:
        print "Str not found"
    time.sleep(2)
    #t.exec_cmd1("jexec 8 tcsh")
    t.close()

if __name__ == '__main__':
    main()
