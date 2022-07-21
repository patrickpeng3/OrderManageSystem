import json
import time
from cmdb_hls.cmdb_logger import SCRIPT_LOGGER
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.viewsets import ModelViewSet
from job_manager.models import JobTask, JobCmd
from job_manager.serializer import JobCmdInfoSerializer, JobCmdSimpleSerializer, JobTaskWebSocketInfoSerializer, \
    JobTaskSimpleSerializer, JobTaskInfoSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from dwebsocket import accept_websocket, require_websocket


# Create your views here.


@login_required
def server_log(request):
    """运维日志页"""
    return render(request, "X-admin/log.html")


class JobTaskInfoViewSet(ModelViewSet):
    """
    任务信息视图集
    """
    queryset = JobTask.objects.all()
    serializer_class = JobTaskInfoSerializer
    search_fields = ('name', 'username')
    ordering_fields = ('start_time', 'end_time')
    filter_fields = ('status',)
    permission_classes = [AllowAny]


class JobCmdInfoViewSet(ModelViewSet):
    """
    命令视图集
    """
    queryset = JobCmd.objects.all()
    serializer_class = JobCmdInfoSerializer
    permission_classes = [AllowAny]
