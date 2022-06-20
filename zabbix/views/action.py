from urllib.error import URLError

from django.contrib.auth.decorators import login_required
import json
import urllib.request
import sys
from django.http import JsonResponse, HttpResponse
from ..tools.base import *


# Create your views here.


def get_group(request):
    """
    主机组
    """
    authID = get_authID()
    data = json.dumps({
        "jsonrpc": "2.0",
        "method": "hostgroup.get",
        "params": {
            "output": ["name"],
        },
        "auth": authID,
        "id": 2
    }).encode("utf-8")
    req = urllib.request.Request(zabbix_url, data=data, headers=zabbix_header)
    res = urllib.request.urlopen(req)
    ret = json.loads(res.read().decode("utf-8"))
    return ret["result"]


def get_host(request):
    """
    主机
    """
    group_ret = get_group(request)
    group_list = group_ret
    groupid = ""
    for group in group_list:
        if group["name"] == "唤灵师-游戏服":
            groupid = group["groupid"]
    if not groupid:
        print("获取groupid失败！")
    data = json.dumps({
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "output": ["hostid", "name"],
            "groupids": groupid
        },
        "auth": get_authID(),
        "id": 2
    }).encode("utf-8")
    req = urllib.request.Request(zabbix_url, data=data, headers=zabbix_header)
    res = urllib.request.urlopen(req)
    ret = json.loads(res.read().decode("utf-8"))
    data_list = []
    for host in ret["result"]:
        host_cfg = {
            "hostid": host["hostid"],
            "name": host["name"]
        }
        data_list.append(host_cfg)
    jsonData = {
        "code": 0,
        "count": len(ret["result"]),
        "data": data_list
    }
    return JsonResponse(jsonData)
