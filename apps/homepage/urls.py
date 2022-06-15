from django.urls import path
from .views import page
from .views import action
from apps.hls.views import page as hls_page
from apps.hls.views import action as hls_action
from users.views import action as users_action
from users.views import page as users_page

urlpatterns = [
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

    path('index/hls', hls_page.server_list),
    path('index/hls_action', hls_action.server_list_action),
    path('index/hls_create', hls_page.create_game),
    path('index/hls_create_action', hls_action.create_game),
]
