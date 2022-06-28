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
import json
import jsonpath
import os
import sys
import time
from datetime import datetime, date, timedelta
from base import *

# 第三方模块

# 自定义模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from ..tool.db.mysql_manage import MysqlManage
from scripts.hls.master.tool.db.mysql_manage import MysqlManage
from scripts.hls.master.tool.runlog.runlog import log
from scripts.hls.master.tool.run_cmd.salt_async import SaltAsync


class GameManage(object):

    def __init__(self, serverid, action, logger, runner, mysql):
        self.serverid = serverid
        self.action = action
        self.logger = logger
        self.runner = runner
        self.mysql = mysql

    def manage(self, opentime=False, version=False, saltid=False, timeout=60):
        """
        :param action: 动作
        :param serverid: 区服id
        :param mysql: 数据库操作
        :param runner: 异步执行
        :param opentime: 开服时间
        :param version: 更新版本
        :param timeout: 查询异步执行结果超时时间
        :return:
        """
        start = time.time()
        jid_list, exist_list, op_ing_list, create_cfg_list, web_port_list = [[] for i in range(5)]
        if saltid:
            saltid = salt_name + saltid
        if self.action == 'create':
            # 创服前检查
            for _id in self.serverid:
                self.mysql.execute(mysqlcfg['check_game'].format(_id))
                game_exist = self.mysql.fetchall()[0][0]
                if game_exist == 1:
                    exist_list.append(_id)
            if exist_list:
                self.logger.info("{}服已存在！".format(exist_list))
                print("{}服已存在！".format(exist_list))
                sys.exit(1)
            # 检查已用端口
            self.mysql.execute(mysqlcfg['web_port'].format(saltid))
            web_port = self.mysql.fetchall()
            for i in range(0, len(web_port)):
                web_port_list.append(web_port[i][0])
        else:
            for _id in self.serverid:
                # 查询saltid
                self.mysql.execute(mysqlcfg['salt_id'].format(_id))
                result = self.mysql.fetchall()
                if not result:
                    continue
                saltid = result[0][0]
                # 执行前检查
                self.mysql.execute(mysqlcfg['check_game'].format(_id))
                game_exist = self.mysql.fetchall()[0][0]
                self.mysql.execute(mysqlcfg['game_status'].format(_id))
                game_status = self.mysql.fetchall()[0][0]
                if game_exist == 0:
                    exist_list.append(_id)
                if op_ing_list == 2:
                    op_ing_list.append(_id)
            if exist_list or op_ing_list:
                if exist_list:
                    self.logger.info("{}服不存在！".format(exist_list))
                    print("{}服不存在！".format(exist_list))
                if op_ing_list:
                    self.logger.info("{}服有操作正在进行中！".format(op_ing_list))
                    print("{}服有操作正在进行中！".format(op_ing_list))
                sys.exit(1)
        # 修改游服状态为2(操作进行中)
        serverid_tuple = tuple(self.serverid)
        if len(serverid_tuple) == 1:
            self.mysql.execute(mysqlcfg['op_one'].format(serverid_tuple[0]))
        else:
            self.mysql.execute(mysqlcfg['op_many'].format(serverid_tuple))
        # 发起异步任务
        for id in self.serverid:
            jid = '{action}-{id}-{nowtime}'.format(action=self.action, id=id, nowtime=datetime.datetime.now().strftime("%Y%m%d_%H%M%S.%f"))
            # 判断操作类型
            if self.action == 'start':
                cmd = hls_game_cmd['{}'.format(self.action)].format(id, game_status)
            elif self.action == 'stop':
                cmd = hls_game_cmd['{}'.format(self.action)].format(id, game_status)
            elif self.action == 'update':
                cmd = hls_game_cmd['{}'.format(self.action)].format(version, id, game_status)
            elif self.action == 'changetime':
                if opentime:
                    cmd = hls_game_cmd['{}'.format(self.action)].format(id, game_status, opentime)
                else:
                    opentime = date.today() + timedelta(1)
                    cmd = hls_game_cmd['{}'.format(self.action)].format(id, game_status, '')
            elif self.action == 'create':
                self.logger.info("即将新建游服！")
                # 后端版本
                self.mysql.execute(mysqlcfg['special_backend'].format(SerType(id)[0]))
                backend_ver = self.mysql.fetchall()[0][0]
                # 获取端口
                for num in range(1991, 2011):
                    if num not in web_port_list:
                        num = num - 1990
                        break
                else:
                    self.logger.info("端口获取错误!")
                if len(self.serverid) > 1:
                    web_port_list.append(1990+num)
                # 生成创服配置
                self.mysql.execute(mysqlcfg['master_ip'].format(saltid))
                server_host = self.mysql.fetchall()[0][0]
                self.mysql.execute(mysqlcfg['private_ip'].format(saltid))
                private_ip = self.mysql.fetchall()[0][0]
                create_time = time.strftime("%Y%m%d%H%M", time.localtime())
                create_cfg = {
                    'id': id,
                    'saltid': saltid,
                    'backend_ver': backend_ver,
                    'server_host': server_host,
                    'private_ip': private_ip,
                    'ws_server_port': 18880 + num,
                    'web_port': 1990 + num,
                    'fep_client_port': 6660 + num,
                    'fep_server_port': 25000 + num,
                    'dp_server_port': 40000 + num,
                    'nginx_port': 10000 + num,
                    'create_time': create_time
                }
                create_cfg_list.append(create_cfg)
                self.logger.info("新建游服配置: {}".format(create_cfg))
                # 执行创服
                cmd = hls_game_cmd['{}'.format(self.action)].format(id=id, backend_ver=backend_ver, num=num)
            elif self.action == 'delete':
                self.mysql.execute(mysqlcfg['special_backend'].format(SerType(id)[0]))
                ver_type = self.mysql.fetchall()[0][0].split("_", 1)[0]
                cmd = hls_game_cmd['{}'.format(self.action)].format(id=id, ver_type=ver_type)
            # 日志
            self.logger.info('执行命令: {}'.format(cmd))
            jid = self.runner.async_cmd(saltid, cmd, jid=jid)
            jid_list.append(jid)
        # 查询异步任务结果,默认60s
        sql = self.runner.jid_sql(tuple(jid_list))
        self.logger.info('执行sql: {}'.format(sql))
        jid_set = select_salt_jid(jid_list, sql, self.runner, hls_salt_version, timeout)
        print(jid_set)
        # 执行失败
        failed_id = []
        if jid_set[2]:
            for jid in jid_set[2]:
                id = jid.split('-')[1]
                failed_id.append(id)
        failed_tuple = tuple(failed_id)
        if failed_tuple:
            if len(failed_tuple) == 1:
                running_mysqlcfg = mysqlcfg['running_one'].format(failed_tuple[0])
                not_running_mysqlcfg = mysqlcfg['not_running_one'].format(failed_tuple[0])
            else:
                running_mysqlcfg = mysqlcfg['running_many'].format(failed_tuple)
                not_running_mysqlcfg = mysqlcfg['not_running_many'].format(failed_tuple)
            if self.action == 'stop':
                self.mysql.execute(running_mysqlcfg)
            elif self.action == 'update' and 'hotfix' in version:
                self.mysql.execute(running_mysqlcfg)
            else:
                self.mysql.execute(not_running_mysqlcfg)
        # 执行成功
        success_list = []
        if jid_set[1]:
            for jid in jid_set[1]:
                id = jid.split('-')[1]
                success_list.append(id)
        success_tuple = tuple(success_list)
        if success_tuple:
            # 停服更新成功，更新模版
            if self.action == 'update' and 'hotfix' not in version:
                self.update_moban(version)
            # 创服成功，绑定负载均衡
            if self.action == 'create':
                self.game_create(success_list, create_cfg_list)
            # 删除成功，删除负载均衡
            if self.action == 'delete':
                self.game_delete(success_list)
            # 修改数据库
            if len(success_tuple) == 1:
                running_mysqlcfg = mysqlcfg['running_one'].format(success_tuple[0])
                delete_mysqlcfg = mysqlcfg['delete_one'].format(success_tuple[0])
                changetime_mysqlcfg = mysqlcfg['changetime_one'].format(opentime, success_tuple[0])
                not_running_mysqlcfg = mysqlcfg['not_running_one'].format(success_tuple[0])
                update_mysqlcfg = mysqlcfg['update_one'].format(version, success_tuple[0])
            else:
                running_mysqlcfg = mysqlcfg['running_many'].format(success_tuple)
                delete_mysqlcfg = mysqlcfg['delete_many'].format(success_tuple)
                changetime_mysqlcfg = mysqlcfg['changetime_many'].format(opentime, success_tuple)
                not_running_mysqlcfg = mysqlcfg['not_running_many'].format(success_tuple)
                update_mysqlcfg = mysqlcfg['update_one'].format(version, success_tuple)
            if self.action == 'start':
                self.mysql.execute(running_mysqlcfg)
            elif self.action == 'update' and 'hotfix' in version:
                self.mysql.execute(running_mysqlcfg)
            elif self.action == 'delete':
                self.mysql.execute(delete_mysqlcfg)
            else:
                if self.action == 'changetime':
                    self.mysql.execute(changetime_mysqlcfg)
                elif self.action == 'update' and 'hotfix' not in version:
                    self.mysql.execute(update_mysqlcfg)
                self.mysql.execute(not_running_mysqlcfg)
        # 输出执行结果
        print(result_sumup(jid_set, self.action, start))
        self.logger.info(result_sumup(jid_set, self.action, start))

    def update_moban(self, version):
        # 更新模版
        moban = os.path.join("/data", "game_Template", "{}".format(version))
        if not os.path.exists(moban):
            update_tmp = hls_game_cmd['update_temp'].format(version)
            ret = shell_run(update_tmp)
            if ret[2] == 0:
                print("更新模版{}成功!".format(version))
                self.logger.info("已更新模版为{}".format(version))
            else:
                print("更新模版{}失败!".format(version))
                self.logger.info("更新模版{}失败!".format(version))

    def game_create(self, success_list, create_cfg_list):
        for _id in success_list:
            for create_id in create_cfg_list:
                if int(create_id['id']) == int(_id):
                    self.mysql.execute(mysqlcfg['create'].format(_id, create_id['saltid'], 0,
                                                                 create_id['backend_ver'],
                                                                 create_id['server_host'],
                                                                 create_id['private_ip'],
                                                                 create_id['ws_server_port'],
                                                                 create_id['web_port'],
                                                                 create_id['fep_client_port'],
                                                                 create_id['fep_server_port'],
                                                                 create_id['dp_server_port'],
                                                                 create_id['nginx_port'],
                                                                 0, 0,
                                                                 create_id['create_time']))
        cmd = "python3 {bind_clb} '{server_id}'".format(bind_clb=bind_clb, server_id=success_list)
        ret = shell_run(cmd)
        print(ret)
        print(cmd)
        if ret[2] != 0:
            self.logger.info("执行绑定负载均衡失败！")
            print("执行绑定负载均衡失败！")
            sys.exit(1)

    def game_delete(self, success_list):
        clb_name_list = []
        for _id in success_list:
            self.mysql.execute(mysqlcfg['clb_name'].format(_id))
            clb_name = self.mysql.fetchall()[0][0]
            clb_name_list.append(clb_name)
        for clb_name in set(clb_name_list):
            clb_port_list, id_list = [[] for i in range(2)]
            # 一次最多删除20个监听器
            if len(success_list) > 20:
                group_num = divmod(len(success_list), 20)[0]
                for i in range(group_num+1):
                    # group_list = []
                    group_list = success_list[20*i:20*(i+1)]
                    id_list.append(group_list)
            else:
                id_list.append(success_list)
            for group in range(len(id_list)):
                for _id in id_list[group]:
                    if int(_id) > 65535:
                        clb_port = divmod(int(_id), 50000)[0] + 10000
                    else:
                        clb_port = int(_id)
                    self.mysql.execute(mysqlcfg['clb_name'].format(_id))
                    clb = self.mysql.fetchall()[0][0]
                    if clb_name == clb:
                        clb_port_list.append(clb_port)
                listener_range = ":".join("%s" % d for d in clb_port_list)
                # 批量删除: python3 clb_manage.py listener - a batchdelete - n clb_name - r 10001_10005
                cmd = "python3 {clb_manage} listener -a batchdelete -n {clb_name} -r {listener_range}".format(clb_manage=clb_manage, clb_name=clb_name, listener_range=listener_range)
                ret = shell_run(cmd)
                if ret[2] != 0:
                    self.logger.info("删除负载均衡监听器失败！")
                    print("删除负载均衡监听器失败！")


def get_options():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help')
    # 添加子命令 game
    parser_game = subparsers.add_parser('game', help='game help')
    parser_game.add_argument('-a', '--action', dest='action', choices=['start', 'stop', 'changetime', 'create', 'restart', 'update', 'delete', 'remove', 'define'], required=True, help='target action, just include start, stop, create, restart, add, update, delete, remove, define')
    parser_game.add_argument('-r', '--range', dest='serverid', required=True, help='target serverid')
    parser_game.add_argument('-t', '--opentime', dest='opentime', help='target opentime')
    parser_game.add_argument('-v', '--version', dest='version', help='target version')
    parser_game.add_argument('-s', '--saltid', dest='saltid', help='target saltid')

    option = parser.parse_args()
    return option


def main():
    start = time.time()
    usage = """
        python3 ops_manage.py { game } ...
        游戏服game:
            启动: python3 ops_manage.py game -a start -r serverid 
            停止: python3 ops_manage.py game -a stop -r serverid 
            停服更新: python3 ops_manage.py game -a update -r serverid -v new_tdc_38_6
            热更新: python3 ops_manage.py game -a update -r serverid -v hotfix_tdc_227
            修改开服时间: python3 ops_manage.py game -a changetime -r serverid {-t 2021-01-01}
            创服: python3 ops_manage.py game -a create -r serverid -s saltid
            删服: python ops_manage.py game -a delete -r serverid 
        """
    # 获取操作类型
    if len(sys.argv) == 1:
        print(usage)
        sys.exit(1)
    options = get_options()
    target = sys.argv[1]
    # 日志
    # log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs', time.strftime("%Y-%m-%d", time.localtime()), target)
    # if not os.path.exists(log_dir):
    #     os.makedirs(log_dir)
    # log_file = os.path.join(log_dir, options.action + time.strftime("%Y%m%d_%H%M%S", time.localtime()) + '.log')
    # logger = log(log_file, reload=True)
    log_file = init_logger(options.action)
    logger = log(log_file, reload=True)
    # 实例化
    mysql = MysqlManage(mysqlcfg['host'], mysqlcfg['port'], mysqlcfg['user'], mysqlcfg['passwd'], logger)
    # 获取游服id
    serverid = id_range(options.serverid)
    logger.info('开始执行任务...')
    print('开始执行任务task:{} range:[{}]\nlogfile:{}'.format(options.action, options.serverid, log_file))
    # 刷新区服配置表
    # logger.info('刷新区服配置表...')
    # cmd = 'cd /data/gitlab/oam-admin/a8h5/salt_sh_dir && sh saltgamelist2.sh && sh saltgamelist.sh'
    # out, err, ret = shell_run(cmd)
    # if ret:
    #     print('刷新区服配置表报错,请检查...err:{}'.format(err))
    #     logger.error('刷新区服配置表报错,,请检查...err:{}'.format(err))
    #     sys.exit(1)
    # 实例化
    # mysql = MysqlManage(mysqlcfg['host'], mysqlcfg['port'], mysqlcfg['user'], mysqlcfg['passwd'], logger)
    # api_mysql = MysqlManage(api_mysqlcfg['host'], api_mysqlcfg['port'], api_mysqlcfg['user'], api_mysqlcfg['passwd'], logger)
    runner = SaltAsync(logger)
    # 检查区服是否对外, 热更不检查
    # if not options.version or 'hotfix' not in options.version:
    #    logger.info('检查区服是否对外...')
    #    status_check(serverid, api_mysql)
    # 更新minion脚本
    if options.saltid:
        saltid_list = []
        saltid = salt_name + options.saltid
        saltid_list.append(saltid)
        logger.info('更新minion脚本...')
    else:
        saltid_list = saltid_range(serverid, mysql)
        logger.info('更新minion脚本...')
    if saltid_list:
        update_minion_script(saltid_list, mysql, runner, logger)
    else:
        logger.info("获取saltid失败!请检查{}服是否存在！".format(serverid))
        print("获取saltid失败！请检查{}服是否存在！".format(serverid))
        sys.exit(1)
    # 根据操作类型执行对应方法
    if target == 'game':
        game = GameManage(serverid, options.action, logger, runner, mysql)
        if options.opentime:
            logger.info('执行任务task:{} opentime:{} range:[{}]  time:{}'.format(options.action, options.opentime, options.serverid, datetime.datetime.now().strftime("%Y%m%d_%H%M%S.%f")))
            game.manage(opentime=options.opentime)
        elif options.version:
            if options.action == 'update':
                logger.info('执行任务task:{} version:{} range:[{}]  time:{}'.format(options.action, options.version, options.serverid, datetime.datetime.now().strftime("%Y%m%d_%H%M%S.%f")))
                unzip_package(options.version, logger)
                logger.info('同步package...')
                update_minion_package(saltid_list, options.version, mysql, runner, logger, timeout=600)
                game.manage(version=options.version, timeout=180)
        elif options.saltid:
            logger.info('执行任务task:{}  range:[{}]  time:{}'.format(options.action, options.saltid, options.serverid, datetime.datetime.now().strftime("%Y%m%d_%H%M%S.%f")))
            game.manage(saltid=options.saltid)
        else:
            logger.info('执行任务task:{}  range:[{}]  time:{}'.format(options.action, options.serverid, datetime.datetime.now().strftime("%Y%m%d_%H%M%S.%f")))
            game.manage(timeout=600)
            if options.action == 'stop':
                time.sleep(60)
    end = time.time()
    print('本次任务结束,耗时{}s...'.format(round(end - start, 3)))
    logger.info('本次任务结束,耗时{}s...'.format(round(end - start, 3)))


if __name__ == '__main__':
    main()
