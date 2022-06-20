from urllib.error import URLError

from django.contrib.auth.decorators import login_required
import json
import urllib.request
import sys
from django.http import JsonResponse, HttpResponse
from ..tools.base import *


# Create your views here.


"""
主机群
"""


def get_host(request):
    hostgroup_ret = get_hostgroup()
    hostgroup_list = hostgroup_ret[1]
    for hostgroup in hostgroup_list:
        if hostgroup["name"] == "唤灵师-游戏服":
            groupid = hostgroup["groupid"]
    data = json.dumps({
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "output": ["hostid", "name"],
            "groupids": groupid
        },
        "auth": hostgroup_ret[2],
        "id": 2
    }).encode("utf-8")
    req = urllib.request.Request(zabbix_url, data=data, headers=zabbix_header)
    res = urllib.request.urlopen(req)
    ret = json.loads(res.read().decode("utf-8"))
    print(ret)
    return HttpResponse(res.status)
