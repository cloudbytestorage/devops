set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}
'''
#### to create the configuration
sh ConfigurationFromCSV.sh final.csv
should_exit $?
python apikey_get.py final.txt
should_exit $?


#### creating tsms
python Tsm.py final.txt
should_exit $?


#### creating iscsi volume
python -u ISCSIVolume.py final.txt
should_exit $?
python -u setISCSIInitiatorGroup.py final.txt all
should_exit $?
'''
### creating nfs volumes
python NFSVolume.py final.txt
should_exit $?
python setNFSclients.py final.txt
should_exit $?
'''
#### attaching iscsi volumes to vms as rdm
python -u esxIscsi.py
should_exit $?
python -u vmlrdmcopy.py final.txt
should_exit $?

'''
####attaching nfs volumes to vms
sh esxmain.sh
should_exit $?
