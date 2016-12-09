from time import ctime
import time
import sys
import os

#dummy vsm dictionary for example
#vsm = {'quotasize': '100G', 'iops': 170, 'backuptpcontrol': 'true', 'blocksize': '32K', 'grace': 'false'}
def createVSM(vsm):
    #vsm is a dictionary that contains all the information needed to create a vsm
    #default properties = 'defaultPrts'
    defaultPrts = {'quotasize': '1T', 'iops': 1000, 'throughput': 4000, 'grace': \
            'false', 'blocksize': '4K', 'latency': 15, 'iopscontrol': \
            'true', 'tpcontrol': 'true', 'backuptpcontrol': 'false', \
            'totalbackupthroughput': 0, 'iqnname': ''}
    for key in vsm:
        if key in defaultPrts:
            defaultPrts[key] = vsm[key]
            if key == 'iops':
                defaultPrts['throughput'] = vsm[key] * 4

