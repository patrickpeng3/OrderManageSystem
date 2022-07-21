from django.urls import path, include
from rest_framework.routers import SimpleRouter
from django.urls import path, include
from cmdb_auth.views import base_info
from cmdb_auth.views import action as auth_action


router = SimpleRouter()
router.register(r'group', base_info.GroupAuthInfoViewSet, basename="用户组权限")
router.register(r'group/list', auth_action.GroupList, basename=r'用户组列表')
router.register(r'group/del', auth_action.GroupDel, basename=r'删除用户组')
router.register(r'cmdb', base_info.CmdbAuthInfoViewSet, basename="系统权限")

urlpatterns = [
]

urlpatterns += router.urls








































