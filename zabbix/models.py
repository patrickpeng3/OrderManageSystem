from django.db import models
from django.utils import timezone

# from zabbix.utils import make_paginator

# Create your models here.


class Groups(models.Model):
    """
    主机群
    """
    group_id = models.IntegerField("群组ID", primary_key=True)
    name = models.CharField("群组名", max_length=256, blank=True, null=True)

    class Meta:
        verbose_name = "主机群"
        verbose_name_plural = verbose_name
        ordering = ['group_id']


class Hosts(models.Model):
    """
    主机
    """
    AVAILABLE_CHOICES = (
        ('0', '未知'),
        ('1', '可用'),
        ('2', '失效'),
    )
    host_id = models.IntegerField("主机ID", primary_key=True)
    host_name = models.CharField("主机名", max_length=256)
    groups = models.ManyToManyField(Groups, related_name=u'hosts')
    error = models.CharField(max_length=256, verbose_name=u'error', default='')
    available = models.CharField("agent可用性", max_length=1, choices=AVAILABLE_CHOICES, default=0)
    snmp_available = models.CharField("snmp可用性", max_length=1, choices=AVAILABLE_CHOICES, default=0)
    ipmi_available = models.CharField("ipmi可用性", max_length=1, choices=AVAILABLE_CHOICES, default=0)
    jmx_available = models.CharField("jmx可用性", max_length=1, choices=AVAILABLE_CHOICES, default=0)
