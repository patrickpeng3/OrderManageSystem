from django.shortcuts import render, redirect, HttpResponse
from django.contrib import auth
from django.http import JsonResponse
# from models import *

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
    return render(request, 'X-admin/login.html')


# 主页
def index(request):
    if request.method == 'GET':
        logout = request.GET.get("logout")
        user = request.user
        if logout == "1":
            auth.logout(request)
            return JsonResponse({"ret": "logout"})
    return render(request, 'X-admin/index.html')


# 会员列表
def memberList(request):
    return render(request, "X-admin/member-list.html")


# 动态会员列表
def memberlist1(request):
    return render(request, "X-admin/member-list1.html")


# 会员删除
def memberdel(request):
    return render(request, "X-admin/member-del.html")


# welcome1
def welcome1(request):
    return render(request, "X-admin/welcome1.html")
