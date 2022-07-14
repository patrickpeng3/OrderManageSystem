from apps.hls.packages.server import get_cmd
from job_manager.packages.easy_tools import job_start_before, task_runner_celery
from cmdb_hls.cmdb_logger import SCRIPT_LOGGER


def create_entry(username, special, number):
    """
    搭服
    :param username: 执行者
    :param special: 专服名
    :param number: 搭服数量
    :return:
    """
    cmd_list = []
    get_cmd.create_game(special, number, cmd_list)
    job_task, job_cmds = job_start_before("搭服", username, create_entry, cmd_list)
    return task_runner_celery(job_task, job_cmds)


def update_entry(username, server_id, version):
    """
    更新
    :param username: 执行者
    :param server_id: 游服id
    :param version: 更新版本
    :return:
    """
    cmd_list = []
    get_cmd.update_game(server_id, version, cmd_list)
    job_task, job_cmds = job_start_before("更新", username, update_entry, cmd_list)
    return task_runner_celery(job_task, job_cmds)


def start_entry(username, server_id):
    """
    启服
    :param username: 执行者
    :param server_id: 游服id
    :return:
    """
    cmd_list = []
    get_cmd.start_game(server_id, cmd_list)
    job_task, job_cmds = job_start_before("启服", username, start_entry, cmd_list)
    return task_runner_celery(job_task, job_cmds)


def stop_entry(username, server_id):
    """
    停服
    :param username: 执行者
    :param server_id: 游服id
    :return:
    """
    cmd_list = []
    get_cmd.stop_game(server_id, cmd_list)
    SCRIPT_LOGGER.info("命令列表：{}".format(cmd_list))
    job_task, job_cmds = job_start_before("停服", username, stop_entry, cmd_list)
    return task_runner_celery(job_task, job_cmds)


def delete_entry(username, server_id):
    """
    删服
    :param username: 执行者
    :param server_id: 游服id
    :return:
    """
    cmd_list = []
    get_cmd.stop_game(server_id, cmd_list)
    job_task, job_cmds = job_start_before("启服", username, delete_entry, cmd_list)
    return task_runner_celery(job_task, job_cmds)
