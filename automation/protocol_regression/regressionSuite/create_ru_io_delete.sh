a=1
while [ $a -le 10 ]
do
    python newtest.py conf.txt
    sleep(100)
    #echo $a
    a=`expr $a + 1`
done
