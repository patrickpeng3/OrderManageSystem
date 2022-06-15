#!/bin/bash

time=$(date +%Y%m%d)
timelog=$(date +'%Y%m%d %T')
log='/data/mysql_backup/mysqlbackup.log'
ip=$(curl -s http://metadata.tencentyun.com/latest/meta-data/public-ipv4)
saltid=$(grep 'sg-gs' /etc/salt/minion|awk '{print $NF}')
mysqlcmd='/data/apps/mysql/bin/mysql'
mysqldumpcmd='/data/apps/mysql/bin/mysqldump'
binlogdir='/data/apps/mysql/data'
backdbdir='/data/mysql_backup/data'
rsyncip='10.1.101.168'
rsyncdbdir='mysql_backup/data'
rsyncbinlogdir='mysql_backup/binlog'
gamedir='/data/game/server'
servers=($(ls -l /data/game | grep ^d | awk '{print $NF}' | egrep 'server|cross' | tr -cd '[0-9]\n' | sort | uniq))


export MYSQL_PWD='dkmwebmysql!q$EWQ23FD23'

mkdir -p ${backdbdir}
echo '4nMA-yz!0z' > /tmp/pass && chmod 600 /tmp/pass

dbbackup(){
for i in ${servers[*]}
do
    cfgfile="${gamedir}${i}/serverbin/server.cfg"
    for dname in $(grep schema $cfgfile | awk '{print $3}'| grep $i|grep -v log)
    do
       $mysqldumpcmd -uroot -h127.0.0.1  -R -E --triggers --skip-opt --create-options -q -e --no-autocommit --master-data=2 --single-transaction $dname|gzip > ${backdbdir}/${dname}_${time}.sql.gz
       if [ $? -eq  0 ];then
           echo "$timelog ${dname} backup secceed" |tee -a $log
           rsync  -az --password-file=/tmp/pass --port=8337 ${backdbdir}/${dname}_${time}.sql.gz qmhy@${rsyncip}::sync/${rsyncdbdir}/${saltid}_${ip}/
           if [ $? -eq  0 ];then
               echo "$timelog ${dname}_${time}.sql.gz rsync secceed" |tee -a $log
           else
               echo "$timelog ${dname}_${time}.sql.gz rsync fail" |tee -a  $log && add_error
           fi
       else
           echo "$timelog ${dname} backup fail" |tee -a  $log && add_error
       fi
    done
done
}

binlogbackup(){
cd ${binlogdir}
for file in $(find . -mtime -2 -type f -name 'mysql-bin.0*'|sed 's#./##g')
do
    rsync  -az --password-file=/tmp/pass --port=8337 ${binlogdir}/${file} qmhy@${rsyncip}::sync/${rsyncbinlogdir}/${saltid}_${ip}/
[ $? -eq  0 ] && echo "$timelog  binlog日志${file}同步成功" |tee -a  $log
done
}

dbdelete(){
cd ${backdbdir} && find . -mtime +7 -type f -delete
[ $? -eq  0 ] && echo "$timelog 7天前数据库备份已清理" |tee -a  $log
}

binlogdelete(){
cd ${binlogdir}
logfile=$(find . -mtime +8 -type f -name 'mysql-bin.0*'|xargs ls -t|head -1|sed 's#./##g')
$mysqlcmd -uroot -h127.0.0.1 -e "purge binary logs to '${logfile}';"
[ $? -eq  0 ] && echo "$timelog 8天前 $logfile binlog日志已清理" |tee -a  $log
}


add_error(){
    error_str+="$saltid:$dname;"
}

main(){
    dbbackup
    binlogbackup
    dbdelete
    binlogdelete
    /usr/bin/zabbix_sender -c /etc/zabbix/zabbix_agentd.conf -k "backup_error" -o "$error_str"
}

main
