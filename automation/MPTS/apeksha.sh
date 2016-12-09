set -o history -o histexpand
should_exit(){
    if [ $1 -ne 0 ];
    then
        echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
        exit
    fi
}
'''

########### get api key for all config files
python apikey_get.py expandVol.txt
python apikey_get.py raidzSameName.txt
python apikey_get.py raidzSameDisk.txt
python apikey_get.py tpAlert.txt
python apikey_get.py spaceReclaim.txt
python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt



###### expansion of volumes
## creating volumes
python ISCSIVolume.py expandVol.txt
should_exit $?
python NFSVolume.py expandVol.txt
should_exit $?
python CIFSVolume.py expandVol.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt
should_exit $?
python setNFSclients.py expandVol.txt
should_exit $?
python setCIFSAuthentication.py expandVol.txt
should_exit $?
## execute
python execution.py expandVol.txt all
should_exit $?
## expand
python expandVol.py expandVol.txt all 3
should_exit $?
## execute after expand
python executeExpand.py expandVol.txt all
should_exit $?



###### creating volumes with same name -- negative testcase
## creating volumes
python ISCSIVolume.py expandVol.txt negative
should_exit $?
python NFSVolume.py expandVol.txt negative
should_exit $?
python CIFSVolume.py expandVol.txt negative
should_exit $?


####### creating pool with same name -- negative testcase
python Pool.py raidzSameName.txt negative


####### creating pool with same disk -- negative testcase
python Pool.py raidzSameDisk.txt negative



####### thin provisioning alert for volume
## creating volume
python ISCSIVolume.py tpAlert.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py tpAlert.txt
should_exit $?
## dump 85% data
python execution.py tpAlert.txt iscsi create linuxmint-13-mate-dvd-64bit.iso
should_exit $?

sleep 300
## check for thin provisioning alert
python tpAlerts.py tpAlert.txt volume 2
should_exit $?
## expand
python expandVol.py tpAlert.txt iscsi 1
should_exit $?
sleep 300
## check for increased space alert
python tpAlerts.py tpAlert.txt volume 1
should_exit $?


####### space reclamation
## creating volumes
python ISCSIVolume.py spaceReclaim.txt
should_exit $?
python NFSVolume.py spaceReclaim.txt
should_exit $?
python CIFSVolume.py spaceReclaim.txt
should_exit $?
## enabling the initiators
python setISCSIInitiatorGroup.py spaceReclaim.txt
should_exit $?
python setNFSclients.py spaceReclaim.txt
should_exit $?
python setCIFSAuthentication.py spaceReclaim.txt
should_exit $?
## reclaim space
python spaceReclaim.py spaceReclaim.txt 20.10.57.103 test all
should_exit $?

'''

####### creating/deleting volumes duing copy process going on iscsi volumes
python ISCSIVolume.py copyVol.txt
should_exit $?
python setISCSIInitiatorGroup.py copyVol.txt
should_exit $?
sleep 10
sh copyIscsi.sh
should_exit $?



####### creating/deleting volumes duing copy process going on nfs volumes
python NFSVolume.py copyVol.txt
should_exit $?
python setNFSclients.py copyVol.txt
should_exit $?
sleep 10
sh copyNfs.sh
should_exit $?




'''
## getting version
python Version.py expandVol.txt
should_exit $?
## mailing
sh mail.sh
should_exit $?

