for((i=100;i>0;i--))
do
    echo "Will sleep for another $i secs"
    sleep 10
    i=`expr $i - 10`
done
exit
iscsiadm -m node  > /tmp/test
while read line
do
    echo $line
    ip=`echo $line | cut -d "," -f 1`
    iqn=`echo $line | cut -d " " -f 2`
    iscsiadm -m node --targetname  $iqn --portal "$ip" --logout
done < /tmp/test
iscsiadm -m node -o delete
exit

python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
python deleteHAAdmin.py regression.txt
should_exit $?
python addHAAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifyHAAdmin.py regression.txt
should_exit $?
