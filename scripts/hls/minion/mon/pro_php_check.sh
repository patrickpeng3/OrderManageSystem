#!/bin/bash
pidfile=/tmp/phpcheck.pid
namecheck(){
	for fname in ws dp ss ls gs;
	do
		check=$(ps -ef|egrep -v "grep|tmux|gdb|core|sh -c"|grep -c ${id}_$fname)
		if [ $check -eq 0 ];then
			php /data/mon/LibSms.php ${id}_$fname
			sleep 300
		fi
		
	done
}

if [  -f $pidfile ] && [[ $(lsof -p $(cat $pidfile)|wc -l) > 0 ]];then
	echo "$0 is running "
 	exit 10
fi
echo $$ >$pidfile
for id in $(ls /data/game/|grep ^server|awk -F'server' '{print $NF}')
do
	
	num=$(ps -ef|egrep -v "grep|tmux|gdb|core|sh -c"|grep -c ${id}_)

        if [ -f /tmp/stop_$id ] && [ -f /tmp/start_$id ] && [ -f /tmp/${id}.pid ] ;then
                if [ $(cat /tmp/stop_$id) -eq 1 ] && [ $(cat /tmp/start_$id) -eq 1 ] && [ $(cat /tmp/${id}.pid) -eq 0 ] ;then
					namecheck
					echo $(date +%F_%T) $id >> /tmp/123
                fi
        else
                if [ $num -lt 5 ]  && [ $num -gt 0 ];then
					namecheck
                fi
        fi

done

rm -f $pidfile



