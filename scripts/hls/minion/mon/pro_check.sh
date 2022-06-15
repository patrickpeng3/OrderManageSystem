#!/bin/bash

PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'

path='/data/game/'
log='/tmp/a8.log'
pslog='/tmp/a8ps.log'
time=$(date +%F_%T)
htime=$(date +%F_%H)
phpfile='/data/mon/huifu.php'
pidfile='/tmp/pro_check.pid'

function checkpro() {
	for fname in ws dp ls ss gs; do
	    pro=$(ps -ef | egrep -v "grep|tmux|gdb|core|sh -c" | grep -c ./${id}_${fname})
		if [[ ${pro} == 0 ]] && ([[ ${fname} == gs ]]||[[ ${fname} == ls ]]); then
			 echo "-------$time------------" >>$pslog
			 ps -ef|grep ${id}|grep -v grep  >>$pslog
		     tmux new-window -a -t ${id} -n ${fname} -d "./${id}_${fname}"
			 php $phpfile ${id}_${fname}
			 echo "$time ${id}_${fname} is restart " >> $log
		elif ([[ $pro != 1 ]] && ([[ $fname == dp ]]||[[ $fname == ws ]]||[[ $fname == ss ]])) || ( [[ $pro > 1 ]] && ([[ $fname == gs ]]||[[ $fname == ls ]])); then
			echo "--------$time-----------" >>$pslog
			ps -ef | grep ${id} | grep -v grep  >>$pslog
			/var/tmp/game_stop.sh $id
			sleep 5
			/var/tmp/game_start.sh $id
		    sleep 5
			echo "$time ${id}_${fname} is restart " >> $log
			php $phpfile ${id}_${fname}
	        [[ `ps -ef|egrep -v "grep|tmux|gdb|core|sh -c"|grep -c ./${id}_` == 5 ]]  
			rm -f $pidfile
			exit 10
		fi		
	done
}


if [ -f $pidfile ] && [[ $(lsof -p $(cat $pidfile)|wc -l) != 0 ]] ;then
  echo
  exit 10
fi
echo $$ >$pidfile

[ ! -f $log ] && touch $log
if	(( $(grep -c $htime $log) >= 10 )); then
	echo "$htime 自动重启脚本1小时内执行3次，请检查"
	rm -f $pidfile
	exit 10
fi

for id in $(ls /data/game/|grep ^server|awk -F'server' '{print $2}'); do
 	gamepath=$path/server$id/serverbin
	cd $gamepath
	gspidfile=/tmp/${id}.pid
	num=$(ps -ef | egrep -v "grep|tmux|gdb|core|sh -c" | grep -c ${id}_)
	if [ -f /tmp/stop_$id ] && [ -f /tmp/start_$id ]; then
		if [ $(cat /tmp/stop_$id) -eq 1 ] && [ $(cat /tmp/start_$id) -eq 1 ] &&  [ $(cat /tmp/${id}.pid) -eq 0 ]; then
			checkpro
		fi
		#if [ -f $gspidfile ] && [ $(cat $gspidfile) -eq 0 ] && [ $(cat /tmp/stop_$id) -eq 1 ]; then
	else 
		if [ $num -lt 5 ]  && [ $num -gt 0 ]; then
			checkpro
		fi
	fi
done

rm -f $pidfile
