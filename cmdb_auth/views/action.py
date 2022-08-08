import time

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

    @action(methods=['post'], detail=False)
    def my_test(self, request):
        data = request.data
        print(data)
        return Response(data)


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
    def del_action(self, request):
        form = request.data
        status = False
        group_name = form.get("group_name")
        try:
            auth_group.objects.get(group_name=group_name).delete()
            status = True
            SCRIPT_LOGGER.info("已删除{}用户组".format(group_name))
        except Exception as e:
            SCRIPT_LOGGER.info("删除{}用户组失败！".format(group_name))
            SCRIPT_LOGGER.info(e)
        return Response(status)


class GroupAdd(ActionBase):
    """
    新增用户组
    """
    @action(methods=['post'], detail=False)
    def add_action(self, request):
        form = request.data
        status = False
        group_name = form.get("group_name")
        explanation = form.get("group_desc")
        try:
            auth_group.objects.create(
                group_name=group_name,
                explanation=explanation,
                date_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            )
            status = True
            SCRIPT_LOGGER.info("新增{}用户组成功！".format(group_name))
        except Exception as e:
            SCRIPT_LOGGER.info("新增用户组失败！")
            print(e)
            SCRIPT_LOGGER.info(e)
        return Response(status)


class GroupAlter(ActionBase):
    """
    修改用户组权限
    """
    @action(methods=['post'], detail=False)
    def alter_action(self, request):
        form = request.data
        group_name = form.get("group_name")
        print(group_name)
        return Response(True)

    @action(methods=['post'], detail=False)
    def alter_action_entry(self, request):
        form = request.data
        print(form)
        group_name = GroupAlter.alter_action
        print(group_name)
        return Response(True)

    @action(methods=['get'], detail=False)
    def my_test(self, request):
        # group_name = auth_group.objects.all()[0]
        # print("查询结果：{}".format(group_name))
        # user_auth_cmdb.objects.create(
        #     select_host=True,
        #     apps=True,
        #     hls=True,
        #     add_user=True,
        #     edit_user=True,
        #     edit_pass=True,
        #     delete_user=True,
        #     add_department=True,
        #     auth_log=True,
        #     group_name=group_name
        # )
        user = request.user
        username = user.username
        return Response(username)






































