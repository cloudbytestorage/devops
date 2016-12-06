from poolUtils import *
from cbrequest import *
from haUtils import *
import time
from time import ctime
import os
config = configFile(sys.argv)
api_key = get_apikey(config)
stdurl = get_url(config, api_key[1])

pool_id = '14d307f7-b2dc-3013-b7cb-9c84e19e865d'
pool_type = 'raidz1'
NODE1_IP = '20.10.96.70'
no_of_disk = 1
disk_type = 'SSD'

def to_replace_disk(pool_type, pool_id,  no_of_disk, disk_type, NODE1_IP):
    list_cntrl = list_controller(stdurl)
    if list_cntrl[0] == 'FAILED':
        return ['FAILED', list_cntrl[1]]
    cntrl_values =  get_controller_info(NODE1_IP, list_cntrl[1])
    if cntrl_values[0] == 'FAILED':
        return ['FAILED' ,cntrl_values[1]]
    disks_avail = getFreeDisk(cntrl_values[6])
    if disks_avail[0] == 'FAILED':
        return ['FAILED',disks_avail[1]]
    diskGroupList =  listDiskGroup(pool_id, stdurl)
    if diskGroupList[0] == 'FAILED':
        return ['FAILED', diskGroupList[1]]
    disk_details = get_value_from_diskGroup(diskGroupList[1], pool_type)
    print disk_details[3]
    if disk_details[0] == 'FAILED':
        return ['FAILED', disk_details[1]]
    shared_disk = listSharedDisk(pool_id, disk_details[3], stdurl)
    if shared_disk[0] == 'FAILED':
        return ['FAILED', shared_disk[1]]
    else:
        #ramdomly taking one disk id for diskgroup list
        for shared_disks in shared_disk[1]:
            pool_disk_id = shared_disks.get('id') #current disk to be replaced
            pool_disk_label = shared_disks.get('disklabel')
            logging.debug('Disk which is going to be replaced is %s: %s', \
                            pool_disk_label, pool_disk_id)
            print pool_disk_label
            break
        disk_list_id = disklistID(disk_details[1], disk_type, no_of_disk,  disks_avail[1])
        if disk_list_id[0] == 'FAILED':
            return ['FAILED', disk_list_id[1]]
        disk_replace = replaceDisk(pool_disk_id, disk_list_id[1], disk_details[3], stdurl)
        if disk_replace[0] == 'FAILED':
            return ['FAILED', disk_replace[1]]
        else:
            return ['PASSED', 'Successfully replaced disk with id "%s" '\
                        'by disk with id "%s"' %(pool_disk_id, disk_list_id[1])]

#cc = to_replace_disk(pool_type, pool_id,  no_of_disk, disk_type, NODE1_IP)
#print cc
'''
node_ip = '20.10.96.70'
while True:
    cmd = 'zpool status Poolz1 | grep "scan\|resilvering"'
    scan = getControllerInfoAppend(node_ip, 'test', cmd, 'results/result.csv')
    print scan
    if 'resilver in progress' in scan:
        print 'resilver of replace disk is happening'
        time.sleep(120)
        continue
    else:
        print 'resilvering completed'
        break
'''
grp_type = 'log_mirror'
disk = 'SS'
if grp_type in  ('spare' , 'vdev') :
    print grp_type
else:
    if grp_type in ('cache', 'log', 'log mirror', 'log_mirror') :
        if disk == 'SSD':
            print grp_type
        else:
            print 'Need ssd'

group_type = 'cache'
if group_type in ('cache', 'log', 'log mirror', 'log_mirror'):
    print group_type
