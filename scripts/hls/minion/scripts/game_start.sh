#!/bin/bash
# a8游戏服启动

# 位置参数
ID=$1
game_status=$2
parm="$*"
parm_num="$#"

# 游戏目录
GS_PATH=/data/game
GAME_PATH=$GS_PATH/server$1
GS_CONF="${GAME_PATH}/server.cfg"

# 操作日志
logdir="/data/gamelog/$(date +%F)"
[ -d "${logdir}" ] || mkdir "${logdir}" -p
logfile="${logdir}/$(date +%H)_${ID}.log"

# 加载系统环境
source /etc/profile

# 检查
function id_check(){
    if [[ ! -d $GS_PATH/server$ID ]];then
        echo "$(date +%F' '%H:%M:%S) ERROR ${ID}服务器不存在,请检查" | tee -a "$logfile"
        echo -e "{\"ServerId\":\"${ID}\",\"Action\":\"Start\",\"Status\":\"Error\"}" | tee -a "${logfile}"
        exit 1
    fi
}

# 端口占用检测
function port_check() {
	num=()
	ports=($(egrep 'ws_server_port|web_port|fep_server_port|dp_server_port' ${GS_CONF}  | awk '{print $NF}'))
	for port in ${ports[*]}; do
        netstat -antulp | awk '{print $4}' | grep -w "$port" && num[${#num[*]}]=${port}
		# lsof -i:${port} &>/dev/null && num[${#num[*]}]=${port}
	done

	if [ ${#num[*]} != '0' ]; then
		echo "$(date +%F' '%H:%M:%S) ERROR ${ID}端口冲突${num[*]}" | tee -a "$logfile"
		echo -e "{\"ServerId\":\"${ID}\",\"Action\":\"Start\",\"Status\":\"Error\"}" | tee -a "${logfile}"
		exit 1
	else 
		echo "$(date +%F' '%H:%M:%S) INFO ${ID}端口未冲突" >> "$logfile"
	fi
}

# 启动
function game_start(){
	echo "$(date +%F' '%H:%M:%S) INFO  ${ID}开始启服" >> "$logfile"
	chown -R hls.hls /data/game/
        su - hls -c "cd $GS_PATH/server$ID/ && ./startsrv" >> "$logfile"
	sleep 5
	for (( i=1 ; i < 35 ; i++  ))
	do 
		CHECK=`ps -ef | egrep -v "grep|tmux|gdb|core|sh"  | grep -c ./${ID}_`
		if [ $CHECK -eq 5 ] || [ $CHECK -eq 6 ] ; then
			tmux ls >> "${logfile}"
			echo -e "{\"ServerId\":\"${ID}\",\"Action\":\"Start\",\"Status\":\"Success\"}" | tee -a "${logfile}"
			break
		elif [ $i -lt 30 ]; then 
			sleep 5
			i=$i+1
			continue
		elif [ $i -gt 30 ]; then
			tmux ls | tee -a "${logfile}"
			echo -e "{\"ServerId\":\"${ID}\",\"Action\":\"Start\",\"Status\":\"Error\"}" | tee -a "${logfile}"
			exit 1
		fi
	done 
}

function main(){
    echo "$(date +%F' '%H:%M:%S) INFO  ${ID}启服操作" >> "$logfile"
    if [ ${parm_num} == '2' ]; then
	if [ ${game_status} == '0' -o ${game_status} == '5' ];then
		id_check
		port_check
		game_start
        else
            echo "$(date +%F' '%H:%M:%S) ERROR ${ID}未处于停服状态!" | tee -a "$logfile"
	    tmux ls | tee -a "${logfile}"
            echo -e "{\"ServerId\":\"${ID}\",\"Action\":\"Start\",\"Status\":\"Error\"}" | tee -a "${logfile}"
        fi
    else
        echo "$(date +%F' '%H:%M:%S) ERROR 参数错误(${parm})" | tee -a "$logfile"
        echo -e "{\"ServerId\":\"${ID}\",\"Action\":\"Start\",\"Status\":\"Error\"}" | tee -a "${logfile}"
    fi
}

main
