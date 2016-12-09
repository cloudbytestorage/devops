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
python -u execution.py copyVol.txt nfs create linuxmint-13-mate-dvd-64bit.iso 2>&1  >> /tmp/nfs1.txt &
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
