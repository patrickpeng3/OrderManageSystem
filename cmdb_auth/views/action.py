from cmdb_auth.models import auth_group, user_auth_cmdb
# import hashlib, time
from cmdb_hls.cmdb_logger import SCRIPT_LOGGER
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


# Create your views here.
class ActionBase(ViewSet):
    permission_classes = [IsAuthenticated]


class GroupList(ActionBase):
    """
    用户组
    """
    @action(methods=['get'], detail=False)
    def list_action(self, request):
        group_list, data_list = [[] for i in range(2)]
        group_list = auth_group.objects.all()
        for group in group_list:
            data_cfg = {
                'group_name': group.group_name,
                'status': group.status,
                'explanation': group.explanation,
                'data_time': group.date_time,
                'auth': 'test'
            }
            data_list.append(data_cfg)
        jsonData = {
            'code': 0,
            'msg': '',
            'count': len(group_list),
            'data': data_list
        }
        return Response(jsonData)


class GroupDel(ActionBase):
    """
    删除用户组
    """
    @action(methods=['post'], detail=False)
    @csrf_exempt
    def del_action(self, request):
        form = request.data
        status = True
        print(form)
        print("test")
        return Response(status)








































