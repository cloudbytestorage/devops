import os
import sys
import time
import json
import logging
from time import ctime
from cbrequest import sendrequest, filesave, timetrack, queryAsyncJobResult, configFile, resultCollection, listVolume, getURL

if len(sys.argv) < 2:
    print "Argument is not correct.. Correct way as below"
    print "python deleteAllVolume.py anyconfiguration.txt"
    exit()

config = configFile(sys.argv)
stdurl = getURL(config)
startTime = ctime()
volumes = listVolume(config)
endTime = ctime()
if volumes[0] == 'PASSED':
    volumes = volumes[1]
else:
    exit()
for volume in volumes:
    vol_id = volume['id']
    querycommand = 'command=deleteFileSystem&id=%s' %(vol_id)
    resp_delete_all_volume = sendrequest(stdurl, querycommand)
    filesave("logs/DeleteAllFileSystem", "a", resp_delete_all_volume)
    data = json.loads(resp_delete_all_volume.text)
    job_id = data["deleteFileSystemResponse"]["jobid"]
    rstatus=queryAsyncJobResult(stdurl, job_id);
    print rstatus

