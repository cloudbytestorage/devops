sh ConfigurationFromCSV.sh smoketestold.csv

python apikey_get.py copyVol.txt
python apikey_get.py dummyVol.txt
python apikey_get.py smoketest.txt
#python Tsm.py copyVol.txt

python NFSVolume.py copyVol.txt

python setNFSclients.py copyVol.txt

sleep 10
echo "sleeping for 10 seconds"

sh copyNfs.sh

#python Version.py smoketest.txt

