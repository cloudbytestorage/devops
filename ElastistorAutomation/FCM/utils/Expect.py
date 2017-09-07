import pexpect
import re

class ssh_Handle:
    #This is to get SSH handle using pem file
    def __init__(self,pem_File,Host_IP):
        self.pem_File = pem_File
        self.IP = Host_IP
        self.command = 'ssh -o "StrictHostKeyChecking no" -i '+self.pem_File+' '+self.IP
        self.Handle = pexpect.spawn(self.command)
        #ADD the exceptions here
        self.prompt = '.*#'
        self.Handle.expect(self.prompt)

    def run_Command(self, command):
        self.command = command
        self.Handle.sendline(self.command)
        self.Handle.expect(self.prompt)
        out = self.Handle.after
        list_out = out.split(self.command)
        string = "\n".join(list_out)
        #string.replace(self.prompt,'')
        string = re.sub(self.prompt,string)
        return string
    def close_Connection(self):
        print('\nClosing the Connection')
        self.Handle.close()


class handle_SSH:
    #This is to get ssh handle using user name and password
    def __init__(self,host_IP, host_User, host_Password):
        self.IP = host_IP
        self.User = host_User
        self.Password = host_Password
        self.command = 'ssh -o \"StrictHostKeyChecking no\" '+self.User+'@'+self.IP
        #print self.command
        self.Handle = pexpect.spawn(self.command)
        self.Prompt = '.*#'
        #self.Handle.expect('Password:\s')
        # #print self.Handle.readafter
        self.Handle.expect('\w+')
        out = self.Handle.after
        if (out == 'Password' or out == 'Warning'):
            self.Handle.sendline(self.Password)
            self.Handle.expect(self.Prompt)
        else:
            self.Handle.expect(self.Prompt)

    def run_Command(self, command):
        self.command = command
        self.Handle.sendline(self.command)
        self.Handle.expect(self.Prompt)
        out = self.Handle.after
        list_out = out.split(self.command)
        string = "\n".join(list_out)
        # string.replace(self.prompt,'')
        string = re.sub(self.Prompt, '', string)
        return string

    def close_Connection(self):
        print('\nClosing the Connection')
        self.Handle.close()
