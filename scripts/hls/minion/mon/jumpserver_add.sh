#!/bin/bash

#useradd
useradd jumpserver -m -s /bin/bash;mkdir /home/jumpserver/.ssh;echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCrqUW/DKoWwKDSolPpt16YgumtNKlfqmAUw+SVn4cIlr8JdhCRoPQMfRrgeCIMspHiSXmULsQyAgmQBT7iiCGuWANLbLqS0IrG4aIc/p8Fzapda/tRaJ/DJ4GijIDnA8ugVO1Jcmu4QPJK8v6UHAI//1spph1M50lrzLfYHmd1KH+ZE9iUKl7HOh+MP3/ptjXRJjPQNBM+uIko7larGuZF5SDczarybBg9amEabbudoZo5Y6O3r6Ivhqh65hAecP9FZYl9lFnsxFZAJ6BMn6W4zwwWKICYP3a6XphKiGYqKVj0FEAMorOGwnOHqDr7msnyMKrkuyQkyVkiey8uZCOt 9130@guest' >> /home/jumpserver/.ssh/authorized_keys;chmod 700 /home/jumpserver;chmod 700 /home/jumpserver/.ssh;chmod 600 /home/jumpserver/.ssh/authorized_keys;chown jumpserver.jumpserver -R /home/jumpserver;echo -e "jumpserver \tALL=(ALL) \tNOPASSWD: ALL" >> /etc/sudoers

#jumpserver
jumpserver(){
    apiurl="http://43.228.183.79:44380/api/v1/assets/assets/"
    #apiurl="http://183.63.145.26:44380/api/v1/assets/assets/"
    #apiurl="http://192.168.40.232/api/v1/assets/assets/"
    token="3d49ba6bd46359de5abc2d2b99ce71f3625b1761"
    id=$(< /dev/urandom tr -dc '0-9a-f'|head -c 32)
    salt=$(grep sg-gs /etc/salt/minion|awk '{print $2}')
    pub_ip=$(curl -s http://metadata.tencentyun.com/latest/meta-data/public-ipv4)
    #ip=$(hostname -I|sed 's/ //g')
    ip=${pub_ip}
    hostname=A8two-${salt}--${pub_ip}
    port=22
    platform=linux
    created_by=Administrator
    a=$(< /dev/urandom tr -dc '0-9'|head -c 6)
    date_created=$(date "+%F %H:%M:%S.${a}")
    admin_user_id=707dbb81460e4a9382a5e11b4843f93f
    domain_id=5cd8150f92be4aba861643156f739385
    node_id=eba2d05bf9844213910df0fb809a6d2c
    protocol=ssh
    protocols=${protocol}/${port}

    

    #echo "INSERT INTO jumpserver.assets_asset ( id,ip,hostname,port,is_active,platform,created_by,date_created,admin_user_id,domain_id,protocol,protocols,comment,org_id ) VALUES ( '${id}','${ip}','${hostname}','${port}','1','${platform}','${created_by}','${date_created}','${admin_user_id}','${domain_id}','${protocol}','${protocols}','','');"

    curl -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' -H "Authorization: Token ${token}" -d "{\"id\": \"${id}\",\"ip\": \"${ip}\",\"hostname\": \"${hostname}\",\"port\": ${port},\"platform\": \"Linux\",\"is_active\": true,\"public_ip\": \"${pub_ip}\",\"domain\": \"${domain_id}\",\"created_by\": null,\"comment\": \"\",\"admin_user\": \"${admin_user_id}\", \"nodes\": [\"${node_id}\"]}"  $apiurl
}

jumpserver
