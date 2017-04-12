#!/bin/bash

set -o history -o histexpand
should_exit(){
    if [ $1 -ne 0 ];
    then
        echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
        exit
    fi
}

>/tmp/cifs1.txt
python -u CIFSVolume.py copyVol.txt
should_exit
python -u setCIFSAuthentication.py copyVol.txt
should_exit
python -u mountCifs.py copyVol.txt mount 2>&1  >> /tmp/cifs1.txt
should_exit

cp linuxmint-13-mate-dvd-64bit.iso mount/Account1copyCIFS1 & 2>&1 >> /tmp/cifs1.txt &
should_exit
sleep 60

echo $!
date1=`date`
pid=`ps -eaf | grep "cp linuxmint-13-mate-dvd-64bit.iso mount/Account1copyCIFS1" | grep -v "grep" | awk '{print $2}'`
echo $pid

python CIFSVolume.py dummyVol.txt 
should_exit $?

sleep 60

python delete.py dummyVol.txt cifs
should_exit $?
ps -eaf | grep "cp linuxmint-13-mate-dvd-64bit.iso mount/Account1copyCIFS1" | grep $pid
x=`echo$?`
count=0
echo entered loop
sleep 1200
#count=`expr $count + 1`
if `ps -eaf | grep "cp linuxmint-13-mate-dvd-64bit.iso mount/Account1copyCIFS1" | grep -v "grep" | awk '{print $2}'` -eq $pid
then
    kill -9 $pid 
    date2=`date`
    echo  $date1, $pid of prccess - python execution.py copyVol.txt cifs is killed due to timeout copy failed during creation/deletion of volumes , FAILED ,,$date2  >> results/result.csv
    exit
fi

python mountCifs.py copyVol.txt umount
should_exit
python delete.py copyVol.txt cifs
should_exit
date2=`date`
echo $date1, creation/deletion of volumes successfull during copy process going on cifs volume, PASSED ,,$date2  >> results/result.csv

