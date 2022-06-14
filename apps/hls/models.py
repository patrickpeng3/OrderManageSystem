from django.db import models
from datetime import datetime

# Create your models here.


class servers(models.Model):
    """
    服务器列表
    """
    id = models.AutoField("id", primary_key=True)
    server_id = models.IntegerField("游服id")
    special_server = models.CharField("专服", max_length=10)
    salt_id = models.CharField("saltid", max_length=16)
    status = models.IntegerField("状态")
    version = models.CharField("后端版本", max_length=20)
    server_host = models.CharField("公网IP", max_length=20)
    private_host = models.CharField("内网IP", max_length=20)
    ws_server_port = models.IntegerField("ws端口号")
    web_port = models.IntegerField("web端口号")
    fep_client_port = models.IntegerField("fep端口号")
    dp_server_port = models.IntegerField("dp端口号")
    nginx_port = models.IntegerField("nginx端口号")
    clb = models.CharField("负载均衡名", max_length=20)
    born_time = models.DateTimeField("开服时间", default=0)
    create_time = models.DateTimeField("创服时间", default=datetime.now)

    class Meta:
        verbose_name = "服务器列表"
        verbose_name_plural = verbose_name
        ordering = ['id']


class machine(models.Model):
    """
    服务器列表
    """
    id = models.AutoField("id", primary_key=True)
    salt_id = models.CharField("saltid", max_length=16)
    master_ip = models.CharField("公网IP", max_length=20)
    private_ip = models.CharField("内网IP", max_length=20)
    system = models.CharField("系统版本", max_length=50, default="")
    cpu_core = models.IntegerField("系统核数", default="8")
    memory = models.IntegerField("内存", default="64")
    max_port = models.IntegerField("最大使用端口")
    current_server = models.CharField("现有游服", max_length=100)
    status = models.IntegerField("状态")

    class Meta:
        verbose_name = "服务器列表"
        verbose_name_plural = verbose_name
        ordering = ['id']


class special(models.Model):
    """
    专服列表
    """
    id = models.AutoField("id", primary_key=True)
    name = models.CharField("专服名", max_length=10)
    salt_range = models.CharField("salt范围", max_length=50)
    id_range = models.CharField("游服id范围", max_length=50)
    begin = models.IntegerField("首服id")
    front_ver = models.IntegerField("前端版本号")
    backend_ver = models.CharField("后端版本号",max_length=30)
    clb = models.CharField("负载均衡名", max_length=15)
    clb_num = models.IntegerField("负载均衡数")

    class Meta:
        verbose_name = "专服列表"
        verbose_name_plural = verbose_name
        ordering = ['id']
