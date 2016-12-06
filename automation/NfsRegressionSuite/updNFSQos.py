import json
import requests
import md5
import subprocess
import os
import time
import logging
from time import ctime
import sys
from tsmUtils import listTSMWithIP_new
from vdbenchUtils import executeVdbenchFile, is_vdbench_alive, kill_vdbench 
from cbrequest import executeCmd, sendrequest, queryAsyncJobResult, get_url,\
        mountNFS, umountVolume, getControllerInfo, getoutput, get_apikey,\
        executeCmdNegative, configFile, resultCollection, umountVolume_new
from volumeUtils import create_volume, delete_volume, addNFSclient,\
        edit_qos_tp, edit_qos_iops, listVolumeWithTSMId_new
from utils import UMain

logging.basicConfig(format = '%(asctime)s %(message)s', filename = 'logs/automation_execution.log',\
        filemode = 'a', level = logging.DEBUG)
logging.info('---Start of script "Edit QoS properties while running IOPS and verify QoS values"---')
IopsEnable_Flag =  TpEnable_flag = 0
if len(sys.argv) == 4:
    if  sys.argv[2].lower() == "%s" %("iopsenable"):
        IopsEnable_Flag = 1
        iops_value = sys.argv[3]
    elif sys.argv[2].lower() == "%s" %("iopsdisable"):
        TpEnable_flag = 1
        throughput_value = sys.argv[3]
    else:
        print "Arguments are not correct,please provide the corrrect arguments as below\n"
        print "python updNFSQos.py conf.txt IopsEnable/IopsDisable Iopsvalue/Throughputvalue"
        print "If you give IopsEnabled give the Iops value or else throughput value"
        exit()
else:
    print "Arguments are not correct,please provide the corrrect arguments as below\n"
    print "python updNFSQos.py conf.txt IopsEnable/IopsDisable Iopsvalue/Throughputvalue"
    print "If you give IopsEnabled give the Iops value or else throughput value"
    exit()

config = configFile(sys.argv)
apikey = get_apikey(config)
stdurl = get_url(config, apikey[1])
tsm_ip = '%s' %(config['ipVSM1'])
passwd = '%s' %(config['password'])

startTime = ctime()
##listing Accounts to get Accname
querycommand = 'command=listAccount'
resp_listAccount = sendrequest(stdurl, querycommand)
data = json.loads(resp_listAccount.text)
AccountList = data['listAccountResponse']
if 'errorcode' in str(AccountList):
    errormsg = str(data['listAccountResponse']['errortext'])
    print errormsg
    endTime = ctime()
    resultCollection('Listing of Account failed',['BLOCKED',''], startTime, endTime)
    exit()
try:
    accounts = data["listAccountResponse"]["account"]
    if data["listAccountResponse"]["count"] > 0:
        accId =  data["listAccountResponse"]["account"][0]["id"]
        accName =  data["listAccountResponse"]["account"][0]["name"]
        
except:
    print 'Accounts not present...Create Account'
    exit()
##listing pool to get poolname
querycommand = 'command=listHAPool'
resp_listHAPool = sendrequest(stdurl, querycommand)
data = json.loads(resp_listHAPool.text)
PoolList = data['listHAPoolResponse']
if 'errorcode' in str(PoolList):
    errormsg = str(data['listHAPoolResponse']['errortext'])
    print errormsg
    endTime = ctime()
    resultCollection('Listing of Pool failed',['BLOCKED',''], startTime, endTime)
    exit()
elif data["listHAPoolResponse"]["count"] > 0:
    poolId = data["listHAPoolResponse"]["hapool"][0]["id"]
    poolName = data["listHAPoolResponse"]["hapool"][0]["name"]
else:
    print 'Pool Not present..create Pool'
    exit()
### Listing Tsm to get id and dataset id
logging.info('Listing Tsm for given TSMIP "%s" to get its ID', tsm_ip)
tsm_list = listTSMWithIP_new(stdurl, tsm_ip)
if 'PASSED' in tsm_list:
    logging.info('TSM present with the given IP "%s"', tsm_ip)
    pass
elif 'BLOCKED' in tsm_list:
    errormsg = 'There is no TSM with IP "%s"' %(tsm_ip)
    print errormsg
    logging.warning('TSM with IP "%s" not present, Create TSM', tsm_ip)
    logging.debug('-------Ending script because no TSM present-------')
    endTime = ctime()
    resultCollection('Listing of Tsm failed',['BLOCKED', ''], startTime, endTime)
    exit()
else:
    errormsg =  'Not able to list TSMs due to: ' + tsm_list[1]
    logging.debug('%s', tsm_list[1])
    logging.debug('-------Ending script because Failed to list TSM-------')
    endTime =ctime()
    resultCollection('Listing of Tsm failed',['BOLCKED',''], startTime, endTime)
    exit()
tsm_id = tsm_list[1][0].get('id')
tsm_name = tsm_list[1][0].get('name')
dataset_id = tsm_list[1][0].get('datasetid')
vsmAccName = tsm_list[1][0].get('accountname')
node_ip = tsm_list[1][0].get('controlleripaddress')
logging.info('Got TSM ID and Dataset ID "%s"  "%s" of "%s"', tsm_id, dataset_id, tsm_name)

if IopsEnable_Flag == 1:
    logging.info('Creating dictionary for creating volume')
    volume1 = {'name': 'IopsVolume1', 'tsmid': tsm_id, 'datasetid': dataset_id,\
            'protocoltype': 'NFS', 'iopscontrol':'true', 'tpcontrol':'false'}
    logging.info('Dictionary created')
    logging.debug('%s', volume1)
    logging.info('creating volume "%s"', volume1['name'])
    create_vol = create_volume(volume1, stdurl)
    print create_vol[0]
    logging.debug('%s', create_vol)
    if 'FAILED' in create_vol:
        errormsg = 'Not able to create vol due to:' + create_vol[1]
        print errormsg
        logging.debug('%s', create_vol[1])
        logging.debug('-------Ending script because Failed to create volume------')
        endTime = ctime()
        resultCollection('creation of volume failed',['BLOCKED',''], startTime, endTime)
        exit()
    logging.info('Listing volumes in the TSM "%s" w.r.t its TSM ID', tsm_name)
    vol_list = listVolumeWithTSMId_new(stdurl, tsm_id)
    if 'PASSED' in vol_list:
        logging.info('Volumes present in the TSM "%s"', tsm_name)
        pass
    else:
        errormsg = 'Not able to list Volumes in TSM "%s" due to: ' \
                %(tsm_name) + vol_list[1]
        print errormsg
        logging.debug('%s', vol_list[1])
        logging.debug('-------Ending script because Failed to list volume-----')
        endTime = ctime()
        resultCollection('Listing of volume Blocked the testcase',\
                ['BLOCKED',''], startTime, endTime)
        exit()
    iops_volid = vol_list[1][0].get('id')
    iops_volname = vol_list[1][0].get('name')
    iopsgroup_id = vol_list[1][0].get('groupid')
    logging.info('Got IopsVolume ID = "%s" and Group ID = "%s" of "%s"',\
            iops_volid, iopsgroup_id, iops_volname)
    addNFSclient(stdurl, iops_volid, 'all')
    mnt_info1 = {'TSMIPAddress' : tsm_ip, 'mountPoint': vsmAccName+iops_volname,\
            'name' : vsmAccName+iops_volname}
    nfsMount1 = mountNFS(mnt_info1)

    if nfsMount1 == 'PASSED':
        logging.info('volume is mounted succesfully')
        logging.info('...executing vdbench....')
        executeVdbenchFile(mnt_info1, 'filesystem_nfs')
    else:
        errormsg = "volume is not mounted succesfully"
        endTime = ctime()
        resultCollection('Mounting volume is failed',['BLOCKED',''], startTime, endTime)
        exit()
    time.sleep(180)
    logging.info('verifying the Iops in volume')
    iops_datapath = poolName+'/'+accName+tsm_name+'/'+iops_volname
    cmd = 'reng stats access dataset %s qos | head -n 4 ; sleep 10 ;\
            echo "-----------------"; reng stats access dataset %s qos |\
            head -n 4' %(iops_datapath, iops_datapath)
    logging.debug('executing the command %s in controller', str(cmd))
    iops_res = getControllerInfo(node_ip, passwd, cmd, 'iopsoutput.txt')
    print iops_res
    logging.debug('iops result is %s', (iops_res))
    res = edit_qos_iops(iopsgroup_id, iops_value, stdurl)
    if res[0] == 'PASSED':
        logging.debug('IOPs value is updated')
        endTime = ctime()
        resultCollection('updating QOS property is Passed',\
                ['PASSED',''], startTime, endTime)
    else:
        logging.debug('IOPs value is not updated')
        endTime = ctime()
        resultCollection('updating QOS property is failed',\
                ['FAILED',''], startTime, endTime)
    time.sleep(15)
    logging.info('verifying the Iops in volume again ')
    cmd = 'reng stats access dataset %s qos | head -n 4 ; sleep 10 ;\
            echo "-----------------" ; reng stats access dataset %s qos |\
            head -n 4' %(iops_datapath, iops_datapath)
    logging.debug('executing the command %s in controller', str(cmd))
    iops_res2 = getControllerInfo(node_ip, passwd, cmd, 'updiopsoutput.txt')
    print iops_res2
    logging.debug('iops result is %s', (iops_res2))
    logging.info('comparing the both iops result')
    io_output = executeCmdNegative('diff iopsoutput.txt updiopsoutput.txt')
    logging.debug('compared result is %s', (io_output))
    if io_output[0] == 'FAILED':
        msg =  "Iops are not running correct"
        logging.debug('Compared result: %s', msg)
        endTime = ctime()
        resultCollection('Iops value are same after updating the value',\
                ['FAILED',''], startTime, endTime)
        print msg
    elif io_output[0] == 'PASSED':
        msg =  "Iops are  running correct"
        logging.debug('Compared result: %s', msg)
        print msg
        endTime = ctime()
        resultCollection('Iops value are different after updating the'\
                'value',['PASSED',''], startTime, endTime)
    else:
        print "problem in comparing files"
    time.sleep(15)

    check_vdbench = is_vdbench_alive(vsmAccName+iops_volname)
    if check_vdbench:
        logging.debug('vdbench is running, going to kill the vdbench process...')
	kill_vdbench()
	time.sleep(2)
	check_vdbench = is_vdbench_alive(vsmAccName+iops_volname)
	if check_vdbench:
            logging.debug('Failed to kill vdbench process, going to kill again...')
	    kill_vdbench()
	else:
            logging.debug('Successfully killed vdbench process')
	    print 'Successfully killed vdbench process'
    else:
	logging.debug('Vdbench process has stopped unexpectedly...')
	print 'Vdbench process has stopped'

    logging.info('Waiting for a few seconds before unmounting...')
    time.sleep(15)

    logging.debug('unmounting the volume %s', (iops_volname))
   
    count = 0
    while True:
	umount = umountVolume_new(mnt_info1)
	if 'FAILED' in umount[0] and 'device is busy' in umount[1]:
	    if count < 5 :
		print 'Unmount is failing as device is busy, hence waiting for 5s'
		logging.info('Since device is busy waiting for 5s and '\
		    'then trying to umount')
		time.sleep(5)
		count = count + 1
		continue
	    else:
		total_time = count * 5
		logging.info('waited for %s seconds still unmount is failing, '\
			'hence unmounting forcefully', total_time)
		print 'waited for %s seconds still unmount is failing, '\
			'hence unmounting forcefully' %total_time
		umount_output = executeCmd('umount -l mount/%s' \
			%(mnt_info1['mountPoint']))
		if umount_output[0] == 'PASSED':
		    logging.debug('Forceful unmount passed for volume "%s"', \
			    mnt_info1['name'])
		    break
	    	else:
		    logging.debug('Forcefull umount failed due to: %s', \
		            umount_output[1])
		    break
	elif 'FAILED' in umount[0]:
		logging.debug('Unmount failed for the volume "%s" due to: %s', \
			 mnt_info1['name'], umount[1])
		break
	else:
	    print umount[1]
	    logging.debug('Volume "%s" umounted successfully', mnt_info1['name'])
	    break

    logging.info('Deleting the created volume')
    del_vol = delete_volume(iops_volid, stdurl)
    print del_vol
    logging.debug('deleteing volume result is %s', (del_vol))

    logging.info('---End of script "Edit QoS properties while running '\
            'IOPS and verify QoS values"---')

if TpEnable_flag ==1:
    logging.info('Creating dictionary for creating volume with throughput enabled')
    volume2 = {'name': 'NFSTpVolume', 'tsmid': tsm_id, 'datasetid': dataset_id,\
            'protocoltype': 'NFS', 'iopscontrol':'false', 'tpcontrol':'true',\
            'iops': 0, 'throughput': 1000}
    logging.info('Dictionary created')
    logging.debug('%s', volume2)
    logging.info('creating volume "%s"', volume2['name'])
    create_vol2 = create_volume(volume2, stdurl)
    print create_vol2
    logging.debug('%s', create_vol2)
    if 'FAILED' in create_vol2:
        print 'Not able to create vol due to:' + create_vol2[1]
        logging.debug('%s', create_vol2[1])
        logging.debug('-------Ending script because Failed to create volume------')
        endTime =ctime()
        resultCollection('creation of volume failed',['BLOCKED',''], startTime, endTime)
        exit()
    logging.info('Listing volumes in the TSM "%s" w.r.t its TSM ID', tsm_name)
    vol_list = listVolumeWithTSMId_new(stdurl, tsm_id)
    if 'PASSED' in vol_list:
        logging.info('Volumes present in the TSM "%s"', tsm_name)
        pass
    else:
        print 'Not able to list Volumes in TSM "%s" due to: ' \
                %(tsm_name) + vol_list[1]
        logging.debug('%s', vol_list[1])
        logging.debug('-------Ending script because Failed to list volume-----')
        endTime = ctime()
        resultCollection('Listing of volume failed',['BLOCKED',''], startTime, endTime)
        exit()
    tp_volid = vol_list[1][0].get('id')
    tp_volname = vol_list[1][0].get('name')
    tpgroup_id = vol_list[1][0].get('groupid')
    logging.info('Got TpVolume ID = "%s" and Group ID = "%s" of "%s"', \
            tp_volid, tpgroup_id, tp_volname)
    addNFSclient(stdurl, tp_volid, 'all')
    mnt_info2 = {'TSMIPAddress' : tsm_ip, 'mountPoint': vsmAccName+tp_volname,\
            'name' : vsmAccName+tp_volname}
    nfsMount2 = mountNFS(mnt_info2)
    if nfsMount2 == 'PASSED':
        logging.info('volume is mounted succesfully')
        logging.info('...executing vdbench....')
        executeVdbenchFile(mnt_info2, 'filesystem_nfs')
    else:
        print "volume is not mounted"
        endTime = ctime()
        resultCollection('Mounting volume is failed',['BLOCKED',''],\
                startTime, endTime)
        logging.debug('-------Ending script because Failed to '\
                'executing vdbench------')
        exit()
    time.sleep(180)
    logging.info('verifying the Throughput in volume')
    tp_datapath =  poolName+'/'+accName+tsm_name+'/'+tp_volname
    cmd = 'reng stats access dataset %s qos | head -n 4 ; sleep 10 ;\
            echo "-----------------" ; reng stats access dataset %s qos |\
            head -n 4' %(tp_datapath, tp_datapath)
    logging.debug('executing the command %s in controller', str(cmd))
    tp_res = getControllerInfo(node_ip, passwd, cmd, 'tpoutput.txt')
    print tp_res
    logging.debug('Throughput result is %s', (tp_res))
    res = edit_qos_tp(tpgroup_id, throughput_value, stdurl)
    if res[0] == 'PASSED':
        logging.debug('Throuhput value is updated while iops is running')
        endTime = ctime()
        resultCollection('updating QOS property is Passed',\
                ['PASSED',''], startTime, endTime)
    else:
        logging.debug('Throughput  value is not updated')
        endTime = ctime()
        resultCollection('updating QOS property is failed',\
                ['FAILED',''], startTime, endTime)
    
    time.sleep(15)

    logging.info('verifying the Throuput in volume again ')
    cmd = 'reng stats access dataset %s qos | head -n 4 ; sleep 10 ;\
            echo "-----------------" ; reng stats access dataset %s qos |\
            head -n 4' %(tp_datapath, tp_datapath)
    logging.debug('executing the command %s in controller', str(cmd))
    tp_res2 = getControllerInfo(node_ip, passwd, cmd, 'updtpoutput.txt')
    print tp_res2
    logging.debug('Throughput result is %s', (tp_res2))

    logging.info('comparing the both Throuput  result')
    tp_output = executeCmdNegative('diff tpoutput.txt updtpoutput.txt')
    logging.debug('compared result is %s', (tp_output))
    if tp_output[0] == 'FAILED':
        msg =  "Throughput are not running succesfully"
        logging.debug('Compared result: %s', msg)
        print msg
        endTime = ctime()
        resultCollection('Throughput value are same after updating '\
                'the value',['FAILED',''], startTime, endTime)
    elif tp_output[0] == 'PASSED':
        msg =  "Throughput are running succesfully"
        logging.debug('Compared result: %s', msg)
        print msg
        endTime = ctime()
        resultCollection('Throughput value are different after updating'\
                'the value and iops are running',['PASSED',''], startTime, endTime)
    else:
        print "Problem in comparing the files"
        print msg
    time.sleep(60)
   
    
    check_vdbench = is_vdbench_alive(vsmAccName+tp_volname)
    if check_vdbench:
        logging.debug('vdbench is running, going to kill the vdbench process...')
	kill_vdbench()
	time.sleep(2)
	check_vdbench = is_vdbench_alive(vsmAccName+tp_volname)
	if check_vdbench:
            logging.debug('Failed to kill vdbench process, going to kill again...')
	    kill_vdbench()
	else:
            logging.debug('Successfully killed vdbench process')
	    print 'Successfully killed vdbench process'
    else:
	logging.debug('Vdbench process has stopped unexpectedly...')
	print 'Vdbench process has stopped'

    logging.info('Waiting for a few seconds before unmounting...')
    time.sleep(15)

    count = 0
    while True:
        umount = umountVolume_new(mnt_info2)
        if 'FAILED' in umount[0] and 'device is busy' in umount[1]:
            if count < 5 :
		print 'Unmount is failing as device is busy, hence waiting for 5s'
		logging.info('Since device is busy waiting for 5s and '\
                        'then trying to umount')
		time.sleep(5)
		count = count + 1
		continue
	    else:
		total_time = count * 5
		logging.info('waited for %s seconds still unmount is failing, '\
			'hence unmounting forcefully', total_time)
		umount_output = executeCmd('umount -l mount/%s' \
			%(mnt_info2['mountPoint']))
		if umount_output[0] == 'PASSED':
		    logging.debug('Forceful unmount passed for volume "%s"', \
		            mnt_info2['name'])
		    break
	    	else:
		    logging.debug('Forcefull umount failed due to: %s', \
			    umount_output[1])
		    break
	elif 'FAILED' in umount[0]:
                logging.debug('Unmount failed for the volume "%s" due to: %s', \
	                 mnt_info2['name'], umount[1])
	        break
     	else:
            print umount[1]
	    logging.debug('Volume "%s" umounted successfully', mnt_info2['name'])
	    break

    logging.info('Deleting the created volume')
    del_vol = delete_volume(tp_volid, stdurl)
    if del_vol[0] == 'PASSED':
        print del_vol[1]
        logging.debug('deleteing volume  is Passed')
    else:
        endTime = ctime()
        resultCollection('Deleting volume failed',['BLOCKED',''], startTime, endTime)
    
    logging.info('---End of script "Edit QoS properties while '\
            'running IOPS and verify QoS values"---')
    
