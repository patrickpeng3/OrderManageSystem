from django.contrib import auth
from django.http import JsonResponse
# from models import *
from users.models import User

# Create your views here.


# 动态会员列表
def memberList(request):
    if request.method == "GET":
        if request.GET.get("method") == "getStatus":
            id = request.GET.get("id")
            user = User.objects.get(id=id)
            if user.status == 1:
                user.status = 0
            else:
                user.status = 1
            user.save()
            return JsonResponse({'status': user.status})
        elif request.GET.get("method") == "searchUser" and request.GET.get("username"):
            user_list, data_list = [[] for i in range(2)]
            try:
                user = User.objects.get(username=request.GET.get("username"))
                user_list.append(user)
                data_cfg = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'sex': user.gender,
                    'city': user.city,
                    'score': user.score,
                    'school': user.school,
                    'status': user.status,
                    # 'operation': "operation",
                }
                data_list.append(data_cfg)
                jsonData = {
                    "code": 0,
                    # "msg": "",
                    "count": len(user_list),
                    "data": data_list
                }
                return JsonResponse(jsonData)
            except Exception:
                return JsonResponse({
                    "code": 0
                })
        else:
            user_list = User.objects.all()
            data_list = []
            for i in range(len(user_list)):
                user = user_list[i]
                data_cfg = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'sex': user.gender,
                    'city': user.city,
                    'score': user.score,
                    'school': user.school,
                    'status': user.status,
                    # 'operation': "operation",
                }
                data_list.append(data_cfg)
            jsonData = {
                "code": 0,
                # "msg": "",
                "count": len(user_list),
                "data": data_list
            }
            return JsonResponse(jsonData)


# 会员删除
def memberdel(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        print(id)
        try:
            User.objects.get(id=id).delete()
            return JsonResponse({'ret': 'success'})
        except Exception:
            print("删除id为{id}的用户失败！".format(id=id))


# 新增用户
def memberAdd(request):
    if request.method == "POST":
        username = request.POST.get("L_username")
        email = request.POST.get("L_email")
        passwd = request.POST.get("L_pass")
        city = request.POST.get("L_city")
        school = request.POST.get("L_school")
        gender = request.POST.get("L_gender")
        try:
            User.objects.create_user(username=username, email=email, password=passwd, city=city, school=school,
                                     gender=gender)
            return JsonResponse({"ret": "success"})
        except Exception:
            print("创建用户失败！")


# 修改密码
def memberPassword(request):
    if request.method == "GET":
        id = request.GET.get("id")
        user = User.objects.get(id=id)
        return JsonResponse({"username": user.username})
    if request.method == "POST":
        username = request.POST.get("L_username")
        oldPasswd = request.POST.get("L_oldpass")
        newPasswd = request.POST.get("L_newpass")
        user = auth.authenticate(username=username, password=oldPasswd)
        if user:
            try:
                user.set_password(newPasswd)
                user.save()
                return JsonResponse({"ret": "success"})
            except Exception:
                return JsonResponse({"ret": "failed"})
        else:
            return JsonResponse({"ret": "failed"})


# 修改用户信息
def memberEdit(request):
    if request.method == 'GET':
        id = request.GET.get("id")
        field = request.GET.get("field")
        value = request.GET.get("value")
        user = User.objects.get(id=id)
        setattr(user, field, value)
        user.save()
        return JsonResponse({"ret": "success"})
    else:
        print("修改失败！")


# 批量删除用户
def memberDelAll(request):
    if request.method == "GET":
        ids = request.GET.get("ids")
        ids = ids.strip("[")
        ids = ids.strip("]")
        ids = ids.replace(",", "")
        ids = list(ids)
        try:
            for id in ids:
                User.objects.get(id=id).delete()
            return JsonResponse({"ret": "success"})
        except Exception:
            return JsonResponse({"ret": "failed"})


# 修改用户性别
def genderChange(request):
    if request.method == "GET":
        id = request.GET.get("id")
        try:
            user = User.objects.get(id=id)
            userGender = user.gender
            if userGender == "female":
                user.gender = "male"
                user.save()
            else:
                user.gender = "female"
                user.save()
        except Exception:
            print("修改用户{}性别失败！".format(id))
        return JsonResponse({"ret": "success"})
