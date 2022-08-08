import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cmdb_hls.settings')
django.setup()
from django.shortcuts import render
import time
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cmdb_hls.settings')
from job_manager.models import JobTask, JobCmd
from job_manager.serializer import JobTaskInfoSerializer, JobTaskSimpleSerializer, JobCmdInfoSerializer, \
    JobCmdSimpleSerializer, JobTaskWebSocketInfoSerializer
# from job_manager.views.base_info import JobCmdInfoViewSet, JobTaskInfoViewSet
from channels.db import database_sync_to_async


def hls_log(request):
    return render(request, 'X-admin/hls/hls_log.html')


# @database_sync_to_async
# def test(self):
#     return str(JobTaskWebSocketInfoSerializer(
#         JobTask.objects.prefetch_related('cmds').filter(confirm=False).all(), many=True
#     ).data)


# async def hls_log_action(scope, receive, send):
#     # print(test())
#     while True:
#         event = await receive()
#
#         if event['type'] == 'websocket.connect':
#             await send({
#                 'type': 'websocket.accept'
#             })
#
#         if event['type'] == 'websocket.disconnect':
#             break
#
#         if event['type'] == 'websocket.receive':
#             if event['text'] == 'ping':
#                 # process = JobTaskWebSocketInfoSerializer(
#                 #     JobTask.objects.prefetch_related('cmds').filter(confirm=False).all(), many=True
#                 # ).data
#                 # process = test()
#                 await send({
#                     'type': 'websocket.send',
#                     # 'text': process,
#                     'text': 'test',
#                 })
#             time.sleep(1)
