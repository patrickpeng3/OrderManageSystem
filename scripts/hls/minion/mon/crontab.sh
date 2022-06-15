#!/bin/bash

crontab -l > /tmp/crontab.bak

cat >> /tmp/crontab.bak <<EOF

#mysql备份
0 3 * * * /bin/bash /data/mon/mysqlbackup.sh > /dev/null 2>&1 &
EOF

crontab /tmp/crontab.bak && rm -f /tmp/crontab.bak
