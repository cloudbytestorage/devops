# s6.py
#!/usr/bin/python
import os, subprocess, sys, argparse

def check_arg(args=None):
    parser = argparse.ArgumentParser(description='Script to learn basic argparse')
    parser.add_argument('-H', '--host',
                        help='host ip',
                        required='True',
                        default='localhost')
    parser.add_argument('-u', '--user',
                        help='user name',
                        default='root')
    parser.add_argument('-i', '--file1',
                        help='user name',
                        default='file.txt')


    return parser.parse_args(args)

def remote_run(arguments):
    host = arguments.host
    user = arguments.user
    file1 = arguments.file1
    cmd_list = []
    with open('commands.txt', 'rb') as f:
        for c in f:
            cmd_list.append(c.replace('\n','').replace('\r','').rstrip())

    exe = {'py':'python', 'sh':'sh', 'pl':'perl'}

    ssh = ''.join(['ssh -i',' ', file1 ,' ' ,user, '@',  host, ' '])
    print ssh
    for cmd in cmd_list:
        type = exe[cmd.split('.')[1]]
        cmd = ssh + type + ' < ' + cmd + '>> mylogs.txt 2>&1'
        os.system(cmd)

if __name__ == '__main__':
    args = check_arg(sys.argv[1:])
    remote_run(args)
