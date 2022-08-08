from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.


# 登录页面
def login(request):
    return render(request, 'X-admin/homepage/login.html')


# 主页
@login_required()
def index(request):
    return render(request, 'X-admin/homepage/index.html')


# welcome1
@login_required()
def welcome1(request):
    return render(request, "X-admin/homepage/welcome1.html")


@login_required()
def orderList(request):
    return render(request, "X-admin/homepage/order-list.html")


@login_required()
def orderList1(request):
    return render(request, "X-admin/homepage/order-list1.html")


def pageTest(request):
    return render(request, 'X-admin/auth/test.html')

