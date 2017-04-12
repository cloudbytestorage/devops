set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

python nodeToMode.py smoketest.txt maintenance 20.10.26.32 test 20.10.38.5 test
should_exit $?

sleep 300

python nodeToMode.py smoketest.txt available 20.10.26.32 test 20.10.38.5 test
should_exit $?


