from cmdb_auth.models import auth_group, user_auth_cmdb
from cmdb_auth.serializers import GroupAuthSerializer, CmdbAuthSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.viewsets import ModelViewSet


class GroupAuthInfoViewSet(viewsets.ModelViewSet):
    """
    用户组视图集
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    queryset = auth_group.objects.all()
    serializer_class = GroupAuthSerializer


class CmdbAuthInfoViewSet(viewsets.ModelViewSet):
    """
    权限视图集
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    queryset = user_auth_cmdb.objects.all()
    serializer_class = CmdbAuthSerializer

















