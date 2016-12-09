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

python createDisableSCSI.py final.txt NODEIP1 NODEPASSWORD1 logs/disablescsi.txt
should_exit $?

python apikey_get.py final.txt
should_exit $?

python updateDetails.py final.txt
should_exit $?

python Site.py final.txt
should_exit $?

python HACluster.py final.txt
should_exit $?

python Node.py final.txt
should_exit $?

python Jbod.py final.txt
should_exit $?
python apikey_get.py raidz1.txt
should_exit $?

python Pool.py raidz1.txt
should_exit $?
python addVDev.py raidz1.txt 
should_exit $?
python parseData.py raidz1.txt NODEIP1 NODEPASSWORD1 PoolRaidz1 logs/output/PoolRaidz1
should_exit $?
python verifyMetaDevices.py raidz1.txt PoolRaidz1
should_exit $?

python Accounts.py final.txt
should_exit $?
python Tsm.py final.txt
should_exit $?

python ISCSIVolume.py final.txt
should_exit $?
python setISCSIInitiatorGroup.py final.txt
should_exit $?


python esxIscsi.py
should_exit $?

python vmlrdmcopy.py final.txt
#sh mail.sh
#should_exit $?


