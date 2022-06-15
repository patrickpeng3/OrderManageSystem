#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Author: dengjm
@Date  : 2020/12/22
@Desc  : 
@Prepare : pip install mysqlclient
@Note  : 直接调用脚本同时执行多条sql语句时附带参数,参数以空格间隔会自动转为列表，需要额外将列表元素也转为列表
"""

# 标准库模块
import argparse
import json
import jsonpath
import os
import sys
import time

# 第三方模块
#import MySQLdb
import pymysql

# 自定义模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ..runlog.runlog import log

class MysqlManage(object):

    def __init__(self, host, port, user, passwd, logger):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.logger = logger
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd)
            self.cursor = self.conn.cursor()
        except Exception as e:
            raise SystemError("数据库连接失败:{}".format(e))

    def execute(self, sql):
        """
        执行sql，执行异常事务回滚
        :param sql:
        :return:
        """
        try:
            # self.logger.info('执行sql: {}'.format(sql))
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            self.logger.error('错误信息: {}'.format(e))
            self.conn.rollback()

    def executemany(self, sql, param):
        """
        执行sql，执行异常事务回滚
        :param sql:
        :return:
        """
        try:
            # self.logger.info('执行sql: {}'.format(sql))
            self.cursor.executemany(sql, param)
            self.conn.commit()
        except Exception as e:
            self.logger.error('错误信息: {}'.format(e))
            self.conn.rollback()

    def fetchall(self):
        return self.cursor.fetchall()

    def select(self, sql):
        self.execute(sql)
        self.fetchall

    def close(self):
        self.cursor.close()
        self.conn.close()


def get_options():
    usage = """
    python %(prog)s -s host -u user -p passwd -P port -r -S sql [-m param] 
    -s: 数据库host
    -u: 数据库用户
    -p: 数据库密码
    -P: 数据库端口
    -r: 查询开关
    -S: 执行sql语句
    -m: 同时执行多条sql语句时附带参数,参数以空格间隔会自动转为列表，需要额外将列表元素也转为列表
    
    
    查询: python %(prog)s -r -S 'select * from ops.test where id = 1;'
          python %(prog)s -r -S 'select * from ops.test where id = %s;' -m 1 2
    插入: python %(prog)s    -S 'insert into ops.test(id, num) values(%s,%s);' -m 1,1 2,2
    删除: python %(prog)s    -S 'delete from ops.test where id = %s;' -m 1 2
    """
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('-s', '--host', dest='host', default='localhost', help='target host, default: localhost')
    parser.add_argument('-u', '--user', dest='user', default='root', help='target user, default: root')
    parser.add_argument('-p', '--passwd', dest='passwd', default='dkmwebmysql!q$EWQ23FD23', help='target passwd, default: 123456')
    parser.add_argument('-P', '--port', dest='port', default=3306, help='target port, default: 3306')
    parser.add_argument('-r', '--read', action='store_true', help='target sql')
    parser.add_argument('-S', '--sql', dest='sql', required=True, help='target sql')
    parser.add_argument('-m', '--param', dest='param', nargs='+', help='target param')

    option = parser.parse_args()
    return option


if __name__ == '__main__':
    start = time.time()
    options = get_options()
    #print(options)
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs',
                           time.strftime("%Y-%m-%d", time.localtime()))
    log_file = os.path.join(log_dir, os.path.basename(__file__).split('.')[0] + '.log')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    logger = log(log_file)
    mysql = MysqlManage(options.host, options.port, options.user, options.passwd, logger)

    print(options.param)
    if options.param:
        param_list = []
        for i in options.param:
            # print(i)
            # print(list(i.split(',')))
            # param_sublist = []
            # for j in i.split(','):
            #     param_sublist.append(int(j))
            # param_list.append(param_sublist)
            param_list.append(i.split(','))
            # print(param_list)
        # print(options.sql, param_list)
        mysql.executemany(options.sql, param_list)
        if options.read:
            result = mysql.fetchall()
            logger.info(result)
    else:
        mysql.execute(options.sql)
        if options.read:
            result = mysql.fetchall()
            logger.info(result)
    # mysql = MysqlManage('42.194.143.25', 3306, 'root', 'dkmwebmysql!q$EWQ23FD23', logger)
    # sql = 'insert into ops.ttt values(%s)'
    # sql = 'delete from ops.ttt where id = %s'
    # sql = 'select * from ops.ttt where id = %s'
    # param = [[70001], [70000]]
    # mysql.execute(sql)
    # mysql.executemany(sql, param)
    # result = mysql.fetchall()
    # logger.info(result)
    mysql.close()
    end = time.time()
    logger.info('耗时: {}s'.format(round(end-start,3)))
