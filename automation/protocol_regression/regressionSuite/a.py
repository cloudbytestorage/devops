from cbrequest import getoutput

def mountPointDetails(mount_dir):
    cmd = 'df -m | grep %s | awk {\'print $2\'}' %(mount_dir)
    used = str(getoutput(cmd))
    used = (used[2:-4])
    return used

Used = mountPointDetails('createDliSCSI1')
print Used
