#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Author: dengjm
@Date  : 2020/12/22
@Desc  :
@Prepare :
@Note  :
"""

import logging

def log(file, reload=False):

    #创建logger，如果参数为空则返回root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  #设置logger日志等级

    #这里进行判断，如果logger.handlers列表为空，则添加，否则，直接去写日志
    # print(logger.handlers)
    if not logger.handlers or reload is True:
        logger.handlers = []
        # 创建控制台 console handler
        ch = logging.StreamHandler()
        # 设置控制台输出时的日志等级
        ch.setLevel(logging.WARNING)

        # 创建文件 handler
        fh = logging.FileHandler('{file}'.format(file=file),encoding='utf-8')
        # 设置写入文件的日志等级
        fh.setLevel(logging.INFO)

        #设置输出日志格式
        formatter = logging.Formatter(
            fmt='%(asctime)s %(levelname)s %(filename)s %(message)s'
            )

        #为handler指定输出格式
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        #为logger添加到日志处理器logger
        # logger.addHandler(ch)
        logger.addHandler(fh)

    return logger #直接返回logger

"""
if __name__ == '__main__':
    logger = log('../logs/20210101/tt.log')
    logger.warning('警告')
    logger.info('提示')
    logger.error('错误')
    logger.debug('查错')
"""