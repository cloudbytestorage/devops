#!/bin/bash

REPOS="$1"
REVISION="$2"

SVNLOOK=/usr/bin/svnlook

#checking if the bugzilla id is valid


bugid=$(grep -i 'BUG-' /svnrepo/esmgmt/hooks/bugzilla.log | cut -d- -f2 | cut -d] -f1,1  )
echo $bugid

if [ $bugid -eq 0 ] || [ $bugid  -eq 00 ] ||  [ $bugid -eq 000 ] || [ $bugid -eq 0000 ]
	then
	echo "This is not a valid bug"
else
	echo "Write the expect condition here"
	echo "$REPOS  $REVISION"  
	expect -f /svnrepo/esmgmt/hooks/bugzilla.expect  10.30.1.0 root qaprod123 $bugid $REPOS $REVISION
fi


    

