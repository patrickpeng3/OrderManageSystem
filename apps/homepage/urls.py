from django.urls import path
from .views import page
from .views import action

urlpatterns = [
    path('login/', page.login),
    path('logintest/', action.login),
    path('index/', page.index),
    path('indextest/', action.index),
    path('index/memberlist', page.memberList),
    path('index/memberlist1', page.memberList1),
    path('index/memberlist1test', action.memberList1),
    path('index/memberdel', page.memberdel),
    path('index/welcome1', page.welcome1),
]
