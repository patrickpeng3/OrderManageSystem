#! /bin/bash

PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'

ID=$1
ver_type=$2
GS_PATH="/data/game/server$ID"
LOG_PATH="/data/game/log/server$ID"
nginxpath='/data/apps/nginx/conf/hosts/'
nginxbin='/data/apps/nginx/sbin/nginx'
export MYSQL_PWD='dkmwebmysql!q$EWQ23FD23'

[[ $ID == '' ]] && echo "please put gameid" && exit 10

# 游服目录检查
function id_check(){
    if [[ ! -d ${GS_PATH} ]];then
        echo "$(date +%F' '%H:%M:%S) ERROR ${ID}目录不存在: ${GS_PATH}" | tee -a "$LOG_PATH"
        echo -e "{\"ServerId\":\"${ID}\",\"Action\":\"Uptime\",\"Status\":\"Error\"}" | tee -a "${LOG_PATH}"
        exit 1
    fi
}

function deletesql() {
	HOST=127.0.0.1
	PORT=3306
	USER=root
	PNAME="${ver_type}_"
	for dname in gamedb logdb memberdb; do
		echo drop database ${PNAME}${dname}_${ID} | /data/apps/mysql/bin/mysql -h${HOST} -u${USER} -P${PORT}
	done
}

function deletefile() {
    [ -d ${GS_PATH} ] && rm -rf ${GS_PATH}
    [ -d ${LOG_PATH} ] && rm -rf ${LOG_PATH}
	rm -f $nginxpath/s${ID}-hls.conf
	$nginxbin -t >/dev/null 2>1
	return=$?
	ngcheck=$(netstat -tnlp | grep -c nginx)
	if [ ${return} -eq 0 ] && [[ ${ngcheck} > 0 ]]; then
		${nginxbin} -s reload && echo "$url 已配置并加载"
	elif [ ${return} -eq 0 ] && [ ${ngcheck} -eq 0 ]; then
		$nginxbin && echo "$url 已配置并启动"
	else
		echo "${nginxpath}/${url}.conf 异常，请检查"
		exit 50
	fi
}

deletefile
deletesql
