#description      :JMX validaition
# author          :Alok
# date            :20160830
# version         :1
# usage           :python module for  NHCQA-234.py
# notes           :
# python_version  :2.7
# ==============================================================================

#!/usr/bin/python
#!/usr/bin/python
import json
#from FCM.utils.DateUtils import DateUtilities as DUtils
#from FCM.utils.ResultUtils import ResultUtilities as rUtils
#import time

from os import system
import os
import sys, argparse
def main():
	list = []
	jmx_data="/opt/emc/nhc/data"
	jmx_log="/opt/emc/nhc/logs"
	status=1
	print status
	if(os.path.exists(jmx_data)and os.path.exists(jmx_log)):
	    status=0
	    
	if(status!= 0):
	     
            sys.exit(1)
	else: 
            sys.exit(0)
		
if __name__ == '__main__':
        main()
