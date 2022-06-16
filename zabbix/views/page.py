from django.shortcuts import render


# Create your views here.

def host_list(request):
    return render(request, "X-admin/hls/hls-host-list.html")