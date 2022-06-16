from urllib.error import URLError

from django.contrib.auth.decorators import login_required
import json
import urllib
import sys

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


class zabbix_tools:
    def __init__(self):
        self.url = "http://company.com/zabbix/api_jsonrpc.php HTTP/1.1"
        self.header = {
            "Content-Type": "application/json-rpc"
        }
        self.authID = self.user_login()

    def user_login(self):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "user.login",
            # "method": "apiinfo.version",
            "params": {
                "user": "pengguanghong",
                "password": "pengguanghong"
            },
            "id": 1
        })
        Request = urllib.request(self.url, data)
        for key in self.header:
            Request.add_header(key, self.header[key])
        try:
            result = urllib.request.urlopen(Request)
        except URLError as e:
            print("Auth Failed, Please Check Your Name And Password:", e.code)
        else:
            response = json.loads(Request.read())
            result.close()
            authID = response['result']
            return authID
