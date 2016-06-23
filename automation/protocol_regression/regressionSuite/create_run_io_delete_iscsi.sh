a=1
while [ $a -lt 3 ]
do
    python newtest2.py conf.txt
    sleep 100
    #echo $a
    a=`expr $a + 1`
done
