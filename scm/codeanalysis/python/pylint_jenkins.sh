####### Below script checks for the new errors or warnings introduced  #######
#note that the path where this script should run is relative to jenkins job
#pylint.log is created from pylint.cfg file which has all the rules defined
#the rules which are not required can be disabled in the .cfg files.
var1=$(grep -i \|error* pylint.log  | head -1  | cut -c32); #searching for the pattern error in pylint.log
var2=$(grep -i \|error* pylint.log  | head -1  | cut -c33-37); #taking the  error symbols into variables
echo $var1
if [ $var1 == = ]
	then
	echo " The checkin is Good to go"
elif [ $var1 == + ]
	then
	echo " The previous checkin has introduced $var2 errors in the build hence failing the build!!!"
	exit 1;   
elif [ $var1 == - ]
	then
	echo  " The previous checkin has removed $var2 errors"
else
	echo "None of condition are met there is some problem with the build job!!!  Please check it!!!"

fi 
