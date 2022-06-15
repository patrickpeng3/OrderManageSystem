#!/bin/bash
# a8游戏服关服

# 位置参数
ID=$1
game_status=$2
parm="$*"
parm_num="$#"

# 游戏目录
GS_PATH=/data/game
GAME_PATH=$GS_PATH/server$1

# mysql
mysql=/data/apps/mysql/bin/mysql
export PATH=$PATH:/usr/local/bin:/usr/local/sbin/

# 操作日志
logdir="/data/gamelog/$(date +%F)"
[ -d "${logdir}" ] || mkdir "${logdir}" -p
logfile="${logdir}/$(date +%H)_${ID}.log"

function id_check(){
    if [[ ! -d $GS_PATH/server$ID ]];then
        echo "$(date +%F' '%H:%M:%S) ERROR ${ID}服务器不存在,请检查" | tee -a "$logfile"
        echo -e "{\"ServerId\":\"${ID}\",\"Action\":\"Stop\",\"Status\":\"Error\"}" | tee -a "${logfile}"
        exit 1
    fi
}

function game_stop() {
    echo "$(date +%F' '%H:%M:%S) INFO  ${ID}开始停服" >> "$logfile"
    chown -R hls.hls /data/game/
    su - hls -c "cd $GS_PATH/server$ID/ && ./stopsrv" >> "$logfile"
    for (( i=1 ; i < 10 ; i++  ))
    do
        CHECK=`ps -ef|grep ${ID}_|egrep -v 'grep|new-session' |wc -l`
        if [[ $CHECK == 0 ]];then
            echo -e "{\"ServerId\":\"${ID}\",\"Action\":\"Stop\",\"Status\":\"Success\"}" | tee -a "${logfile}"
            break
        elif (( $i < 10 ));then
            sleep 5
            i=$i+1
            continue
        else
            echo -e "{\"ServerId\":\"${ID}\",\"Action\":\"Stop\",\"Status\":\"Error\"}" | tee -a "${logfile}"
            tmux ls | tee -a "${logfile}"
            echo "$(ps -ef|grep $ID|egrep -v 'grep|new-session')" >> "${logfile}"
            exit 1
        fi
    done
}

function db_bak() {
    HOST=127.0.0.1
    PORT=3306
    USER=root
    time=$(date +%F_%H%M)
    BAK_PATH=/data/backup
    export MYSQL_PWD='dkmwebmysql!q$EWQ23FD23'

    dos2unix $GAME_PATH/serverbin/server.cfg &> /dev/null
    for dname in $(grep schema $GAME_PATH/server.cfg | awk '{print $3}'| grep $ID|grep -v 'logdb'); do
        
        echo "$(date +%F' '%H:%M:%S) INFO  开始备份数据库${dname}" >> "$logfile"

        mysqlcheck=$($mysql -h${HOST} -u${USER}  -P${PORT} -e "show databases" | grep -c ${dname})

        if [[ $dname == '' ]];then
            echo "$(date +%F' '%H:%M:%S) ERROR 未找到对应数据库，请检查" | tee -a "$logfile"
        elif [ $mysqlcheck -eq 0 ];then
            echo "$(date +%F' '%H:%M:%S) ERROR 数据库中未找到${dname}" | tee -a "$logfile"
        else
            /data/apps/mysql/bin/mysqldump -h${HOST} -u${USER}  -R -E  -P${PORT} --databases $dname |gzip >$BAK_PATH/${dname}_${time}.sql.gz &&\
            /data/apps/mysql/bin/mysqldump -h${HOST} -u${USER}  -R -E -d  -P${PORT}  $dname | sed 's/AUTO_INCREMENT=[0-9]*\s//g' >$BAK_PATH/${dname}_jiegou.sql
            if [ $? == '0' ];then 
                echo "$(date +%F' '%H:%M:%S) INFO  数据库${dname}备份完成" >> "$logfile"
            else 
                echo "$(date +%F' '%H:%M:%S) ERROR 数据库${dname}备份失败" | tee -a "$logfile"
            fi
        fi
    done
}


function main(){
    echo "$(date +%F' '%H:%M:%S) INFO  ${ID}停服操作" >> "$logfile"
    if [ ${parm_num} == '2' ]; then 
        if [ ${game_status} == '1' -o ${game_status} == '5' ]; then
            id_check
            game_stop
            db_bak
        else
            echo "$(date +%F' '%H:%M:%S) ERROR ${ID}未运行!" | tee -a "$logfile"
            echo -e "{\"ServerId\":\"${ID}\",\"Action\":\"Stop\",\"Status\":\"Error\"}" | tee -a "${logfile}"
        fi
    else
        echo "$(date +%F' '%H:%M:%S) ERROR 参数错误(${parm})" | tee -a "$logfile"
        echo -e "{\"ServerId\":\"${ID}\",\"Action\":\"Stop\",\"Status\":\"Error\"}" | tee -a "${logfile}"
    fi
}

main
