from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.viewsets import ModelViewSet
from users.models import User, department_Mode, DepartmentGroup
from users.serializer import UsersSerializer, DepartmentSerializer, DepartmentGroupSerializer


class UserInfoViewSet(ModelViewSet):
    """
    用户视图集
    """
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    search_fields = ('username',)
    ordering_fields = ('id',)
    permission_classes = [IsAuthenticated]
    select_tag = 'name'


class DepartmentInfoViewSet(ModelViewSet):
    """
    部门视图集
    """
    queryset = department_Mode.objects.all()
    serializer_class = DepartmentSerializer
    search_fields = ('department_name',)
    ordering_fields = ('id',)
    permission_classes = [IsAuthenticated]
    select_tag = 'name'


class DepartmentGroupInfoViewSet(ModelViewSet):
    """
    部门组视图集
    """
    queryset = DepartmentGroup.objects.all()
    serializer_class = DepartmentGroupSerializer
    search_fields = ('department_groups_name',)
    ordering_fields = ('id',)
    permission_classes = [IsAuthenticated]
    select_tag = 'name'
