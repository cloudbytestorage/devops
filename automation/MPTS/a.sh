set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

### Generate Smoke Test
##Usage Style
##python *.py config.txt 
##python parsedata.py config.txt nodeIP nodePassword PoolName outputFileName
##python verifyDedup.py config.txt nodeIP nodePassword PoolName
##python verifyMetaSize.py config.txt nodeIP nodePassword PoolName
##python verifyMetaDevices.py config.txt PoolName 

> results/result.csv

sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

python createDisableSCSI.py regression.txt 20.10.57.103 test logs/disablescsi.txt
should_exit $?

python updateDetails.py smoketest.txt
should_exit $?

python Site.py smoketest.txt
should_exit $?

python HACluster.py smoketest.txt
should_exit $?

python Node.py smoketest.txt
should_exit $?

python Jbod.py smoketest.txt
should_exit $?

python apikey_get.py raidz2.txt
should_exit $?
python Pool.py raidz2.txt
should_exit $?
python addVDev.py raidz2.txt
should_exit $?
python parseData.py raidz2.txt 20.10.57.103 test PoolRaidz2 logs/output/PoolRaidz2
should_exit $?
python verifyMetaDevices.py raidz2.txt PoolRaidz2
should_exit $?
python delete.py raidz2.txt Pool
should_exit $?

python apikey_get.py mirror.txt
should_exit $?
python Pool.py mirror.txt
should_exit $?
python addVDev.py mirror.txt
should_exit $?
python parseData.py mirror.txt 20.10.57.103 test PoolMirror logs/output/PoolMirror
should_exit $?
python verifyMetaDevices.py mirror.txt PoolMirror
should_exit $?
python delete.py mirror.txt Pool
should_exit $?

python apikey_get.py raidz1.txt
should_exit $?
python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt 20.10.57.103 test PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

sh ConfigurationFromCSV.sh regression.csv
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

#python verifyDedup.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?
#python verifyMetaSize.py regression.txt 20.10.57.103 test PoolRaidz1 
#should_exit $?

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
python vlanDelete.py regression.txt
should_exit $?

python staticIPAdd.py regression.txt     
should_exit $?
python staticIPDelete.py regression.txt
should_exit $?
python staticIPAdd.py regression.txt     
should_exit $?
python staticIPDelete.py regression.txt
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


python Accounts.py smoketest.txt
should_exit $?

python Tsm.py smoketest.txt
should_exit $?

python ISCSIVolume.py smoketest.txt
should_exit $?

python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

python NFSVolume.py smoketest.txt
should_exit $?

python setNFSclients.py smoketest.txt
should_exit $?

python CIFSVolume.py smoketest.txt
should_exit $?

python setCIFSAuthentication.py smoketest.txt
should_exit $?

python FCVolume.py smoketest.txt
should_exit $?

#python dataIntegrity.py
python execution.py smoketest.txt
should_exit $?

python Version.py smoketest.txt
should_exit $?

sh mail.sh
should_exit $?

