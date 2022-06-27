from celery_task.celery_app import app
from job_manager.models import JobTask, JobCmd
from job_manager.packages.job_cmd_run import cmd_run
import time


def job_start_before(name, username, fun, cmds, serial=''):
    """
    :param name: 任务名
    :param username: 执行者
    :param fun: 函数名
    :param parames: 参数
    :param cmd: 命令
    :param serial: 串行标识
    :return:
    """
    job_info = {
        "name": name,
        "username": username,
        # "parames": parames,
        "function_name": fun.__name__,
        "status": "waiting",
        "serial": serial
    }
    job_task = JobTask.objects.create(**job_info)
    job_cmds = []
    for cmd in cmds:
        job_cmd = JobCmd.objects.create(
            cmd=cmd,
            # run_type=cmd_info['run_type'],
            status="waiting",
            job_task=job_task,
        )
        job_cmds.append({
            "model": job_cmd,
        })
    return job_task, job_cmds


@app.task()
def task_runner_celery(job_task, job_cmds, serial=None):
    """
    :param job_task: 任务队列模型
    :param job_cmds: 任务命令信息
    :param serial: 串行
    :return: 错误信息或None
    """
    error = None
    status = "success"
    serial = serial
    out, error = cmd_run(job_cmds["model"].cmd)
    print("out:{}".format(out))
    print("error:{}".format(error))
    return out, error
