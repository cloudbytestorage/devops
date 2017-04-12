import json
import requests
from hashlib import md5
import fileinput
import subprocess
import time
from cbrequest import sendrequest, filesave1, timetrack, queryAsyncJobResult, configFile, executeCmd, createSFTPConnection, getControllerInfo, getoutput
file='logs/if_config_output';
IP = "20.10.57.103"
passwd = "test"
command = "zpool status -v Pool1"
t=getControllerInfo(IP, passwd, command, file)
poolType ='';
poolDisks = 0;
noDiskGroups = 0;
noOfSpares = 0;noOfCaches = 0;noOfLogs = 0;noOfMetaDisks = 0; noOfMetaDiskGroups = 0; noCacheDisks = 0; noSpareDisks = 0 ;noLogDisks = 0;noLogMirrDisks = 0 ;
poolName = 'Pool1'

#### Function(s) Declartion Ends
output =[]


list = getoutput('cat %s' %(file));
for st in list:
    s = st.split();
    output = output + st.split();

del output[0];
del output[0];
output.append("last");
print output
pool = {
        "pool" : "", 
        "state" : "", 
        "noOfDataDisks" : "", 
        "noOfDataDiskGroups" : "0", 
        "dataDiskGroupType" : "",
        "noOfLogs" : "0", 
        "noOfLogDisks" : "0",
        "noOfCaches" : "0", 
        "noOfCacheDisks" : "0",
        "noOfSpares" : "0", 
        "noOfSpareDisks" : "0",
        "noOfMetaGroups" : "0", 
        "noOfMetaDisks" : "0"
        }

if poolName in output:
    pool["pool"] = poolName;
if 'state:' in  output:
    stateIndex  = output.index('state:');
    pool["state"] = output[stateIndex+1];


x = 0;
for x in range(1, len(output) - 1):
   if output[x] == poolName:
       x = x + 5;
       y = x;
       while (1 == 1):
           if output[y].split('/')[0] == 'multipath':
               poolType = "Strip"
               poolDisks = poolDisks + 1;
               y = y + 5;
           else:
               break ;
       y = x;
       while (1 == 1):
           if output[y].split('-')[0] == 'raidz1':
               poolType = 'raidz1';
               noDiskGroups = noDiskGroups + 1; 
           elif output[y].split('/')[0] == 'multipath':
               poolDisks = poolDisks + 1;
           else:
               break ;
           y = y + 5;
       y = x;
       while (1 == 1):
           if output[y].split('-')[0] == 'raidz2':
               poolType = 'raidz2';
               noDiskGroups = noDiskGroups + 1;
           elif output[y].split('/')[0] == 'multipath':
               poolDisks = poolDisks + 1;
           else:
               break ;
           y = y + 5 ;
       y = x;
       while (1 == 1):
           if output[y].split('-')[0] == 'raidz3':
               poolType = 'raidz3';
               noDiskGroups = noDiskGroups + 1;
           elif output[y].split('/')[0] == 'multipath':
               poolDisks = poolDisks + 1;
           else:
                break ;
           y = y + 5 ;
       y = x;
       while (1 == 1):
            if output[y].split('-')[0] == 'mirror':
                poolType  = 'mirror';
                noDiskGroups = noDiskGroups + 1;
            elif output[y].split('/')[0] == 'multipath':
                poolDisks = poolDisks + 1;
            else:    
                break ;
            y = y + 5 ;
   if output[x] == 'spares':
       y = x;
       while (1 == 1):
           if output[y] == 'spares':
               type = 'spares';
               y = y + 1;
           elif output[y].split('/')[0] == 'multipath':
               noSpareDisks = noSpareDisks + 1;
               y = y + 5;
           else:
               break ;
   if output[x] == 'logs':
       y = x;
       while (1 == 1):
           if output[y] == 'logs':
               type3 = 'logs';
               y = y + 1;
           elif output[y].split('/')[0] == 'multipath':
               noLogDisks = noLogDisks + 1;
               y = y + 5;
           elif output[y].split('-')[0] == 'mirror':
               y = y + 5;
               continue ;
           else:
               break ;
   if output[x] == 'cache':
       y = x;
       while (1 == 1):
           if output[y] == 'cache':
               type4 = 'cache';
               y = y + 1;
           elif output[y].split('/')[0] == 'multipath':
               noCacheDisks = noCacheDisks + 1;
               y = y + 5;
           else:
               break;
   if output[x] == 'meta':
      y = x;
      while (1 == 1):
          if output[y].split('-')[0] == 'meta':
               type5 = 'meta';
               y = y + 1;
          elif output[y].split('-')[0] == 'raidz1':
              noOfMetaDiskGroups = noOfMetaDiskGroups + 1;
              y = y + 5;
          elif output[y].split('/')[0] == 'multipath':
              noOfMetaDisks = noOfMetaDisks + 1;
              y = y + 5;
          else:
              break ;
pool["dataDiskGroupType"] = "%s" %(poolType)
pool["noOfDataDiskGroups"] = "%d" %(noDiskGroups)
pool["noOfDataDisks"] = "%s" %(poolDisks)
pool["noOfLogs"] = "%d" %(noOfLogs)
pool["noOfLogDisks"] = "%d" %(noLogDisks)
pool["noOfCaches"] = "%d" %(noOfCaches)
pool["noOfCacheDisks"] = "%d" %(noCacheDisks)
pool["noOfSpares"] = "%d" %(noOfSpares)
pool["noOfSpareDisks"] =  "%d" %(noSpareDisks)
pool["noOfMetaGroups"] = "%d" %(noOfMetaDiskGroups)
pool["noOfMetaDisks"] = "%d" %(noOfMetaDisks)
print "test"
print str(pool)
filesave1("poolDetails.txt", "w", str(pool))
