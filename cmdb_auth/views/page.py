from django.shortcuts import render


# 用户组列表
def GroupList(request):
    return render(request, "X-admin/auth/group-list.html")


# 修改用户组
def GroupAlter(request):
    return render(request, 'X-admin/auth/group-alter.html')


# 新增用户组
def GroupAdd(request):
    return render(request, 'X-admin/auth/group-add.html')

















