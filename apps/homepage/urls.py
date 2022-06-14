from django.urls import path
from .views import page
from .views import action
from apps.hls.views import page as hls_page
from apps.hls.views import action as hls_action

urlpatterns = [
    path('login/', page.login),
    path('loginAction/', action.login),
    path('index/', page.index),
    path('indexAction/', action.index),
    path('index/memberlist', page.memberList),
    path('index/memberlistAction', action.memberList),
    path('index/memberdel', page.memberdel),
    path('index/memberdelAction', action.memberdel),
    path('index/welcome1', page.welcome1),
    path('index/memberAdd', page.memberAdd),
    path('index/memberAddAction', action.memberAdd),
    path('index/orderList', page.orderList),
    path('index/orderList1', page.orderList1),
    path('index/memberEdit', page.memberEdit),
    path('index/memberPassword', page.memberPassword),
    path('index/memberPasswordAction', action.memberPassword),
    path('index/memberEditAction', action.memberEdit),
    path('index/memberDelAllAction', action.memberDelAll),
    path('index/genderChangeAction', action.genderChange),
    path('index/hls', hls_page.server_list),
    path('index/hls_action', hls_action.server_list_action),
]
