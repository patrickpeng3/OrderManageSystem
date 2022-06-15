#!/bin/bash
portarray=(`sudo netstat -tnlp|egrep -i "nginx|mysql|_gs"|awk {'print$4'}|egrep -v '^127.0.0|^[1-9]|443|1888|4000'|awk -F':' '{if ($NF~/^[0-9]*$/) print $NF}'|sort|uniq`)
length=${#portarray[@]}
printf "{\n"
printf  '\t'"\"data\":["
for ((i=0;i<$length;i++))
  do
     printf '\n\t\t{'
     printf "\"{#TCP_PORT}\":\"${portarray[$i]}\"}"
     if [ $i -lt $[$length-1] ];then
                printf ','
     fi
  done
printf  "\n\t]\n"
printf "}\n"
