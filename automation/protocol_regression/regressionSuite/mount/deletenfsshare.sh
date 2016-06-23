echo "Enter name of datsatore to be deleted "
read name
 esxcli storage nfs list |cut -d "-" -f 2 |cut -d " " -f 1|grep $name > /scripts/share

       while read line
       do
              esxcli storage nfs remove -v $line
      
	done < /scripts/share

