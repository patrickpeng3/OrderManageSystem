ps aux |awk '{print $4}'|egrep -v '0.0|MEM'|awk '{ NUM += $1} END {print NUM}'
