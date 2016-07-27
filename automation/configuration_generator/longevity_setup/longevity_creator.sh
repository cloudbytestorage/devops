
set -o history -o histexpand
should_exit(){
        if [ $1 -ne 0 ];
        then
            echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
            exit
        fi
}

#creating configuratio...
sh ConfigurationFromCSV.sh smoketest.csv
should_exit $?

#setting apikey...
python apikey_set.py smoketest.txt

#getting apikey to configuration file...
python apikey_get.py smoketest.txt

python Pool.py smoketest.csv
should_exit $?

#creating TSMs...
python Tsm.py smoketest.txt
should_exit $?

#creating NFS volumes...
python NFSVolume.py smoketest.txt
should_exit $?

#setting NFS clients to ALL...
python setNFSclients.py smoketest.txt
should_exit $?

#creating iSCSI volumes...
python ISCSIVolume.py smoketest.txt
should_exit $?

#setting iscsi Initiator group to All...
python setISCSIInitiatorGroup.py smoketest.txt
should_exit $?

#creating CIFS volumes...
python CIFSVolume.py smoketest.txt
should_exit $?

#creating FC volumes...
#python FCVolume.py smoketest.txt
#should_exit $?
