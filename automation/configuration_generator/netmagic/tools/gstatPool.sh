> /tmp/t1
poolname=$1
echo "Script to print gstat for the Pool"
#zpool status $1 | awk '{print $1}' | grep multipath > /tmp/t
zpool list | awk '{print $1}' | grep $1 
if [ $? -ne 0 ]
then 
    zpool list | awk '{print $1}' | sed s/NAME//
    echo ""
    echo "Enter the Pool Name from the available Poollist"
    read poolname
fi
zpool status $poolname | awk '{print $1}' | grep multipath > /tmp/t
while read line
do
    gmultipath status | grep "$line" | awk '{print "^"$3"$|"}' >> /tmp/t1
done < /tmp/t
echo "end" >> /tmp/t1
a=`cat /tmp/t1`
echo $a
b=`echo $a | sed s/\ //g`
echo $b
gstat -d -f  "$b"
