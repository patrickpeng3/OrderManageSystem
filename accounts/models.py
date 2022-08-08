from django.db import models
from users.models import User
from django import forms

# Create your models here.
manage_demo = [(i, i) for i in (u'经理', u'主管', u'项目负责人', u'管理员', u'BOSS')]


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
