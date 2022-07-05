from django.http import JsonResponse
# from models import *
from apps.hls.models import Servers
from apps.hls.packages.server.action_entry import update_entry, start_entry, create_entry, delete_entry, stop_entry
from cmdb_hls.cmdb_logger import SCRIPT_LOGGER
from django.contrib.auth.decorators import login_required


# Create your views here.


# 表格
@login_required()
def server_list_action(request):
    if request.method == "GET":
        server_list = Servers.objects.all()
        data_list = []
        if request.GET.get("method") == "search" and request.GET.get("search_input"):
            server_list = []
            search_input = request.GET.get("search_input")
            server_value_list = Servers.objects.all().values_list()
            for server_value in server_value_list:
                for value in server_value:
                    if str(search_input) in str(value):
                        server_list.append(Servers.objects.filter(id=server_value[0]))
                        break
            for server in server_list:
                server = server[0]
                # if str(search_input) == str(server.server_id):
                data_cfg = {
                    "server_id": server.server_id,
                    "special_server": server.special_server,
                    "salt_id": server.salt_id,
                    "server_host": server.server_host,
                    "backend_version": server.version,
                    "status": server.status,
                    "operation": "operation"
                }
                data_list.append(data_cfg)
                # else:
                #     continue
            if len(data_list) > 0:
                jsonData = {
                    "code": 0,
                    "msg": "",
                    "count": len(data_list),
                    "data": data_list
                }
            else:
                jsonData = {
                    "code": 0
                }
        else:
            for server in server_list:
                data_cfg = {
                    "server_id": server.server_id,
                    "special_server": server.special_server,
                    "salt_id": server.salt_id,
                    "server_host": server.server_host,
                    "backend_version": server.version,
                    "status": server.status,
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
@login_required()
def create_game(request):
    if request.method == "POST":
        special = request.POST.get("L_special")
        number = request.POST.get("L_num")
        SCRIPT_LOGGER.info("执行创服\n专服：{}\n创服数：{}".format(special, number))
        username = request.user.username
        status = create_entry(username, special, number)
        return JsonResponse({"ret": status})


# 更新
@login_required()
def update_game(request):
    if request.method == "POST":
        server_id = request.POST.get("L_serverid")
        version = request.POST.get("L_version")
        SCRIPT_LOGGER.info("执行更新\n游服：{}\n后端版本：｛｝!".format(server_id, version))
        username = request.user.username
        status = update_entry(username, server_id, version)
        return JsonResponse({"ret": status})


# 启服
@login_required()
def start_game(request):
    if request.method == "POST":
        server_id = request.POST.get("L_serverid")
        SCRIPT_LOGGER.info("执行启{}服!".format(server_id))
        username = request.user.username
        status = start_entry(username, server_id)
        return JsonResponse({"ret": status})


# 停服
@login_required()
def stop_game(request):
    if request.method == "POST":
        server_id = request.POST.get("L_serverid")
        SCRIPT_LOGGER.info("执行停{}服!".format(server_id))
        username = request.user.username
        status = stop_entry(username, server_id)
        return JsonResponse({"ret": status})


# 删服
@login_required()
def delete_game(request):
    if request.method == "POST":
        server_id = request.POST.get("L_serverid")
        SCRIPT_LOGGER.info("执行删{}服!".format(server_id))
        username = request.user.username
        status = delete_entry(username, server_id)
        return JsonResponse({"ret": status})


# 修改信息
@login_required()
def edit_game(request):
    if request.method == "GET":
        _id = request.GET.get("id")
        server = Servers.objects.get(server_id=_id)
        jsonData = {
            "server_id": server.server_id,
            "special": server.special_server,
            "servername": server.salt_id,
            "server_host": server.server_host,
            "version": server.version
        }
        return JsonResponse(jsonData)
    if request.method == "POST":
        server_id = request.POST.get("L_serverid")
        special = request.POST.get("L_special")
        servername = request.POST.get("L_server")
        server_host = request.POST.get("L_serverhost")
        version = request.POST.get("L_version")
        try:
            Servers.objects.filter(server_id=server_id).update(
                special_server=special,
                salt_id=servername,
                server_host=server_host,
                version=version
            )
            return JsonResponse({"ret": "success"})
        except Exception:
            return JsonResponse({"ret": "failed"})
