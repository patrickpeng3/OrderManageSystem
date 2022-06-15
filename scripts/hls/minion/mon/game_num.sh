#!/bin/bash

list=()
servers=($(ls -l /data/game | grep ^d | awk '{print $NF}' | egrep 'server|cross' | tr -cd '[0-9]\n' | sort | uniq))

printf "{\n"
printf  '\t'"\"data\":["

for i in ${servers[*]};do
    printf '\n\t\t{'
    printf "\"{#SERVERID}\":\"${i}\"}"

    if [ ${i} != ${servers[${#servers[@]}-1]} ]; then
        printf ','
    fi
done

printf  "\n\t]\n"
printf "}\n"
