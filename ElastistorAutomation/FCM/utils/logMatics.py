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
import subprocess
def main():

        p1 = subprocess.Popen(["ls", "/opt/emc/nhc/data"], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["wc", "-l"], stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
        output,err = p2.communicate()
	intvar = int(output)
        if(intvar == 0):
            sys.exit(1)
	else:
            sys.exit(0)

if __name__ == '__main__':
        main()
        #if(output== 0):
        #        sys.exit(1)
        #else:
        #        sys.exit(0)



