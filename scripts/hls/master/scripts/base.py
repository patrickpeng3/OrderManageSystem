#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Author: pengguanghong
@Date  : 2022/03/07
@Desc  :
@Prepare : pip install
@Note  :
"""

# 标准库模块
import argparse
import datetime
import os
import sys
import time

# 自定义模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tool.run_cmd.shell_cmd import shell_run
from tool.db.mysql_manage import MysqlManage
from tool.runlog.runlog import log

# saltid
salt_name = 'sg-gs-'

# 负载均衡
clb_manage = "/data/gitlab/oam-admin/hls/master/tool/txcloud/clb/clb_manage.py"
domain = "/data/gitlab/oam-admin/hls/master/tool/alicloud/dns/domain.py"
bind_clb = "/data/gitlab/oam-admin/hls/master/scripts/bind_clb.py"
net_type = 'OPEN'
forward = 1
vpc_id = 'vpc-1yrvi0lp'
project_id = '1251518'

# salt版本
hls_salt_version = 2019

# 更新包
package_dir = '/data/www/bingfing_game/game_file/'
zip_passwd = 'HRsBkzGxhfwnt9SPLhUGjLDFrFSSEQrQCLlitCWh'


# 本机mysql
mysqlcfg  = {'host': '127.0.0.1',
             'port': 3306,
             'user': 'root',
             'passwd': 'dkmwebmysql!q$EWQ23FD23',
             'servercfg_select': 'select {} from ops.server_cfg where serverid = {}',
             'saltlist2_select': 'select {} from ops.saltlist2 where serverid = {}',

             # Game_Admin_V2.server
             'salt_id': 'select salt_id from Game_Admin_V2.server where server_id = {}',
             'check_game': 'select count(1) from Game_Admin_V2.server where server_id = "{}"',
             'server_host': 'select server_host from Game_Admin_V2.server where server_id = {}',
             'game_status': 'select server_status from Game_Admin_V2.server where server_id = {}',
             'web_port': 'select web_port from Game_Admin_V2.server where  salt_id = "{}"',
             'op_one': 'update Game_Admin_V2.server set server_status = 2 where server_id = {}',
             'op_many': 'update Game_Admin_V2.server set server_status = 2 where server_id in {}',
             'update_one': 'update Game_Admin_V2.server set version = "{}" where server_id = {}',
             'update_many': 'update Game_Admin_V2.server set version = "{}" where server_id in {}',
             'create': 'insert into Game_Admin_V2.server values ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", {})',
             'clbname_one': 'update Game_Admin_V2.server set clb = "{}" where server_id = {}',
             'clbname_many': 'update Game_Admin_V2.server set clb = "{}" where server_id in {}',
             'clb_name': 'select clb from Game_Admin_V2.server where server_id = {}',
             'changetime_one': 'update Game_Admin_V2.server set born_time = "{}" where server_id = {}',
             'changetime_many': 'update Game_Admin_V2.server set born_time = "{}" where server_id in {}',
             'running_one': 'update Game_Admin_V2.server set server_status = 1 where server_id = {}',
             'running_many': 'update Game_Admin_V2.server set server_status = 1 where server_id in {}',
             'not_running_one': 'update Game_Admin_V2.server set server_status = 0 where server_id = {}',
             'not_running_many': 'update Game_Admin_V2.server set server_status = 0 where server_id in {}',
             'delete_one': 'delete from Game_Admin_V2.server where server_id = {}',
             'delete_many': 'delete from Game_Admin_V2.server where server_id in {}',
             'nginx_port_one': 'select nginx_port from Game_Admin_V2.server where server_id = {}',
             'nginx_port_many': 'select nginx_port from Game_Admin_V2.server where server_id in {}',

             # Game_Admin_V2.special
             'special_backend': 'select backend_ver from Game_Admin_V2.special where name = "{}"',
             'special_clb': 'select clb from Game_Admin_V2.special where name = "{}"',
             'update_backend': 'update Game_Admin_V2.special set backend_ver = "{}" where name = "{}"',
             'special_cfg': 'select name,id_range,clb from Game_Admin_V2.special',
             'clbnum': 'select clbnum from Game_Admin_V2.special where clb = "{}"',
             'add_clb': 'update Game_Admin_V2.special set clbnum  = {} where clb = "{}"',

             # Game_Admin_V2.machine
             'master_ip': 'select master_ip from Game_Admin_V2.machine where salt_id = "{}"',
             'private_ip': 'select private_ip from Game_Admin_V2.machine where salt_id = "{}"',
             }

# APImysql
api_mysqlcfg = {'host': '10.1.100.6',
                'port': 3306,
                'user': 'root',
                'passwd': 'dkmwebmysql!q$EWQ23FD23',
                'status_select': 'select status, is_private from wenming_admin.rd_server where server_id = {}'}

# 远程操作命令
hls_game_cmd = {'start': '/bin/bash /data/scripts/game_start.sh {} {}',
                'stop': '/bin/bash /data/scripts/game_stop.sh {} {}',
                'update': '/bin/bash /data/scripts/game_update.sh {} {} {}',
                'changetime': '/bin/bash /data/scripts/game_change_data.sh {} {} {}',
                'update_temp': '/bin/bash /data/gitlab/oam-admin/hls/master/scripts/moban_update.sh {}',
                'create': '/bin/bash /data/scripts/gamenew_install_VX.sh {id} {backend_ver} {num}',
                'delete': '/bin/bash /data/scripts/game_recycle.sh {id} {ver_type}'}
tyqy_game_cmd = {'start': 'cd /data/cmdb_script && /bin/bash /data/cmdb_script/xjqy_server_start.sh {} {} 5',
                'stop': 'cd /data/cmdb_script && /bin/bash /data/cmdb_script/xjqy_server_stop.sh {} {}',
                'update': 'cd /data/cmdb_script && /bin/bash /data/cmdb_script/xjqy_server_update.sh {} {}'}


def init_logger(action):
    # 日志
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs',
                           time.strftime("%Y-%m-%d", time.localtime()))
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file = os.path.join(log_dir, action + time.strftime("%Y%m%d_%H%M%S", time.localtime()) + '.log')
    return log_file


# 获取区服id列表
# 根据id范围返回具体id列表
def id_range(serverid):
    """
    根据id范围返回具体id列表
    :param serverid: 格式需符合1_3:6_8,以_分隔连续id,以:分隔不连续id
    :return: id_list: id列表
    """
    id_list = []
    for i in serverid.split(':'):
        if '_' not in i:
            id_list.append(int(i))
        else:
            begin = int(i.split('_')[0])
            end = int(i.split('_')[1])
            for j in range((end - begin) + 1):
                a = begin + j
                id_list.append(a)
    return list(set(id_list))


# 获取区服id对应saltid列表
def saltid_range(serverid, mysql):
    """
    根据id范围返回具体saltid列表
    :param serverid: 区服id
    :return: saltid_list: saltid列表
    """
    saltid_list = []
    for id in serverid:
        mysql.execute(mysqlcfg['salt_id'].format(id))
        result = mysql.fetchall()
        if not result:
            continue
        saltid = result[0][0]
        saltid_list.append(saltid)
    return list(set(saltid_list))


# 区服状态检查
def status_check(serverid, mysql, timeout=10):
    """
    区服状态检查
    :param serverid: 区服id
    :param timeout: 超时时间
    :return:
    """
    running = []
    for id in serverid:
        mysql.execute(api_mysqlcfg['status_select'].format(id))
        status = mysql.fetchall()
        if status:
            if status[0] == (1, 0):
                running.append(id)
    if len(running):
        print(running, '运行中,请检查...')
        exit(1)


# 更新minion脚本
def update_minion_script(saltid_list, mysql, runner, logger, timeout=60):
    """
    更新minion脚本
    :param serverid: 区服id列表
    """
    start = time.time()
    task = 'update_minion_script'
    jid_list = []
    for saltid in saltid_list:
        jid = '{}-{}-{}'.format(task, saltid.replace('-','_'), datetime.datetime.now().strftime("%Y%m%d_%H%M%S.%f"))
        cmd = "echo '4nMA-yz!0z' > /etc/rsyncd.qmhy && chmod 600 /etc/rsyncd.qmhy && " + rsync_source_from('10.1.220.5', '/data/scripts/', 'gitlab/oam-admin/hls/minion/scripts/')
        # print(cmd)
        jid = runner.async_cmd(saltid, cmd, jid=jid)
        jid_list.append(jid)
    #  查询异步任务结果,默认60s
    sql = runner.jid_sql(tuple(jid_list))
    logger.info('执行sql: {}'.format(sql))
    jid_set = select_salt_jid(jid_list, sql, runner, hls_salt_version, timeout)
    logger.info(result_sumup(jid_set, task, start))
    end = time.time()
    logger.info('更新minion脚本完毕,耗时:{}s'.format(round(end - start, 3)))


# 解压
# def unzip_package(version):
def unzip_package(version, logger):
    """
    更新包解压
    :param version:  更新包版本
    :return:
    """
    package_path = os.path.join(package_dir, version + '.zip')
    unzip_bakdir = os.path.join(package_dir, 'bak')
    unzip_dir = os.path.join(unzip_bakdir, version)
    unzip_path = os.path.join(unzip_dir, version + '.zip')
    if not os.path.exists(unzip_bakdir):
        os.makedirs(unzip_bakdir)
    if not os.path.exists(package_path):
        print('{}包不存在,请检查'.format(package_path))
        logger.error('{}包不存在,请检查'.format(package_path))
        exit(1)
    if not os.path.exists(unzip_dir):
        cmd1 = 'unzip -o -P{} {}  -d {} >/dev/null && unzip -o {} -x server.cfg -d {}'.format(zip_passwd, package_path, unzip_bakdir, unzip_path, unzip_dir)
        cmd2 = 'cd {} && find ./ -type f | xargs md5sum | egrep -v "{}.zip|md5.list" > md5.list'.format(unzip_dir, version)
        for cmd in (cmd1, cmd2):
            # print(cmd)
            out, err, ret = shell_run(cmd)
            # print(ret)
            if ret:
                print('解压失败,请检查...err:{}'.format(err))
                logger.error('解压失败,请检查...err:{}'.format(err))
                exit(1)


# 同步更新包到目标机器
def update_minion_package(saltid_list, version, mysql, runner, logger, timeout=60):
    """
    同步更新包到目标机器
    :param saltid_list: saltid列表
    :param version:
    :param mysql:
    :param runner:
    :param logger:
    :param timeout:
    :return:
    """
    start = time.time()
    task = 'update_minion_package'
    source_path = os.path.join('bak', version)
    target_path = '/data/gs_hotfix/'
    jid_list = []
    for saltid in saltid_list:
        jid = '{}-{}-{}'.format(task, saltid.replace('-','_'), datetime.datetime.now().strftime("%Y%m%d_%H%M%S.%f"))
        cmd = "echo 'o7XNa0KAsz9vQck0jO' > /etc/pass.wmsg && chmod 600 /etc/pass.wmsg && " + rsync_source_from('10.1.220.5', target_path, source_path, user='hls', pass_file='/etc/pass.wmsg', mode_name='packhotfix')
        # print(cmd)
        jid = runner.async_cmd(saltid, cmd, jid=jid)
        jid_list.append(jid)
    #  查询异步任务结果,默认60s
    sql = runner.jid_sql(tuple(jid_list))
    logger.info('执行sql: {}'.format(sql))
    jid_set = select_salt_jid(jid_list, sql, runner, hls_salt_version, timeout)
    logger.info(result_sumup(jid_set, task, start))
    end = time.time()
    logger.info('同步package完毕,耗时:{}s'.format(round(end - start, 3)))


# rsync同步文件
def rsync_source_to(ip, source, dest, user='qmhy', pass_file='/etc/rsyncd.qmhy', mode_name='sync', port=8337):
    """
    发送文件
    :param ip: 目标ip
    :param port: rsync server port
    :param user: rsync auth name
    :param pass_file: rsync password file path
    :param mode_name: rsync auth mode
    :param source: source dir
    :param dest: dest dir
    :return:
    """
    return 'rsync -az --port={port} --password-file={pass_file} {source} {user}@{ip}::{mode_name}/{dest}'.format(
            port=port, pass_file=pass_file, source=source, user=user, ip=ip, mode_name=mode_name, dest=dest)


def rsync_source_from(ip, source, dest, user='qmhy', pass_file='/etc/rsyncd.qmhy', mode_name='sync', port=8337):
    """
    拉取文件
    :param ip: 源ip
    :param port: rsync server port
    :param user: rsync auth name
    :param pass_file: rsync password file path
    :param mode_name: rsync auth mode
    :param source: source dir
    :param dest: dest dir
    :return:
    """
    return 'rsync -az --port={port} --password-file={pass_file} {user}@{ip}::{mode_name}/{dest} {source}'.format(
            port=port, pass_file=pass_file, source=source, user=user, ip=ip, mode_name=mode_name, dest=dest)


# 查询salt异步结果
def select_salt_jid(jid_list, sql, runner, salt_version, timeout):
    """
    查询salt异步结果
    :param jid_list: jid列表
    :param sql: sql查询语句
    :param runner: salt实例
    :param salt_version:
    :param timeout:
    :return: jid_set: jid查询结果
    """
    for i in range(timeout * 5):
        time.sleep(0.2)
        last = timeout * 5 - 1
        if i == last:
            jid_set = runner.jid_return(tuple(jid_list), sql, salt_version)
        else:
            jid_set = runner.jid_return(tuple(jid_list), sql, salt_version, log=False)
        if not jid_set[3]:
            runner.jid_return(tuple(jid_list), sql, salt_version)
            break
    return jid_set


# 总结归纳salt异步结果
def result_sumup(jid_set, task, start):
    """
    总结归纳salt异步结果
    :param jid_set: salt异步jid
    :param task: 任务名字
    :param start: 任务开始时间
    :return: message: 总结信息
    """
    end = time.time()
    finish = len(jid_set[0])
    succeed = len(jid_set[1])
    #fail = len(jid_set[2])
    fail_id = []
    for jid in list(jid_set[2]):
        id = jid.split('-')[1]
        fail_id.append(id)
    else:
        fail = len(jid_set[2])
        unfinish = len(jid_set[3])
    # print(fail_id)
    # print(jid_set[2])
    #unfinish = len(jid_set[3])
    unfinish_id = []
    for jid in list(jid_set[3]):
        id = jid.split('-')[1]
        unfinish_id.append(id)
    spent = round(end - start, 3)
    last = datetime.datetime.now().strftime("%Y%m%d_%H%M%S.%f")
    if not unfinish_id:
        if fail_id:
            message = '{} finish\n{} succeed\n{} fail id:{}\n{} unfinish\n{} spent time {}s  end:{}'.format(finish, succeed, fail, fail_id, unfinish, task, spent, last)
        else:
            message = '{} finish\n{} succeed\n{} fail\n{} unfinish\n{} spent time {}s  end:{}'.format(finish, succeed, fail, unfinish, task, spent, last)
    else:
        if fail_id:
            message = '{} finish\n{} succeed\n{} fail id:{}\n{} unfinish id:{}\n{} spent time {}s  end:{}'.format(finish, succeed, fail, fail_id, unfinish, unfinish_id, task, spent, last)
        else:
            message = '{} finish\n{} succeed\n{} fail\n{} unfinish id:{}\n{} spent time {}s  end:{}'.format(finish, succeed, fail, unfinish, unfinish_id, task, spent, last)
    return message


def get_options():
    usage = """
    python %(prog)s -a action -d domain_name -r record_key [-t record_type] [-v record_value]
    -a: 指定动作['add', 'update', 'select', 'delete']
    -d: 指定域名
    -r: 指定解析记录
    -t: 指定解析记录类型，默认类型A记录
    -v: 指定解析记录值

    添加域名解析: python %(prog)s -a add -d baidu.com -r www -t A -v 1.1.1.1
    修改域名解析: python %(prog)s -a update -d baidu.com -r www -t A -v 1.1.1.1
    查询域名解析: python %(prog)s -a select -d baidu.com -r www -t A
    删除域名解析: python %(prog)s -a add -d baidu.com -r www -t A
    """
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('-a', '--action', dest='action', choices=['select', 'add', 'update', 'delete'], required=True,
                        help='target action,just include selete, add, update, detele')
    parser.add_argument('-d', '--domain', dest='domain_name', default='shxil.com', help='target domain_name')
    parser.add_argument('-r', '--rr', dest='rr', required=True, help='target record_key')
    parser.add_argument('-t', '--type', dest='record_type', default='A', help='target record_type ,default: A')
    parser.add_argument('-v', '--value', dest='value', help='target record_value')

    option = parser.parse_args()
    return option


if __name__ == '__main__':
    start = time.time()
    usage = """
    python clb_manage.py { clb, listener, backend } ..
    负载均衡器:
        查询: python clb_manage.py clb -a select -n clb_name
        添加: python clb_manage.py clb -a add -n clb_name -t net_type -f forward -v vpc_id -p project_id
    监听器:
        查询个数: python clb_manage.py listener -a count -n clb_name
        查询是否存在: python clb_manage.py listener -a select -n clb_name -p port
        添加: python clb_manage.py listener -a add -n clb_name -p port -N listener_name -P listener_protocal
        删除: python clb_manage.py listener -a delete -n clb_name -p port
    监听器后端:
        查询: python clb_manage.py backend -a select -n clb_name -p port
        添加: python clb_manage.py backend -a add -n clb_name -p port -b server -P server_port -w weight
        删除: python clb_manage.py backend -a delete -n clb_name -p port -b server -P server_port
    """
    # if len(sys.argv) == 1:
    #     print(usage)
    #     sys.exit(1)
    # target = sys.argv[1]
    # options = get_options()
    # #print(options)
    # log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs',
    #                        time.strftime("%Y-%m-%d", time.localtime()))
    # log_file = os.path.join(log_dir, os.path.basename(__file__).split('.')[0] + '.log')
    # if not os.path.exists(log_dir):
    #     os.makedirs(log_dir)
    # logger = log(log_file)
    # clb = ClbManage(access_keyid, access_secret, region, logger)
    unzip_package('new_tdc_57_0')


# 获取专服配置字典
def get_special_cfg():
    # 实例化
    mysql = MysqlManage(mysqlcfg['host'], mysqlcfg['port'], mysqlcfg['user'], mysqlcfg['passwd'], log(init_logger("special_cfg"), reload=True))
    special_cfg = {}
    mysql.execute(mysqlcfg['special_cfg'])
    special_cfg_list = mysql.fetchall()
    for cfg in special_cfg_list:
        range_cfg = {}
        id_range_list = []
        if ':' in cfg[1]:
            id_range_list = cfg[1].split(":")
        else:
            id_range = cfg[1]
            id_range_list.append(id_range)
        begin_list, end_list = [[] for i in range(2)]
        for id_range in id_range_list:
            begin = id_range.split("_", 1)[0]
            end = id_range.split("_", 1)[1]
            begin_list.append(begin)
            end_list.append(end)
        range_cfg['begin'] = begin_list
        range_cfg['end'] = end_list
        range_cfg['clb'] = cfg[2]
        special_cfg[cfg[0]] = range_cfg
    return special_cfg


the_special_cfg = get_special_cfg()


# 获取专服名称及clb名称
def SerType(_id):
    special_name, clb = ["" for i in range(2)]
    for k, v in the_special_cfg.items():
        for i in range(len(v['begin'])):
            if int(v['end'][i]) > int(_id) > int(v['begin'][i]):
                special_name = k
                clb = v['clb']
    return special_name, clb
