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


# 更新页面
def update_game(request):
    return render(request, "X-admin/hls/hls_update_game.html")


# 启服页面
def start_game(request):
    return render(request, "X-admin/hls/hls_start_game.html")


# 停服页面
def stop_game(request):
    return render(request, "X-admin/hls/hls_stop_game.html")


# 删服页面
def delete_game(request):
    return render(request, "X-admin/hls/hls_delete_game.html")
