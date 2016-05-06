#!/bin/bash

REPOS="$1"
TXN="$2"

SVNLOOK=/usr/bin/svnlook

#checking if the bugzilla id is valid

/usr/bin/svnlook dirs-changed -t  "${TXN}" "${REPOS}"   | grep 'es1.4.0.p5'

# change the above pattern to branch needed 'es1.4.0.p6'

var1=($?)
#echo "var1=  $var1"
if [ $var1 == 0 ];
then
echo " the change is made in P5 "

bugid=$(/usr/bin/svnlook log -t $TXN $REPOS  | grep -i 'BUG-'| cut -d- -f2 | cut -d] -f1,1)
echo "this is bug id: $bugid"
echo $TXN
#bugid=9999

if [ $bugid -eq 0 ] || [ $bugid  -eq 00 ] ||  [ $bugid -eq 000 ] || [ $bugid -eq 0000 ]
        then
        echo "This is not a valid bug for P5 ! ! Please put the correct BUG ID from bugzilla "
        exit 1;
else
        echo "Write the expect condition here"
        #"this part will check if the bug given by user is a valid bug or not"
        echo "$REPOS  $TXN"
        #expect -f /svnrepo/esmgmt/hooks/bugzilla_verifybug.expect  10.30.1.0 root qaprod123 $bugid $REPOS $TXN
fi


else
echo " the change not made in p5 "
fi

/usr/bin/svnlook dirs-changed -t  "${TXN}" "${REPOS}"   | grep 'es13-netmagic-patch09'

# change the above pattern to branch needed  ex: 'es1.4.0.p6'

var1=($?)
#echo "var1=  $var1"
if [ $var1 == 0 ];
then
echo " the change is made in es13-netmagic-patch09 branch "
bugid=$(/usr/bin/svnlook log -t $TXN $REPOS  | grep -i 'BUG-'| cut -d- -f2 | cut -d] -f1,1)
echo "this is bug id: $bugid"
echo $TXN
#bugid=9999

if [ $bugid -eq 0 ] || [ $bugid  -eq 00 ] ||  [ $bugid -eq 000 ] || [ $bugid -eq 0000 ]
        then
        echo "This is not a valid bug for es13-netmagic-patch09 ! Please put the correct BUG ID from bugzilla "
        exit 1;
else
        echo "Write the expect condition here"
        #"this part will check if the bug given by user is a valid bug or not"
        echo "$REPOS  $TXN"
       # expect -f /svnrepo/esmgmt/hooks/bugzilla_verifybug.expect  10.30.1.0 root qaprod123 $bugid $REPOS $TXN
fi

else
echo " the change not made in netmagic 09 branch "
fi

#check for p6
/usr/bin/svnlook dirs-changed -t  "${TXN}" "${REPOS}"   | grep 'es1.4.0.p6'

# change the above pattern to branch needed 'es1.4.0.p6'

var1=($?)
#echo "var1=  $var1"
if [ $var1 == 0 ];
then
echo " the change is made in P6 "

bugid=$(/usr/bin/svnlook log -t $TXN $REPOS  | grep -i 'BUG-'| cut -d- -f2 | cut -d] -f1,1)
echo "this is bug id: $bugid"
echo $TXN
#bugid=9999

if [ $bugid -eq 0 ] || [ $bugid  -eq 00 ] ||  [ $bugid -eq 000 ] || [ $bugid -eq 0000 ]
        then
        echo "This is not a valid bug for P6 ! ! Please put the correct BUG ID from bugzilla "
        exit 1;
else
        echo "Write the expect condition here"
        #"this part will check if the bug given by user is a valid bug or not"
        echo "$REPOS  $TXN"
        #expect -f /svnrepo/esmgmt/hooks/bugzilla_verifybug.expect  10.30.1.0 root qaprod123 $bugid $REPOS $TXN
fi


else
echo " the change not made in p6 "
fi
#check ends
