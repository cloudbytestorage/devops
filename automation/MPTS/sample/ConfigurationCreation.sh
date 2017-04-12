#!/bin/bash
mkdir mount temp logs results previous_results > /dev/null 2>&1
umount -a -t cifs -l
umount -a -t cifs -l
umount -fa
umount -fa
rm temp/*
rm logs/*
rm -rf mount/*
>temp/site.txt; >temp/account.txt; >temp/tsm.txt; >temp/nfsvolume.txt; >temp/iscsivolume.txt; >temp/cifsvolume.txt; >config.txt; >logs/tracktime;
> results/result.csv; > previous_results/result.csv; >results/config_creation_result.csv; >previous_results/config_creation_result.csv

cp sample/creation.py .
cp sample/execution.py .
cp sample/fdisk_response_file .
QUIT=y
NoofTSMs=0
NoofNFSVolumes=0
NoofISCSIVolumes=0
NoofCIFSVolumes=0

echo "Configuration File Creation Begins"

##### To Create Sites 
echo -en Do you want to configure the Site Press "\033[32m y \033[0m" else "\033[32m n \033[0m" : 
echo ""
read line
if [ "$line" == "y" ] || [ "$line" == "Y" ]
then
    echo -en Enter the"\033[32m Number of Sites \033[0m"to be created
    echo ""
    read line
    echo "  \"Number_of_Sites\": \"$line\", " >> temp/site.txt
    echo "" >> temp/site.txt
    for ((i=1; i<=$line; i++))
    do
        cat sample/site.txt >> temp/site.txt
        sed -i s/_#MyVaLuE#_/$i/g temp/site.txt
    done
else
    echo "Continuing with next step"
fi

##### To Create Accounts
echo ""
echo -en Do you want to configure Accounts Press "\033[32m y \033[0m" else "\033[32m n \033[0m" : 
echo ""
read line
if [ "$line" == "y" ] || [ "$line" == "Y" ]
then
    echo -en Enter the"\033[32m Number of Accounts \033[0m"to be created
    echo ""
    read line
    echo "  \"Number_of_Accounts\": \"$line\", " >> temp/account.txt
    echo "" >> temp/account.txt
    echo -en Enter the"\033[32m Account Name \033[0m"
    echo ""
    read accountname
    for ((i=1; i<=$line; i++))
    do
        cat sample/account.txt >> temp/account.txt
        sed -i s/_#MyVaLuE#_/$i/g temp/account.txt
        sed -i s/ACCOUNT/$accountname/g temp/account.txt
    done
else
    echo "Continuing with next step"
fi

##### To Create TSMs
while [ "$QUIT" == "y" ] || [ "$QUIT" == "y" ]
do
    echo ""
    echo -en Do you want to configure TSM Press "\033[32m y \033[0m" else "\033[32m n \033[0m" : 
    echo ""
    read line
    if [ "$line" == "y" ] || [ "$line" == "Y" ]
    then
        NoofTSMs=`expr $NoofTSMs + 1`
        echo ""  >> temp/tsm.txt
        echo -en  Enter the "\033[32m TSM Name \033[0m"
        echo ""
        read tsmname
        echo -en Enter the"\033[32m Pool Name \033[0m"you have to associate the TSM 
        echo ""
        read poolname
        echo -en Enter the"\033[32m Account Name \033[0m"you have to associate the TSM
        echo ""
        read accountname
        echo -en Enter the"\033[32m IP Address \033[0m"you have to associate the TSM
        echo ""
        read ipaddress
        echo -en Enter the"\033[32m Interface \033[0m"you have to associate the TSM
        echo ""
        read interface
        cat sample/tsm.txt >> temp/tsm.txt
        sed -i s/_#MyVaLuE#_/$NoofTSMs/g temp/tsm.txt
        sed -i s/TSMNAME/$tsmname/g temp/tsm.txt
        sed -i s/POOLNAME/$poolname/g temp/tsm.txt
        sed -i s/ACCOUNTNAME/$accountname/g temp/tsm.txt
        sed -i s/IPADDRESS/$ipaddress/g temp/tsm.txt
        sed -i s/INTERFACE/$interface/g temp/tsm.txt
    else
        echo "Continuing with next step"
    fi

    ##### To Create NFS Volumes
    echo ""
    echo -en Do you want to configure NFS Volumes for the $tsmname "\033[32m y \033[0m" else "\033[32m n \033[0m" : 
    echo ""
    read line
    if [ "$line" == "y" ] || [ "$line" == "Y" ]
    then
        echo -en Enter the"\033[32m Number of NFS Volumes \033[0m"to be created
        echo ""
        read line
        echo -en Enter the"\033[32m NFS Volumes Name \033[0m"
        echo ""
        read nfsname
        echo "" >> temp/nfsvolume.txt
        temp=`expr $NoofNFSVolumes + 1`
        NoofNFSVolumes=`expr $NoofNFSVolumes + $line`
        #echo -en Enter the"\033[32m Pool Name \033[0m"you have to associate the NFS Volume
        #echo ""
        #read poolname
        #echo -en Enter the"\033[32m Account Name \033[0m"you have to associate the NFS Volume
        #echo ""
        #read accountname
        #echo -en Enter the"\033[32m TSM Name \033[0m"you have to associate the NFS Volume
        #echo ""
        #read tsmname
        for ((i=temp; i<=$NoofNFSVolumes; i++))
        do
            cat sample/nfsvolume.txt >> temp/nfsvolume.txt
            sed -i s/_#MyVaLuE#_/$i/g temp/nfsvolume.txt
            sed -i s/NFSVOLUMENAME/$nfsname/g temp/nfsvolume.txt
        done
        sed -i s/POOLNAME/$poolname/g temp/nfsvolume.txt
        sed -i s/TSMNAME/$tsmname/g temp/nfsvolume.txt
        sed -i s/ACCOUNTNAME/$accountname/g temp/nfsvolume.txt
        sed -i s/IPADDRESS/$ipaddress/g temp/nfsvolume.txt
        
    else
        echo "Continuing with next step"
    fi

    ##### To Create iSCSI Volumes
    echo ""
    echo -en Do you want to configure iSCSI Volumes for the $tsmname "\033[32m y \033[0m" else "\033[32m n \033[0m" : 
    echo ""
    read line
    if [ "$line" == "y" ] || [ "$line" == "Y" ]
    then
        echo -en Enter the"\033[32m Number of iSCSI Volumes \033[0m"to be created
        echo ""
        read line
        echo -en Enter the"\033[32m iSCSI Volumes Name \033[0m"
        echo ""
        read iscsiname
        echo "" >> temp/iscsivolume.txt
        temp=`expr $NoofISCSIVolumes + 1`
        NoofISCSIVolumes=`expr $NoofISCSIVolumes + $line`
        #echo -en Enter the"\033[32m Pool Name \033[0m"you have to associate the iSCSI Volume
        #echo ""
        #read poolname
        #echo -en Enter the"\033[32m Account Name \033[0m"you have to associate the iSCSI Volume
        #echo ""
        #read accountname
        #echo -en Enter the"\033[32m TSM Name \033[0m"you have to associate the iSCSI Volume
        #echo ""
        #read tsmname
        for ((i=temp; i<=$NoofISCSIVolumes; i++))
        do
            cat sample/iscsivolume.txt >> temp/iscsivolume.txt
            sed -i s/_#MyVaLuE#_/$i/g temp/iscsivolume.txt
            sed -i s/ISCSIVOLUMENAME/$iscsiname/g temp/iscsivolume.txt
        done
        sed -i s/POOLNAME/$poolname/g temp/iscsivolume.txt
        sed -i s/TSMNAME/$tsmname/g temp/iscsivolume.txt
        sed -i s/ACCOUNTNAME/$accountname/g temp/iscsivolume.txt
        sed -i s/IPADDRESS/$ipaddress/g temp/iscsivolume.txt
    else
        echo "Continuing with next step"
    fi
    ##### To Create CIFS Volumes
    echo ""
    echo -en Do you want to configure CIFS Volumes for the $tsmname "\033[32m y \033[0m" else "\033[32m n \033[0m" : 
    echo ""
    read line
    if [ "$line" == "y" ] || [ "$line" == "Y" ]
    then
        echo -en Enter the"\033[32m Number of CIFS Volumes \033[0m"to be created
        echo ""
        read line
        echo -en Enter the"\033[32m CIFS Volumes Name \033[0m"
        echo ""
        read cifsname
        echo "" >> temp/cifsvolume.txt
        temp=`expr $NoofCIFSVolumes + 1`
        NoofCIFSVolumes=`expr $NoofCIFSVolumes + $line`
        #echo -en Enter the"\033[32m Pool Name \033[0m"you have to associate the CIFS Volume
        #echo ""
        #read poolname
        #echo -en Enter the"\033[32m Account Name \033[0m"you have to associate the CIFS Volume
        #echo ""
        #read accountname
        #echo -en Enter the"\033[32m TSM Name \033[0m"you have to associate the CIFS Volume
        #echo ""
        #read tsmname
        for ((i=temp; i<=$NoofCIFSVolumes; i++))
        do
            cat sample/cifsvolume.txt >> temp/cifsvolume.txt
            sed -i s/_#MyVaLuE#_/$i/g temp/cifsvolume.txt
            sed -i s/CIFSVOLUMENAME/$cifsname/g temp/cifsvolume.txt
        done
        sed -i s/POOLNAME/$poolname/g temp/cifsvolume.txt
        sed -i s/TSMNAME/$tsmname/g temp/cifsvolume.txt
        sed -i s/ACCOUNTNAME/$accountname/g temp/cifsvolume.txt
        sed -i s/IPADDRESS/$ipaddress/g temp/cifsvolume.txt
    else
        echo "Continuing with next step"
    fi


    echo -en To Continue creating TSM... Press "\033[32m y \033[0m" else "\033[32m n \033[0m" :
    echo ""
    read QUIT
    echo ""
    echo ""
done
#echo ""
#echo -en Do you want to write the configuration files "\033[32m y \033[0m" else "\033[32m n \033[0m" : 
#echo ""
#read line
sed -i '1s/^/  \"Number_of_NFSVolumes\": \"NoofNFSVolumes\",/' temp/nfsvolume.txt
sed -i '1s/^/  \"Number_of_TSMs\": \"NoofTSMS\",/' temp/tsm.txt
sed -i '1s/^/  \"Number_of_ISCSIVolumes\": \"NoofISCSIVolumes\",/' temp/iscsivolume.txt
sed -i '1s/^/  \"Number_of_CIFSVolumes\": \"NoofCIFSVolumes\",/' temp/cifsvolume.txt
sed -i s/NoofNFSVolumes/$NoofNFSVolumes/g temp/nfsvolume.txt
sed -i s/NoofTSMS/$NoofTSMs/g temp/tsm.txt
sed -i s/NoofISCSIVolumes/$NoofISCSIVolumes/g temp/iscsivolume.txt
sed -i s/NoofCIFSVolumes/$NoofCIFSVolumes/g temp/cifsvolume.txt
###Aggregating config files
cat sample/header.txt >> config.txt
cat temp/site.txt >> config.txt
cat sample/cluster_pool.txt >> config.txt
cat temp/account.txt  >> config.txt
cat temp/tsm.txt >> config.txt
cat temp/nfsvolume.txt  >> config.txt
cat temp/iscsivolume.txt >> config.txt
cat temp/cifsvolume.txt >> config.txt
cat sample/trailer.txt >> config.txt
###Aggregating config files
echo "No of TSMs = $NoofTSMs"
echo "No of NFS Volumes = $NoofNFSVolumes "
echo "No of ISCSI Volumes = $NoofISCSIVolumes"
echo "No of CIFS Volumes = $NoofCIFSVolumes"
echo "Configuration File Creation Done"
exit
#### Script Ends Here

echo ""
echo -en Enter "\033[32m I Agree \033[0m" Do the Configuration or Press Any Key to abort to run the rest api calls
echo ""
read line
if [ "$line" == "I Agree" ]
then
    echo "Start time`date`" >> logs/tracktime
    python creation.py
    echo "End time`date`" >> logs/tracktime
else
    echo -en You have aborted the configuration --- Run the command"\033[32m python creation.py \033[0m"to do the configuraion
    echo ""
    exit
fi

