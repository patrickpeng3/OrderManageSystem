from rest_framework import serializers
from cmdb_auth.models import auth_group, user_auth_cmdb


class GroupAuthSerializer(serializers.ModelSerializer):
    """
    用户组序列化器
    """
    class Meta:
        model = auth_group
        fields = '__all__'


class CmdbAuthSerializer(serializers.ModelSerializer):
    """权限序列化器"""
    class Meta:
        model = user_auth_cmdb
        fields = '__all__'










