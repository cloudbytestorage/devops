set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

sh ConfigurationFromCSV.sh regression.csv
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py 
should_exit $?
python verifyMetaDevices.py raidz2.txt
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py 
should_exit $?
python verifyMetaDevices.py mirror.txt
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt
should_exit $?
python parseData.py 
should_exit $?
python verifyMetaDevices.py raidz1.txt
should_exit $?


python apikey_get.py regression.txt
should_exit $?
python Accounts.py regression.txt
should_exit $?

python Tsm.py regression.txt
should_exit $?

python ISCSIVolume.py regression.txt
should_exit $?

python setISCSIInitiatorGroup.py regression.txt
should_exit $?

python NFSVolume.py regression.txt
should_exit $?

python setNFSclients.py regression.txt
should_exit $?

python CIFSVolume.py regression.txt
should_exit $?

python setCIFSAuthentication.py regression.txt
should_exit $?


python verifyDedup.py regression.txt
should_exit $?
python verifyMetaSize.py regression.txt
should_exit $?

python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?
python deleteSiteAdmin.py regression.txt
should_exit $?
python addSiteAdmin.py regression.txt
should_exit $?
python apikey_set_delegatedAdmin.py regression.txt
should_exit $?
python verifySiteAdmin.py regression.txt
should_exit $?

python vlanAdd.py regression.txt
should_exit $?
python vlanDelete.py regression.txt
should_exit $?
python vlanAdd.py regression.txt
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



python Version.py regression.txt
should_exit $?

cat results/results.csv

