#discription      :JMX validaition
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
	jmx="/opt/APG/Collecting/JMX-Collector/JMX-Collector/conf/jmx-collector.xml"
	jmx_data="/opt/APG/Collecting/JMX-Collector/JMX-Collector/conf/jmx-collector-data.xml"
	status=1
	if(os.path.exists(jmx)and os.path.exists(jmx_data)):
	    status=0
	if(status== 0):
             sys.exit(0)
	else: 
             sys.exit(1)
		
if __name__ == '__main__':
        main()

