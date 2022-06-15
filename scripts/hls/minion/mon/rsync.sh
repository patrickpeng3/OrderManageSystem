#!/bin/bash


pro_check=$(ps -ef|grep rsync|grep daemon|grep -v grep|wc -l)
if [ $pro_check == 0 ];then
cat > /etc/rsyncd.conf <<EOF
uid = 0
gid = 0
port = 8337
use chroot = true
auth users = qmhy
transfer logging = yes
log file = /var/log/rsyncd.log
pid file = /var/run/rsync.pid
lock file = /var/run/rsyncd.lock
secrets file = /etc/rsyncd.secrets
[sync]
comment =
path = /data/game
read only = no
ignore errors = yes
timeout 900
EOF

echo 'qmhy:4nMA-yz!0z' > /etc/rsyncd.secrets
chmod 600 /etc/rsyncd.secrets
sed -i 's/RSYNC_ENABLE=false/RSYNC_ENABLE=true/g' /etc/default/rsync
rm -f /var/run/rsync.pid
rsync --daemon
fi
