from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from users.models import User
from django.contrib.sessions.backends.db import SessionStore
import json
from cmdb_auth.forms import cmdb_from, auth_add, auth_add_user
from cmdb_auth.models import auth_group, user_auth_cmdb
# import hashlib, time
from accounts.auth_session import auth_class


# Create your views here.
@login_required
def cmdb_auth(request):
    data = cmdb_from()
    if request.method == 'POST':
        uf = cmdb_from(request)
        if uf.is_valid():
            uf.save()

            return HttpResponseRedirect("")
    return render(request, '')


# 更新权限
def auth_session_class(uuid):
    auth_group_id = auth_group.objects.get(uuid=uuid)
    """查询出该用户组所有用户"""
    all_user = auth_group_id.group_user.all()
    for user in all_user:
        if user.session_key:
            s = SessionStore(session_key=user.session_key)
            """查询出权限并设置"""
            s['fun_auth'] = auth_class(user)
            s.save()
    return True


@login_required()
def add_auth(request, uuid):
    """
    增加用户权限
    :param request:
    :param uuid:
    :return:
    """
    uuid = str(uuid)
    """根据传入的uuid查询出用户组"""
    _group = auth_group.objects.get(uuid=uuid)

    try:
        group_auth = user_auth_cmdb.objects.get(group_name=uuid)
        data = auth_add(instance=group_auth)
    except Exception as e:
        data = auth_add()

    if request.method == 'POST':
        try:
            uf = auth_add(request.POST, instance=group_auth)
        except Exception as e:
            uf = auth_add(request.POST)

        if uf.is_valid():
            uf.save()
            auth_session_class(uuid)
    return render(request, '')


@login_required
def delete_auth(request, uuid):
    """
    删除权限
    :param request:
    :param uuid:
    :return:
    """
    uuid = str(uuid)
    _group = auth_group.objects.get(uuid=uuid)
    """删除用户组中的用户"""
    _group.group_user.clear()
    """删除用户组"""
    _group.delete()

    return HttpResponseRedirect("")


def add_group_user(request, uuid):
    """
    用户组添加用户
    :param request:
    :param uuid:
    :return:
    """
    uuid = str(uuid)
    _group = auth_group.objects.get(uuid=uuid)

    if request.method == 'POST':
        uf = auth_add_user(request.POST, instance=_group)
        if uf.is_valid():
            uf.save()
            auth_session_class(uuid)

    user_all = User.objects.all()
    group_user = _group.group_user.all()

    user_list = [x.username for x in group_user]

    return render(request, '')


@login_required
def edit_auth(request, uuid):
    """
    编辑权限
    :param request:
    :param uuid:
    :return:
    """
    uuid = str(uuid)
    _group = auth_group.objects.get(uuid=uuid)
    if request.method == 'POST':
        uf = cmdb_from(request.POST, instance=_group)
        if uf.is_valid():
            uf.save()
            return HttpResponse(
                json.dumps({
                    'status': 200,
                    'msg': 'ok'
                }, ensure_ascii=False, indent=4
                ))
    else:
        return render(request, '')


@login_required
def edit_status(request, uuid):
    """

    :param request:
    :param uuid:
    :return:
    """
    uuid = str(uuid)
    _group = auth_group.objects.get(uuid=uuid)
    if _group.enable:
        _group.enable = False
        _group.save()
        auth_session_class(uuid)
    else:
        _group.enable = True
        _group.save()
        auth_session_class(uuid)
    return HttpResponse(
        json.dumps({
            'status': 200,
            'msg': 'ok'
        }, ensure_ascii=False, indent=4)
    )
