from django.shortcuts import render


# Create your views here.


# 动态会员列表
def memberList(request):
    return render(request, "X-admin/users/member-list.html")


# 新增会员
def memberAdd(request):
    return render(request, "X-admin/users/member-add.html")


# 修改会员密码
def memberPassword(request):
    return render(request, "X-admin/users/member-password.html")


# 部门列表
def departmentList(request):
    return render(request, "X-admin/auth/department-list.html")


# 角色列表
def roleList(request):
    return render(request, "X-admin/auth/admin-role.html")


# 角色列表
def roleAdd(request):
    return render(request, "X-admin/auth/role-add.html")
