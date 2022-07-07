import json

from django.http import JsonResponse
# from models import *
from apps.hls.models import Servers
from apps.hls.packages.server.action_entry import update_entry, start_entry, create_entry, delete_entry, stop_entry
from cmdb_hls.cmdb_logger import SCRIPT_LOGGER
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.request import Request
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action


# Create your views here.


class ActionBase(ViewSet):
    """
    执行基础
    """
    permission_classes = [IsAuthenticated]


class GameList(ActionBase):
    """
    游服列表
    """
    @action(methods=['get'], detail=False)
    def action(self, request):
        server_list = Servers.objects.all()
        data_list = []
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
        form = request.data
        print(form.get("method"))
        print(form.get("search_input"))
        print(form)
        return Response(jsonData)


class CreateGame(ActionBase):
    """
    创服
    """
    @action(methods=['post'], detail=False)
    def action(self, request):
        form = request.data
        special = form.get("L_special")
        number = form.get("L_num")
        SCRIPT_LOGGER.info("执行创服\n专服：{}\n创服数：{}".format(special, number))
        username = request.user.username
        status = create_entry(username, special, number)
        print(special)
        print(number)
        return Response(status)


class UpdateGame(ActionBase):
    """
    更新
    """
    @action(methods=['post'], detail=False)
    def action(self, request):
        form = request.data
        server_id = form.get("L_serverid")
        version = form.get("L_version")
        SCRIPT_LOGGER.info("执行更新\n游服：{}\n后端版本：{}!".format(server_id, version))
        username = request.user.username
        status = update_entry(username, server_id, version)
        print(username)
        print(server_id)
        print(version)
        print(status)
        return Response(status)


class StartGame(ActionBase):
    """
    启服
    """
    @action(methods=['post'], detail=False)
    def action(self, request):
        form = request.data
        server_id = form.get("L_serverid")
        SCRIPT_LOGGER.info("执行启{}服".format(server_id))
        username = request.user.username
        status = start_entry(username, server_id)
        print(server_id)
        print(status)
        return Response(status)


class DeleteGame(ActionBase):
    """
    删服
    """
    @action(methods=['post'], detail=False)
    def action(self, request):
        form = request.data
        server_id = form.get("L_serverid")
        SCRIPT_LOGGER.info("执行删{}服".format(server_id))
        username = request.user.username
        status = delete_entry(username, server_id)
        print(server_id)
        print(status)
        return Response(status)


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


class StopGame(ActionBase):
    """
    停服
    """
    @action(methods=['post'], detail=False)
    def action(self, request):
        form = request.data
        server_id = form.get("L_serverid")
        SCRIPT_LOGGER.info("执行停{}服!".format(server_id))
        username = request.user.username
        status = stop_entry(username, server_id)
        print(server_id)
        print(status)
        return Response(status)
