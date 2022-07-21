from django.shortcuts import render, get_object_or_404
import json, time, urllib
from django import forms
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import RequestContext
from audit.models import ssh_audit
from django.views.decorators.csrf import csrf_exempt
from cmdb_hls.cmdb_logger import SCRIPT_LOGGER


# Create your views here.
@csrf_exempt
def audit_save(request):
    """
    用户操作记录入库
    :param request:
    :return:
    """
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        bash_shell = request.POST.get('bash_shell')
        audit_data_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        server_ip = request.POST.get('server_ip')
        ssh_audit_data = ssh_audit(user_name=user_name, bash_shell=bash_shell, audit_data_time=audit_data_time,
                                   server_ip=server_ip)
        s = ssh_audit_data.save()
        return HttpResponse(json.dumps(
            {
                'status': 200,
                'result': u'已入库'
            }, ensure_ascii=False, indent=4
        ))


def audit_list(request):
    """
    用户审计记录页面
    :param request:
    :return:
    """
    audit_data = ssh_audit.objects.all().order_by('-audit_data_time')
    return render(request, 'X-admin/hls/hls_log.html')


@csrf_exempt
def audit_list_action(request):
    """
    用户审计记录
    :param request:
    :return:
    """
    audit_data = ssh_audit.objects.all().order_by('-audit_data_time')
    data_list = []
    for audit in audit_data:
        data_cfg = {
            'id': audit.uuid,
            'username': audit.user_name,
            'bash_shell': audit.bash_shell,
            'audit_data_time': audit.audit_data_time,
            'server_ip': audit.server_ip
        }
        data_list.append(data_cfg)
    jsonData = {
        "code": 0,
        "msg": "",
        "count": len(audit_data),
        "data": data_list
    }
    return JsonResponse(jsonData)


@csrf_exempt
def auth_select(request):
    """
    查询服务器操作记录
    :param request:
    :return:
    """
    if request.method == 'POST':
        ip = request.POST.get('ip')
        try:
            audit_page = int(request.POST.get('num'))
        except Exception as e:
            audit_page = 0
        if audit_page > 0:
            num = audit_page
            audit_data = ssh_audit.objects.filter(server_ip=ip).order_by('-audit_data_time')[:num]
        else:
            audit_data = ssh_audit.objects.filter(server_ip=ip).order_by('-audit_data_time')

        data = []
        for i in audit_data:
            data.append({
                'bash_shell': '%s %s %s' % (i.user_name, i.audit_data_time, i.bash_shell)
            })
        return HttpResponse(json.dumps(
            {
                'status': 200,
                'result': data
            }, ensure_ascii=False, indent=4
        ))
    return HttpResponse(json.dumps(
        {
            'status': 200,
            'result': 'error'
        }, ensure_ascii=False, indent=4
    ))
