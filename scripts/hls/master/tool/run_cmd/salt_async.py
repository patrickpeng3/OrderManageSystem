#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Author: dengjm
@Date  : 2020/12/22
@Desc  : 
@Prepare : pip install 
@Note  : 查询jid结果需salt配置缓存到MySQL
"""

# 标准库模块
import argparse
import json
import jsonpath
import os
import sys
import time

# 第三方模块
import salt.client

# 自定义模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ..db.mysql_manage import MysqlManage
from ..runlog.runlog import log

class SaltAsync(object):

    def __init__(self, logger):
        self.client = salt.client.LocalClient()
        self.mysql_host = '127.0.0.1'
        self.mysql_port = 3306
        self.mysql_user = 'root'
        self.mysql_passwd = 'dkmwebmysql!q$EWQ23FD23'
        self.logger = logger

    def async_cmd(self, host, cmd, jid):
        """
        异步执行远程命令
        :param host: salt主机
        :param cmd:  远程命令
        :param jid:  自定义jid
        :return: jid
        """
        cmd_list = []
        cmd_list.append(cmd)
        # self.logger.info('开始执行异步任务{host}--{cmd}'.format(host=host, cmd=cmd))
        jid = self.client.cmd_async(host, 'cmd.run', cmd_list, jid=jid)
        return jid

    def jid_sql(self, jid_tuple):
        """
        组建jid查询sql
        :param jid_tuple: 任务id
        :return: sql
        """
        if len(jid_tuple) == 1:
            sql = 'select full_ret from salt.salt_returns where jid = "{}";'.format(jid_tuple[0])
        else:
            sql = 'select full_ret from salt.salt_returns where jid in {};'.format(jid_tuple)
        # print(sql)
        return sql

    def jid_return(self, jid_tuple, sql, salt_version, log=True):
        """
        查看异步任务结果
        :param jid_tuple: 任务id
        :param sql: jid_sql函数返回的jid查询sql
        :param salt_version:
        :param log: 是否打印日志,默认打印
        :return:
        """
        mysql = MysqlManage(self.mysql_host, self.mysql_port, self.mysql_user, self.mysql_passwd, self.logger)
        mysql.execute(sql)
        result = mysql.fetchall()
        result_list = []
        for each in list(result):
            # print(json.loads(''.join(each)))
            result_list.append(json.loads(''.join(each)))
        # self.logger.info(result_list)
        jid_set = set(jid_tuple)
        jid_finish_set = set()
        jid_success_set = set()
        jid_fail_set = set()
        for jid in list(jid_tuple):
            for result in result_list:
                if result['jid'] == jid:
                    if result['retcode'] == 0:
                        # print('jid:{},task:{} succeed'.format(result['jid'], result['fun_args']))
                        if log:
                            if salt_version == 2019:
                                # salt2019
                                self.logger.info('saltid:{},jid:{},code:{},status:{},return:{}'.format(result['id'], result['jid'], result['retcode'], result['success'], result['return']))
                            elif salt_version > 2019:
                                # salt3000
                                self.logger.info('saltid:{},jid:{},task:{},code:{},status:{},return:{}'.format(result['id'], result['jid'], result['fun_args'], result['retcode'], result['success'], result['return']))
                        jid_success_set.add(jid)
                    else:
                        # print('jid:{},task:{} fail'.format(result['jid'], result['fun_args']))
                        if log:
                            if salt_version == 2019:
                                # salt2019
                                self.logger.error('saltid:{},jid:{},code:{},status:{},return:{}'.format(result['id'], result['jid'], result['retcode'], result['success'], result['return']))
                            elif salt_version > 2019:
                                # salt3000
                                self.logger.error('saltid:{},jid:{},task:{},code:{},status:{},return:{}'.format(result['id'], result['jid'], result['fun_args'], result['retcode'], result['success'], result['return']))
                        jid_fail_set.add(jid)
                    jid_finish_set.add(jid)
                    break
        jid_unfinish_set = jid_set - jid_finish_set
        return jid_finish_set, jid_success_set, jid_fail_set, jid_unfinish_set, result_list


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
    # options = get_options()
    #print(options)
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs',
                           time.strftime("%Y-%m-%d", time.localtime()))
    log_file = os.path.join(log_dir, os.path.basename(__file__).split('.')[0] + '.log')
    #print(log_file)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    logger = log(log_file, reload=True)
    host = '127.0.0.1'
    port = 3306
    user = 'root'
    passwd = 'dkmwebmysql!q$EWQ23FD23'
    runner = SaltAsync(logger)
    jid_list = []
    # print(runner.async_cmd('ywsg-test', 'pwd', 'jid_pwd'))
    jid_list.append(runner.async_cmd('ywsg-test', 'pwd', 'jid_pwd'))
    jid_list.append(runner.async_cmd('ywsg-test', 'ppd', 'jid_ppd'))
    jid_tuple = tuple(jid_list)
    for i in range(60):
        jid_set = runner.jid_return(jid_tuple)
        if not jid_set[3]:
            break
        else:
            time.sleep(1)
    end = time.time()
    print('{} finish,{} succeed, {} fail, {} unfinish ,spent time {}s'.format(len(jid_set[0]), len(jid_set[1]), len(jid_set[2]) ,len(jid_set[3]), round(end-start,3)))
    logger.info('{} finish,{} succeed, {} fail, {} unfinish ,spent time {}s'.format(len(jid_set[0]), len(jid_set[1]),
                                                                              len(jid_set[2]), len(jid_set[3]),
                                                                              round(end - start, 3)))
