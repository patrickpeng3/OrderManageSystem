from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login),
    path('index/', views.index),
    path('index/memberlist', views.memberList),
    path('index/memberlist1', views.memberlist1),
    path('index/memberdel', views.memberdel),
    path('index/welcome1', views.welcome1),
]
