i=0
echo "Enter datastore name to be added "
read name

	while read line
	do
  		if [[ ! -z $line ]]; then
			
			folder=${name}${i}
  			a=$line
  			#echo "cool = $a"
  			echo $folder
  			esxcli storage nfs add -H TSMIP -s $line -v $folder
  		fi	
  		i=$(( ${i} + 1 ))
done < /scripts/esxtest

