from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def hls_log(request):
    return render(request, 'X-admin/hls/hls_log.html')
