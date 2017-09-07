import datetime
import time

#!/usr/bin/env python
_author_='naveenkumar b'
_email_='naveen.b@emc.com'

class DateUtilities:
    @staticmethod
    def getCurrentDate(format):
        #print(time.strftime(format))
        return time.strftime(format)

DateUtilities.getCurrentDate("%H:%M:%S")
DateUtilities.getCurrentDate("%d-%m-%y")







