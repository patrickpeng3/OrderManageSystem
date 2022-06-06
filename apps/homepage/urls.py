from django.urls import path
from .views import page
from .views import action

urlpatterns = [
    path('login/', page.login),
    path('loginAction/', action.login),
    path('index/', page.index),
    path('indexAction/', action.index),
    path('index/memberlist', page.memberList),
    path('index/memberlist1', page.memberList1),
    path('index/memberlist1Action', action.memberList1),
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
]
