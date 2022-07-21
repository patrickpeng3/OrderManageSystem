from django.urls import path, include
from rest_framework.routers import SimpleRouter
from job_manager.serializer import JobTaskInfoSerializer, JobTaskSimpleSerializer, JobTaskWebSocketInfoSerializer, \
    JobCmdSimpleSerializer, JobCmdInfoSerializer
from job_manager.views import base_info


urlpatterns = [

]

router = SimpleRouter()
router.register(r'task', base_info.JobTaskInfoViewSet, basename="任务")
router.register(r'cmd', base_info.JobCmdInfoViewSet, basename="任务命令")


urlpatterns += router.urls
