ps -aux | grep cpuhog.sh | awk '{print $2}' | xargs kill -9
ps -aux | grep t.sh | awk '{print $2}' | xargs kill -9
