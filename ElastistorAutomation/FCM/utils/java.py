#!/usr/bin/python
import json
from FCM.utils.DateUtils import DateUtilities as DUtils
from FCM.utils.ResultUtils import ResultUtilities as rUtils
import time

from os import system

#phpstatus = system('php --version')
javastatus = system('java -version')
#print javastatus
def main():
    list = []
    #javastatus=10
    try:
        javastatus = system('java -version')
	print javastatus
       # rUtils.logger(list, "TC136 Starts.............&&-&&-&&info")
        time.sleep(2)
        #if (javastatus==0):
            print "hello"
	   # rUtils.logger(list, "Validate java installed :","dasd","dasd","pass")
           
        #else:
         #   rUtils.logger(list, "java is not installed :","dasd","dasd","fail")

       
	   
        #time.sleep(2)
        #rUtils.logger(list, "TC136 Ends...........&&-&&-&&info","","")
    #except:
        #rUtils.logger(list, "Exception occurred", "-", "-","exception")
    finally:
        #print json.dumps(list)
	#print list
    if(javastatus != 0):
   	sys.exit(-1)
if __name__ == '__main__':
    main()

       
#if(javastatus != 0):
#   sys.exit(-1)

#    print 'Missing: Java'
