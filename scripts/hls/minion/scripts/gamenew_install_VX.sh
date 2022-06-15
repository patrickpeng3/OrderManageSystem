#! /bin/bash
#文明曙光新服脚本

PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'

ID=$1
listen_port=$1
moban_name=$2
GS_PATH="/data/game/server$ID"
LOG_PATH="/data/game/log/server$ID"
GS_CONF="${GS_PATH}/server.cfg"
IP=$(curl -s http://metadata.tencentyun.com/latest/meta-data/public-ipv4)
ip2=$(ip a | grep inet | awk -F'[ /]+' '{print $3}' | grep -v 127.0.0.1)
nginxpath='/data/apps/nginx/conf/hosts/'
#BAK_ID=$3
should_ver=$(echo ${moban_name} | awk -F'hls_' '{print $2}')
ver_type=$(echo ${moban_name} | awk -F_ '{print $1}')
sql_ver=$(echo ${moban_name} | awk -F_ '{print $3}')
NUM=$3

url="s${ID}-hls.sh9130.com"
nginxbin='/data/apps/nginx/sbin/nginx'
BAK_PATH='/data/backup'
export MYSQL_PWD='dkmwebmysql!q$EWQ23FD23'

[[ $ID == '' ]] && echo "please put gameid" && exit 10
[[ -d ${GS_PATH} ]] && echo " $ID 已经存在  " && exit 20
[ -d ${LOG_PATH} ] || mkdir -p ${LOG_PATH}
[[ ! -d ${BAK_PATH} ]] && mkdir ${BAK_PATH}

function filersync() {
	echo "4nMA-yz!0z" >/etc/pass.wmsg
	chmod 600 /etc/pass.wmsg
	rsync -av --password-file=/etc/pass.wmsg qmhy@10.1.220.5::sync/game_Template/${moban_name}/ $GS_PATH/ --port=8337 >/dev/null 2>1
	if [ $? = 0 ]; then
		apt-get install dos2unix >/dev/null && dos2unix ${GS_CONF} >/dev/null 2>1
		sed -i 's/db_member_schema = hls_memberdb/db_member_schema = '${ver_type}'_memberdb_'$ID'/g' ${GS_CONF}
		sed -i 's/db_game_schema = hls_gamedb/db_game_schema = '${ver_type}'_gamedb_'$ID'/g' ${GS_CONF}
		sed -i 's/db_log_schema = hls_logdb/db_log_schema = '${ver_type}'_logdb_'$ID'/g' ${GS_CONF}
		sed -i 's/server_cluster =.*/server_cluster = '$ID'/g' ${GS_CONF}
		sed -i 's/fep_ip = .*/fep_ip = '$ip2'/g' ${GS_CONF}
		sed -i 's/ws_ip = .*/ws_ip = '$ip2'/g' ${GS_CONF}
		sed -i 's/ip_for_server = .*/ip_for_server = '$ip2'/g' ${GS_CONF}
		sed -i 's/ip_for_client_connect =.*/ip_for_client_connect = '$IP'/g' ${GS_CONF}
		sed -i 's/web_port =.*/web_port = '$(echo 1990+${NUM} | bc)'/g' ${GS_CONF}
		sed -i 's/ws_server_port =.*/ws_server_port = '$(echo 18880+${NUM} | bc)'/g' ${GS_CONF}
		sed -i 's/fep_client_port =.*/fep_client_port = '$(echo 6660+${NUM} | bc)'/g' ${GS_CONF}
		sed -i 's/fep_server_port =.*/fep_server_port = '$(echo 25000+${NUM} | bc)'/g' ${GS_CONF}
		sed -i 's/dp_server_port =.*/dp_server_port = '$(echo 40000+${NUM} | bc)'/g' ${GS_CONF}
	#	echo "=======version: `cat $GS_PATH/version.txt`======="
	else
		echo "game is not rsync,please check it"
		exit 10
	fi
}

function createsql() {
	HOST=127.0.0.1
	PORT=3306
	USER=root
	PNAME="${ver_type}_"
	for dname in gamedb logdb memberdb; do
		echo create database ${PNAME}${dname}_${ID} DEFAULT CHARACTER SET utf8 | /data/apps/mysql/bin/mysql -h${HOST} -u${USER} -P${PORT}
	done

	time=$(date +%F)
	BAK_HOST=10.1.220.5
	#BAK_ID=9999
	for dname in gamedb logdb memberdb; do
		/data/apps/mysql/bin/mysqldump -h${BAK_HOST} -u${USER} -p'dkmwebmysql!q$EWQ23FD23' -R -E -d -P${PORT} ${ver_type}_${dname}_${sql_ver} >$BAK_PATH/${PNAME}${dname}_${time}_jiegou.sql
	done

	for dname in gamedb logdb memberdb; do
		/data/apps/mysql/bin/mysql -h${HOST} -u${USER} -P${PORT} ${PNAME}${dname}_${ID} <$BAK_PATH/${PNAME}${dname}_${time}_jiegou.sql
	done
}

function nginxconf() {
	cat >$nginxpath/s${ID}-hls.conf <<EOF
upstream my_server$ID {                                                         
    server 127.0.0.1:$((1990 + ${NUM}));                                                
    keepalive 2000;
}
server {
    listen       ${listen_port} ssl;
    #server_name  $url;
    client_max_body_size 1024M;
    ssl_certificate    /data/apps/nginx/conf/ssl/sh9130.com.crt;
    ssl_certificate_key   /data/apps/nginx/conf/ssl/sh9130.com.key;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location  / {
        proxy_pass http://my_server$ID/;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header Host \$host;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
         proxy_http_version 1.1;
   proxy_set_header Upgrade \$http_upgrade;
   proxy_set_header Connection "upgrade";
    }
    access_log /data/logs/${url}.log main;
}
EOF

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

function printinfo() {
  gsport=$(grep ^web_port ${GS_CONF})
  ver=$(grep version ${GS_PATH}/version.txt | head -1|awk -F' ' '{print $3}')
  type=$(grep type ${GS_PATH}/version.txt|tail -1|awk -F' ' '{print $3}')

  if [[ $ver == $should_ver ]];then
      echo "${gsport}"'|res_version = '"${ver}"
  else
      echo "游服"$ID"版本号不一致！"
      echo "当前版本："$ver"  应装版本："$should_ver
      exit 5
  fi
	
	ver1=$(echo $ver|awk -F_ '{print $1}')
  ver2=$(echo $ver|awk -F_ '{print $2}')
	if [[ $type == $ver_type ]];then
		echo "版本类型：$ver_type"
	else
		echo "版本类型错误!"
		exit 5
	fi
}

filersync
createsql
nginxconf
printinfo
#mysql -uroot  -e "grant all on *.* to ht@10.1.100.2 identified by 'mysql!q$EWQ23FD23';"
#mysql -uroot  -e "grant all on *.* to ht@10.1.100.4 identified by 'mysql!q$EWQ23FD23';"
mysql -uroot -e "grant all on *.* to cpread@14.29.126.52 identified by 'kaIla.1k12';"
mysql -uroot -e "grant all on *.* to cpread@127.0.0.1 identified by 'kaIla.1k12';"
