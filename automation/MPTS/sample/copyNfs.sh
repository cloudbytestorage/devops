#!/bin/bash

set -o history -o histexpand
should_exit(){
    if [ $1 -ne 0 ];
    then
        echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
        exit
    fi
}

>/tmp/nfs1.txt
python -u execution.py copyVol.txt nfs create /cloudbyte/data/linuxmint-13-mate-dvd-64bit.iso 2>&1  >> /tmp/nfs1.txt & 
echo $!
date1=`date`
pid=`ps -eaf | grep "python -u execution.py copyVol.txt nfs" | grep -v "grep" | awk '{print $2}'`
echo $pid

python NFSVolume.py dummyVol.txt 
should_exit $?

python setNFSclients.py dummyVol.txt
should_exit $?

sleep 30

python delete.py dummyVol.txt nfs
should_exit $?
`ps -eaf | grep "python -u execution.py copyVol.txt nfs" | grep $pid`
x=`echo $?`
count=0
while  [ "$x" -ne 1 ];
do
    echo entered loop
    count=`expr $count + 1`
    if [ "$count" -eq 100 ];
    then
        kill -9 $pid 
        date2=`date`
        echo  $date1, $pid of prccess - python execution.py copyVol.txt nfs is killed due to timeout copy failed during creation/deletion of volumes , FAILED ,,$date2  >> results/result.csv
        exit
    fi
    `ps -eaf | grep "python -u execution.py copyVol.txt nfs" | grep $pid`
    x=`echo $?`
    sleep 1
done

date2=`date`
echo $date1, creation/deletion of volumes successfull duing copy process going on nfs volume, PASSED ,,$date2  >> results/result.csv
