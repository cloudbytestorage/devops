#!/bin/sh
echo "Enter tsm ip "

read ip

iscsiadm -m discovery -t sendtargets -p $ip | cut -d " " -f 2 > iqnlist

echo "Enter 1 for login session or 2 for logout session"

read option

if [ $option -eq 1 ]; then
        while read iqn
        do
                iscsiadm --mode node --targetname $iqn --portal $ip:3260 --login
                done < iqnlist
else
        while read iqn
        do

                iscsiadm --mode node --targetname $iqn --portal $ip:3260 --logout

        done < iqnlist
fi

