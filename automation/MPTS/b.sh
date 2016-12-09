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



