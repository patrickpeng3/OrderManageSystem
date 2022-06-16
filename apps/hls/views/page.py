from django.shortcuts import render


# Create your views here.
# 游服列表
def server_list(request):
    return render(request, "X-admin/hls/hls-server-list.html")


# 创服页面
def create_game(request):
    return render(request, "X-admin/hls/hls_create_game.html")


# 操作日志
def game_log(request):
    return render(request, "X-admin/hls/hls-log.html")