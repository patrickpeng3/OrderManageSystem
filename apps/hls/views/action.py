from django.http import JsonResponse
# from models import *
from apps.hls.models import Servers
from apps.hls.packages.server import get_cmd
from job_manager.packages.easy_tools import job_start_before


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


def create_game(request):
    if request.method == "POST":
        special = request.POST.get("L_special")
        number = request.POST.get("L_num")
        cmd = get_cmd.create_game(special, number)
        return JsonResponse({"ret": "success"})


def update_game(request):
    if request.method == "POST":
        server_id = request.POST.get("L_serverid")
        version = request.POST.get("L_version")
        cmd_list = []
        get_cmd.update_game(server_id, version, cmd_list)
        job_task, job_cmds = job_start_before("更新", "pengguanghong", update_game, cmd_list)
        print("job_task:{}".format(job_task))
        print("job_cmds:{}".format(job_cmds))
        for job_cmd in job_cmds:
            cmd = job_cmd["model"].cmd
            print("CMD:{}".format(cmd))
        return JsonResponse({"ret": "success"})
