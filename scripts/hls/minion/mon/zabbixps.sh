#!/bin/bash
portarray=(`sudo ps aux | awk '{print $11}' |egrep  "_ls|_ss|_dp|_ws|_gs"|grep -v grep|egrep -v 'session|core|tar'|awk -F'/' {'print $NF'}|sort|uniq|grep ^[1-9]`)
length=${#portarray[@]}
printf "{\n"
printf  '\t'"\"data\":["
for ((i=0;i<$length;i++))
  do
     printf '\n\t\t{'
     printf "\"{#PS}\":\"${portarray[$i]}\"}"
     if [ $i -lt $[$length-1] ];then
                printf ','
     fi
  done
printf  "\n\t]\n"
printf "}\n"
