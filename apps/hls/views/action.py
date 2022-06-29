from django.http import JsonResponse
# from models import *
from apps.hls.models import Servers
from apps.hls.packages.server import get_cmd
from apps.hls.packages.server.action_entry import update_entry, start_entry, stop_entry, create_entry, delete_entry
from job_manager.packages.easy_tools import job_start_before, task_runner_celery


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
            "backend_version": server.version,
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


# 搭服
def create_game(request):
    if request.method == "POST":
        special = request.POST.get("L_special")
        number = request.POST.get("L_num")
        username = request.user.username
        create_entry(username, special, number)
        return JsonResponse({"ret": "success"})


# 更新
def update_game(request):
    if request.method == "POST":
        server_id = request.POST.get("L_serverid")
        version = request.POST.get("L_version")
        username = request.user.username
        update_entry(username, server_id, version)
        return JsonResponse({"ret": "success"})


# 启服
def start_game(request):
    if request.method == "POST":
        server_id = request.POST.get("L_serverid")
        username = request.user.username
        start_entry(username, server_id)
        return JsonResponse({"ret": "success"})


# 停服
def stop_game(request):
    if request.method == "POST":
        server_id = request.POST.get("L_serverid")
        username = request.user.username
        stop_entry(username, server_id)
        return JsonResponse({"ret": "success"})


# 删服
def delete_game(request):
    if request.method == "POST":
        server_id = request.POST.get("L_serverid")
        username = request.user.username
        delete_entry(username, server_id)
        return JsonResponse({"ret": "success"})
