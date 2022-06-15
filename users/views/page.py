from django.shortcuts import render


# Create your views here.


# 动态会员列表
def memberList(request):
    return render(request, "X-admin/member-list.html")


# 会员删除
def memberdel(request):
    return render(request, "X-admin/member-del.html")


# 新增会员
def memberAdd(request):
    return render(request, "X-admin/member-add.html")


# 编辑会员
def memberEdit(request):
    return render(request, "X-admin/member-edit.html")


# 修改会员密码
def memberPassword(request):
    return render(request, "X-admin/member-password.html")
