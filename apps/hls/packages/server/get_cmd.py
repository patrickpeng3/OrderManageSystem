from config.project.get_config import get_hls_config
from cmdb_hls.settings import SCRIPT_BASE_DIR


class GetCmdBase(object):
    def __init__(self):
        self.master_script_dir = get_hls_config("base", "master_scripts_dir").format(cmdb_script_base_dir=SCRIPT_BASE_DIR)

    def get_one_cmd_info(self, section, option, run_type='local', add_string="", out_check=None,
                         check_params=None, ignore_error=None, **params):
        """
        :param section: ini配置文件中用[]标识的内容
        :param option: 键
        :param run_type: 命令类型
        :param add_string: 增加的字符
        :param out_check: 输出检查方法
        :param check_params: 检查方法参数
        :param ignore_error:
        :param params: cmd参数
        :return:
        """
        params.update({
            "master_scripts_dir": self.master_script_dir
        })
        cmd = get_hls_config(section, option).format(**params)
        return {
            "cmd": cmd,
            "run_type": run_type,
            "add_string": add_string,
            "out_check": out_check,
            "check_params": check_params,
            "ignore_error": ignore_error
        }


def create_game(special, number, cmd_list):
    """
    创服
    :param special: 专服名
    :param number: 搭服数量
    :param cmd_list: 命令列表
    :return:
    """
    cmd_base = GetCmdBase()
    cmd_list.append(cmd_base.get_one_cmd_info("master", "create_game", special=special, number=number))


def update_game(server_id, version, cmd_list):
    """
    更新
    :param server_id: 游服id
    :param version: 后端版本
    :param cmd_list: 命令列表
    :return:
    """
    cmd_base = GetCmdBase()
    cmd_list.append(cmd_base.get_one_cmd_info("master", "update_game", server_id=server_id, version=version))


def start_game(server_id, cmd_list):
    """
    启服
    :param server_id: 游服id
    :param cmd_list: 命令列表
    :return:
    """
    cmd_base = GetCmdBase()
    cmd_list.append(cmd_base.get_one_cmd_info("master", "start_game", server_id=server_id))


def stop_game(server_id, cmd_list):
    """
    停服
    :param server_id: 游服id
    :param cmd_list: 命令列表
    :return:
    """
    cmd_base = GetCmdBase()
    cmd_list.append(cmd_base.get_one_cmd_info("master", "stop_game", server_id=server_id))


def delete_game(server_id, cmd_list):
    """
    停服
    :param server_id: 游服id
    :param cmd_list: 命令列表
    :return:
    """
    cmd_base = GetCmdBase()
    cmd_list.append(cmd_base.get_one_cmd_info("master", "delete_game", server_id=server_id))
