from rest_framework import serializers
from cmdb_auth.models import auth_group, user_auth_cmdb
from users.models import User


class GroupAuthSerializer(serializers.ModelSerializer):
    """
    用户组序列化器
    """
    # groups = serializers.ManyRelatedField(source='id')

    class Meta:
        model = auth_group
        fields = '__all__'


class CmdbAuthSerializer(serializers.ModelSerializer):
    """权限序列化器"""

    auths = serializers.PrimaryKeyRelatedField(many=True, queryset=auth_group.objects.all())

    class Meta:
        model = user_auth_cmdb
        fields = '__all__'










