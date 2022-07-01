import subprocess
from celery_task.celery_app import app
from threading import Timer


def runner(cmd, timeout=300):
    """
    基本运行
    :param cmd: 命令
    :param timeout: 超时
    :return: 结果，错误信息，状态码
    """
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    timer = Timer(timeout, lambda x: x.terminate(), [p])
    timer.daemon = True
    timer.start()
    out, err = p.communicate()
    out.decode('GBK')
    err = err.decode('GBK')
    if "Python 3.6 is no longer supported by the Python core team." in err:
        err = ""
    status = p.returncode
    if status == -15:
        return "{cmd}命令超过{timeout}秒未返回".format(timeout=timeout, cmd=cmd)
    timer.cancel()
    return out, err, status


# ---------------------------------------执行本地命令-----------------------------------------------
# 执行本地命令
@app.task()
def cmd_run_local(cmd, cmd_name="", need_raise=False, timeout=300):
    """
    本地命令运行
    :param cmd: 命令
    :param cmd_name: 命令命名
    :param need_raise: 是否抛出错误
    :param timeout: 超时
    :return:
    """
    out, err, status = runner(cmd, timeout=timeout)
    out = out.strip()
    ret = {
        "cmd_name": cmd_name,
        "cmd": cmd,
        "err": err,
        "out": out,
        "status": status
    }
    if need_raise and ret['status'] != 0:
        raise Exception("{cmd_name}错误:\n{out}\b{err}".format(cmd_name=cmd_name, out=ret['out'], err=ret['err']))
    return ret


# -------------------------------------------执行salt命令---------------------------------------
# def get_cmd_values(section, option):
#     """
#     根据传入的section获取对应的value
#     :param section: ini配置文件中用[]标识的内容
#     :param option: 键
#     :return:
#     """
#     return ""
#
#
# def salt_make_cmd(target, cmd, run_type="sync"):
#     """
#     命令组装、防止冲突
#     :param target:
#     :param cmd:
#     :param run_type:
#     :return:
#     """
#     base = get_cmd_values("salt", "base")
#
#     if cmd.find("'") != -1:
#         cmd = cmd.replace('"', '\\"')
#         cmd = get_cmd_values("salt", run_type + "_").format(**locals())
#     else:
#         cmd = cmd.replace("'", "\\'")
#         cmd = get_cmd_values('salt', run_type).format(**locals())
#     return cmd


# salt同步命令
@app.task()
def salt_sync_run(target, cmd, cmd_name="", need_raise=False, time_out=300):
    """
    salt同步命令
    :param target: 目标salt_id
    :param cmd: 命令
    :param cmd_name: 命令命名
    :param need_raise: 是否抛出错误
    :param time_out: 超时
    :return:
    """
    print("salt同步命令")
    # cmd = salt_make_cmd(target, cmd, run_type='sync')
    # out, err, status = runner(cmd, time_out)


# salt异步命令
def salt_async_run(target, cmd):
    print("salt异步命令")


# salt异步结果查询
@app.task()
def salt_get_result(target, jid):
    print("salt异步结果查询")
