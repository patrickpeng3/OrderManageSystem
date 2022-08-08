from django.urls import path, include
from .views import page
from .views import action
from apps.hls.views import page as hls_page
from apps.hls.views import action as hls_action
from users.views import action as users_action
from users.views import page as users_page
from zabbix.views import page as zabbix_page
from zabbix.views import action as zabbix_action
from rest_framework.routers import SimpleRouter
from apps.hls.views import base_info as hls_base
from users.views import base_info as users_base
from job_manager.views import action as job_action
from audit import views as audit_action
from cmdb_auth.views import page as auth_page
# from cmdb_auth.views import action as auth_action


urlpatterns = [
    # path('', include(router.urls)),
    path('login/', page.login),
    path('loginAction/', action.login),
    path('index/', page.index),
    path('indexAction/', action.index),
    path('index/welcome1', page.welcome1),
    path('index/orderList', page.orderList),
    path('index/orderList1', page.orderList1),

    # 用户列表
    path('index/memberlist', users_page.memberList),
    # 新增用户
    path('index/memberAdd', users_page.memberAdd),
    # 修改用户密码
    path('index/memberPassword', users_page.memberPassword),

    # 部门列表
    path('index/GroupList', auth_page.GroupList),
    path('index/GroupAdd', auth_page.GroupAdd),
    path('index/GroupAlter', auth_page.GroupAlter),
    # 测试
    path('index/test', page.pageTest),

    # 游服列表
    path('index/hls', hls_page.server_list),
    # 搭服
    path('index/hls_create', hls_page.create_game),
    # 日志
    path('index/hls_log', hls_page.game_log),
    # 更新
    path('index/hls_update', hls_page.update_game),
    # 修改信息
    path('index/hls_edit', hls_page.edit_game),
    # 启服
    path('index/hls_start', hls_page.start_game),
    # 停服
    path('index/hls_stop', hls_page.stop_game),
    # 删服
    path('index/hls_delete', hls_page.start_game),
    # 日志
    path('index/hls_log', job_action.hls_log),
    path('index/hls_log_action', job_action.hls_log_action),
    path('index/audit_list', audit_action.audit_list),
    path('index/audit_list_action', audit_action.audit_list_action),

    # zabbix
    path('index/zabbix_host_list', zabbix_page.host_list),
    path('index/zabbix_host_list_action', zabbix_action.get_host),
]

router = SimpleRouter()
# 用户管理
router.register(r'users', users_base.UserInfoViewSet, basename="用户管理")
# 用户列表
router.register(r'users/list', users_action.MemberList, basename="用户列表")
# 删除用户
router.register(r'users/delete', users_action.MemberDel, basename="删除用户")
# 新增用户
router.register(r'users/add', users_action.MemberAdd, basename="新增用户")
# 修改用户密码
router.register(r'users/passwd', users_action.MemberPasswd, basename="修改用户密码")
# 修改用户性别
router.register(r'users/gender', users_action.GenderChange, basename="修改用户性别")
# 修改用户信息
router.register(r'users/edit', users_action.MemberEdit, basename="修改用户信息")

# 部门管理
router.register(r'department', users_base.DepartmentInfoViewSet, basename="部门管理")
# 部门列表
router.register(r'department/list', users_action.DepartmentList, basename="部门列表")


# 唤灵师
router.register(r'hls', hls_base.ServerInfoViewSet, basename="服务")
# 停服
router.register(r'hls/stop', hls_action.StopGame, basename="停服")
# 删服
router.register(r'hls/delete', hls_action.DeleteGame, basename="删服")
# 启服
router.register(r'hls/start', hls_action.StartGame, basename="启服")
# 更新
router.register(r'hls/update', hls_action.UpdateGame, basename="更新")
# 创服
router.register(r'hls/create', hls_action.CreateGame, basename="创服")
# 游服列表
router.register(r'hls/list', hls_action.GameList, basename="游服列表")
# 修改信息
router.register(r'hls/edit', hls_action.EditGame, basename="修改信息")

urlpatterns += router.urls
