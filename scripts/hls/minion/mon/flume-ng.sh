#!/bin/bash

source /etc/profile
echo '10.1.100.11 yf-zk-01' >> /etc/hosts
echo '10.1.100.11 yf-kafka-01' >> /etc/hosts
nohup /usr/local/flume/bin/flume-ng agent -c /usr/local/flume/conf -z yf-zk-01:2181 -p /flume/agent_config -n game -Dflume.root.logger=INFO,console >/dev/null 2>&1 &
