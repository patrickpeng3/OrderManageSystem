#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@Author: pengguanghong
@Date  : 2022/04/20
@Desc  :
@Prepare : pip install
@Note  :
"""
# 标准库模块
import sys

from base import *

# 自定义模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ..tool.db.mysql_manage import MysqlManage
from ..tool.runlog.runlog import log
from ..tool.run_cmd.shell_cmd import shell_run

# 获取server_id列表
server_id = sys.argv[1]
server_id = server_id.strip("[")
server_id = server_id.strip("]")
server_id = server_id.split(", ")

# 日志
logger = log(init_logger("clb"), reload=True)
# 实例化数据库
mysql = MysqlManage(mysqlcfg['host'], mysqlcfg['port'], mysqlcfg['user'], mysqlcfg['passwd'], logger)


# 查询负载均衡剩余可创建监听器数
def clb_avail_num(clb_name):
    mysql.execute(mysqlcfg['clbnum'].format(clb_name))
    clb_num = mysql.fetchall()[0][0]
    total_avail_num = 0
    avail_num_dict = {}
    for i in range(1, clb_num + 1):
        clb_name_game = clb_name + str(i)
        cmd = "python3 {clb_manage} listener -a count -n {clb_name_game}".format(
            clb_manage=clb_manage,
            clb_name_game=clb_name_game
        )
        ret = shell_run(cmd)
        if ret[2] != 0:
            logger.info("查询{}监听器数量失败！".format(clb_name_game))
            print("查询{}监听器数量失败！".format(clb_name_game))
            sys.exit(1)
        avail_num = 200 - int(ret[0].split("\n", 2)[1])
        total_avail_num = total_avail_num + avail_num
        avail_num_dict[clb_name_game] = avail_num
    else:
        avail_num_dict['total_avail_num'] = total_avail_num
    return avail_num_dict, clb_num


# 判断是否需要购买负载均衡
def need_add_clb(server_id, clb_name_list):
    for clb_name in clb_name_list:
        total_avail_num = clb_avail_num(clb_name)[0]['total_avail_num']
        clb_num = clb_avail_num(clb_name)[1]
        # 需购买负载均衡
        if len(server_id) > total_avail_num:
            add_clb_num = divmod(len(server_id) - total_avail_num, 200)[0] + 1
            for i in range(clb_num + 1, clb_num + add_clb_num + 1):
                clb_name_game = clb_name + str(i)
                add_clb(clb_name_game)
                mysql.execute(mysqlcfg['add_clb'].format(i, clb_name))
        else:
            print("{}无需购买负载均衡".format(clb_name))


# 购买负载均衡和解析
def add_clb(clb_name):
    # 购买
    cmd = "python3 {clb_manage} clb -a add -n {clb_name} -t {net_type} -f {forward} -v {vpc_id} -p {project_id}".format(
        clb_manage=clb_manage,
        clb_name=clb_name,
        net_type=net_type,
        forward=forward,
        vpc_id=vpc_id,
        project_id=project_id
    )
    ret = shell_run(cmd)
    if ret[2] != 0:
        logger.info("新增{}负载均衡失败!".format(clb_name))
        print("新增{}负载均衡失败!".format(clb_name))
        sys.exit(1)
    # 查询clb_ip
    cmd = "python3 {clb_manage} clb -a select -n {clb_name}".format(
        clb_manage=clb_manage,
        clb_name=clb_name
    )
    ret = shell_run(cmd)
    if ret[2] != 0:
        logger.info("查询负载均衡ip失败！")
        print("查询负载均衡ip失败！")
        sys.exit(1)
    clb_ip = ret[0].split("\n", 2)[0]
    # 解析
    cmd = "python3 {domain} -a -o sh9130.com -r {clb_name} -v {clb_ip}".format(
        domain=domain,
        clb_name=clb_name,
        clb_ip=clb_ip
    )
    ret = shell_run(cmd)
    if ret[2] != 0:
        logger.info("解析clb失败！")
        print("解析clb失败！")
        sys.exit(1)


# 生成负载均衡监听器配置
def get_clb_cfg(server_id, clb_name_list):
    # server_id排序
    for num in range(len(server_id)):
        for index in range(len(server_id) - 1 - num):
            if server_id[index] > server_id[index + 1]:
                server_id[index], server_id[index + 1] = server_id[index + 1], server_id[index]
    for clb_name in clb_name_list:
        # 获取专服下的id列表
        special_id_list = []
        for _id in server_id:
            clb = SerType(_id)[1]
            if clb == clb_name:
                special_id_list.append(_id)
        clb_num = clb_avail_num(clb_name)[1]
        for i in range(1, clb_num + 1):
            # 获取clb剩余可用监听器数量
            clb_name_game = clb_name + str(i)
            avail_num = int(clb_avail_num(clb_name)[0][clb_name_game])
            avail_group = divmod(avail_num, 50)[0]
            # 创建负载均衡监听器
            for g in range(avail_group):
                if special_id_list:
                    id_list = special_id_list[:50]
                    clb_port_list, server_host_list = [[] for i in range(2)]
                    for _id in id_list:
                        mysql.execute(mysqlcfg['server_host'].format(_id))
                        server_host = mysql.fetchall()[0][0]
                        if int(_id) > 65535:
                            clb_port = divmod(int(_id), 50000)[0] + 10000
                        else:
                            clb_port = int(_id)
                        clb_port_list.append(clb_port)
                        server_host_list.append(server_host)
                    listener_range = ":".join("%s" % d for d in clb_port_list)
                    # 创建负载均衡监听器
                    create_clb_listener(clb_name_game, listener_range)
                    # 查询nginx端口
                    print(id_list)
                    if len(id_list) == 1:
                        mysql.execute(mysqlcfg['nginx_port_one'].format(tuple(id_list)[0]))
                    else:
                        mysql.execute(mysqlcfg['nginx_port_many'].format(tuple(id_list)))
                    nginx_port_tuple = mysql.fetchall()
                    nginx_port_list = []
                    for j in range(len(nginx_port_tuple)):
                        nginx_port_list.append(nginx_port_tuple[j][0])
                    # 绑定后端
                    bind_backend(clb_name_game, listener_range, server_host_list, nginx_port_list)
                    # 更新special_id_list
                    special_id_list = list(set(special_id_list) - set(id_list))
                    # 修改数据库游服clb信息
                    if len(id_list) == 1:
                        mysql.execute(mysqlcfg['clbname_one'].format(clb_name_game, tuple(id_list)[0]))
                    else:
                        mysql.execute(mysqlcfg['clbname_many'].format(clb_name_game, tuple(id_list)))
                else:
                    break


# 创建负载均衡监听器
def create_clb_listener(clb_name, listener_range):
    cmd = "python3 {clb_manage} listener -a batchcreate -n {clb_name} -r {listener_range}".format(
        clb_manage=clb_manage,
        clb_name=clb_name,
        listener_range=listener_range
    )
    ret = shell_run(cmd)
    if ret[2] != 0:
        logger.info("创建负载均衡监听器失败！")
        print("创建负载均衡监听器失败！")
        sys.exit(1)


# 绑定后端
def bind_backend(clb_name, listener_range, server_host_list, server_port_list):
    cmd = 'python3 {clb_manage} batchbind -a batchbind -n {clb_name} -r {listener_range} -b "{server_host}" -P "{server_port}"'.format(
        clb_manage=clb_manage,
        clb_name=clb_name,
        listener_range=listener_range,
        server_host=server_host_list,
        server_port=server_port_list
    )
    ret = shell_run(cmd)
    if ret[2] != 0:
        logger.info("负载均衡绑定后端失败！")
        print("负载均衡绑定后端失败！")
        sys.exit(1)


def main():
    print("server_id = {}".format(list(server_id)))
    clb_name_list, not_exist_id = [[] for i in range(2)]
    # 检查游服是否存在
    for _id in server_id:
        mysql.execute(mysqlcfg['check_game'].format(_id))
        exist = mysql.fetchall()[0][0]
        if exist != 1:
            not_exist_id.append(_id)
    if not_exist_id:
        logger.info("{}服不存在，请检查！".format(not_exist_id))
        print("{}服不存在，请检查！".format(not_exist_id))
        sys.exit(1)
    # 查询专服负载均衡信息
    for _id in server_id:
        clb_name = SerType(_id)[1]
        clb_name_list.append(clb_name)
    clb_name_list = list(set(clb_name_list))
    # 绑定负载均衡
    need_add_clb(server_id, clb_name_list)
    get_clb_cfg(server_id, clb_name_list)


if __name__ == '__main__':
    main()
