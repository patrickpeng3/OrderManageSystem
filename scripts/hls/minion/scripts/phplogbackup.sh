#!/bin/bash

ip=$(curl -s http://metadata.tencentyun.com/latest/meta-data/public-ipv4)
salt=$(grep sg-gs /etc/salt/minion|awk '{print $2}')

now=$(date +%Y%m%d)
DAYS=$(date -d"3 day ago"  +"%F")
source_dir='/data/phplogbak/phplog'
bak_dir='/data/backup/phplog'
SENDER='/usr/bin/zabbix_sender'

phplogbak(){
    mkdir -p ${bak_dir}
    cd ${source_dir} && find .  -type f -name "*$DAYS*" -print > /tmp/filelist.txt && tar -zcvf ${bak_dir}/phplog_${now}.tgz --files-from /tmp/filelist.txt
    if [ $? -eq 0 ];then
        if [ $ip != '' ];then
            echo "本地备份成功!"
            md5sum ${bak_dir}/phplog_${now}.tgz > ${bak_dir}/phplog_${now}.md5 && sed -i "s?${bak_dir}?./${salt}_$ip?" ${bak_dir}/phplog_${now}.md5
            echo '4nMA-yz!0z' > /etc/rsyncd.qmhy && chmod 600 /etc/rsyncd.qmhy
            rsync -auvz --progress  --port=8337  --bwlimit=10000 ${bak_dir}/phplog_${now}*  qmhy@10.1.101.168::baksyncdata3/backup/phplog/${salt}_$ip/ --password-file=/etc/rsyncd.qmhy 
            if [ $? -ne 0 ];then
                echo "异地备份失败,请检查!"
                $SENDER -c /etc/zabbix/zabbix_agentd.conf -k "backup_phplog" -o "phplog remote backup failed"
                /usr/bin/python2 /data/mon/wechat.py  2 "A8$salt 备份phplog异常,请检查"
                exit 1
            fi
        else
            echo "公网ip没成功获取,请检查!!!"
            $SENDER -c /etc/zabbix/zabbix_agentd.conf -k "backup_phplog" -o "phplog remote backup failed"
            /usr/bin/python2 /data/mon/wechat.py  2 "A8$salt 备份phplog异常,请检查"
            exit 1
        fi        
    else
        echo "备份失败，请检查!!!"
        $SENDER -c /etc/zabbix/zabbix_agentd.conf -k "backup_phplog" -o "phplog backup failed"
        exit 1
    fi

    $SENDER -c /etc/zabbix/zabbix_agentd.conf -k "backup_phplog" -o ""
    #cd ${source_dir} && find .  -type f -mtime -$DAYS -delete
    #cd ${bak_dir} && find .  -type f -mtime -$DAYS -delete
}

phplogbak
