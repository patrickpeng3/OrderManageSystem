import subprocess
from celery_task.celery_app import app


# 执行本地命令
def cmd_run_local(cmd, cmd_name="", need_raise=False):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    status = p.returncode
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


# salt同步命令
def salt_sync_run(target, cmd):
    print("salt同步命令")


# salt异步命令
def salt_async_run(target, cmd):
    print("salt异步命令")


# salt异步结果查询
@app.task()
def salt_get_result(target, jid):
    print("salt异步结果查询")
