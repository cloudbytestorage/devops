set -o history -o histexpand
should_exit(){
   if [ $1 -ne 0 ];
   then
       echo "Configuration failed Exit Status `history | tail -n 3 | awk 'NR==2 { print; exit }'`"
       exit
   fi
}

python nodeToMode.py smoketest.txt maintenance NODEIP1 NODEPASSWORD1 NODEIP2 NODEPASSWORD2
should_exit $?

sleep 300

python nodeToMode.py smoketest.txt available NODEIP1 NODEPASSWORD1 NODEIP2 NODEPASSWORD2
should_exit $?


