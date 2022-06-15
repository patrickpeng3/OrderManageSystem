#!/bin/bash
#同步研发日志到内网机
source_dir='/home/developer/log-down'

devlog(){
   echo '4nMA-yz!0z' > /etc/rsyncd.qmhy && chmod 600 /etc/rsyncd.qmhy
   rsync -auvz --progress --port=8337  --bwlimit=10000 ${source_dir}/  qmhy@183.63.145.26::a8h5/ --password-file=/etc/rsyncd.qmhy 
   if [ $? -ne  0 ];then
       echo "异地同步失败,请检查!!!"
   fi

}

devlog
