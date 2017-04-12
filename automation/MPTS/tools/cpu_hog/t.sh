count=0
while [ $count -ne 100000 ]
do
count=`expr $count + 1`
echo $count
done
