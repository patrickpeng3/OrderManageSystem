#!/bin/bash

# 位置参数
ID=$1
game_status=$2
ctime=$3
parm="$*"
parm_num="$#"

# 游戏目录
GS_PATH=/data/game
GAME_PATH=${GS_PATH}/server${ID}
statusdir='/data/game/status'
pidfile="${statusdir}/${ID}.pid"
start_shpid=/tmp/start_sh.pid
htime=$(date "-d +1 day" +%F)

# 操作日志
logdir="/data/gamelog/$(date +%F)"
[ -d "${logdir}" ] || mkdir "${logdir}" -p
logfile="${logdir}/$(date +%H)_${ID}.log"

[[ $ctime == '' ]]&& ctime=$htime

# 游服目录检查
function id_check(){
    if [[ ! -d ${GAME_PATH} ]];then
        echo "$(date +%F' '%H:%M:%S) ERROR ${ID}目录不存在: ${GAME_PATH}" | tee -a "$logfile"
        echo -e "{\"ServerId\":\"${ID}\",\"Action\":\"Uptime\",\"Status\":\"Error\"}" | tee -a "${logfile}"
        exit 1
    fi
}

# 游戏状态检测
function gsstart_check(){
    echo ${game_status}
    if [[ ${game_status} != 0 ]];then
        echo "$(date +%F' '%H:%M:%S) ERROR ${ID}未处于停服状态!" | tee -a "$logfile"
        echo -e "{\"ServerId\":\"${ID}\",\"Action\":\"Uptime\",\"Status\":\"Error\"}" | tee -a "${logfile}"
        exit 1
    fi

    process_num=$(tmux ls 2> /dev/null | awk -F: '{print $1}' | grep -c ^${ID})
    if [ ${process_num} -gt '0' ]; then 
        echo "$(date +%F' '%H:%M:%S) ERROR ${ID}正在运行，tmux ls" | tee -a "$logfile"
        echo -e "{\"ServerId\":\"${ID}\",\"Action\":\"Uptime\",\"Status\":\"Error\"}" | tee -a "${logfile}"
        exit 1
    else
        echo "$(date +%F' '%H:%M:%S) INFO 检测到${ID}已停服，修改开服时间" >> "$logfile"
    fi
}

# 修改开服时间
function changetime(){
    CONF=$GS_PATH/server$ID/server.cfg
    sed -i "s/^server_born_time =.*/server_born_time = $ctime 00:00:00/g" $CONF &&\
    grep ^server_born_time $CONF >> "${logfile}" &&\
    echo -e "{\"ServerId\":\"${ID}\",\"Action\":\"Uptime\",\"Status\":\"Success\"}" | tee -a "${logfile}"
}

function main(){
    if [ ${parm_num} = '3' ]; then
        id_check
        gsstart_check
        changetime
    elif [ ${parm_num} = '2' ]; then
        ctime=$htime
        id_check
        gsstart_check
        changetime
    else 
        echo "$(date +%F' '%H:%M:%S) ERROR 参数错误(${parm})" | tee -a "$logfile"
        echo -e "{\"ServerId\":\"${ID}\",\"Action\":\"Uptime\",\"Status\":\"Error\"}" | tee -a "${logfile}"
    fi
}

main
