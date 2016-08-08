### Edit the below lines  
source="test1 test2"
destination="/usr/local/bin/"
serviceName="istgt"
### Edit Stop
jls | sed 1d | awk '{print $1}' > id
jls | sed 1d | awk '{print $2}' > ip
jls | sed 1d | awk '{print $3}' > address
jls | sed 1d | awk '{print $4}' > path
count=0
iteration=`cat id | wc -l`
while [ $count -ne $iteration ]
do
	count=`expr $count + 1`
	jailID=`sed -n "$count"p id`
	echo "Stopping the $jailID jail"
	jexec $jailID service $serviceName onestop
	sleep 2
	jexec $jailID service $serviceName onestatus | grep "not running"
	if [ $? -ne 0 ]
	then
		echo "Failed Stopping of Service $service in the Jail $jailID"
		exit
	fi
	destinationJailPath=`sed -n "$count"p path`
	cp -v $source $destinationJailPath$destination 
	echo "Starting the $jailID jail"
	jexec $jailID service $serviceName onestart
	sleep 2
	jexec $jailID service $serviceName onestatus | grep "running as pid"
	if [ $? -ne 0 ]
	then
		echo "Failed Starting of Service $service in the Jail $jailID"
		exit
	fi
done
