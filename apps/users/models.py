from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    """
    会员列表
    """
    GENDER_CHOICES = (
        ("male", u"男"),
        ("female", u"女")
    )
    id = models.AutoField("id", primary_key=True)
    name = models.CharField("用户名", max_length=50)
    number = models.CharField("手机号", max_length=11, null=True, blank=True)
    email = models.EmailField("邮箱", max_length=100, null=True, blank=True)
    gender = models.CharField("性别", max_length=6, choices=GENDER_CHOICES, default="female")
    city = models.CharField("城市", max_length=100, null=True, blank=True, default="")
    score = models.IntegerField("积分", default=0)
    school = models.CharField("学校", max_length=100, null=True, blank=True, default="")
    status = models.IntegerField('状态', max_length=1, default=1)
    add_time = models.DateTimeField("添加时间", default=datetime.now)

    class Meta:
        verbose_name = "会员列表"
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.username
