#------------------------------------------------------------------------------
#!/usr/bin/env python
#title           :SSHConnection.py
#description     :These methods will help to perform remote ssh functions.
#note            :These methods are written using EC of P5 1.4.0.1089 build.
#author          :Sudarshan Darga
#date            :2017/07/26
#version         :1
#usage           :python SSHConnection.py
#notes           :
#python_version  :2.7.12
#==============================================================================

import paramiko
import os, time, subprocess, re
from ES_1.GUIConfig import GuiConfig as const


__SCRIPTDELAY__ = .5

class SSHConnection():
    def __init__(self):
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
        if sshcon:
            print('Successfully logged into %s via ' % \
                (self._host))
        else:
            print('Unsuccessful login to %s via ' % \
                (self._host))

        sleep(__SCRIPTDELAY__)
        self.connections.append(sshcon)

    def exec_cmd(self, command):
        for conn in self.connections:
            print conn
            stdin, stdout, stderr = conn.exec_command(command)
            data = stdout.read()
            print data
            return data

    def network_down(self, username, password, host, interface):
        t = SSHConnection()
        t.createSSHConnection(host=host, username=username, password=password)
        time.sleep(5)
        user = const.node_username
        pwd = const.node_password
        host1 = const.Node1_IP
        interface = const.interface
        out = t.exec_cmd("ifconfig %s down" % interface)

    def cbdpctl_status(self,username,password,host,vsm_ip):
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

    def check_Ping(self,ip):
        ps = subprocess.Popen(['ping', ip, '-c', '1'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
        out = ps.communicate()[0]
        regex = re.compile('ttl' + r'=(\d+)')
        match = regex.findall(out)
        try:
            if (match[0] != 0):
                return True
        except IndexError as e:
            return False

    def SSHthread(self,host,username="",password="",command=""):
        self._host = host
        self._username = username
        self._password = password
        self._timeout = 5
        from time   import sleep
        sshcon = paramiko.SSHClient()
        sshcon.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        rtn = sshcon.connect(self._host,username=self._username,password=self._password)
        print sshcon
        if sshcon:
            print('Successfully logged into %s via ' % \
                (self._host))
        else:
            print('Unsuccessful login to %s via ' % \
                (self._host))

        sleep(__SCRIPTDELAY__)
        self.connections.append(sshcon)
        for conn in self.connections:
            print conn
            stdin, stdout, stderr = conn.exec_command(command)
            data = stdout.read()
            print data
            conn.close()
            return data

    def close(self):
        for conn in self.connections:
            conn.close()

