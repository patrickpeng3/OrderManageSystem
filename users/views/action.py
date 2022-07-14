from django.contrib import auth
from django.http import JsonResponse
# from models import *
from users.models import User, department_Mode
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import action
from cmdb_hls.cmdb_logger import SCRIPT_LOGGER
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


class ActionBase(ViewSet):
    """
    用户管理基础
    """
    permission_classes = [IsAuthenticated]


class MemberList(ActionBase):
    """
    用户列表
    """

    @action(methods=['get'], detail=False)
    def user_action(self, request):
        form = request.GET
        user_list, data_list = [[] for i in range(2)]
        method = form.get("method")
        search_value = form.get("search_input")
        if method == "search" and search_value:
            user_value_list = User.objects.all().values()
            for user_value in user_value_list:
                for k, v in user_value.items():
                    if str(search_value) in str(v):
                        server = User.objects.filter(id=user_value['id'])[0]
                        user_list.append(server)
                        break
        else:
            user_list = User.objects.all()
        for user in user_list:
            department = user.department
            data_cfg = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'sex': user.gender,
                'number': user.number,
                'department': department.department_name,
                'status': user.is_active,
            }
            data_list.append(data_cfg)
        jsonData = {
            "code": 0,
            "msg": "",
            "count": len(user_list),
            "data": data_list
        }
        return Response(jsonData)

    @action(methods=['get'], detail=False)
    def status_action(self, request):
        form = request.GET
        status = False
        _id = form.get("id")
        user = User.objects.get(id=_id)
        if user.is_active == 1:
            user_status = 0
        else:
            user_status = 1
        try:
            user.is_active = user_status
            user.save()
            status = True
            SCRIPT_LOGGER.info("修改{}状态成功！".format(user.username))
        except Exception as e:
            print(e, "\n修改{}状态失败！".format(user.username))
            SCRIPT_LOGGER.info(e, "\n修改{}状态失败！".format(user.username))
        return Response(status)


class MemberDel(ActionBase):
    """
    删除用户
    """

    @action(methods=['get'], detail=False)
    def user_action(self, request):
        form = request.GET
        _id = form.get("id")
        status = False
        try:
            User.objects.get(id=_id).delete()
            status = True
            SCRIPT_LOGGER.info("已删除id为{}的用户！".format(_id))
        except Exception:
            SCRIPT_LOGGER.info("删除id为{}的用户失败！".format(_id))
            print("删除id为{}的用户失败！".format(_id))
        return Response(status)

    @action(methods=['get'], detail=False)
    def all_action(self, request):
        form = request.GET
        ids = eval(form.get("ids"))
        status = False
        for _id in ids:
            user = User.objects.get(id=_id)
            try:
                User.objects.get(id=_id).delete()
                status = True
                SCRIPT_LOGGER.info("删除用户{}成功！".format(user.username))
            except Exception as e:
                SCRIPT_LOGGER.info(e, "\n删除用户{}失败！".format(user.username))
                print(e, "\n删除用户{}失败！".format(user.username))
        return Response(status)


class MemberAdd(ActionBase):
    """
    新增用户
    """

    @action(methods=['post'], detail=False)
    def user_action(self, request):
        form = request.data
        status = False
        username = form.get("L_username")
        passwd = form.get("L_pass")
        email = form.get("L_email")
        number = form.get("L_number")
        gender = form.get("L_gender")
        department = form.get("L_department")
        try:
            User.objects.create_user(username=username, email=email, number=number, password=passwd,
                                     gender=gender, department_id=department)
            status = True
            SCRIPT_LOGGER.info("新增{}用户成功！".format(username))
        except Exception as e:
            SCRIPT_LOGGER.info("新增{}用户失败！".format(username))
            print("新增{}用户失败！".format(username))
            print(e)
        return Response(status)


class MemberPasswd(ActionBase):
    """
    修改密码
    """

    @action(methods=['post'], detail=False)
    def user_action(self, request):
        form = request.data
        status = False
        username = form.get("L_username")
        oldPasswd = form.get("L_oldpass")
        newPasswd = form.get("L_newpass")
        user = auth.authenticate(username=username, password=oldPasswd)
        if user:
            try:
                user.set_password(newPasswd)
                user.save()
                status = True
                SCRIPT_LOGGER.info("{}修改密码完成！".format(username))
            except Exception:
                print("用户{}修改密码失败！".format(username))
                SCRIPT_LOGGER.info("用户{}修改密码失败！".format(username))
        else:
            print("用户名或密码错误！")
        return Response(status)


class MemberEdit(ActionBase):
    """
    修改用户信息
    """

    @action(methods=['get'], detail=False)
    def user_action(self, request):
        form = request.GET
        status = False
        _id = form.get("id")
        field = form.get("field")
        value = form.get("value")
        user = User.objects.get(id=_id)
        try:
            setattr(user, field, value)
            user.save()
            status = True
            SCRIPT_LOGGER.info("修改{username}的{field}为{value}".format(
                username=user.username,
                field=field,
                value=value
            ))
        except Exception as e:
            SCRIPT_LOGGER.info(e, "\n修改{username}的{field}为{value}".format(
                username=user.username,
                field=field,
                value=value
            ))
        return Response(status)


class GenderChange(ActionBase):
    """
    修改用户性别
    """

    @action(methods=['get'], detail=False)
    def user_action(self, request):
        form = request.GET
        status = False
        _id = form.get("id")
        user = User.objects.get(id=_id)
        try:
            if user.gender == "female":
                gender = "male"
            else:
                gender = "female"
            user.gender = gender
            user.save()
            status = True
            print("修改用户{username}性别为{gender}!".format(username=user.username, gender=gender))
            SCRIPT_LOGGER.info("修改用户{username}性别为{gender}！".format(username=user.username, gender=gender))
        except Exception:
            SCRIPT_LOGGER.info("修改用户{}性别失败！".format(user.username))
            print("修改用户{}性别失败！".format(user.username))
        return Response(status)


class DepartmentList(ActionBase):
    """
    部门管理
    """

    @action(methods=['get'], detail=False)
    def department_action(self, request):
        department_list = department_Mode.objects.all()
        data_list = []
        for department in department_list:
            data_cfg = {
                'id': department.id,
                'name': department.department_name,
                'description': department.description,
                'desc_id': department.desc_gid,
            }
            data_list.append(data_cfg)
        jsonData = {
            "code": 0,
            "msg": "",
            "count": len(department_list),
            "data": data_list
        }
        return Response(jsonData)
