from django.contrib.auth.decorators import login_required
import json
import urllib.request
import sys
from django.http import JsonResponse, HttpResponse
from config.project.tools import get_config_base

zabbix_url = get_config_base("zabbix", "base", "url")
zabbix_header = json.loads(get_config_base("zabbix", "base", "header"))


def get_authID():
    data = json.dumps({
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": "XXXX",
            "password": "XXXX"
        },
        "id": 2
    }).encode("utf-8")
    req = urllib.request.Request(zabbix_url, data=data, headers=zabbix_header)
    res = urllib.request.urlopen(req)
    ret = json.loads(res.read().decode("utf-8"))
    authID = ret["result"]
    return res.status, authID


def get_hostgroup():
    authID = get_authID()[1]
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
    return res.status, ret["result"], authID
