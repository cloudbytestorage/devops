import paramiko
#import Logging
import os, time


#from error import SSHConnectionError

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

    def createSSHConnection_neg(self, host, username="", pswd=""):
        '''
                  author: Sudarshan
                  :This method is used to SSH without pem file
                  '''

        self._host = host
        self._username = username
        self._pswd = pswd
        self._timeout = 5
        # import time.sleep as sleep
        from time import sleep
        sshcon = paramiko.SSHClient()
        sshcon.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        rtn = sshcon.connect(self._host, username=self._username, key_filename=self._pswd)
        print sshcon
        if sshcon:  # if login attempt returned True
            # self.prompt = self.conn.prompt
            print('Successfully logged into %s via ' % \
                  (self._host))
        else:  # else login attempt returned False
            print('Unsuccessful login to %s via ' % \
                  (self._host))

        sleep(__SCRIPTDELAY__)  # slow script down
        self.connections.append(sshcon)

    def exec_cmd(self,command):
        for conn in self.connections:
            print conn
            stdin, stdout, stderr = conn.exec_command(command)
            data = stdout.read()
            print data
            # logging.debug(data)
            '''
            if 'running' in data:
                self.log.info('logstash service is running as expected')
            else:
                print 'service is not running'
                '''
            return data

    def append_file_mnr(self, cmd):
        '''
                  author: Sudarshan
                  :This method is used to add logs to mnr
                  '''
        self.cmd = cmd
        for conn in self.connections:
            stdin, stdout, stderr = conn.exec_command(cmd)
            # stdin, stdout, stderr = conn.exec_command('echo elasticsearch_index_indexing >> /var/log/elasticsearch/elasticsearch_index_indexing_slowlog.log')
            data = stdout.read()
            self.log.info(data)
            return data

    def executeCommand(self, cmd):
        '''
                  author: Sudarshan
                  :This method is used to execute any commands in SSH session
                  '''
        self.cmd = cmd
        for conn in self.connections:
            stdin, stdout, stderr = conn.exec_command(cmd)
            data = stdout.read()
            self.log.info(data)
            return data

    def deluser(self, username):
        '''
                  author: Sudarshan
                  :This method is used to delete users
                  '''
        for conn in self.connections:
            stdin, stdout, stderr = conn.exec_command('userdel %s' % (username))
            print "User deleted"
            data = stdout.read()
            self.log.info(data)
            return data

    def createuser(self, username, password):
        for conn in self.connections:
            # print username+str(datetime.now())
            cmd_list = 'useradd -m suse'
            stdin, stdout, stderr = conn.exec_command('useradd -m -p %s -s /bin/bash %s' % (password, username))
            print "User added", username
            return username

    def close(self):
        for conn in self.connections:
            conn.close()


def main():
    username = "root"
    password = "test"
    host = "20.10.31.30"
    cmd = "ls"

    filename = os.path.abspath(__file__)

    t = SSHConnection(host=host, username=username, password=password)
    t.createSSHConnection()
    time.sleep(5)
    t.exec_cmd("ls")
    t.close()

if __name__ == '__main__':
    main()

#user="root"
#mySSHK   = r'C:\Users\aarthi\Desktop\nhc-privatekey.pem'
#sshcon   = paramiko.SSHClient()  # will create the object
#sshcon.set_missing_host_key_policy(paramiko.AutoAddPolicy())# no known_hosts error
#sshcon.connect("192.168.232.134", username=user, key_filename=mySSHK) # no passwd needed