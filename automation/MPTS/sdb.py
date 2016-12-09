import json
import sys
import time
from time import ctime
from cbrequest import configFile, executeCmdWithOutput, executeCmdNegative,  resultCollection, getoutput

result = executeCmdWithOutput('fdisk -l | grep GB | wc -l')
print result
#print res[1]

