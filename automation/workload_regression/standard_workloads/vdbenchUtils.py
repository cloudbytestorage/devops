import os
import sys
import csv
import math
import json
import time
import numpy
import dislin
import logging
import argparse
import subprocess
from time import ctime
from cbrequest import executeCmd, getoutput

#make sure the standard file is present in templates folder to run vdbench

def executeVdbench(confFile, outputFile):
    logging.info('.....inside excecute_vdbench method....')
    logging.info('executing vdbench command')
    out = os.system('./vdbench/vdbench -f vdbench/%s -o vdbench/%s ' 
            %(confFile, outputFile))
    return

##To Execute vdbench
def excecute_vdbench(volume):
    ##volume is dictionary
    logging.info('.....inside excecute_vdbench method....')
    logging.info(' overwriting the file fileconfig with std path')
    executeCmd('yes | cp -rf vdbench/templates/fileconfig vdbench/fileconfig')
    output = getoutput('mount | grep %s | awk \'{print $3}\'' %(volume['mountPoint']))
    old_str = 'mountDirectory'
    new_str = output[0].rstrip('\n')
    path = 'vdbench12/fileconfig'
    logging.info('Replacing the std path with volume mountpoint')
    res = executeCmd("sed -i 's/%s/%s/' %s " %(old_str.replace('/', '\/'),\
            new_str.replace('/', '\/'), path ))
    logging.info('executing vdbench command')
    out = os.system('./vdbench/vdbench -f vdbench/fileconfig -o vdbench/output &')
    logging.debug('vdbench command result:%s', out)

###execute vdbench by passing sample file
def executeVdbenchFile(volume, vdbfile):
    ##volume is dictionary
    logging.info('.....inside excecute_vdbench method....')
    logging.info(' overwriting the file fileconfig with std path')
    executeCmd('yes | cp -rf vdbench/templates/%s vdbench/%s' %(vdbfile, volume['name']))
    output = getoutput('mount | grep %s | awk \'{print $3}\'' %(volume['mountPoint']))
    old_str = 'mountDirectory'
    new_str = output[0].rstrip('\n')
    path = 'vdbench/%s' %volume['name']
    logging.info('Replacing the std path with volume mountpoint')
    res = executeCmd("sed -i 's/%s/%s/' %s " %(old_str.replace('/', '\/'), new_str.replace('/', '\/'), path ))
    logging.info('executing vdbench....')
    out = os.system('./vdbench/vdbench -f vdbench/%s -o vdbench/output &' %volume['name'])
    #out = os.system('./vdbench12/vdbench -f vdbench12/fileconfig &')
    return out

##for more mountpoint within a single file
def writingVDBfile(x, volume):
    output = getoutput('mount | grep %s | awk \'{print $3}\'' %(volume['mountPoint']))
    old_str = 'mountDirectory%s' %x
    new_str = output[0].rstrip('\n')
    path = 'vdbench/%s' %vdbNewFile
    logging.info('Replacing the std path with volume mountpoint')
    res = executeCmd("sed -i 's/%s/%s/' %s " %(old_str.replace('/', '\/'), new_str.replace('/', '\/'), path ))

###vdbFile - name of the vdbench file that is running
def is_vdbench_alive(vdbFile):
    pidCheck = os.popen("ps -eo pid,command | grep './vdbench/vdbench "\
            "-f vdbench/%s -o vdbench/output' | grep -v grep | "\
            "awk '{print $1}'" %(vdbFile)).read().rstrip('\n')
    return pidCheck

###get vdbench pid and will check till process completes
##vdbfile = name of file to run vdbench
def vdbench_pid(vdbfile):
    while True:
        pidCheck = os.popen("ps -eo pid,command | grep './vdbench/vdbench "\
                "-f vdbench/%s -o vdbench/output' | grep -v grep | "\
                "awk '{print $1}'" %vdbfile).read().rstrip('\n')
        if not pidCheck:
            break
        else:
            continue
    return pidCheck

def kill_vdbench():
    logging.debug('inside kill_vdbench...')
    pid = getoutput('ps -aux |grep vdbench |awk \'{print $2}\'')
    logging.debug('vdbench process going to be killed...: %s', pid)
    processlist =[]
    for process in pid:
        p1 = process.rstrip('\n')
        processlist.append(p1)
    #print processlist
    logging.debug('vdbench process ids...: %s', processlist)
    cmd = 'kill -9'
    for proc in processlist:
        cmd = cmd + ' %s' %(proc)
       # print proc
    res = executeCmd(cmd)
    #print res
    if res[0] == 'PASSED' or 'No such process' in str(res[1]):
        print 'vdbench process is killed'
        logging.debug('vdbench process are killed')
    else:
        print 'vdbench process are not killed'
        logging.debug('one or more vdbench process is not killed, Error: %s', \
                res[1])

##process_name : process you want to search and kill the process
def kill_process(process_name):
    logging.debug('inside kill_process...')
    pid = getoutput('ps -aux |grep %s |awk \'{print $2}\'' %(process_name))
    logging.debug('process going to be killed...: %s', pid)
    processlist =[]
    for process in pid:
        p1 = process.rstrip('\n')
        processlist.append(p1)
    #print processlist
    logging.debug('%s process ids...: %s', process_name, processlist)
    cmd = 'kill -9'
    for proc in processlist:
        cmd = cmd + ' %s' %(proc)
    res = executeCmd(cmd)
    if res[0] == 'PASSED' or 'No such process' in str(res[1]):
        print 'process is killed'
        logging.debug('process are killed')
    else:
        print 'process are not killed'
        logging.debug('one or more process is not killed, Error: %s', \
                res[1])

def createRunTimeConfig(confFile, userValues):
    # confFile is a template for creating config file
    # userValues is a directory, that contains new values to... 
    # ...updated in config file

    FIRSTELEMENT = 0
    EQUALOPERATOR = '='
    QUOMAOPERATOR = ','
   
    # removing the dummy text file if it exits
    os.system('rm -rf dummyConfFile.txt')
    
    # Opening source file(template)
    with open(confFile, "r") as sourceFile:
        for line in sourceFile:
        
            # creating a dummy file for newly updated values
            with open("dummyConfFile.txt", "a") as dummyFile:

                # making sure no empty line procede further
                if not line.strip():
                    continue
                
                # converting the line into a list, and will get only one value
                line = line.split()

                # In above code we converted whole line in a list with single element
                # getting the only present element from the list
                line = str(line[FIRSTELEMENT])

                # splitting all the values by "," from the above string and getting list 
                line = line.split(QUOMAOPERATOR)
                
                # proceding all the elements of the list
                newLine = []
                for element in line:
                    
                    # splitting elements by "=" into a sub list
                    subList = element.split(EQUALOPERATOR)
                    
                    # matching all the values with the user given values and updating the same
                    if subList[0] in userValues:
                        subList[1] = userValues[subList[0]]
                    
                    newLine.append(subList[0] + EQUALOPERATOR + subList[1])
                
                newLine = ','.join(newLine) + "\n"

                # writing newly created newLine into dummyFile
                dummyFile.write(str(newLine))

    # once dummy file is generated successfully, 
    # updating source file with the latest values
    with open("dummyConfFile.txt") as df:
        with open(confFile, "w") as sf:
            for line in df:
                sf.write(line)

def vdParser(flatfile, param, parsedfile):
     # Perform the vdbench result parse using parseflat util
     subprocess.call ("./vdbench parseflat -i %s -c %s -o %s" %(flatfile, param, parsedfile),  shell=True)

     # Removes header data from resulting csv, i.e., parse output
     subprocess.call ("sed -i -e '1d' %s" %(parsedfile), shell=True)

def vdProcessor(parsedfile, param):
    # Determine the total number of data points available - i.e., interval count
    intervalcount = subprocess.check_output ("cat %s | wc -l" %(parsedfile), shell=True)
    n = int(intervalcount)

    # Define values for the param plot's x-axis
    x = range(n)

    # Define values for the param plot's y-axis
    y = []

    with open(parsedfile, 'rU') as data:
        reader = csv.reader(data)
        for row in reader:
            for cell in row:
                cell = float(cell)
                y.append(cell)

    # Add into numpy list for obtaining data essentials
    data = numpy.genfromtxt(parsedfile, dtype='float',usecols=0)

    # Get the min and max values of the numpy list, i.e., param values
    minVal = data.min()
    maxVal = data.max()
    avgVal = data.mean()

    print "The minimum %s observed in %s" %(param, minVal)
    print "The maximum %s observed is %s" %(param, maxVal)
    print "The average %s observed in %s" %(param, avgVal)

    statsDict = {'x-range': x, 'y-range': y, 'min-param': minVal, 'max-param': maxVal, 'mean-param': avgVal}
    return (statsDict)

def dislinPlot(xvals, yvals, ylimit):

    # Set the plot output file format
    dislin.metafl (plot_filetype)

    # Dislin routine initialization
    dislin.disini ()

    # Set the font type on graph
    dislin.complx ()

    # Set the Graph color
    dislin.color (plot_color)

    # Fix the position of axes on graph area
    dislin.axspos (axes_pos_x,axes_pos_y)

    # Fix the length of axes on graph area
    dislin.axslen (axes_len_l,axes_len_h)

    # Set name of axes
    dislin.name (x_axis_name, 'X')
    dislin.name (y_axis_name, 'Y')

    # Num of digits after decimal point ; "-2" refers automatic selection
    dislin.labdig (-2, 'X')

    # Num of ticks on axes b/w values
    dislin.ticks (x_axis_ticks,'X')
    dislin.ticks (y_axis_ticks,'Y')

    # Plot title text
    dislin.titlin ('y_axis_name vs x_axis_name', 1)

    # Plot details; xlower., xupper., x1stlabel., xstep., ylower., yupper., y1stlabel., ystep
    dislin.graf (0., float(data_samples), 0., float(x_step), 0., float(ylimit), 0., float(y_step))

    # Write title on plot
    dislin.title()

    # Curve changes if called multiple times
    dislin.chncrv ('NONE')

    # Plot the Curve
    dislin.curve (xvals, yvals, data_samples)

    # Dislin routine conclusion
    dislin.disfin ()

def vdParseAndPlotImage(flatfile, param):

    data_samples = 180            # Num of data samples; max = total(csv rows)
    plot_filetype = 'xwin'        # Type of plot file; xwin, pdf, jpeg, png
    plot_color = 'RED'            # Plot color; red, yellow, blue; orange; magenta, white, green
    axes_pos_x = 450              # Position of axes of lower left corner - x co-ordinate
    axes_pos_y = 1800             # Position of axes of lower left corner - y co-ordinate
    axes_len_l = 2200             # Length of axes on x-side
    axes_len_h = 1200             # Height of axes on y-side
    x_axis_name = 'INTERVAL'      # Name of x-axis
    y_axis_name = param.upper()   # Name of y-axis
    x_step = 10                   # values b/w x-axis labels ; modify based on data_samples size
    y_step = 1000                 # values b/w y-axis labels ; modify based on max value of param
    x_axis_ticks = 600            # ticks b/w x-axis labels ; Resolution along x-axis
    y_axis_ticks = 1000           # ticks b/w y-axis labels ; Resoluti

    # GLOBAL VARIABLE FOR PARSED CSV NAME
    parsedfile = '%s.csv' %(param)

    # First Parse flatfile
    vdParser(flatfile, param, parsedfile)
    # Second, Get vital i/o stats
    processedDict = vdProcessor(parsedfile, param)
    # Create the plot
    dislinPlot(processedDict["x-range"], processedDict["y-range"], processedDict["max-param"])
