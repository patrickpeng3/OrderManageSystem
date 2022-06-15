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
import datetime
import json
import os
import sys
import time

start = time.time()
starttime = datetime.datetime.now()

# 自定义模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from runlog import log

log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),'logs',time.strftime("%Y-%m-%d", time.localtime()))
log_file = os.path.join(log_dir,os.path.basename(os.path.abspath(__file__))+time.strftime("%H%M%S", time.localtime())+'.log')

log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs',
                       time.strftime("%Y-%m-%d", time.localtime()))
log_file = os.path.join(log_dir, os.path.basename(os.path.abspath(__file__)).split('.')[0] + '.log')

if not os.path.exists(log_dir):
    os.makedirs(log_dir)
logger = log(log_file)
logger.info('log by {name}'.format(name='dengjm'))
logger.error('log by {name}'.format(name='error'))
#
# endtime = datetime.datetime.now()
# end = time.time()
#
# print((endtime - starttime).seconds)
# print(round(end-start,2))
# print(os.path.dirname(os.path.abspath(__file__)))
# print(os.path.basename(__file__))

# a = '4_5'
# b = []
# for i in a.split(':'):
#     if '_' not in i:
#         b.append(int(i))
#     else:
#         begin = int(i.split('_')[0])
#         end = int(i.split('_')[1])
#         for j in range((end - begin) + 1):
#             c = begin + j
#             b.append(c)
# #print(b)
# for i in b:
#     exec('var{} = {}'.format(i, i))
#     #exec(print('var{}'.format(i)))
#     exec('print(var{}, end=" ")'.format(i))
