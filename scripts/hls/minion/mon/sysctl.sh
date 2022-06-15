#!/bin/bash

nofile=$(grep -r MemTotal /proc/meminfo | awk '{printf("%d",$2/10)}')

cat >> /etc/sysctl.conf <<EOF

vm.swappiness = 10
fs.file-max = $nofile
fs.nr_open = ${nofile}0
EOF

sysctl -p
