#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Author: dengjm
@Date  : 2020/12/22
@Desc  : 
@Prepare : pip install 
@Note  : 
"""

# 标准库模块
import argparse
import json
import jsonpath
import os
import sys
import time

# 第三方模块

# 自定义模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from runlog.runlog import log


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
    if len(sys.argv) == 1:
        print(usage)
        sys.exit(1)
    target = sys.argv[1]
    options = get_options()
    #print(options)
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'logs',
                           time.strftime("%Y-%m-%d", time.localtime()))
    log_file = os.path.join(log_dir, os.path.basename(__file__).split('.')[0] + '.log')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    logger = log(log_file)
    clb = ClbManage(access_keyid, access_secret, region, logger)
