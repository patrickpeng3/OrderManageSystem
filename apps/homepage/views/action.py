from django.shortcuts import render, redirect, HttpResponse
from django.contrib import auth
from django.http import JsonResponse
# from models import *
from rest_framework.response import Response

from apps.users.models import User


# Create your views here.


# 登录页面
def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST.get("username"),
                                 password=request.POST.get("password"))
        if user:
            auth.login(request, user)
            return JsonResponse({"login": "success"})
        else:
            return JsonResponse({"login": "failed"})


# 主页
def index(request):
    if request.method == 'GET':
        logout = request.GET.get("logout")
        user = request.user
        if logout == "1":
            auth.logout(request)
            return JsonResponse({"ret": "logout"})


# 动态会员列表
def memberList(request):
    if request.method == "GET":
        if request.GET.get("method") == "getStatus":
            id = request.GET.get("id")
            user = User.objects.get(id=id)
            if user.status == 1:
                user.status = 0
            else:
                user.status = 1
            user.save()
            return JsonResponse({'status': user.status})
        elif request.GET.get("method") == "sreachUser":
            try:
                username = request.GET.get("username")
                user_list = []
                user = User.objects.get(username=username)
                user_list.append(user)
                data_list = []
                data_cfg = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'sex': user.gender,
                    'city': user.city,
                    'score': user.score,
                    'school': user.school,
                    'status': user.status,
                }
                data_list.append(data_cfg)
                jsonData = {
                    "code": 0,
                    # "msg": "",
                    "count": len(user_list),
                    "data": data_list
                }
                print(jsonData)
                return JsonResponse(jsonData)
            except Exception:
                return JsonResponse({"sreachUser": "failed"})
        else:
            user_list = User.objects.all()
            data_list = []
            for i in range(len(user_list)):
                user = user_list[i]
                data_cfg = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'sex': user.gender,
                    'city': user.city,
                    'score': user.score,
                    'school': user.school,
                    'status': user.status,
                    # 'operation': "operation",
                }
                data_list.append(data_cfg)
            jsonData = {
                "code": 0,
                # "msg": "",
                "count": len(user_list),
                "data": data_list
            }
            # print(jsonData)
            return JsonResponse(jsonData)


# 会员删除
def memberdel(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        print(id)
        try:
            User.objects.get(id=id).delete()
            return JsonResponse({'ret': 'success'})
        except Exception:
            print("删除id为{id}的用户失败！".format(id=id))


def memberAdd(request):
    if request.method == "POST":
        username = request.POST.get("L_username")
        email = request.POST.get("L_email")
        passwd = request.POST.get("L_pass")
        print(username)
        try:
            User.objects.create_user(username=username, email=email, password=passwd)
            return JsonResponse({"ret": "success"})
        except Exception:
            print("创建用户失败！")


def memberPassword(request):
    if request.method == "GET":
        id = request.GET.get("id")
        user = User.objects.get(id=id)
        return JsonResponse({"username": user.username})
    if request.method == "POST":
        username = request.POST.get("L_username")
        oldPasswd = request.POST.get("L_oldpass")
        newPasswd = request.POST.get("L_newpass")
        user = auth.authenticate(username=username, password=oldPasswd)
        if user:
            try:
                user.set_password(newPasswd)
                user.save()
                return JsonResponse({"ret": "success"})
            except Exception:
                return JsonResponse({"ret": "failed"})
        else:
            return JsonResponse({"ret": "failed"})


def memberEdit(request):
    if request.method == 'GET':
        id = request.GET.get("id")
        field = request.GET.get("field")
        value = request.GET.get("value")
        user = User.objects.get(id=id)
        setattr(user, field, value)
        user.save()
        return JsonResponse({"ret": "success"})
    else:
        print("修改失败！")


def memberDelAll(request):
    if request.method == "GET":
        ids = request.GET.get("ids")
        ids = ids.strip("[")
        ids = ids.strip("]")
        ids = ids.replace(",", "")
        ids = list(ids)
        try:
            for id in ids:
                User.objects.get(id=id).delete()
            return JsonResponse({"ret": "success"})
        except Exception:
            return JsonResponse({"ret": "failed"})
