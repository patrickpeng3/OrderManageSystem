from apps.hls.models import Servers, Special, Machine
from apps.hls.serializer import ServerSerializer, SpecialSerializer, MachineSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.viewsets import ModelViewSet


class TestViewSet(viewsets.ModelViewSet):
    """
    测试视图
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    queryset = Servers.objects.all()
    serializer_class = ServerSerializer


class ServerInfoViewSet(ModelViewSet):
    """
    游服视图集
    """
    queryset = Servers.objects.all()
    serializer_class = ServerSerializer
    search_fields = ('server_id',)
    ordering_fields = ('server_id',)
    permission_classes = [IsAuthenticated]
    select_tag = 'name'
