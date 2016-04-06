####### Below script checks for the new errors or warnings introduced  #######

var1=$(grep -i \|error* pylint.log  | head -1  | cut -c32);
var2=$(grep -i \|error* pylint.log  | head -1  | cut -c33-37);
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
