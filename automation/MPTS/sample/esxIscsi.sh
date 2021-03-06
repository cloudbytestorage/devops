> esxIscsi.py
> vmlrdmcopy.py
> temp/vm.txt > temp/createvml.sh
#echo "{" >> temp/vm.txt
QUIT="Y"
NoofVMs=0
echo ""  >> esxIscsi.py
echo -en  Enter the "\033[32m  Do you want ESX configuration for ISCSI  \033[0m"
echo ""
read esxconfirmation
echo -en  Enter the "\033[32m ESX IP  \033[0m"
echo ""
read esxip
echo -en  Enter the "\033[32m ESX Password  \033[0m"
echo ""
read esxpassword
echo -en  Enter the "\033[32m Number of volumes you want per VM  \033[0m"
echo ""
read noofvolumes
cat sample/esxIscsi.py >> esxIscsi.py
cat sample/vmlrdmcopy.py >> vmlrdmcopy.py
cat sample/createvml.sh >> temp/createvml.sh
sed -i s/ESXIP/$esxip/g esxIscsi.py
sed -i s/ESXPASSWORD/$esxpassword/g esxIscsi.py
sed -i s/NOOFVOLUMES/$noofvolumes/g temp/createvml.sh
sed -i s/ESXIP/$esxip/g vmlrdmcopy.py
sed -i s/ESXPASSWORD/$esxpassword/g vmlrdmcopy.py
while [ "$QUIT" == "y" ] || [ "$QUIT" == "Y" ]
do
    echo ""
    echo -en Do you want to configure VM for ISCSI Press "\033[32m y \033[0m" else "\033[32m n \033[0m" :
    echo ""
    read vmconfirmation
        echo ""  >> temp/vm.txt
        echo -en  Enter the "\033[32m Datastore Name \033[0m"
        echo ""
        read datastorename
        echo -en  Enter the "\033[32m VM Name \033[0m"
        echo ""
        read vmname
        echo -en  Enter the "\033[32m VM IP \033[0m"
        echo ""
        read vmip
        echo -en  Enter the "\033[32m VM Password \033[0m"
        echo ""
        read vmpassword
    if [ "$vmconfirmation" == "y" ] || [ "$vmconfirmation" == "Y" ]
    then
        cat sample/vm.txt >> temp/vm.txt
        NoofVMs=`expr $NoofVMs + 1`
        sed -i s/_#MyVaLuE#_/$NoofVMs/g temp/vm.txt
        sed -i s/VMNAME/$vmname/g temp/vm.txt
        sed -i s/DATASTORENAME/$datastorename/g temp/vm.txt
        sed -i s/VMIP/$vmip/g temp/vm.txt
        sed -i s/VMPASSWORD/$vmpassword/g temp/vm.txt
    else
        echo "Continuing with next step"
    fi
    echo -en To Continue configure VM for ISCSI... Press "\033[32m y \033[0m" else "\033[32m n \033[0m" :
    echo ""
    read QUIT
    echo "Quit Value is $QUIT"
    echo ""
    echo ""
done

sed -i '1s/^/\n/' temp/vm.txt
sed -i '1s/^/  \"Number_of_VMs\": \"NoofVMS\",/' temp/vm.txt
sed -i s/NoofVMS/$NoofVMs/g temp/vm.txt
sed -i '1s/^/\n/' temp/vm.txt
sed -i '1s/^/\n/' temp/vm.txt
sed -i '1s/^/  \"Number_of_Disk_per_VMs\": \"'$noofvolumes'\",/' temp/vm.txt
sed -i '1s/^/\n/' temp/vm.txt
sed -i '1s/^/  \"esxpassword\": \"'$esxpassword'\",/' temp/vm.txt
sed -i '1s/^/\n/' temp/vm.txt
sed -i '1s/^/  \"esxip\": \"'$esxip'\",/' temp/vm.txt
sed -i '1s/^/\n/' temp/vm.txt
sed -i '1s/^/  \"_ESX Configuration ISCSI\": \"Details for VM\",/' temp/vm.txt

#echo "\"End of VM configuration\":\"end\"" >> temp/vm.txt 
#echo "" >> temp/vm.txt
#echo "}" >> temp/vm.txt

'''
###Aggregating config files
cat temp/header.txt >> config.txt
cat temp/site.txt >> config.txt
cat temp/cluster.txt >> config.txt
cat temp/node.txt >> config.txt
cat temp/jbod.txt >> config.txt
cat temp/pool.txt >> config.txt
cat temp/account.txt  >> config.txt
cat sample/siteAdmin.txt >> config.txt
cat sample/haAdmin.txt >> config.txt
cat temp/vlan.txt >> config.txt
cat temp/staticIP.txt >> config.txt
cat temp/tsm.txt >> config.txt
cat temp/nfsvolume.txt  >> config.txt
cat temp/iscsivolume.txt >> config.txt
cat temp/cifsvolume.txt >> config.txt
cat temp/fcvolume.txt >> config.txt
cat temp/vm.txt >> config.txt
cat sample/trailer.txt >> config.txt
###Aggregating config files
echo "No of TSMs = $NoofTSMs"
echo "No of NFS Volumes = $NoofNFSVolumes "
echo "No of ISCSI Volumes = $NoofISCSIVolumes"
echo "No of CIFS Volumes = $NoofCIFSVolumes"
echo "No of FC Volumes = $NooffcVolumes"
echo "Configuration File Creation Done"
'''
