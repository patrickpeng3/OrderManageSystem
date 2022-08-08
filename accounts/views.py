from django.shortcuts import render
from users.models import User
from cmdb_auth.models import auth_group, user_auth_cmdb

# Create your views here.


def perm_select(func):
    def perm(user):
        print("test")

    return perm


# @perm_select
def test(user_id):
    user = User.objects.filter(id=user_id)
