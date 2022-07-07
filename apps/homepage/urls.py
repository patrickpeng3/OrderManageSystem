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
from apps.hls.views import base_info


urlpatterns = [
    # path('', include(router.urls)),
    path('login/', page.login),
    path('loginAction/', action.login),
    path('index/', page.index),
    path('indexAction/', action.index),
    path('index/welcome1', page.welcome1),
    path('index/orderList', page.orderList),
    path('index/orderList1', page.orderList1),

    path('index/memberlist', users_page.memberList),
    path('index/memberlistAction', users_action.memberList),
    path('index/memberAdd', users_page.memberAdd),
    path('index/memberAddAction', users_action.memberAdd),
    path('index/memberdel', users_page.memberdel),
    path('index/memberdelAction', users_action.memberdel),
    path('index/memberEdit', users_page.memberEdit),
    path('index/memberEditAction', users_action.memberEdit),
    path('index/memberPassword', users_page.memberPassword),
    path('index/memberPasswordAction', users_action.memberPassword),
    path('index/memberDelAllAction', users_action.memberDelAll),
    path('index/genderChangeAction', users_action.genderChange),

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
    path('index/hls_edit_action', hls_action.edit_game),
    # 启服
    path('index/hls_start', hls_page.start_game),
    # 停服
    path('index/hls_stop', hls_page.start_game),
    # 删服
    path('index/hls_delete', hls_page.start_game),

    path('index/zabbix_host_list', zabbix_page.host_list),
    path('index/zabbix_host_list_action', zabbix_action.get_host),
]

router = SimpleRouter()
router.register(r'hls', base_info.ServerInfoViewSet, basename="服务")
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

urlpatterns += router.urls
