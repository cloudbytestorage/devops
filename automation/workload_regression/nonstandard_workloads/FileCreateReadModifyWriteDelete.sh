#! /bin/sh

# Local mount point to run the workload, taken from calling python script

nfs_local_mnt_pt=$1

# Location of result file, created for verification by calling python scipt

test_log=/root/FileCreateReadModifyWriteDelete.log

# Determine num of files based on active size chosen for testcase

No2kFiles=200  
No4kFiles=200 
No8kFiles=200
No16kFiles=200
No32kFiles=200

# Fn to create recursive dir structures and call file create fn

Create()
{
    for x in a b c d 
    do
        mkdir -p $nfs_local_mnt_pt/$x
        cd $nfs_local_mnt_pt/$x
        for y in a b c d 
        do
            mkdir -p $nfs_local_mnt_pt/$x/$x$y
            cd $nfs_local_mnt_pt/$x/$x$y
            CreateFiles 2k
            CreateFiles 4k
            CreateFiles 8k
            CreateFiles 16k
            CreateFiles 32k
        done
    done
 echo "FILES CREATED" > $test_log
}

# Fn to perform reads and modify-writes in parallel in each dir

ReadModifyWrite()
{
    for x in a b c d
    do
        for y in a b c d
        do 
            cd $nfs_local_mnt_pt/$x/$x$y
            ReadFiles 2k 
            ReadFiles 8k 
            ReadFiles 16k 
            ModifyWriteFiles 4k 
            ModifyWriteFiles 16k 
            #wait    
        done
    done
 echo "FILES READ MODIFIED WRITTEN" >> $test_log
}

# Fn to call file-delete fn for different sized files in each dir

Delete()
{
    for x in a b c d
    do
        for y in a b c d
        do
            cd $nfs_local_mnt_pt/$x/$x$y
            DeleteFiles 2k
            DeleteFiles 4k
            DeleteFiles 8k
            DeleteFiles 16k
            DeleteFiles 32k
        done
    done
    echo "FILES DELETED" >> $test_log
 }

 # Fn to create files of specified number using dd command

CreateFiles()
{
    FileSize=$1

    if [ "$FileSize" == "2k" ]
    then
        NumFiles=$No2kFiles
        ddBlockSize=512
    
    elif [ "$FileSize" == "4k" ]
    then 
        NumFiles=$No4kFiles
        ddBlockSize=1k

    elif [ "$FileSize" == "8k" ]
    then
        NumFiles=$No8kFiles
        ddBlockSize=2k 

    elif [ "$FileSize" == "16k" ]
    then
        NumFiles=$No16kFiles
        ddBlockSize=4k

    elif [ "$FileSize" == "32k" ]
    then
        NumFiles=$No32kFiles
        ddBlockSize=8k

    fi

    i=1
    while [ $i -le $NumFiles ] 
    do
        {
            dd if=/dev/urandom of=file$FileSize-$i bs=$ddBlockSize count=4
            i=`expr $i + 1`
        }
    done
}

# Fn to read from files using dd

ReadFiles()
{
    FileSize=$1

    if [ "$FileSize" == "2k" ]
    then
        NumFiles=$No2kFiles
        ddBlockSize=512

    elif [ "$FileSize" == "4k" ]
    then
        NumFiles=$No4kFiles
        ddBlockSize=1k

    elif [ "$FileSize" == "8k" ]
    then
        NumFiles=$No8kFiles
        ddBlockSize=2k

    elif [ "$FileSize" == "16k" ]
    then
        NumFiles=$No16kFiles
        ddBlockSize=4k

    elif [ "$FileSize" == "32k" ]
    then
        NumFiles=$No32kFiles
        ddBlockSize=8k

    fi

    i=1
    while [ $i -le $NumFiles ]
    do
        {
            dd if=file$FileSize-$i of=/dev/null bs=$ddBlockSize count=4
            i=`expr $i + 1`
        }
    done
 }

 # Fn to modify file blocks in existing files using dd with conv=notrunc param

ModifyWriteFiles()
{
    FileSize=$1

    if [ "$FileSize" == "2k" ]
    then
        NumFiles=$No2kFiles
        ddBlockSize=512

    elif [ "$FileSize" == "4k" ]
    then
        NumFiles=$No4kFiles 
        ddBlockSize=1k

    elif [ "$FileSize" == "8k" ]
    then
        NumFiles=$No8kFiles
        ddBlockSize=2k

    elif [ "$FileSize" == "16k" ]
    then
        NumFiles=$No16kFiles
        ddBlockSize=4k

    elif [ "$FileSize" == "32k" ]
    then
        NumFiles=$No32kFiles
        ddBlockSize=8k

    fi

    i=1
    while [ $i -le $NumFiles ]
    do
        {
            dd if=/dev/urandom of=file$FileSize-$i bs=$ddBlockSize count=2 conv=notrunc
            i=`expr $i + 1`
        }
    done
}

# Fn to delete different-sized files in the dir

DeleteFiles()
{
    FileSize=$1

    if [ "$FileSize" == "2k" ]
    then
        rm -rf file$FileSize*

    elif [ "$FileSize" == "4k" ]
    then
        rm -rf file$FileSize*

    elif [ "$FileSize" == "8k" ]
    then
        rm -rf file$FileSize*

    elif [ "$FileSize" == "16k" ]
    then
        rm -rf file$FileSize*

    elif [ "$FileSize" == "32k" ]
    then
        rm -rf file$FileSize*

    fi
 }

# MAIN FUNCTION 

logger "Workload Test Started"
Create;
ReadModifyWrite;
Delete;
logger "Workload Test Ended"


