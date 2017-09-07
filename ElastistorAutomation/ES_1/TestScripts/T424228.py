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
    host = "20.10.31.30"
    vsm_ip = "16.10.92.203"
    mount_point = "TestVolfghij1234567890_CB5112345"
    t = SSHConnection(host=host, username=username, password=password)
    t.createSSHConnection()
    time.sleep(5)
    out = t.exec_cmd("jls")
    out1 = out.split()
    if vsm_ip in out1:
        jls = out1.index(vsm_ip)
        jls_id = int(out1[jls-1])
        output = t.exec_cmd(("jexec %s ls /%s/.zfs/snapshot" % (jls_id, mount_point)))
        o1 = output.split('\n')
        command = ("jexec %s ls /%s/.zfs/snapshot/%s" % (jls_id, mount_point, o1[0]))
        print command
        time.sleep(2)
        validate = t.exec_cmd(command)
        error = "File name too long"
        if error in validate:
            print "IO error occured"
        else:
            print "Able to access .zfs mount point"
    else:
        print "Str not found"
    time.sleep(2)
    t.close()

if __name__ == '__main__':
    main()
