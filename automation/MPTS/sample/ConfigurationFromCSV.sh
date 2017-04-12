> tmp.csv
> tmp1.csv
> response
> response1
> filename
rm *response

cp sample/automation.sh automation.sh
cp sample/autoiscsi.sh autoiscsi.sh
no_of_disk=`fdisk -l | grep GB | wc -l`

if [ $no_of_disk -eq 1 ]
then
    sed -i 's/\/dev\/sdc/\/dev\/sdb/g' *.py
    sed -i 's/\/dev\/sdd/\/dev\/sdb/g' *.py
elif [ $no_of_disk -eq 2 ]
then
    sed -i 's/\/dev\/sdb/\/dev\/sdc/g' *.py
    sed -i 's/\/dev\/sdd/\/dev\/sdc/g' *.py
elif [ $no_of_disk -eq 3 ]
then
    sed -i 's/\/dev\/sdb/\/dev\/sdd/g' *.py
    sed -i 's/\/dev\/sdc/\/dev\/sdd/g' *.py
fi


if [ $# -eq 0 ]
then
    echo "Enter the CSV file from which Configuration has to be created"
    read response
else
    response=$1
    echo $response
fi

cp $response tmp.csv
sed -i '/TSM Configuration Begins/,$d' tmp.csv
sed -i /"Configuration Begins"/d tmp.csv
sed -i /"Configuration Ends"/d tmp.csv
sed -i s/Begins,//g tmp.csv
sed -i s/,End.*$//g tmp.csv

while read line
do
    echo $line | tr ',' '\n' >> response
    sh -x Creation_Site_to_Pool.sh  < response
    configfile=`echo $response | cut -d "." -f 1`.txt
done < tmp.csv
cp -v config.txt $configfile
echo "Config File Created : $configfile"


cp $response tmp2.csv
sed -i '1,/ESX Configuration ISCSI Begins/d' tmp2.csv
sed -i '/VM Configuration ISCSI Ends/,$d' tmp2.csv
sed -i /"Configuration ISCSI Begins"/d tmp2.csv
sed -i /"Configuration ISCSI Ends"/d tmp2.csv
sed -i s/Begins,//g tmp2.csv
sed -i s/,End.*$//g tmp2.csv
while read line
do
        echo $line | tr ',' '\n' >> response1
        sh -x esxIscsi.sh < response1
        configfile=`echo $response | cut -d "." -f 1`.txt
done < tmp2.csv
cp -v config.txt $configfile
echo "Config File Created : $configfile"

cp $response tmp1.csv
sed -i '1,/TSM Configuration Begins/d' tmp1.csv
sed -i '/TSM Configuration Ends/,$d' tmp1.csv
sed -i /"Configuration Begins"/d tmp1.csv
sed -i /"Configuration Ends"/d tmp1.csv
sed -i s/Begins,//g tmp1.csv
sed -i s/,End.*$//g tmp1.csv
while read line
do
    echo $line | cut -d "," -f 1 >> filename
    file_resp=`echo $line | cut -d "," -f 1`
    echo $line | cut -d "," -f 2-24 | tr ',' '\n' >> $file_resp.response
done < tmp1.csv

awk '!x[$0]++' filename > filename1
while read line
do
    sh -x Creation_TSM_Volume.sh < $line.response
    cp -v config.txt $line
    echo "Config File Created : $line"
    #sleep 1
done < filename1

rm config.txt


