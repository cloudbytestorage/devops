#!/bin/bash
mkdir mount temp logs results previous_results > /dev/null 2>&1
umount -a -t cifs -l
umount -a -t cifs -l
umount -fa
umount -fa
rm temp/*
rm logs/*
rm -rf mount/*
rm installed_version
>temp/site.txt; >temp/account.txt; >temp/tsm.txt; >temp/nfsvolume.txt; >temp/iscsivolume.txt; >temp/cifsvolume.txt; >temp/fcvolume.txt; >config.txt; >logs/tracktime;
> results/result.csv; > previous_results/result.csv; >results/config_creation_result.csv; >previous_results/config_creation_result.csv

cp sample/creation.py .
cp sample/execution.py .
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
echo -en Enter the"\033[32m Number of Sites \033[0m"to be created
echo ""
read noof_sites
echo  -en Enter the"\033[32m Site Name \033[0m"
echo ""
read sitename
if [ "$line" == "y" ] || [ "$line" == "Y" ]
then
    echo "  \"Number_of_Sites\": \"$noof_sites\", " >> temp/site.txt
    echo "" >> temp/site.txt
    for ((i=1; i<=$noof_sites; i++))
    do
        cat sample/site.txt >> temp/site.txt
        sed -i s/Site_/$sitename\_/g temp/site.txt
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
echo -en Enter the"\033[32m Number of Accounts \033[0m"to be created
echo ""
read noof_accounts
echo -en Enter the"\033[32m Account Name \033[0m"
echo ""
read accountname
if [ "$line" == "y" ] || [ "$line" == "Y" ]
then
    echo "  \"Number_of_Accounts\": \"$noof_accounts\", " >> temp/account.txt
    echo "" >> temp/account.txt
    for ((i=1; i<=$noof_accounts; i++))
    do
        cat sample/account.txt >> temp/account.txt
        sed -i s/_#MyVaLuE#_/$i/g temp/account.txt
        sed -i s/ACCOUNT/$accountname/g temp/account.txt
    done
else
    echo "Continuing with next step"
fi

##### To Create TSMs
while [ "$QUIT" == "y" ] || [ "$QUIT" == "Y" ]
do
    echo ""
    echo -en Do you want to configure TSM Press "\033[32m y \033[0m" else "\033[32m n \033[0m" : 
    echo ""
    read tsmconfirmation
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
    if [ "$tsmconfirmation" == "y" ] || [ "$tsmconfirmation" == "Y" ]
    then
        cat sample/tsm.txt >> temp/tsm.txt
        NoofTSMs=`expr $NoofTSMs + 1`
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
    read confirmation
        echo -en Enter the"\033[32m Number of NFS Volumes \033[0m"to be created
        echo ""
        read line
        echo -en Enter the"\033[32m NFS Volumes Name \033[0m"
        echo ""
        read nfsname
        echo "" >> temp/nfsvolume.txt
    if (([ "$confirmation" == "y" ] || [ "$confirmation" == "Y" ]) && ([ "$tsmconfirmation" == "y" ] || [ "$tsmconfirmation" == "Y" ])) 
    then
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
    read confirmation
        echo -en Enter the"\033[32m Number of iSCSI Volumes \033[0m"to be created
        echo ""
        read line
        echo -en Enter the"\033[32m iSCSI Volumes Name \033[0m"
        echo ""
        read iscsiname
        echo "" >> temp/iscsivolume.txt
    if (([ "$confirmation" == "y" ] || [ "$confirmation" == "Y" ]) && ([ "$tsmconfirmation" == "y" ] || [ "$tsmconfirmation" == "Y" ])) 
    then
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
    read confirmation
        echo -en Enter the"\033[32m Number of CIFS Volumes \033[0m"to be created
        echo ""
        read line
        echo -en Enter the"\033[32m CIFS Volumes Name \033[0m"
        echo ""
        read cifsname
        echo "" >> temp/cifsvolume.txt
    if (([ "$confirmation" == "y" ] || [ "$confirmation" == "Y" ]) && ([ "$tsmconfirmation" == "y" ] || [ "$tsmconfirmation" == "Y" ])) 
    then
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
    #
    #
    #
    ##### To Create FC  Volumes
    echo ""
    echo -en Do you want to configure FC Volumes for the $tsmname "\033[32m y \033[0m" else "\033[32m n \033[0m" :
    echo ""
    read confirmation 
    echo -en Enter the"\033[32m Initiator \033[0m"you have to associate the TSM
    echo ""
    read initiator
    echo -en Enter the"\033[32m Number of FC Volumes \033[0m"to be created
    echo ""
    read line
    echo -en Enter the"\033[32m FC Volumes Name \033[0m"
    echo ""
    read fcname
    echo "" >> temp/fcvolume.txt
    if (([ "$confirmation" == "y" ] || [ "$confirmation" == "Y" ]) && ([ "$tsmconfirmation" == "y" ] || [ "$tsmconfirmation" == "Y" ]))
    then
       temp=`expr $NooffcVolumes + 1`
       NooffcVolumes=`expr $NooffcVolumes + $line`
       for ((i=temp; i<=$NooffcVolumes; i++))
       do
           cat sample/fcvolume.txt >> temp/fcvolume.txt
           sed -i s/_#MyVaLuE#_/$i/g temp/fcvolume.txt
           sed -i s/FCVOLNAME/$fcname/g temp/fcvolume.txt
       done
       sed -i s/POOLNAME/$poolname/g temp/fcvolume.txt
       sed -i s/TSMNAME/$tsmname/g temp/fcvolume.txt
       sed -i s/ACCOUNTNAME/$accountname/g temp/fcvolume.txt
       sed -i s/IPADDRESS/$ipaddress/g temp/fcvolume.txt
       sed -i s/INITIATOR/$initiator/g temp/fcvolume.txt
       else
          echo "Continuing with next step"
       fi
    #
    #
    #
    echo -en To Continue creating TSM... Press "\033[32m y \033[0m" else "\033[32m n \033[0m" :
    echo ""
    read QUIT
    echo "Quit Value is $QUIT"
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
sed -i '1s/^/  \"Number_of_fcVolumes\": \"NoofFCVolumes\",/' temp/fcvolume.txt
sed -i s/NoofNFSVolumes/$NoofNFSVolumes/g temp/nfsvolume.txt
sed -i s/NoofTSMS/$NoofTSMs/g temp/tsm.txt
sed -i s/NoofISCSIVolumes/$NoofISCSIVolumes/g temp/iscsivolume.txt
sed -i s/NoofCIFSVolumes/$NoofCIFSVolumes/g temp/cifsvolume.txt
sed -i s/NoofFCVolumes/$NooffcVolumes/g temp/fcvolume.txt
###Aggregating config files
cat sample/header.txt >> config.txt
cat temp/site.txt >> config.txt
cat sample/cluster_pool.txt >> config.txt
cat sample/addVDev.txt >> config.txt
cat temp/account.txt  >> config.txt
cat temp/tsm.txt >> config.txt
cat temp/nfsvolume.txt  >> config.txt
cat temp/iscsivolume.txt >> config.txt
cat temp/cifsvolume.txt >> config.txt
cat temp/fcvolume.txt >> config.txt
cat sample/trailer.txt >> config.txt
###Aggregating config files
echo "No of TSMs = $NoofTSMs"
echo "No of NFS Volumes = $NoofNFSVolumes "
echo "No of ISCSI Volumes = $NoofISCSIVolumes"
echo "No of CIFS Volumes = $NoofCIFSVolumes"
echo "No of FC Volumes = $NooffcVolumes"
echo "Configuration File Creation Done"
