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
    def game_action(self, request):
        server_list, data_list = [[] for i in range(2)]
        form = request.GET
        method = form.get("method")
        search_value = form.get("search_input")
        if method == "search" and search_value:
            server_value_list = Servers.objects.all().values()
            for server_value in server_value_list:
                for k, v in server_value.items():
                    if str(search_value) in str(v):
                        server = Servers.objects.filter(id=server_value['id'])[0]
                        server_list.append(server)
                        break
        else:
            server_list = Servers.objects.all()
        for server in server_list:
            data_cfg = {
                "server_id": server.server_id,
                "special_server": server.special_server,
                "salt_id": server.salt_id,
                "server_host": server.server_host,
                "front_version": server.front_version,
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
        return Response(jsonData)


class CreateGame(ActionBase):
    """
    创服
    """
    @action(methods=['post'], detail=False)
    def game_action(self, request):
        form = request.data
        status = "success"
        special = form.get("L_special")
        number = form.get("L_num")
        SCRIPT_LOGGER.info("执行创服\n专服：{}\n创服数：{}".format(special, number))
        username = request.user.username
        create_entry(username, special, number)
        return Response(status)


class UpdateGame(ActionBase):
    """
    更新
    """
    @action(methods=['post'], detail=False)
    def game_action(self, request):
        form = request.data
        status = "success"
        server_id = form.get("L_serverid")
        version = form.get("L_version")
        SCRIPT_LOGGER.info("执行更新\n游服：{}\n后端版本：{}!".format(server_id, version))
        username = request.user.username
        update_entry(username, server_id, version)
        return Response(status)


class StartGame(ActionBase):
    """
    启服
    """
    @action(methods=['post'], detail=False)
    def game_action(self, request):
        form = request.data
        status = "success"
        server_id = form.get("L_serverid")
        SCRIPT_LOGGER.info("执行启{}服".format(server_id))
        username = request.user.username
        start_entry(username, server_id)
        return Response(status)


class StopGame(ActionBase):
    """
    停服
    """
    @action(methods=['post'], detail=False)
    def game_action(self, request):
        form = request.data
        status = "success"
        server_id = form.get("L_serverid")
        SCRIPT_LOGGER.info("执行停{}服!".format(server_id))
        username = request.user.username
        stop_entry(username, server_id)
        return Response(status)


class DeleteGame(ActionBase):
    """
    删服
    """
    @action(methods=['post'], detail=False)
    def game_action(self, request):
        form = request.data
        status = "success"
        server_id = form.get("L_serverid")
        SCRIPT_LOGGER.info("执行删{}服".format(server_id))
        username = request.user.username
        delete_entry(username, server_id)
        return Response(status)


class EditGame(ActionBase):
    """
    修改信息
    """
    @action(methods=['post'], detail=False)
    def game_action(self, request):
        form = request.data
        status = "success"
        server_id = form.get("L_serverid")
        special_server = form.get("L_special")
        salt_id = form.get("L_server")
        server_host = form.get("L_serverhost")
        front_version = form.get("L_frontver")
        version = form.get("L_version")
        try:
            Servers.objects.filter(server_id=server_id).update(
                special_server=special_server,
                salt_id=salt_id,
                server_host=server_host,
                front_version=front_version,
                version=version
            )
        except Exception:
            status = "failed"
            SCRIPT_LOGGER.info("{}服修改信息失败！".format(server_id))
        return Response(status)


