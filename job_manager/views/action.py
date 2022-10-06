import os
import time
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from job_manager.models import JobTask, JobCmd


class ActionBase(ViewSet):
    """
    执行基础
    """
    # permission_classes = [IsAuthenticated]


class TaskList(ViewSet):
    """
    任务列表
    """
    @action(methods=['get'], detail=False)
    def log_action(self, request):
        task_list, data_list = [[] for i in range(2)]
        form = request.GET
        method = form.get("method")
        search_value = form.get("search_input")
        if method == "search" and search_value:
            server_value_list = JobTask.objects.all().values()
            for server_value in server_value_list:
                for k, v in server_value.items():
                    if str(search_value) in str(v):
                        server = JobTask.objects.filter(id=server_value['id'])[0]
                        task_list.append(server)
                        break
        else:
            task_list = JobTask.objects.all()
        for task in task_list:
            data_cfg = {
                "name": task.name,
                "username": task.username,
                "start_time": task.start_time,
                "end_time": task.end_time,
                "status": task.status,
            }
            data_list.append(data_cfg)
        jsonData = {
            "code": 0,
            "msg": "",
            "count": len(task_list),
            "data": data_list
        }
        return Response(jsonData)
