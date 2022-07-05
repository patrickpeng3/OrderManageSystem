from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.


# 登录页面
def login(request):
    return render(request, 'X-admin/login.html')


# 主页
@login_required()
def index(request):
    return render(request, 'X-admin/index.html')


# welcome1
@login_required()
def welcome1(request):
    return render(request, "X-admin/welcome1.html")


@login_required()
def orderList(request):
    return render(request, "X-admin/order-list.html")


@login_required()
def orderList1(request):
    return render(request, "X-admin/order-list1.html")

