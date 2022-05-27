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
    # user['id'] = User.objects.all()\
    username = User.objects.filter(id=1).values('username')[0]['username']
    jsonData = {
        "code": 0,
        "msg": "",
        "count": 1,
        "data": {
            "username": username
        }
    }
    print(jsonData)
    return JsonResponse(jsonData)


# 会员删除
def memberdel(request):
    return render(request, "X-admin/member-del.html")

