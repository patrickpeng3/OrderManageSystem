from django.shortcuts import render


# Create your views here.


# 登录页面
def login(request):
    return render(request, 'X-admin/login.html')


# 主页
def index(request):
    return render(request, 'X-admin/index.html')


# welcome1
def welcome1(request):
    return render(request, "X-admin/welcome1.html")


def orderList(request):
    return render(request, "X-admin/order-list.html")


def orderList1(request):
    return render(request, "X-admin/order-list1.html")

