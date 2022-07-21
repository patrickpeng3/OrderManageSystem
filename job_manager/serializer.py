# -*- coding: utf-8 -*-
from rest_framework import serializers
from job_manager.models import JobCmd, JobTask


class JobCmdSimpleSerializer(serializers.ModelSerializer):
    """
    任务命令简洁信息
    """
    class Meta:
        model = JobCmd
        fields = ('id', 'cmd', 'start_time', 'end_time', 'status')


class JobCmdInfoSerializer(serializers.ModelSerializer):
    """
    任务命令序列化器
    """
    class Meta:
        model = JobCmd
        fields = '__all__'


class JobTaskSimpleSerializer(serializers.ModelSerializer):
    """
    任务简洁信息
    """
    class Meta:
        model = JobTask
        fields = ('id', 'name', 'username', 'status', 'start_time', 'end_time')


class JobTaskInfoSerializer(serializers.ModelSerializer):
    """
    任务序列化器
    """
    class Meta:
        model = JobTask
        fields = '__all__'


class JobTaskWebSocketInfoSerializer(serializers.ModelSerializer):
    """
    任务进度信息序列化器
    """
    cmds = JobCmdInfoSerializer(read_only=True, many=True)

    class Meta:
        model = JobTask
        fields = '__all__'
