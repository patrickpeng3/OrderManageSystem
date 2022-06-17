from urllib.error import URLError

from django.contrib.auth.decorators import login_required
import json
import urllib.request
import sys
from django.http import JsonResponse, HttpResponse

# Create your views here.


"""
主机群
"""


@login_required
def host_group(request):
    """
    zabbix主机群
    :param request:
    :return:
    """
    select = request.GET.get("select")


def user_login(request):
    url = "http://XXXXX/zabbix/api_jsonrpc.php"
    header = {
        "Content-Type": "application/json-rpc"
    }
    data = json.dumps({
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": "XXXX",
                "password": "XXXX"
            },
            "id": 2
    }).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=header)
    res = urllib.request.urlopen(req)
    ret = json.loads(res.read().decode("utf-8"))
    authID = ret["result"]
    print(authID)
    return HttpResponse(res.status)
