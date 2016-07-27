rm temp/*
>temp/site.txt; >temp/account.txt; >temp/cluster.txt; >temp/node.txt; >temp/jbod.txt; >temp/pool.txt; >temp/vlan.txt >temp/staticIP.txt  >config.txt; >logs/tracktime;
#cp sample/raidz1.txt sample/raidz2.txt sample/raidzSameDisk.txt sample/raidzSameName.txt sample/raidzDiffernetSizeDisk.txt  sample/mirror.txt .
> autoiscsi.sh
cp sample/fdisk_response_file .
QUIT=y
NoofClusters=0
NoofNodes=0
NoofPools=0
NoofVlans=0
NoofStaticIPs=0
echo -en Enter the"\033[32m Number of Sites \033[0m"to be created
echo ""
read devmanip
cat sample/header.txt >> temp/header.txt
sed -i s/DEVMANIP/$devmanip/g temp/header.txt
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

##### To Create Clusters
while [ "$QUIT" == "y" ] || [ "$QUIT" == "Y" ]
do
    echo ""
    echo -en Do you want to configure Cluster Press "\033[32m y \033[0m" else "\033[32m n \033[0m" : 
    echo ""
    read clusterconfirmation
        echo ""  >> temp/cluster.txt
        echo -en  Enter the "\033[32m Cluster Name \033[0m"
        echo ""
        read clustername
        echo -en Enter the"\033[32m Site Name \033[0m"you have to associate the Cluster
        echo ""
        read sitename
        echo -en Enter the"\033[32m Cluster Description \033[0m"
        echo ""
        read clusterdescription
        echo -en Enter the"\033[32m Cluster Start IP Address \033[0m"
        echo ""
        read startip
        echo -en Enter the"\033[32m Cluster End IP Address \033[0m"
        echo ""
        read endip
    if [ "$clusterconfirmation" == "y" ] || [ "$clusterconfirmation" == "Y" ]
    then
        cat sample/cluster.txt >> temp/cluster.txt
        NoofClusters=`expr $NoofClusters + 1`
        sed -i s/_#MyVaLuE#_/$NoofClusters/g temp/cluster.txt
        sed -i s/CLUSTERNAME/$clustername/g temp/cluster.txt
        sed -i s/SITENAME/$sitename/g temp/cluster.txt
        sed -i s/CLUSTERDESCRIPTION/$clusterdescription/g temp/cluster.txt
        sed -i s/CLUSTERSTARTIP/$startip/g temp/cluster.txt
        sed -i s/CLUSTERENDIP/$endip/g temp/cluster.txt
    else
        echo "Continuing with next step"
    fi
    echo -en To Continue creating Cluster... Press "\033[32m y \033[0m" else "\033[32m n \033[0m" :
    echo ""
    read QUIT
    echo "Quit Value is $QUIT"
    echo ""
    echo ""
done

QUIT=y
##### To Create Nodes
while [ "$QUIT" == "y" ] || [ "$QUIT" == "Y" ]
do
    echo ""
    echo -en Do you want to configure Node Press "\033[32m y \033[0m" else "\033[32m n \033[0m" :
    echo ""
    read nodeconfirmation
        echo ""  >> temp/node.txt
        echo -en  Enter the "\033[32m Node Name \033[0m"
        echo ""
        read nodename
        echo -en Enter the"\033[32m Site Name \033[0m"you have to associate the node
        echo ""
        read sitename
        echo -en Enter the"\033[32m Cluster Name \033[0m"you have to associate the node
        echo ""
        read clustername
        echo -en Enter the"\033[32m Node IP Address \033[0m"
        echo ""
        read nodeip
        echo -en Enter the"\033[32m Node Password \033[0m"
        echo ""
        read nodepasswd
    if [ "$nodeconfirmation" == "y" ] || [ "$nodeconfirmation" == "Y" ]
    then
        cat sample/node.txt >> temp/node.txt 
        NoofNodes=`expr $NoofNodes + 1`
        sed -i s/_#MyVaLuE#_/$NoofNodes/g temp/node.txt
        sed -i s/NODENAME/$nodename/g temp/node.txt
        sed -i s/SITENAME/$sitename/g temp/node.txt
        sed -i s/CLUSTERNAME/$clustername/g temp/node.txt
        sed -i s/NODEIP/$nodeip/g temp/node.txt
        sed -i s/NODEPASSWORD/$nodepasswd/g temp/node.txt
        if [ "$NoofNodes" == 1 ]
        then
            #cat sample/automation.sh >> automation.sh
            #cat sample/autoiscsi.sh >> autoiscsi.sh
            sed -i s/NODEIP1/$nodeip/g automation.sh
            sed -i s/NODEPASSWORD1/$nodepasswd/g automation.sh
            sed -i s/NODEIP1/$nodeip/g autoHA.sh
            sed -i s/NODEPASSWORD1/$nodepasswd/g autoHA.sh
            sed -i s/NODEIP1/$nodeip/g autoiscsi.sh
            sed -i s/NODEPASSWORD1/$nodepasswd/g autoiscsi.sh
        fi
        if [ "$NoofNodes" == 2 ]
        then
            sed -i s/NODEIP2/$nodeip/g autoHA.sh
            sed -i s/NODEPASSWORD2/$nodepasswd/g autoHA.sh
        fi
    else
        echo "Continuing with next step"
    fi
    echo -en To Continue creating Node... Press "\033[32m y \033[0m" else "\033[32m n \033[0m" :
    echo ""
    read QUIT
    echo "Quit Value is $QUIT"
    echo ""
    echo ""
done


##### To Create JBOD
echo ""
echo -en Do you want to configure JBOD Press "\033[32m y \033[0m" else "\033[32m n \033[0m" :
echo ""
read line
echo -en Enter the"\033[32m JBOD Name \033[0m"
echo ""
read jbodname
echo -en Enter the"\033[32m Number of Disks \033[0m"to be created
echo ""
read noofdisks
if [ "$line" == "y" ] || [ "$line" == "Y" ]
then
    echo "" >> temp/jbod.txt
    baynumber=""
    for ((i=1; i<=$noofdisks; i++))
    do
        baynumber+=$i","
    done
    baynumber=`echo $baynumber | sed s/.$//`
    cols=`expr $noofdisks + 4`
    cat sample/jbod.txt >> temp/jbod.txt
    sed -i s/JBODNAME/$jbodname/g temp/jbod.txt
    sed -i s/NOOFDISKS/$baynumber/g temp/jbod.txt
    sed -i s/COLS/$cols/g temp/jbod.txt
fi

QUIT=y
##### To Create Pool
while [ "$QUIT" == "y" ] || [ "$QUIT" == "Y" ]
do
    echo ""
    echo -en Do you want to configure Pool Press "\033[32m y \033[0m" else "\033[32m n \033[0m" :
    echo ""
    read line
    echo -en Enter the"\033[32m Pool Name \033[0m"
    echo ""
    read poolname
    echo -en Enter the"\033[32m Site Name \033[0m"you have to associate the Pool
    echo ""
    read sitename
    echo -en Enter the"\033[32m Cluster Name \033[0m"you have to associate the Pool
    echo ""
    read clustername
    echo -en Enter the"\033[32m Node Name \033[0m"you have to associate the Pool
    echo ""
    read nodename
    if [ "$line" == "y" ] || [ "$line" == "Y" ]
    then
        echo "" >> temp/pool.txt
        cat sample/pool.txt >> temp/pool.txt
        NoofPools=`expr $NoofPools + 1`
        sed -i s/_#MyVaLuE#_/$NoofPools/g temp/pool.txt
        sed -i s/POOLNAME/$poolname/g temp/pool.txt
        sed -i s/SITENAME/$sitename/g temp/pool.txt
        sed -i s/CLUSTERNAME/$clustername/g temp/pool.txt
        sed -i s/NODENAME/$nodename/g temp/pool.txt
    else
        echo "Continuing with next step"
    fi
    echo -en To Continue creating Pool... Press "\033[32m y \033[0m" else "\033[32m n \033[0m" :
    echo ""
    read QUIT
    echo "Quit Value is $QUIT"
    echo ""
    echo ""
done


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

QUIT=y
##### To Create VLAN
while [ "$QUIT" == "y" ] || [ "$QUIT" == "Y" ]
do
    echo ""
    echo -en Do you want to configure VLAN Press "\033[32m y \033[0m" else "\033[32m n \033[0m" :
    echo ""
    read line
    echo -en Enter the"\033[32m Interface \033[0m"
    echo ""
    read interface
    echo -en Enter the"\033[32m Tag Value \033[0m"
    echo ""
    read tagvalue
    echo -en Enter the"\033[32m Cluster Name \033[0m"you have to associate the vlan
    echo ""
    read clustername
    if [ "$line" == "y" ] || [ "$line" == "Y" ]
    then
        echo "" >> temp/vlan.txt
        cat sample/vlan.txt >> temp/vlan.txt
        NoofVlans=`expr $NoofVlans + 1`
        sed -i s/_#MyVaLuE#_/$NoofVlans/g temp/vlan.txt
        sed -i s/INTERFACE/$interface/g temp/vlan.txt
        sed -i s/TAGVALUE/$tagvalue/g temp/vlan.txt
        sed -i s/CLUSTERNAME/$clustername/g temp/vlan.txt
    else
        echo "Continuing with next step"
    fi
    echo -en To Continue creating Vlan... Press "\033[32m y \033[0m" else "\033[32m n \033[0m" :
    echo ""
    read QUIT
    echo "Quit Value is $QUIT"
    echo ""
    echo ""
done

QUIT=y
##### To Create StaticIP
while [ "$QUIT" == "y" ] || [ "$QUIT" == "Y" ]
do
    echo ""
    echo -en Do you want to configure StaticIP Press "\033[32m y \033[0m" else "\033[32m n \033[0m" :
    echo ""
    read line
    echo -en Enter the"\033[32m Interface \033[0m"
    echo ""
    read interface
    echo -en Enter the"\033[32m Static Ip Address \033[0m"
    echo ""
    read staticip
    echo -en Enter the"\033[32m Subnet \033[0m"
    echo ""
    read subnet
    echo -en Enter the"\033[32m Gateway \033[0m"
    echo ""
    read gateway
    echo -en Enter the"\033[32m Nodename \033[0m"you want to associate the staticip
    echo ""
    read nodename
    if [ "$line" == "y" ] || [ "$line" == "Y" ]
    then
        echo "" >> temp/staticIP.txt
        cat sample/staticIP.txt >> temp/staticIP.txt
        NoofStaticIPs=`expr $NoofStaticIPs + 1`
        sed -i s/_#MyVaLuE#_/$NoofStaticIPs/g temp/staticIP.txt
        sed -i s/INTERFACE/$interface/g temp/staticIP.txt
        sed -i s/STATICIP/$staticip/g temp/staticIP.txt
        sed -i s/SUBNET/$subnet/g temp/staticIP.txt
        sed -i s/GATEWAY/$gateway/g temp/staticIP.txt
        sed -i s/NODENAME/$nodename/g temp/staticIP.txt
    else
        echo "Continuing with next step"
    fi
    echo -en To Continue creating StaticIP... Press "\033[32m y \033[0m" else "\033[32m n \033[0m" :
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
sed -i '1s/^/  \"Number_of_Clusters\": \"NoofClusters\",/' temp/cluster.txt
sed -i '1s/^/  \"Number_of_Nodes\": \"NoofNodes\",/' temp/node.txt
sed -i '1s/^/  \"Number_of_Pools\": \"NoofPools\",/' temp/pool.txt
sed -i '1s/^/  \"Number_of_Vlans\": \"NoofVlans\",/' temp/vlan.txt
sed -i '1s/^/  \"Number_of_StaticIPs\": \"NoofStaticIPs\",/' temp/staticIP.txt
sed -i s/NoofClusters/$NoofClusters/g temp/cluster.txt
sed -i s/NoofNodes/$NoofNodes/g temp/node.txt
sed -i s/NoofPools/$NoofPools/g temp/pool.txt
sed -i s/NoofVlans/$NoofVlans/g temp/vlan.txt
sed -i s/NoofStaticIPs/$NoofStaticIPs/g temp/staticIP.txt
'''
###Aggregating config files
cat temp/header.txt >> config.txt
cat temp/site.txt >> config.txt
cat temp/cluster.txt >> config.txt
cat temp/node.txt >> config.txt
cat temp/jbod.txt >> config.txt
cat temp/pool.txt >> config.txt
#cat sample/vdev.txt >> config.txt
cat temp/account.txt  >> config.txt
cat sample/siteAdmin.txt >> config.txt
cat sample/haAdmin.txt >> config.txt
cat temp/vlan.txt >> config.txt
cat temp/staticIP.txt >> config.txt
cat sample/trailer.txt >> config.txt
###Aggregating config files
'''

#########Configuring pool files
cat temp/header.txt > raidz1.txt
cat sample/raidz1.txt >> raidz1.txt
cat sample/trailer.txt >> raidz1.txt

cat temp/header.txt > raidz2.txt
cat sample/raidz2.txt >> raidz2.txt
cat sample/trailer.txt >> raidz2.txt

cat temp/header.txt > raidzSameDisk.txt
cat sample/raidzSameDisk.txt >> raidzSameDisk.txt
cat sample/trailer.txt >> raidzSameDisk.txt

cat temp/header.txt > raidzSameName.txt
cat sample/raidzSameName.txt >> raidzSameName.txt
cat sample/trailer.txt >> raidzSameName.txt

cat temp/header.txt > raidzDiffernetSizeDisk.txt
cat sample/raidzDiffernetSizeDisk.txt >> raidzDiffernetSizeDisk.txt
cat sample/trailer.txt >> raidzDiffernetSizeDisk.txt

cat temp/header.txt > mirror.txt
cat sample/mirror.txt >> mirror.txt
cat sample/trailer.txt >> mirror.txt


echo "Configuration File Creation Done"
