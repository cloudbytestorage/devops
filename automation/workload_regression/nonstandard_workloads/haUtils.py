import os
import sys
import time
import json
import logging
from time import ctime
from cbrequest import sendrequest, configFile, getControllerInfo, executeCmd, queryAsyncJobResult

logging.basicConfig(format = '%(asctime)s %(message)s', filename = \
        'logs/automation_execution.log', filemode = 'a', level=logging.DEBUG)

def ping_machine(ip):
    pingvalue = executeCmd('ping -c 1 %s' %(ip))
    count = 1
    if pingvalue[0] == 'PASSED':
        logging.debug('Able to ping IP: %s', ip)
        return ['PASSED', '']
    while pingvalue[0] == 'FAILED':
        if count == 15:
            print '%s is unreachable' %ip
            logging.error('Node with IP %s is unreachable', ip)
            return ['FAILED', 'Node is unreachable']
        pingvalue = executeCmd('ping -c 1 %s' %(ip))
        count = count + 1
        time.sleep(2)

def verify_mode_value(mode):
    if mode.lower() == 'maintenance':
        logging.debug('Node status would change to Maintenance')
        mode = 'Maintenance'
        return ['PASSED', mode]
    elif  mode.lower() == 'available':
        logging.debug('Node status would change to Available')
        mode = 'Available'
        return ['PASSED', mode]
    else:
        print 'mode value  has to be maintenance or available'
        logging.error('mode value %s is not correct, it has to be '\
                'maintenance or available', mode)
        return ['FAILED', 'mode value is not correct']

def list_controller(stdurl):
    querycommand = 'command=listController'
    logging.debug('Executing listController...')
    resp_listcontroller = sendrequest(stdurl, querycommand)
    data = json.loads(resp_listcontroller.text)
    if 'errorcode' in str(data):
        errormsg = str(data['listControllerResponse']['errortext'])
        logging.error('Not able to list controllers Error: %s', errormsg)
        result = ['FAILED', errormsg]
    elif 'controller' in data['listControllerResponse']:
        controllerlist = data['listControllerResponse']['controller']
        result = ['PASSED', controllerlist]
    else:
        print 'There is no Node'
        logging.debug('There is no Node available to list')
        result = ['FAILED', 'There is no Node available to list']
    return result

def get_controller_info(node1_ip, controllerlist):
    for controller in controllerlist:
        ctrl_id = None
        if node1_ip == controller.get('hamanageripaddress'):
            status = controller.get('managedstate')
            ctrl_name = controller.get('name')
            ctrl_id = controller.get('id')
            ctrl_ip = controller.get('hamanageripaddress')
            ctrl_cluster_id = controller.get('clusterid')
            ctrl_disks = controller.get('disks')
            site_id = controller.get('siteid')
            if ctrl_id is None:
                return ['FAILED', 'Not able to get controller id']
            return ['PASSED', status, ctrl_name, ctrl_id, ctrl_ip, \
                    ctrl_cluster_id, ctrl_disks, site_id]

def get_value(result):
    status = result[1]
    ctrl_name = result[2]
    ctrl_id = result[3]
    ctrl_ip = result[4]
    ctrl_cluster_id = result[5]
    ctrl_disks = result[6]
    site_id = result[7]
    return status, ctrl_name, ctrl_id, ctrl_ip, ctrl_cluster_id, \
            ctrl_disks, site_id

def change_state(stdurl, ctrl_id, mode, ctrl_name):
    querycommand = 'command=changeControllerState&id=%s&state=%s' \
            %(ctrl_id, mode)
    logging.debug('Executing changeControllerState...')
    resp_stateofnode= sendrequest(stdurl, querycommand)
    data = json.loads(resp_stateofnode.text)
    if 'errorcode' in str(data):
        errormsg = str(data['changeControllerStateResponse']['errortext'])
        logging.error('Not able to execute changeControllerState: %s', errormsg)
        return ['FAILED', errormsg]
    hajob_id = data['changeControllerStateResponse']['controller']['hajobid']
    querycommand = 'command=listHAJobActivities&hajobid=%s' %(hajob_id)
    logging.debug('Executing listHAJobActivities...')
    hajob = sendrequest(stdurl, querycommand)
    data = json.loads(hajob.text)
    if 'errorcode' in str(data):
        errormsg = str(data['listHAJobActivitiesResponse']['errortext'])
        logging.error('Not able to execute listHAJobActivitiesResponse: %s',\
                errormsg)
        return ['FAILED', errormsg]
    job_id = data['listHAJobActivitiesResponse']['jobid']
    rstatus = queryAsyncJobResult(stdurl, job_id)
    querycommand = 'command=listHAJob&jobstatus=running'
    logging.debug('Executing listHAJob...')
    hajob = sendrequest(stdurl, querycommand)
    data = json.loads(hajob.text)
    logging.debug('response for listHAJob... %s', hajob)
    logging.debug('executing queryAsyncJobResult method for job: %s', job_id)
    rstatus = queryAsyncJobResult(stdurl, job_id)
    if rstatus[0] == 'PASSED':
        logging.debug('Node %s moved to %s successfully', ctrl_name, mode)
        return ['PASSED', '']
    else:
        logging.debug('Node %s failed to moved to %s', ctrl_name, mode)
        return ['FAILED', '']

#call this metthod for bring node to maintenance/available state!
def change_node_state(stdurl, node1_ip, mode):
    #mode value will be 'available' or 'maintenance'
    logging.info('Inside the change_node_state method...')
    mode_result = verify_mode_value(mode)
    if mode_result[0] == 'FAILED':
        return ['FAILED', mode_result[1]]
    mode = mode_result[1]
    node_result = list_controller(stdurl)
    if node_result[0] == 'FAILED':
        return ['FAILED', node_result[1]]
    controllerlist = node_result[1]
    ping_result = ping_machine(node1_ip)
    if ping_result[0] == 'FAILED':
        return ['FAILED', 'Node is unreachable']
    result = get_controller_info(node1_ip, controllerlist)
    if result[0] == 'FAILED':
        return ['FAILED', result[1]]
    #status, ctrl_name, ctrl_id, ctrl_ip = get_value(result)
    status, ctrl_name, ctrl_id, ctrl_ip, ctrl_cluster_id, \
            ctrl_disks, site_id = get_value(result)
    if mode == status:
        errormsg = 'Node %s is already in %s state' %(ctrl_name, mode)
        logging.debug('Node %s is already in %s state', ctrl_name, mode)
        return ['FAILED', errormsg]
    logging.debug('Node detals... current_status: %s, name: %s, ip: %s, id: '\
            '%s', status, ctrl_name, ctrl_ip, ctrl_id)
    logging.debug('Node %s is in %s state so moving to %s state', \
            ctrl_name, status, mode)
    result = change_state(stdurl, ctrl_id, mode, ctrl_name)
    if result[0] == 'PASSED':
        logging.debug('Node with IP:%s moved to %s successfully', \
                node1_ip, mode)
        return ['PASSED', '']
    else:
        logging.debug('Node with IP:%s failed to move to %s', node1_ip, mode)
        return ['FAILED', '']

def get_node_IP(controllers):
    node_ip_list = []
    num_of_Nodes = 0
    for controller in controllers:
        num_of_Nodes = num_of_Nodes + 1
        nodeIP  = controller.get('ipAddress')
        nodeName = controller.get('name')
        node_ip_list.append(nodeIP)
        return node_ip_list, num_of_Nodes
