# copy this file inside vdbench directory than only it will execute

# """ import statements for required modules """

import os
import sys
import time
import argparse
import subprocess

sleep_time = 2

# creating object for argument parser
parser = argparse.ArgumentParser()

# assigning defination for required paramaters
parser.add_argument("--vsms_ip", nargs='+', help="give vsms ip with space separated as parameter")

# assigning required parameters to args
args = parser.parse_args()
vsms_ip = args.vsms_ip

def execute_cmd_to_local_box(command):
    """ executing a shell command at local client """

    link = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, \
            stderr=subprocess.PIPE, close_fds=True)
    return

def execute_cmd_to_local_box_with_output(command):
    """ executing a shell command at local client with output """
    
    link = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, \
            stderr=subprocess.PIPE, close_fds=True)
    ldata = link.stdout.readlines()
    output, errors = link.communicate()
    rco = link.returncode
    try:
        if ldata == []:
            output = ['BLOCKED', '']
        else:
            output = ['PASSED', ldata]
    except:
        output = ['FAILED', errors]
    return output

def get_all_nfs_shares_of_all_vsms():
    """ creating a list with all the mountpoint of nfs shares """
    
    shares = []
    for vsm_ip in vsms_ip:
        # getting all the NFS shares for the given vsm_ip
        command = "showmount -e %s | cut -d ':' -f 2 | cut -d ' ' -f 1 | awk 'NF {print $1}'" %(vsm_ip)
        nfs_shares = execute_cmd_to_local_box_with_output(command)

        if nfs_shares[0] == 'BLOCKED':
            print 'There is no NFS share to access at the given server %s' %(vsm_ip)
            exit()
        elif nfs_shares[0] == 'FAILED':
            print 'Not able to get mount_point, error is: %s' %(nfs_shares[1])
            exit()
        else:
            print 'Following NFS shares are present at VSM with IP %s: %s' \
                    %(vsm_ip, nfs_shares[1])
            nfs_shares = nfs_shares[1]

        # removing the new line from showmount command and adding mountpoint to shares list
        for mount_point in nfs_shares:
            mount_point =  mount_point.strip('\n')
            shares.append(mount_point)
    
    return shares

def mount_nfs_shares():
    """ creating directory and mounting all the NFS share """
    
    for vsm_ip in vsms_ip:
        # command for showmount, create directory and mount the NFS share
        command = "showmount -e %s | cut -d ':' -f 2 | cut -d ' ' -f 1 | awk 'NF {system(\"mkdir -p /mnt\"$1); system(\"mount -o mountproto=tcp,sync,nolock %s:\"$1 \" /mnt\"$1)}'" %(vsm_ip, vsm_ip)
    
        # executing command to mount NFS share
        execute_cmd_to_local_box(command)

def get_vdbench_config_file(mnt_points_at_client):
    """ creating a vdbench config file for all the mounted NFS shares """

    # creating a nfsVDConfig file for newly updated values
    with open("nfsVDConfig", "a") as cfFile:
        j = 1
        for client_mnt_point in mnt_points_at_client:
            sdLine = 'fsd=fsd%s,anchor=%s,depth=1,width=1,files=1,size=2G' %(j, client_mnt_point) + '\n'
            cfFile.writelines(sdLine)
            j = j + 1
        wdLine = 'fwd=fwd1,fsd=fsd*,xfersize=4k,rdpct=80,fileio=random,threads=1' + '\n'
        cfFile.writelines(wdLine)
        rdLine = 'rd=rd1,fwd=fwd*,elapsed=5000000,interval=1,fwdrate=max,format=yes' + '\n'
        cfFile.writelines(rdLine)
    vdConfigFile = "nfsVDConfig"
    return vdConfigFile
    
def get_client_side_mount_point():
    """ getting client side mountpoits """

    mnt_points_at_client = []
    for vsm_ip in vsms_ip:
        command = "mount | grep %s | awk {'print $3'}" %(vsm_ip)
        client_mnt_points = execute_cmd_to_local_box_with_output(command)
        if client_mnt_points[0] == 'PASSED':
            client_mnt_points = client_mnt_points[1]
            #mnt_points_at_client.append(client_mnt_points[1])
            for client_mnt_point in client_mnt_points:
                client_mnt_point =  client_mnt_point.strip('\n')
                mnt_points_at_client.append(client_mnt_point)
        else:
            print 'Not able to get client mount points'
            exit()
    return mnt_points_at_client

def verify_mount(nfs_shares, mnt_points_at_client):
    """ verifying the mount for all the NFS shares """

    for mount_point in nfs_shares:
        if mount_point in str(mnt_points_at_client):
            continue
        else:
            mount_check = False
            print 'NFS share with mount point %s is not mounted' %(mount_point)
            print 'umounting the mounted NFS shares and exiting...'
            #have to write code for umount as some of the nfs share are already mounted
            exit()
# -------------------------------------------------------------------------------------


# nfs_shares is list of all the NFS volumes from all the given vsms
nfs_shares = get_all_nfs_shares_of_all_vsms()
print '\nTotal NFS shares are going to be mount', nfs_shares

# molunt all the NFS shares
mount_nfs_shares()

# after mounting the NFS shares it will take some time to show in mount command
time.sleep(sleep_time)

# getting the mounted directory from client for mounted NFS shares
mnt_points_at_client = get_client_side_mount_point()

# verifying mount for all the NFS shares from all the VSMs
verify_mount(nfs_shares, mnt_points_at_client)

print '\nAll the NFS shares are mounted succeffully'
print 'Following are the client mount points: ', mnt_points_at_client

# removing the conf file if it exits
os.system('rm -rf nfsVDConfig')

# get the vdbench config file
vdConfigFile = get_vdbench_config_file(mnt_points_at_client)

# executing vdbench
out = os.system('./vdbench -f %s -o %s '%(vdConfigFile, 'output'))
