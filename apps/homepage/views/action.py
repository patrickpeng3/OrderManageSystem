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
    user = User.objects.all()[0]
    _id = user.id
    username = user.username
    sex = user.gender
    score = user.score
    city = user.city
    school = user.school
    email = user.email
    jsonData = {
        "code": 0,
        # "msg": "",
        "count": 1,
        "data": [
            {
                'id': _id,
                'username': username,
                'email': email,
                'sex': sex,
                'city': city,
                'experience': score,
                'dw_xinzhi': school,
            }
        ]
    }
    print(jsonData)
    return JsonResponse(jsonData)


# 会员删除
def memberdel(request):
    return render(request, "X-admin/member-del.html")

