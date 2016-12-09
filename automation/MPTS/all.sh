set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

rpcbind restart
cd /root/automation/2.0.0/

#### to create the configuration
sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

#### to run BST and MPTS
sh automation.sh
should_exit $?

### Sending mail to Team
sh mail.sh
should_exit $?
