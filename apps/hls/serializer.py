from rest_framework import serializers
from apps.hls.models import Servers, Special, Machine


class ServerSerializer(serializers.ModelSerializer):
    """
    游服序列化器
    """
    class Meta:
        model = Servers
        fields = '__all__'


class MachineSerializer(serializers.ModelSerializer):
    """
    主机序列化器
    """
    class Meta:
        model = Machine
        fields = '__all__'


class SpecialSerializer(serializers.ModelSerializer):
    """
    专服序列化器
    """
    class Meta:
        model = Special
        fields = '__all__'
