import os
import sys
import time
import json
import logging
import subprocess
from itertools import groupby
from cbrequest import sendrequest, queryAsyncJobResult
from volumeUtils import get_params, get_querycommand
from haUtils import list_controller, get_controller_info, get_value, get_node_IP

def get_pool_default_params():
    pool_def_params = {'name': '', 'siteid': '', 'clusterid': '', \
            'controllerid': '', 'latency': 3, 'iops': 5000, \
            'graceallowed': 'true', 'diskslist': '', 'grouptype': '',\
            'sectorsize': 0, 'scsireserved': 'true'}
    return pool_def_params

def listPool(stdurl):
    querycommand = 'command=listHAPool'
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API for Listing pool: %s', str(rest_api))
    resplistPool = sendrequest(stdurl, querycommand)
    data = json.loads(resplistPool.text)
    logging.debug('response for Listing Pool: %s', str(data))
    if 'hapool' in str(data['listHAPoolResponse']):
        pools = data['listHAPoolResponse']['hapool']
        result = ['PASSED', pools]
        logging.debug('Result of Listing Pool: %s', result)
        return result
    elif not 'errorcode' in str(data['listHAPoolResponse']):
        errormsg = 'There is no pool'
        result = ['BLOCKED', 'There is no pool to list']
        logging.error('Not able to List Pool due to: %s', errormsg)
        return result
    else:
        errormsg = str(data['listHAPoolResponse'].get('errortext'))
        result = ['FAILED', errormsg]
        logging.error('Not able to List Pool due to: %s', errormsg)
        return result

def get_pool_info(list_pool, pool_name):
    for pool in list_pool:
        if pool_name is None:
            pool_id = pool.get('id')
            pool_size = pool.get('currentTotalSpace')
            pool_iops = pool.get('totaliops')
            result = ['PASSED', pool_id, pool_size, pool_iops]
            return result
        if pool_name == pool.get('name'):
            pool_id = pool.get('id')
            pool_size = pool.get('currentTotalSpace')
            pool_iops = pool.get('totaliops') 
            result = ['PASSED', pool_id, pool_size, pool_iops]
            return result
    else:
        result = ['FAILED', 'Not able to find the pool']
        return result

def listPoolWithID(pool_id, stdurl):
    logging.info('Inside the list pool with id method...')
    querycommand = 'command=listHAPool&id=%s' %(pool_id)
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API for listing Pool with ID: %s', str(rest_api))
    resp_listPool = sendrequest(stdurl, querycommand)
    data = json.loads(resp_listPool.text)
    logging.debug('response for listing pool wit ID: %s', str(data))
    if 'errorcode' in str(data):
        errormsg = str(data['listHAPoolResponse'].get('errortext'))
        print errormsg
        result = ['FAILED', errormsg]
        logging.error('Not able to list pool with ID due to: %s', errormsg)
        return result
    elif 'hapool' in str(data['listHAPoolResponse']):
        pools = data['listHAPoolResponse']['hapool']
        result = ['PASSED', pools]
        return result
    else:
        print 'There is no pool'
        result = ['BLOCKED', 'There is no pool for given id to list']
        return result

        
def listPoolWithControllerId(stdurl, controller_id):
    querycommand = 'command=listHAPool&controllerid=%s' %(controller_id)
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API for Listing pool: %s', str(rest_api))
    resp_listPool = sendrequest(stdurl, querycommand)
    data = json.loads(resp_listPool.text)
    logging.debug('response for Listing Pool: %s', str(data))
    if 'hapool' in str(data['listHAPoolResponse']):
        pools = data['listHAPoolResponse']['hapool']
        result = ['PASSED', pools]
        logging.debug('Result of Listing Pool: %s', result)
        return result
    elif not 'errorcode' in str(data['listHAPoolResponse']):
        errormsg = 'There is no pools'
        result = ['BLOCKED', 'There is no pool to list']
        logging.error('Not able to List Pool due to: %s', errormsg)
        return result
    else:
        errormsg = str(data['listHAPoolResponse'].get('errortext'))
        result = ['FAILED', errormsg]
        logging.error('Not able to List Pool due to: %s', errormsg)
        return result

###result = cntrl_disks
def getFreeDisk(result):
    logging.info('inside getFreeDisk method...')
    disklist = []
    dict = {}
    for disk  in result:
        if 'usage' in disk:
            if disk["usage"] == 'not-used':
                dict["writecacheenabled"] = disk["writecacheenabled"]
                dict["size"] = disk["size"]
                dict["type"] = disk["type"]
                dict["label"] = disk["label"]
                dict["id"] = disk["id"]
                disklist.append(dict.copy())
    if disklist == []:
        return ['FAILED', 'No free disks available']
    logging.debug('Free disks are %s', disklist) 
    return ['PASSED', disklist]

##Use this method for pool creation and for adding /cache/log/log mirror
def getDiskToAllocate(free_disks, num_of_disk, disk_type):
    disk_type = disk_type.upper()
    logging.info('inside getDiskToAllocate method...')
    final_disk = []
    final_size = []
    count = 0
    i = 0
    if num_of_disk == 0:
        return ['FAILED', 'Number of disk to create pool cant be zero, '\
                        'please provide vaild data']

    for p_disk in free_disks:
        if p_disk['type'] == disk_type:
            disk_size = p_disk['size']
            final_size.append(disk_size)
    
    #C = Counter(final_size) # this can be used if python supports Counter from collections module
    #group = [ [k,]*v for k,v in C.items()]
    group = [list(j) for i, j in groupby(final_size)] #using groupby from itertools fn
    grp_len = len(list(group))
    for i in range(0, grp_len):
        p = len(list(group[i]))
        if int(p == num_of_disk):
            group = group[i]
            break
        else:
            if int(p) >= int(num_of_disk):
                group = group[i]
                break
    else:
        if group == []:
            msg = 'Not able to find the disk of given disk type: "%s"' %disk_type
            return ['FAILED', msg]
        if p < num_of_disk:
            msg = 'Insufficient disks to create pool'
            return ['FAILED', msg]
    
    for disk in free_disks:
        if count == num_of_disk:
            break
        if group[0] == disk['size']:
            disk_id = disk['id']
            final_disk.append(disk_id)
            count = count + 1
        
    final_disk = list(set(final_disk))
    allocation_disk = '%3B'.join(final_disk)
    result =['PASSED', allocation_disk]
    logging.debug('Disk to be allocated are %s', result)
    return result

def create_pool(user_params, stdurl):
    logging.info('inside create_pool method...')
    command = 'command=addHAPool' 
    logging.info('getting defaults parameters for create pool...')
    pool_def_params = get_pool_default_params()
    logging.debug('defaults parameters for create pool: %s', str(pool_def_params))
    logging.info('getting final parametrs for creating pool...')
    pool_params = get_params(pool_def_params, user_params)
    logging.info('final parametrs for creating pool: %s', str(pool_params))
    querycommand = get_querycommand(command, pool_params, 'pool')
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API for creating pool: %s', str(rest_api))
    resp_createPool = sendrequest(stdurl, querycommand)
    data = json.loads(resp_createPool.text)
    logging.debug('response for create Pool: %s', str(data))
    if 'errorcode' in str(data):
        errormsg = str(data['addHAPoolResponse'].get('errortext'))
        logging.error('Not able to create pool due to: %s', errormsg)
        result = ['FAILED', errormsg]
        return result
    logging.info('getting create pool job id...')
    job_id = data['addHAPoolResponse']['jobid']
    logging.debug('create pool job id: %s', job_id)
    logging.info('calling queryAsyncJobResult method...')
    create_pool_status = queryAsyncJobResult(stdurl, job_id)
    logging.debug('create_pool_status: %s', create_pool_status)
    if create_pool_status[0] == 'PASSED':
        result = ['PASSED', 'Pool created successfuly']
    else:
        result = ['FAILED', create_pool_status]
    logging.debug('result of create_pool: %s', str(result))
    return result

##result : result of listpoolwithID
def get_pool_properties(result):
    if result[0] == 'PASSED':
        iops = result[1][0].get('totaliops')
        grace = result[1][0].get('graceallowed')
        dedup = result[1][0].get('deduplication')
        failover = result[1][0].get('ispooltakeoveronpartialfailure')
        backend_throttle = result[1][0].get('penaltyenforcementfactor')
        multiplication_factor = result[1][0].get('readmultiplicationfactor')
        avg_blk_size = result[1][0].get('avgblocksize')
        result = [iops, grace, dedup, failover, backend_throttle,\
                multiplication_factor, avg_blk_size]
        return result
    else:
        return ['FAILED', 'Not able to get pool properties']

def pool_default_properties():
    pool_def_prpts = {'graceallowed': 'true', 'deduplication' : 'off',\
            'ispooltakeoveronpartialfailure': 'true', \
            'penaltyenforcementfactor' : 'no', 'readmultiplicationfactor': 4 \
            ,'avgblocksize': 4}
    return pool_def_prpts

def pool_updated_properties(result):
    pool_updated_prpts = {'graceallowed': result[1], 'deduplication' : result[2],\
            'ispooltakeoveronpartialfailure': result[3], \
            'penaltyenforcementfactor' : result[4], \
            'readmultiplicationfactor': result[5], 'avgblocksize': result[6]}
    return pool_updated_prpts

def modify_prpts_params(pool_def_prpts, pool_updated_prpts):
    for key in pool_updated_prpts:
        if key in pool_def_prpts:
            pool_def_prpts [key] = pool_updated_prpts[key]
    else:
        new_list =  dict(pool_updated_prpts.items() + pool_def_prpts.items())
    return new_list

###edit pool proreties
###pool properties : iops, grace, dedup, partial_failover, backend_throttling, \
##        multiplication_factor, avg_blk_size
# prpts stands for properties
def editPoolProperties(pool_id, prpts, prptsValue, stdurl):
    if prpts.lower() in ('iops'):
        pool_prpts_param = {'totaliops': prptsValue, \
                'totalthroughput': int(prptsValue)*128}
    elif prpts.lower() in ('grace'):
        if prptsValue.lower() == 'true' or prptsValue.lower() == 'false':
            pool_prpts_param = {'graceallowed': prptsValue} #'deduplication': 'off'}
        else:
            result = ['FAILED', 'Please specify "true" or "false" for grace']
            return result
    elif prpts.lower() in ('deduplication'):
        if prptsValue.lower() == 'on' or prptsValue.lower() == 'off':
            pool_prpts_param = {'deduplication': prptsValue}
        else:
            result = ['FAILED', 'Please specify "on" or "off" for deduplication']
            return result
    elif  prpts.lower() in ('partial_failover'):
        if prptsValue.lower() == 'true' or prptsValue.lower() == 'false':
            pool_prpts_param = {'ispooltakeoveronpartialfailure': prptsValue}
        else:
            result = ['FAILED', 'Please specify "true" or "false" '\
                    'for partial failover']
            return result
    elif prpts.lower() in ('backend_throttling'):
        if prptsValue.lower() == 'yes' or prptsValue.lower() == 'no':
            pool_prpts_param = {'penaltyenforcementfactor': prptsValue}
        else:
            result = ['FAILED', 'Please specify "yes" or "no" '\
                    'for backend throttling']
            return result
    elif prpts.lower() in ('read_multiplication_factor'):
        value_range = ['1', '2', '3', '4', '5', '6', '7', '8']
        if prptsValue in value_range:
            pool_prpts_param = {'readmultiplicationfactor': prptsValue}
        else:
            result = ['FAILED', 'Value should be in range of "1 to 8"'\
                    'for read multiplication factor']
            return result
    elif prpts.lower() in ('average_block_size'):
        blk_range = ['4', '8', '16', '32', '64', '128', '256', '512', '1024']
        if prptsValue in blk_range:
            pool_prpts_param = {'avgblocksize': prptsValue}
        else:
            result = ['FAILED', 'Blk range should be in any of these %s ' %blk_range]
            return result
    else:
        result = ['FAILED', 'Given property does not exists..']
        return result

    poolList = listPoolWithID(pool_id, stdurl)
    if poolList[0] == 'FAILED':
        return ['FAILED', poolList[1]]
    prpts_value = get_pool_properties(poolList)
    if prpts_value[0] == 'FAILED':
        return ['FAILED', prpts_value[1]]
    #pool_def_prpts = pool_default_properties()
    #print 'default :%s' %pool_def_prpts
    pool_updated_prpts = pool_updated_properties(prpts_value)
    print 'updated:%s' %pool_updated_prpts
    #new_prpts_params = modify_prpts_params(pool_def_prpts, pool_updated_prpts)
    #print 'combine of default & updated :%s' %new_prpts_params
    final_prpts_params = modify_prpts_params(pool_updated_prpts, pool_prpts_param)
    print 'Final : %s' %final_prpts_params
    command = 'command=updateHAPool&id=%s' %(pool_id)
    querycommand = form_querycommand(command, final_prpts_params)
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API for editing pool property: %s', str(rest_api))
    edit_poolProp = sendrequest(stdurl, querycommand)
    data = json.loads(edit_poolProp.text)
    logging.debug('response for editing pool %s: %s', prpts, str(data))
    if 'errorcode' in str(data):
        errormsg = str(data['updateHAPoolResponse'].get('errortext'))
        print errormsg
        logging.error('%s', errormsg)
        result = ['FAILED', errormsg]
        return result
    else:
        result = ['PASSED', 'Successfully updated pool property']
        return result

def listDiskGroup(pool_id, stdurl):
    logging.info('inside list disk group method..')
    querycommand = 'command=listDiskGroup&poolid=%s' %pool_id
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API for listing disk group: %s', str(rest_api))
    resp_listDisk = sendrequest(stdurl, querycommand)
    data = json.loads(resp_listDisk.text)
    logging.debug('response for listing disk group: %s', str(data))
    if 'errorcode' in str(data):
        errormsg = str(data['listDiskGroupResponse'].get('errortext'))
        print errormsg
        result = ['FAILED', errormsg]
        logging.error('Not able  list disk group: %s', errormsg)
        return result
    else:
        diskGroup = data['listDiskGroupResponse']['diskgroup']
        result = ['PASSED', diskGroup]
        return result

###grouptype = pool_type/spare/cache/log/log_mirror and so on
def get_value_from_diskGroup(diskGroupList, grouptype):
    if '_' in grouptype:
        grouptype = grouptype.replace('_' , ' ')
    for diskGrp in diskGroupList:
        grp_type = diskGrp.get('type')
        if str(grouptype) == str(grp_type):
            disk_grp_id = diskGrp.get('id')
            disk_size = diskGrp['diskList'][0].get('size')
            type_of_disk =diskGrp['diskList'][0].get('type')
            return ['PASSED', disk_size, type_of_disk, disk_grp_id]
    else:
        return ["FAILED", 'Not able to get disk group details']

def listSharedDisk(pool_id, disk_grp_id, stdurl):
    logging.info('inside list shared disk  method..')
    querycommand = 'command=listSharedDisk&diskgroupid=%s&poolid=%s' \
            %(disk_grp_id, pool_id)
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API for listing Shared disk: %s', str(rest_api))
    sharedDisk_list = sendrequest(stdurl, querycommand)
    data = json.loads(sharedDisk_list.text)
    logging.debug('response for listing Shared disk: %s', str(data))
    if 'errorcode' in str(data):
        errormsg = str(data['listSharedDiskResponse'].get('errortext'))
        print errormsg
        result = ['FAILED', errormsg]
        logging.error('Not able list Shared disk: %s', errormsg)
        return result
    else:
        sharedDisk = data['listSharedDiskResponse']['shareddisk']
        result = ['PASSED', sharedDisk]
        return result

def changeDiskState(sharedDisk_id, state, disk_grp_id, stdurl):
    querycommand = 'command=changeDiskState&shareddiskid=%s&state=%s&id=%s'\
            %(sharedDisk_id, state, disk_grp_id)
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API for changing disk state: %s', str(rest_api))
    disk_state = sendrequest(stdurl, querycommand)
    data = json.loads(disk_state.text)
    logging.debug('response for changing disk state: %s', str(data))
    if 'errorcode' in str(data):
        errormsg = str(data['changeDiskStateResponse'].get('errortext'))
        print errormsg
        result = ['FAILED', errormsg]
        logging.error('Not able change disk state: %s', errormsg)
        return result
    else:
        result = ['PASSED', 'Successfully changed the disk state']
        return result

def replaceDisk(curr_disk_id, new_disk_id, disk_grp_id, stdurl):
    querycommand = 'command=replaceDisk&currentdiskid=%s&newdiskid=%s&id=%s' \
            %(curr_disk_id, new_disk_id, disk_grp_id)
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API for replacing disk : %s', str(rest_api))
    disk_replace = sendrequest(stdurl, querycommand)
    data = json.loads(disk_replace.text)
    logging.debug('response for replacing disk state: %s', str(data))
    if 'errorcode' in str(data):
        errormsg = str(data['replaceDiskResponse'].get('errortext'))
        print errormsg
        result = ['FAILED', errormsg]
        logging.error('Not able replace disk: %s', errormsg)
        return result
    else:
        result = ['PASSED', 'Successfully replaced disk']
        return result

###getting few parameter value from list disk group
###disktype = SSD/SAS/SATA
###use this method for adding Disk group that shd be equal or greater than the pool size
##like spare/vdev
def disklistID(disk_size, type_of_disk, num_of_disk, disks):
    count = 0
    final_size = []
    disk_list_id = []
    disk_type_list = []
    i = 0
    if num_of_disk == 0:
        return ['FAILED', 'Number of disk to create disk group cant be zero, '\
                'please provide vaild data']

    for disk in disks:
        if disk['type'] == type_of_disk :
            disk_type_list.append(disk['type'])
            if disk_size >= disk['size']: 
                disks_size = disk['size']
                final_size.append(disks_size)
    
    if disk_type_list == []:
        msg = 'Not able to find the disk of given disk type: "%s"' %type_of_disk
        return ['FAILED', msg]
       
    #C = Counter(final_size) # this can be used if python supports Counter from collections module
    #group = [[k,]*v for k,v in C.items()] 
    group = ([list(j) for i, j in groupby(final_size)]) #using groupby from itertools fn
    grp_len = len(list(group))
    for i in range(0, grp_len):
        p = len(list(group[i]))
        if group[i][0] == disk_size and p >= num_of_disk:
            group = group[i]
            break
        else:
            if float(group[i][0]) > float(disk_size) and p >= num_of_disk:
                group = group[i]
                break
    else:
        if (final_size and group) == []:
            msg = 'Not able to find the disk of size greater or equal to '\
                    'that of given size "%s"' %disk_size
            return ['FAILED', msg]
        if p < num_of_disk:
            msg = 'Insufficient disks to add disk group'
            return ['FAILED', msg]
    
    for new_disk in disks:
        if count == num_of_disk:
            break
        if group[0] == new_disk['size']:
            disk_id = new_disk['id']
            disk_list_id.append(disk_id)
            count = count + 1

    disk_list_id = list(set(disk_list_id))
    allocation_disk = '%3B'.join(disk_list_id)
    result =['PASSED', allocation_disk]
    logging.debug('Disk to be allocated are %s', result)
    return result

###Group = spare/cache/log/log_mirror
###metavdevs : meta_mirror/meta_raidz1/meta_raidz2/meta_raidz3
###sector size = 4096/512/0
def addDiskGroup(pool_id, clstr_id, group, disk_list, sctr_size, stdurl):
    #if group.lower() == 'log_mirror':
     #   group = 'log%20mirror'
    if '_' or ' ' in group:
        group = group.replace('_', '%20').replace(' ' , '%20')
    logging.info('inside addDiskGroup method..')
    querycommand = 'command=addDiskGroup&poolid=%s&clusterid=%s&'\
        'grouptype=%s&diskslist=%s&sectorsize=%s' \
        %(pool_id, clstr_id, group, disk_list, sctr_size)
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API adding Disk group: %s', str(rest_api))
    add_diskGroup = sendrequest(stdurl, querycommand)
    data = json.loads(add_diskGroup.text)
    logging.debug('response for adding disk group: %s', str(data))
    if 'errorcode' in str(data):
        errormsg = str(data['addDiskgroupResponse'].get('errortext'))
        print errormsg
        result = ['FAILED', errormsg]
        logging.error('Not able to add disk group due to: %s', errormsg)
        return result
    logging.info('getting add disk group job id...')
    job_id = data['addDiskgroupResponse']['jobid']
    logging.info('calling queryAsyncJobResult method...')
    addDiskGrp_status = queryAsyncJobResult(stdurl, job_id)
    logging.debug('Adding Disk group status: %s', addDiskGrp_status)
    if addDiskGrp_status[0] == 'PASSED':
        result = ['PASSED', 'Added Disk Group successfully']
    else:
        result = ['FAILED', addDiskGrp_status]
    logging.debug('result of Adding  Disk Group : %s', str(result))
    return result

###stripe/mirror/raidz1/raidz2/raidz3
###metavdevs : meta_mirror/meta_raidz1/meta_raidz2/meta_raidz3
###(nested raid configuration)
def addDiskGroup_vdev(pool_id, clstr_id, group, disk_list, iops, sctr_size, stdurl):
    if '_' or ' ' in group:
        group = group.replace('_', '%20').replace(' ' , '%20')
    logging.info('inside addDiskGroup_vdev method..')
    throughput = iops * 128
    querycommand = 'command=addDiskGroup&poolid=%s&clusterid=%s&'\
        'grouptype=%s&diskslist=%s&sectorsize=%s&totaliops=%s&totalthroughput=%s' \
        %(pool_id, clstr_id, group, disk_list, sctr_size, iops, throughput)
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API adding Disk group: %s', str(rest_api))
    add_diskGroup = sendrequest(stdurl, querycommand)
    data = json.loads(add_diskGroup.text)
    logging.debug('response for adding disk group: %s', str(data))
    if 'errorcode' in str(data):
        errormsg = str(data['addDiskgroupResponse'].get('errortext'))
        print errormsg
        result = ['FAILED', errormsg]
        logging.error('Not able to add disk group due to: %s', errormsg)
        return result
    logging.info('getting add disk group job id...')
    job_id = data['addDiskgroupResponse']['jobid']
    logging.info('calling queryAsyncJobResult method...')
    addDiskGrp_status = queryAsyncJobResult(stdurl, job_id)
    logging.debug('Adding disk group status: %s', addDiskGrp_status)
    if addDiskGrp_status[0] == 'PASSED':
        result = ['PASSED', 'Added Disk Group successfuly']
    else:
        result = ['FAILED', addDiskGrp_status]
    logging.debug('result of Adding  Disk Group : %s', str(result))
    return result

def delete_diskGroup(diskGrp_id, stdurl):
    logging.info('Inside the delete disk group method...')
    querycommand = 'command=deleteDiskGroup&id=%s' %diskGrp_id
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API for deleting disk group: %s', str(rest_api))
    diskGrp_delete = sendrequest(stdurl, querycommand)
    data = json.loads(diskGrp_delete.text)
    logging.debug('response for deleting disk group: %s', str(data))
    if 'errorcode' in str(data):
        errormsg = str(data['deleteDiskgroupResponse'].get('errortext'))
        print errormsg
        result = ['FAILED', errormsg]
        logging.error('Not able to delete disk group due to: %s', errormsg)
        return result
    else:
        result = ['PASSED', 'Successfully deleted Disk group']
        return result

def delete_pool(pool_id, stdurl):
    logging.info('Inside the delete pool method...')
    querycommand = 'command=deleteHAPool&id=%s' %(pool_id)
    rest_api = str(stdurl) + str(querycommand)
    logging.debug('REST API for deleting Pool: %s', str(rest_api))
    resp_deletePool = sendrequest(stdurl, querycommand)
    data = json.loads(resp_deletePool.text)
    logging.debug('response for deleting pool: %s', str(data))
    if 'errorcode' in str(data):
        errormsg = str(data['deleteHAPoolResponse']['errortext'])
        print errormsg
        result = ['FAILED', errormsg]
        logging.error('Not able to delete pool due to: %s', errormsg)
        return result
    else:
        result = ['PASSED', 'Successfully deleted Pool']
        return result

#pool_params : name, iops, pool type
def pool_creation_flow(stdurl, pool_params, num_of_disks, disk_type):
    list_cntrl = list_controller(stdurl)
    if list_cntrl[0] == 'FAILED':
        return ['FAILED', list_cntrl[1]]
    controllers_ip, num_of_Nodes = get_node_IP(list_cntrl[1])
    logging.debug('num_of_Nodes: %s, controllers_ip: %s', \
            num_of_Nodes, controllers_ip) 
    if num_of_Nodes == 1:
        NODE1_IP = controllers_ip[0]
    elif num_of_Nodes == 2:
        NODE1_IP = controllers_ip[0]
        NODE2_IP = controllers_ip[1]
    else:
        logging.debug('Number of Nodes are more than 2, please revisit the code')
        exit()
    cntrl_info = get_controller_info(NODE1_IP, list_cntrl[1])
    if cntrl_info[0] == 'FAILED':
        return ["FAILED", cntrl_info[1]]
    status, ctrl_name, ctrl_id, ctrl_ip, ctrl_cluster_id, ctrl_disks, \
            site_id  = get_value(cntrl_info)
    logging.info('Controller details is as follows:')
    logging.debug('status: %s, ctrl_name: %s, ctrl_id: %s, ctrl_ip: %s', \
            status, ctrl_name, ctrl_id, ctrl_ip)
    logging.debug('ctrl_cluster_id: %s, ctrl_disks: %s, site_id: %s', \
            ctrl_cluster_id, ctrl_disks, site_id)
    #Checking Node state
    if status.lower() == 'maintenance' and num_of_Nodes == 2:
        logging.debug('Node1 is in maintenance, checking status of Node2')
        cntrl_info = get_controller_info(NODE2_IP, list_cntrl[1])
        if cntrl_info[0] == 'FAILED':
            return ["FAILED", cntrl_info[1]]
        status, ctrl_name, ctrl_id, ctrl_ip, ctrl_cluster_id, ctrl_disks, \
                site_id  = get_value(cntrl_info)
        if status.lower() == 'maintenance':
            msg = 'Both nodes are in maintenance, testcase cannot proceed'
            return ['FAILED', msg]
    elif status.lower() == 'maintenance' and num_of_Nodes == 1:
        msg = 'The single node in HAgroup is in maintenance, '\
                'testcase cannot proceed'
        return ['FAILED', msg]
    free_disks =  getFreeDisk(ctrl_disks)
    if free_disks[0] == 'FAILED':
        return ['FAILED', free_disks[1]]
    disklist_id = getDiskToAllocate(free_disks[1], num_of_disks, disk_type)
    if disklist_id[0] == 'FAILED':
        return ['FAILED', disklist_id[1]]
    disklist_id = disklist_id[1]
    logging.debug('disklist_id: %s', disklist_id)

    #forming pool requried parameters for pool creation
    req_ids = {'siteid': site_id, 'clusterid': ctrl_cluster_id, \
            'controllerid': ctrl_id, 'diskslist': disklist_id }
    final_pool_params = dict(pool_params.items() + req_ids.items())
    pool_creation = create_pool(final_pool_params, stdurl)
    if pool_creation[0] == 'FAILED':
        return ['FAILED', pool_creation[1]]
    return ["PASSED", 'Successfully created pool']
    









