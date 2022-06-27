# -*- coding: UTF-8 -*-
import configparser
import os
from cmdb_hls.settings import CONFIG_BASE_DIR


def get_config_base(witch, section, option, name='config.ini'):
    """
    获取配置
    :param witch: 哪个项目
    :param section: 选项
    :param option: 键
    :param name: 文件名
    :return:
    """
    # BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    src = os.path.join(CONFIG_BASE_DIR, 'project', witch, name)
    config = configparser.RawConfigParser()
    config.read(src)
    return config.get(section=section, option=option)


def get_env_config(section, option):
    """
    获取环境配置
    :param section: ini配置文件中用[]标识的内容
    :param option: 键
    :return:
    """
    env_map = {
        'hls': {
            'api': 'hls',
            'script': 'hls',
            'mail': 'hls',
        },
    }
    value = get_config_base('common', section, option, name='env.ini')
    if section == 'base' and option == 'project':
        return env_map[value]
    else:
        return value


def get_hls_config(section, option):
    """
    :param section: ini配置文件中用[]标识的内容
    :param option: 键
    :return:
    """
    return get_config_base("hls", section, option)
