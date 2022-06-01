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
def memberList1(request):
    user_list = User.objects.all()
    data_list = []
    for i in range(len(user_list)):
        user = user_list[i]
        _id = user.id
        username = user.username
        sex = user.gender
        score = user.score
        city = user.city
        school = user.school
        email = user.email
        status = 1
        operation = "TestOperation"
        data_cfg = {
            'id': _id,
            'username': username,
            'email': email,
            'sex': sex,
            'city': city,
            'experience': score,
            'school': school,
            'status': status,
            'operation': operation,
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


# 会员删除
def memberdel(request):
    print("memberdel")


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
    # username = request.POST['username']
    oldPasswd = request.POST.get("L_oldpass")
    test = request.POST.get("test")
    print("TEST")
    print(test)
    print(oldPasswd)
    return JsonResponse({"ret": "ret"})
