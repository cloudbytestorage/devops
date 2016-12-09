#! /bin/sh
now=$(date +"%Y-%m-%d-%H-%M-%S");
cd /tmp;

#take backup of config.xml every one hour
cp /cf/conf/config.xml /cf/conf/config.xml.$now;


#remove the old backup files and retain only 10 copies of hourly backup file
if ls /cf/conf/config.xml.* >>/dev/null 2>&1; then
	file_count=`ls -1 /cf/conf/config.xml.* | wc -l`;
	if [ $file_count -gt 10 ]
	then
		remove_file=` ls -t /cf/conf/config.xml.* | tail -n1`;
		rm -f $remove_file;
	fi;
fi


#take backup of config files every day at night between 1AM to 2AM
time=`date +%H`;
if [ $time -ge 15 -a $time -lt 19 ];
then
	#create a temp and copy all config files to that directory. And create a backup tar	
	tempFolder=`hostname`_`date +%s`
	mkdir $tempFolder

	#copy all config files to temp directory
	cp  /cf/conf/config.xml $tempFolder/
	cp  /cf/conf/haconfig.xml $tempFolder/
	cp  /usr/local/agent/listener/ipmi.conf $tempFolder/
	cp  /usr/local/agent/cbc_node_id $tempFolder/
	cp  /usr/local/agent/cbd_node_id $tempFolder/

	#create a tar ball to store the backup
	tar -cvf $tempFolder.tar $tempFolder
	mv  $tempFolder.tar /cf/conf/
	rm -rf $tempFolder
	logger "Backup For `hostname` available at $tempFolder.tar";
	
fi;

#remove old tar ball and retain only last 5 copies
file_name=`hostname`;
if  ls /cf/conf/"$file_name"_*.tar >>/dev/null 2>&1; then
	file_count_bkp=`ls -1 /cf/conf/"$file_name"_*.tar | wc -l`;
	if [ $file_count_bkp -gt 5 ]
	then
		remove_file=`ls -t /cf/conf/"$file_name_"*.tar | tail -n1`;
		rm -f $remove_file;
	fi;
fi

