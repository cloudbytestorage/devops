#basic command "ping" to check connectivity.
#In case the machines are down the jenkins job will send out a notification 
#to recipients for the failure of the job
echo "checking the Main ESX"

        ping -c 4 20.10.48.1
        esxmain=$(echo $?)
        echo $esxmain

echo "checking the BST node"

        ping -c 4 20.10.48.140
        bstnode=$(echo $?)
        echo $bstnode

echo "checking the BST node"

        ping -c 4 20.10.48.5
        bstnode=$(echo $?)
        echo $bstnode

#echo "checking the dummy IP"
#        ping -c 4 20.10.48.66  
#        dummy=$(echo $?)
#        echo $dummy


#conditions to check for
        if [ $esxmain -ne 0 ]
                then
                        echo " The main ESX is down"
        else
                        echo " The Main ESX is UP and running"
        fi

        if [ $bstnode -ne 0 ]
                then
                        echo " The BST node is down"
        else
                        echo " The BST node is UP and running"
        fi


