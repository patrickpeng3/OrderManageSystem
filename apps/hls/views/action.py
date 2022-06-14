from django.shortcuts import render, redirect, HttpResponse
from django.contrib import auth
from django.http import JsonResponse
# from models import *
from rest_framework.response import Response
from apps.hls.models import Servers


# Create your views here.


def server_list_action(request):
    server_list = Servers.objects.all()
    data_list = []
    for i in range(len(server_list)):
        server = server_list[i]
        data_cfg = {
            "server_id": server.server_id,
            "special_server": server.special_server,
            "salt_id": server.salt_id,
            "server_host": server.server_host,
            "operation": "operation"
        }
        data_list.append(data_cfg)
    jsonData = {
        "code": 0,
        "msg": "",
        "count": len(server_list),
        "data": data_list
    }
    return JsonResponse(jsonData)

