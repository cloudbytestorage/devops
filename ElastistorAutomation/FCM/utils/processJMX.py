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
        p1 = subprocess.Popen(["ps", "-ef"], stdout=subprocess.PIPE)
        #p2 = subprocess.Popen(["grep", "/opt/APG/Java/Sun-JRE/8.0.51/bin/java -Xms256m -Xmx512m"], stdin=p1.stdout, stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["grep", "java -Xms64m -Xmx2048m -javaagent"], stdin=p1.stdout, stdout=subprocess.PIPE)
	p3 = subprocess.Popen(["grep", "-v" , "grep"], stdin=p2.stdout, stdout=subprocess.PIPE )

        p4 = subprocess.Popen(["wc" ,"-l"], stdin=p3.stdout, stdout=subprocess.PIPE)
        #out2=p2.communicate()
        #out3,err3 = p3.communicate()
        p3.stdout.close()
        p2.stdout.close()
        p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
        output,err = p4.communicate()
        f = open("/root/lenproc.txt", "w")
        f.write(output)
        #f.write(out2)
        #f.write(out2)
        f.close
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


