pidname=$1
if [ -z $pidname ];then
    echo 
else
	num=$(sudo lsof -c $pidname |wc -l)
	echo $num
fi
