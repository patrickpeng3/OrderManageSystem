from config.project.get_config import get_hls_config
from cmdb_hls.settings import SCRIPT_BASE_DIR


class GetCmdBase(object):
    def __init__(self):
        self.master_script_dir = get_hls_config("base", "master_scripts_dir").format(cmdb_script_base_dir=SCRIPT_BASE_DIR)

    def get_one_cmd_info(self, section, option, **params):
        """
        :param section: ini配置文件中用[]标识的内容
        :param option: 键
        :param params: cmd参数
        :return:
        """
        params.update({
            "master_scripts_dir": self.master_script_dir
        })
        cmd = get_hls_config(section, option).format(**params)
        return cmd


def create_game(server_id, salt_id):
    cmd_base = GetCmdBase()
    cmd = cmd_base.get_one_cmd_info("master", "create_game", server_id=server_id, salt_id=salt_id)


def update_game(server_id, version, cmd_list):
    cmd_base = GetCmdBase()
    cmd_list.append(cmd_base.get_one_cmd_info("master", "update_game", server_id=server_id, version=version))
