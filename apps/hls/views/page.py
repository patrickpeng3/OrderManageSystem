from django.shortcuts import render


# Create your views here.
def server_list(request):
    return render(request, "X-admin/hls/hls-list.html")


def create_game(request):
    return render(request, "X-admin/hls/hls_create_game.html")