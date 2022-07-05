from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
# 游服列表
@login_required()
def server_list(request):
    return render(request, "X-admin/hls/hls_server_list.html")


# 创服页面
@login_required()
def create_game(request):
    return render(request, "X-admin/hls/hls_create_game.html")


# 操作日志
@login_required()
def game_log(request):
    return render(request, "X-admin/hls/hls_log.html")


# 更新页面
@login_required()
def update_game(request):
    return render(request, "X-admin/hls/hls_update_game.html")


# 启服页面
@login_required()
def start_game(request):
    return render(request, "X-admin/hls/hls_start_game.html")


# 停服页面
@login_required()
def stop_game(request):
    return render(request, "X-admin/hls/hls_stop_game.html")


# 删服页面
@login_required()
def delete_game(request):
    return render(request, "X-admin/hls/hls_delete_game.html")


# 修改信息
@login_required()
def edit_game(request):
    return render(request, "X-admin/hls/hls_edit_game.html")
