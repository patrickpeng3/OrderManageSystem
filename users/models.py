from django.utils import timezone
from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
# Create your models here.


manager_demo = [(i, i) for i in (u"经理", u"主管", u"项目负责人", u"管理员", u"BOSS")]
Department = [(u"ops", u"plat", u"dev")]
auth_id = [(u"普通用户", u"普通用户"), (u"管理员", u"管理员")]
auth_gid = [(1001, u"运维部"), (1002, u"测试部"), (1003, u"研发部")]


class DepartmentGroup(models.Model):
    Department_groups_name = models.CharField(u"组名", max_length=64, blank=True, null=True)
    description = models.TextField(u"介绍", blank=True, null=True)

    def __unicode__(self):
        return self.Department_groups_name

    class Meta:
        verbose_name = u"部门组"
        verbose_name_plural = verbose_name


class department_Mode(models.Model):
    department_name = models.CharField(u"部门名称", max_length=64, blank=True, null=True)
    description = models.TextField(u"介绍", blank=True, null=True)
    desc_gid = models.IntegerField(u"部门组", choices=auth_gid, blank=True, null=True)

    def __unicode__(self):
        return self.department_name

    class Meta:
        verbose_name = u"部门"
        verbose_name_plural = verbose_name


class User(AbstractUser):
    """
    会员列表
    """
    GENDER_CHOICES = (
        ("male", u"男"),
        ("female", u"女")
    )
    id = models.AutoField("id", primary_key=True)
    number = models.CharField(u"手机号", max_length=11, null=True, blank=True)
    email = models.EmailField(u"邮箱", max_length=100, null=True, blank=True)
    gender = models.CharField(u"性别", max_length=6, choices=GENDER_CHOICES, default="female")
    department = models.ForeignKey(department_Mode, blank=True, on_delete=models.PROTECT)
    date_joined = models.DateTimeField("添加时间", default=timezone.now)

    class Meta:
        verbose_name = "会员列表"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.username

    # def get_department(self):
    #     return department_Mode.objects.filter(id=self.department_id)
