from django.shortcuts import render


# Create your views here.
def server_list(request):
    return render(request, "X-admin/hls-list.html")