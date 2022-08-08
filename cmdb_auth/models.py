from django.db import models
from users.models import User
import uuid


# Create your models here.
class auth_group(models.Model):
    """
    授权组
    """
    uuid = models.UUIDField(auto_created=True, primary_key=True, default=uuid.uuid4, editable=False)
    group_name = models.CharField(u"组名", max_length=100, unique=True)
    group_user = models.ManyToManyField(User, blank=True, verbose_name=u"所属用户")
    status = models.BooleanField(u"是否启用", default=True)
    explanation = models.TextField(u"角色描述", blank=True, null=True)
    date_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.group_name

    class Meta:
        verbose_name = u"角色管理"
        verbose_name_plural = verbose_name


class user_auth_cmdb(models.Model):
    """
    cmdb权限
    所有字段全部以0，1来表示
    1表示有此权限，0表示无此权限
    所有数据全部外键关联user表，当用户删除时相应权限也随之删除
    """
    uuid = models.UUIDField(auto_created=True, primary_key=True, default=uuid.uuid4, editable=False)

    """资产管理"""
    select_host = models.BooleanField(u"查看资产", default=False)

    """项目管理"""
    apps = models.BooleanField(u"查看项目", default=False)
    hls = models.BooleanField(u"唤灵师", default=False)

    """用户管理"""
    add_user = models.BooleanField(u"添加用户", default=False)
    edit_user = models.BooleanField(u"修改用户", default=False)
    edit_pass = models.BooleanField(u"修改密码", default=False)
    delete_user = models.BooleanField(u"删除用户", default=False)
    add_department = models.BooleanField(u"部门管理", default=False)

    """日志管理"""
    auth_log = models.BooleanField(u"salt执行记录", default=False)

    group_name = models.ForeignKey(auth_group, help_text=u"添加角色组权限", on_delete=models.CASCADE, verbose_name=u"所属角色")

    def __unicode__(self):
        return self.group_name

    class Meta:
        verbose_name = u"权限管理"
        verbose_name_plural = verbose_name

