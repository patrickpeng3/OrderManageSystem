import json
from cmdb_auth.models import user_auth_cmdb, auth_group
from django_redis import get_redis_connection
from cmdb_hls.settings import ACC_JUMP


def auth_class(user):
    # if ACC_JUMP:
    #     auth_dic = {}
    #     if user:
    #         conn = get_redis_connection('acc_auth')
    #         auth_lis = conn.get('acc_{username}'.format(username=user.username))
    #         if auth_lis is not None:
    #             auth_lis = json.loads(auth_lis)
    #             for auth in auth_lis:
    #                 auth_lis[auth] = True
    #     return auth_dic
    # else:
    auth_group_data = {}
    auth_list = [
        'select_host',
        'apps',
        'hls',
        'add_user',
        'edit_user',
        'edit_pass',
        'delete_user',
        'add_department',
        'auth_log',
    ]
    if user:
        """查询用户所属活跃的用户组"""
        group_auth = user.auth_group_set.all().filter(enable=True)
        # 权限
        for group in group_auth:
            group_uuid = str(group.uuid)
            group_data = auth_group.objects.get(uuid=group_uuid)
            try:
                """获取到每个用户组中的详细权限"""
                auth_info = user_auth_cmdb.objects.get(group_name=group_data)
                """查询用户组中权限的boolean值"""
                for _auth in auth_list:
                    try:
                        b = getattr(auth_info, _auth)
                        """若该用户组拥有该权限，则将该权限加入到auth_group_data中"""
                        if b:
                            auth_group_data[_auth] = b
                    except AttributeError as e:
                        pass
            except Exception as e:
                pass
    return auth_group_data













