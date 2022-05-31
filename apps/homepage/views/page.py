from django.shortcuts import render, redirect, HttpResponse
from apps.users.models import User

# Create your views here.


# 登录页面
def login(request):
    return render(request, 'X-admin/login.html')


# 主页
def index(request):
    return render(request, 'X-admin/index.html')


# 会员列表
def memberList(request):
    return render(request, "X-admin/member-list.html")


# 动态会员列表
def memberList1(request):
    return render(request, "X-admin/member-list1.html")


# 会员删除
def memberdel(request):
    return render(request, "X-admin/member-del.html")


# welcome1
def welcome1(request):
    return render(request, "X-admin/welcome1.html")


def memberAdd(request):
    return render(request, "X-admin/member-add.html")
