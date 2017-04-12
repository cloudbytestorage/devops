#!/bin/bash
> results/regression_result.csv
cp config.txt tconfig.txt
sh ConfigurationFromCSV.sh regression.csv
python apikey_get.py
cp config.txt regression_config.txt

for((i=1; i<=100; i++))
do
    echo " " >> "results/regression_result.csv"
    echo ""
    echo -en '\E[47;44m' "\033[1m Iteration $i Start time `date` \033[0m" 
    echo "Iteration $i Start time `date`" >> "results/regression_result.csv"
    echo ""
    umount -a -t cifs -l > /dev/null 2>&1
    umount -a -t cifs -l > /dev/null 2>&1
    umount -fa > /dev/null 2>&1
    umount -fa > /dev/null 2>&1
    python regression_create.py  
    sleep 5
    python regression_execution.py
    sleep 5
    umount -a -t cifs -l > /dev/null 2>&1
    umount -a -t cifs -l > /dev/null 2>&1
    umount -fa > /dev/null 2>&1
    umount -fa > /dev/null 2>&1
    python  regression_delete.py 
    sleep 5
    echo "Iteration $i End time `date`" >> "results/regression_result.csv"
    echo " " >> "results/regression_result.csv"
    grep -i failed "results/regression_result.csv"
    if [ $? -eq 0 ]
    then
        echo -en '\E[47;41m'"\033[1m  Some or all of the Testcase in this set --  FAILED    Exiting the loop after iteration $i \033[0m"
        echo ""
        exit
    fi
done
echo -en '\E[47;42m'"\033[1m  All the Testcase in this set --  PASSED   \033[0m"
echo ""
