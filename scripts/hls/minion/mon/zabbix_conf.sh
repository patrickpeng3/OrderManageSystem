#!/bin/bash

id=$(grep sg-gs /etc/salt/minion|awk -F- '{print $NF}')
ip=$(curl -s http://metadata.tencentyun.com/latest/meta-data/public-ipv4)
cd /etc/zabbix
sed -i 's/ServerActive=127.0.0.1/ServerActive=118.89.35.203/g' zabbix_agentd.conf
sed -i "s/Hostname=Zabbix server/Hostname=hls-game${id}-${ip}/g" zabbix_agentd.conf
#/etc/init.d/zabbix-agent restart
