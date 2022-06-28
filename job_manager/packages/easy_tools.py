import time
import traceback

from celery_task.celery_app import app
from job_manager.models import JobTask, JobCmd
from job_manager.packages.job_cmd_run import cmd_run
from celery.result import allow_join_result


# ---------------------------------------任务执行前，初始化任务、命令模型-----------------------------------------------
def job_start_before(name, username, fun, cmds, serial=''):
    """
    :param name: 任务名
    :param username: 执行者
    :param fun: 函数名
    :param parames: 参数
    :param cmd: 命令
    :param serial: 串行标识
    :return: job_task, job_cmds 模型
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
    print(job_cmds)
    return job_task, job_cmds


# ------------------------------------------任务队列模型-----------------------------------------------
def job_task_start(job_task):
    """
    任务开始
    :param job_task: 任务队列模型
    :return:
    """
    JobTask.objects.filter(id=job_task.id).update(
        status="running",
        start_time=int(time.time())
    )


def job_task_finished(job_task):
    """
    任务完成
    :param job_task: 任务队列模型
    :return:
    """
    JobTask.objects.filter(id=job_task.id).update(
        status="finished",
        end_time=int(time.time())
    )


def job_task_interrupt(job_task, error):
    """
    任务中断
    :param job_task: 任务队列模型
    :param error: 错误信息
    :return:
    """
    JobTask.objects.filter(id=job_task.id).update(
        status="interrupt",
        end_time=int(time.time()),
        error=error
    )


def job_task_confirm(job_task):
    """
    任务确认
    :param job_task: 任务队列模型
    :return:
    """
    time.sleep(30)
    JobTask.objects.filter(id=job_task.id).update(
        confirm=True
    )


def job_task_serial_waiting(job_task, serial):
    """
    任务串行
    :param job_task: 任务队列模型
    :param serial: 串行标识
    :return:
    """
    try:
        if serial:
            while all([
                JobTask.objects.filter(serial=serial, confirm=False).count() > 1,
                JobTask.objects.filter(serial=serial, confirm=False).first().id != job_task.id
            ]):
                time.sleep(5)
    except Exception:
        traceback.print_exc()


# ------------------------------------------任务命令模型-----------------------------------------------
def job_cmd_success(job_cmd, out=None):
    """
    命令成功
    :param job_cmd: 任务命令模型
    :param out: 输出
    :return:
    """
    JobCmd.objects.filter(id=job_cmd.id).update(
        status="success",
        end_time=int(time.time()),
        out=out
    )


def job_cmd_failed(job_cmd, error=None, out=None):
    """
    命令失败
    :param job_cmd: 任务命令模型
    :param error: 错误信息
    :param out: 输出
    :return:
    """


# ------------------------------------------celery任务-----------------------------------------------
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
    try:
        job_task_start(job_task)
        for job_cmd in job_cmds:
            with allow_join_result():
                out, error = cmd_run(job_cmd)
            if error:
                print("shell_run_error：{}".format(error))
        job_task_finished(job_task)
    except Exception as e:
        if error is None:
            error = traceback.format_exc()
        job_task_interrupt(job_task, error)
        status = "error"
    finally:
        async_runner.delay(job_task_confirm, job_task)
        return status


@app.task()
def async_runner(async_fun, *args, **kwargs):
    """
    异步任务
    :param async_fun: 要异步执行的函数
    :param args: 参数
    :param kwargs: 参数
    :return:
    """
    with allow_join_result():
        async_fun(*args, **kwargs)
