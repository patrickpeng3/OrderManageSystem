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
import subprocess
import sys
import time

# 第三方模块

# 自定义模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ..runlog.runlog import log

def shell_run(cmd):
    subp = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True)
    # print(subp.pid)
    # subp.wait()
    out, err = subp.communicate()
    # out = out.strip()
    return out, err, subp.returncode



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
    # print(options)
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs',
                           time.strftime("%Y-%m-%d", time.localtime()))
    log_file = os.path.join(log_dir, os.path.basename(__file__).split('.')[0] + '.log')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    logger = log(log_file)
    print(shell_run('date && sleep 1 && date'))
    logger.info(shell_run('date && sleep 1 && date'))