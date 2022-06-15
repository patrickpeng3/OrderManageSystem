#!/bin/bash

function game_status_check() {
    serverid="$1"
    nginx="/data/apps/nginx/conf/hosts"
    server_conf="/data/game/server${serverid}/serverbin/server.cfg"
    
    ports=($(egrep 'ws_server_port|web_port|fep_server_port|dp_server_port' ${server_conf}  | awk '{print $NF}'))
    
    # 进程数
    process_num=$(ps -ef | egrep -v "grep|tmux|gdb|core|sh"  | egrep -c ./${serverid}_'[ss|ls|ws|gs|dp]')
    # 端口状态
    True=()
    for port in ${ports[*]}; do
        netstat -ntul | grep LISTEN | egrep -w ".*:${port}" > /dev/null &&  True[${#True[*]}]=${port}
    done
    # nginx端口
    if [ "${serverid}" -ge 20000 ]; then
        urlid="${serverid}"
        else
        urlid=$(($serverid-10000))
    fi
    conf="${nginx}"/s"${urlid}"-mrjqtwo.sh9130.com.conf
    nport=$(grep listen $conf  | grep ssl | grep -v \# | awk '{print $2}')
    netstat -ntul | grep LISTEN | egrep -w ".*:${nport}" > /dev/null
    n_return=$?

    # pid文件检测
    statusdir='/data/game/status'
    status=$(cat ${statusdir}/${serverid}.pid)


    if [ "${status}" == '1' ]; then
        echo 1
    elif [ "${process_num}" == '5' ] && [ ${#True[*]} == '4' ] && [ "${status}" == '0' ] && [ "${n_return}" == '0' ] ;then
        echo 1
    else
        echo 0
    fi    
}

game_status_check "$1"
