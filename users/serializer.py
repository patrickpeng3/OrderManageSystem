from rest_framework import serializers
from users.models import User, department_Mode, DepartmentGroup


class UsersSerializer(serializers.ModelSerializer):
    """
    用户序列化器
    """

    class Meta:
        model = User
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    """
    部门序列化器
    """

    class Meta:
        model = department_Mode
        fields = '__all__'


class DepartmentGroupSerializer(serializers.ModelSerializer):
    """
    部门组序列化器
    """

    class Meta:
        model = DepartmentGroup
        fields = '__all__'
