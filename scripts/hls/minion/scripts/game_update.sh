#!/bin/bash
# 大版本更新

# 位置参数
ID=$2
GS_FILE=$1
game_status=$3
parm="$*"
parm_num="$#"

# 游戏目录 
GS_PATH=/data/game
GAME_PATH=${GS_PATH}/server$ID
GSFIX_PATH=/data/gs_hotfix
BAK_GS=/data/bak_game
GS_CONF="${GAME_PATH}/server.cfg"

# 版本
update_version=$(echo ${GS_FILE} | awk -F_ '{print $3}')           #需要更新版本
version=$(grep 'major_version' ${GAME_PATH}/version.txt|awk '{print $3}')

# 操作日志
logdir="/data/gamelog/$(date +%F)"
[ -d "${logdir}" ] || mkdir "${logdir}" -p
logfile="${logdir}/$(date +%H)_${ID}.log"

# mysql
mysql=/data/apps/mysql/bin/mysql
export MYSQL_PWD='dkmwebmysql!q$EWQ23FD23'

# 检查游服目录
function id_check(){
    if [[ ! -d $GAME_PATH ]];then
        echo "$(date +%F' '%H:%M:%S) ERROR ${ID}目录不存在: ${GAME_PATH}" | tee -a "$logfile"
        echo -e "{\"ServerId\":\"${ID}\",\"Action\":\"Start\",\"Status\":\"Error\"}" | tee -a "${logfile}"
        exit 1
    fi
}

# 获取更新包
function sync_package() {
    echo "$(date +%F' '%H:%M:%S) INFO  ${ID}获取更新包${GS_FILE}" >> "$logfile"

    echo "o7XNa0KAsz9vQck0jO" >/etc/pass.wmsg
    chmod 600 /etc/pass.wmsg
    [ ! -d $GSFIX_PATH ] && mkdir $GSFIX_PATH
    rsync -av --password-file=/etc/pass.wmsg gamebf@10.1.220.5::packhotfix/bak/${GS_FILE} $GSFIX_PATH --port=8337 >/dev/null
    
    if [ $? == '0' ] && [ -f $GSFIX_PATH/${GS_FILE}/${GS_FILE}.zip ]; then 
        echo "$(date +%F' '%H:%M:%S) INFO  ${ID}成功获取更新包: ${GS_FILE}" >> "$logfile"
    else
        echo "$(date +%F' '%H:%M:%S) ERROR ${ID}未获取更新包: ${GS_FILE}" >> "$logfile"
        echo -e "{\"ServerId\":\"${ID}\",\"Action\":\"Update\",\"Status\":\"Error\"}" | tee -a "${logfile}"
        exit 1
    fi
}

# 停服更新
function update_game(){
    echo "$(date +%F' '%H:%M:%S) INFO  ${ID}开始更新 ${GS_FILE}" >> "$logfile"
    [ ! -d $GSFIX_PATH ] && mkdir $GSFIX_PATH

    if [ ! -f $GSFIX_PATH/${GS_FILE}/${GS_FILE}.zip ];then
        echo "$(date +%F' '%H:%M:%S) ERROR ${ID}未获取更新包: ${GS_FILE}"|tee -a "$logfile"
        exit 1
    fi

    cd $GAME_PATH && unzip -o $GSFIX_PATH/${GS_FILE}/${GS_FILE}.zip -x server.cfg -d ./ > /dev/null 2>&1 && echo "$(date +%F' '%H:%M:%S) INFO  ${ID}成功解压${GS_FILE}至$GAME_PATH" >> "$logfile"
    for fname in ws dp ss ls gs; do
        if [ -f "$fname" ]; then
            chmod +x $fname
        fi
    done

    listmd5=`md5sum -c $GSFIX_PATH/$GS_FILE/md5.list |awk '{print $NF}'|sort|uniq`
    listcheckmd5=`md5sum -c $GSFIX_PATH/$GS_FILE/md5.list |awk '{print $NF}'|sort|uniq -c|wc -l`
    if [ $listcheckmd5 != 1 -o ${listmd5} != 'OK' ];then
       echo "$(date +%F' '%H:%M:%S) ERROR ${ID}MD5对比失败 ${GS_FILE}" | tee -a "$logfile"
       echo -e "{\"ServerId\":\"${ID}\",\"Action\":\"Update\",\"Status\":\"Error\"}" | tee -a "${logfile}"
       exit 1
    else
       echo "$(date +%F' '%H:%M:%S) INFO  ${ID}MD5对比成功,更新文件完成 ${GS_FILE}" >> "$logfile" 
    fi
}

function createsql(){
    HOST=127.0.0.1
    PORT=3306
    USER=root

    dos2unix $GAME_PATH/server.cfg  >/dev/null 2>1 &
    
    # 写入新表
    for dname in $(grep schema $GAME_PATH/server.cfg |awk '{print $3}'|grep $ID); do
        mysqlcheck=$($mysql -h${HOST} -u${USER}  -P${PORT} -e "show databases" | grep -c ${dname})
        
        if [ $mysqlcheck -eq 0 ];then
            echo "$(date +%F' '%H:%M:%S) ERROR 未找到该数据库: ${dname}" | tee -a "$logfile"
            echo -e "{\"ServerId\":\"${ID}\",\"Action\":\"Update\",\"Status\":\"Error\"}" | tee -a "${logfile}"
            exit 1
        else
            pname=$(echo $dname|awk -F'_' '{print $2}')
            for ver in $(seq $(expr $version + 1) ${update_version});do
                $mysql -h${HOST} -u${USER}  -P${PORT} ${dname} < $GAME_PATH/db_script/${ver}/reset_${pname}.sql  
                if [ $? == '0' ]; then 
                    echo "$(date +%F' '%H:%M:%S) INFO ${dname}已更新sql文件: $GAME_PATH/db_script/${ver}/reset_${pname}.sql" >> "$logfile"
                else
                    echo "$(date +%F' '%H:%M:%S) ERROR ${dname}更新sql文件: $GAME_PATH/db_script/${ver}/reset_${pname}.sql失败" | tee -a "$logfile"
                    exit 1
                fi
            done
        fi
    done

}

function sql_check(){
    game_db=$(grep ^db_game_schema ${GS_CONF} | awk '{print $3}')
	
    num=$(${mysql} -h${HOST} -uroot -N -e "use ${game_db}; select count(1) from server_sql_ver where version=${update_version} ;" )
  
    if [ ${num} == 0 ]; then
        echo "$(date +%F' '%H:%M:%S) ERROR ${ID}更新${update_version}版本SQL失败" | tee -a "$logfile"
        echo -e "{\"ServerId\":\"${ID}\",\"Action\":\"Update\",\"Status\":\"Error\"}" | tee -a "${logfile}"
        exit 1
    elif [ ${num} == 1 ];then
        echo "$(date +%F' '%H:%M:%S) INFO ${ID}更新${update_version}版本SQL成功" | tee -a "$logfile"
        echo -e "{\"ServerId\":\"${ID}\",\"Action\":\"Update\",\"Status\":\"Success\"}" | tee -a "${logfile}"
    else
        echo "$(date +%F' '%H:%M:%S) ERROR ${ID}更新${update_version}异常,检查数据库" | tee -a "$logfile"
        echo -e "{\"ServerId\":\"${ID}\",\"Action\":\"Update\",\"Status\":\"Error\"}" | tee -a "${logfile}"
        exit 1
    fi

}

function hotfix_game() {
    echo "$(date +%F' '%H:%M:%S) INFO  ${ID}开始热更 ${GS_FILE}" >> "$logfile"

    cd $GAME_PATH && unzip -o $GSFIX_PATH/${GS_FILE}/${GS_FILE}.zip -x server.cfg -d ./ &> /dev/null && echo "$(date +%F' '%H:%M:%S) INFO  ${ID}成功解压${GS_FILE}至$GAME_PATH" >> "$logfile"

    listmd5=`md5sum -c $GSFIX_PATH/$GS_FILE/md5.list |awk '{print $NF}'|sort|uniq`
    listcheckmd5=`md5sum -c $GSFIX_PATH/$GS_FILE/md5.list |awk '{print $NF}'|sort|uniq -c|wc -l`

    if [ $listcheckmd5 != 1 -o ${listmd5} != 'OK' ]; then
        echo "$(date +%F' '%H:%M:%S) ERROR ${ID}MD5对比失败 ${GS_FILE}" | tee -a "$logfile"
        echo -e "{\"ServerId\":\"${ID}\",\"Action\":\"Update\",\"Status\":\"Error\"}" | tee -a "${logfile}"
        exit 1
    else
        echo "$(date +%F' '%H:%M:%S) INFO ${ID}MD5一致，调用研发脚本 ${GS_FILE}" >> "$logfile"
        bash $GAME_PATH/hotfix.sh >> "$logfile"
        if [ $? == '0' ]; then
            echo -e "{\"ServerId\":\"${ID}\",\"Action\":\"Update\",\"Status\":\"Success\"}" | tee -a "${logfile}"
        else
            echo "$(date +%F' '%H:%M:%S) ERROR ${ID}MD5热更返回值非0 ${GS_FILE}" | tee -a "$logfile"
            echo -e "{\"ServerId\":\"${ID}\",\"Action\":\"Update\",\"Status\":\"Error\"}" | tee -a "${logfile}"
            exit 1
        fi
    fi

    for fname in ws dp ss ls gs; do
        if [ -f "$fname" ]; then
            chmod +x $fname
        fi
    done
}

function main(){
    echo "$(date +%F' '%H:%M:%S) INFO  ${ID}更新${GS_FILE}操作" >> "$logfile"
    if [ ${parm_num} != '3' ]; then 
        echo "$(date +%F' '%H:%M:%S) ERROR 参数错误(${parm})" | tee -a "$logfile"
        echo -e "{\"ServerId\":\"${ID}\",\"Action\":\"Update\",\"Status\":\"Error\"}" | tee -a "${logfile}"
        exit 1
    fi
    if [[ ${GS_FILE} =~ bs_hls_.* ]]; then
        if [ ${game_status} != 0 ]; then
            echo "$(date +%F' '%H:%M:%S) ERROR ${ID}未处于停服状态!" | tee -a "$logfile"
            echo -e "{\"ServerId\":\"${ID}\",\"Action\":\"Update\",\"Status\":\"Error\"}" | tee -a "${logfile}"
            exit 1
        else
            id_check
            num=`expr $update_version - $version`
            if [ "${num}" -lt 0 ]; then
                echo "$(date +%F' '%H:%M:%S) ERROR 请检查更新版本是否正确" | tee -a "$logfile"
                echo -e "{\"ServerId\":\"${ID}\",\"Action\":\"Update\",\"Status\":\"Error\"}" | tee -a "${logfile}"
                exit 1
            elif [ "${num}" -eq 0 ]; then
                #sync_package
                update_game
            elif [ "${num}" -gt 0 ]; then
                #sync_package
                update_game
                createsql
                sql_check
            fi
        fi
    elif [[ ${GS_FILE} =~ hotfix_tdc_.* ]]; then
		id_check
		#sync_package
		hotfix_game
    fi
}

main
