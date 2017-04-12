
#sh ConfigurationFromCSV.sh final.csv

python addNfsEsx.py final.txt

No_of_VMs=`cat final.txt | grep "Number_of_NFS_VMs" | awk -F' ' '{print $2}' | awk -F'"' '{print $2}'`
i=1
while [ $i -le $No_of_VMs ]
do
    datastorename=`grep nfsdatastoreName$i final.txt | awk '{print $2}' | sed s/\"//g |sed s/\,//g`
    vmname=`grep nfsvmName$i final.txt | awk '{print $2}' | sed s/\"//g |sed s/\,//g`
    #size=`grep nfsvmfsSize$i final.txt | awk '{print $2}' | sed s/\"//g |sed s/\,//g`
    echo $datastorename
    echo $vmname
    python mapNfsDatastoreToVM.py final.txt $i $vmname $datastorename
    i=`expr $i + 1`
done

