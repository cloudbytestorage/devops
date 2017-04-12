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

python apikey_get.py regression.txt 
should_exit $?

for((i=0; i<5; i++))
do
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

    python execution.py regression.txt
    should_exit $?

    python delete.py regression.txt NFS CIFS FC ISCSI TSM ACC
    should_exit $?
done

python Version.py regression.txt
should_exit $?

cat results/results.txt

