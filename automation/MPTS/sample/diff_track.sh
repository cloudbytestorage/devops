#diff -rqn ~/cloudbyte/split /root/sourcecode/tools/automation/ | sort -n | more
### Steps for SVN
#svn add sample/*
#svn add *
#svn ci -m "[BUG-0000][RB-0000] MPTS Automation Merge first time" *
### Steps for SVN
clear
if [ -z $1 ]
then
    searchfile="*.py" 
else
    searchfile="*.$1"
fi
echo "Starting the Script"
for i in `ls $searchfile | xargs  -i basename {}`
do
		#echo File Comparing $i
                #vimdiff -o $i sample/$i
		#vimdiff  $i sample/$i
		diff  -q  $i sample/$i
		#diff  $i ~/cloudbyte/apeksha/split/$i
                #diff $i ../apeksha/$i
                if [ $? -eq 0 ]
                then
                   #echo -en '\E[47;42m'"\033[1m Files are same $i sample/$i\033[0m"
                   echo -en '\E[47;41m'"\033[1m \033[0m"
                   #echo ""
                   #echo "Files are same $i sample/$i"
                else
                   echo -en '\E[47;46m'"\033[1m  Files differ $i sample/$i \033[0m"
                   echo ""
                   #echo "Do you want to Copy.. Note -- If no file in destination directory it will be copied"
		   read
		   vimdiff  $i sample/$i 
                   #cp -iv $i sample/$i
                fi
		#sleep 1
done
echo "Ending the Script"
