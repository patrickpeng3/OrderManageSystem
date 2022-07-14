# -*- coding: utf-8 -*-
import time
import traceback
from django.db import transaction
from cmdb_hls.cmdb_logger import SCRIPT_LOGGER
from celery_task.celery_app import app
from celery.result import allow_join_result
from job_manager.models import JobTask, JobCmd
from job_manager.cmd_runner.cmd_run_celery import cmd_run_local, salt_sync_run, salt_async_run, salt_get_result


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
    with transaction.atomic():
        job_task = JobTask.objects.create(**job_info)
        job_cmds = []
        for cmd_info in cmds:
            job_cmd = JobCmd.objects.create(
                cmd=cmd_info['cmd'],
                run_type=cmd_info['run_type'],
                status="waiting",
                job_task=job_task,
            )
            job_cmds.append({
                "model": job_cmd,
                "out_check": cmd_info['out_check'],
                "check_params": cmd_info['check_params'],
                "ignore_error": cmd_info.get('ignore_error'),
            })
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
    JobCmd.objects.filter(id=job_cmd.id).update(
        status="failed",
        end_time=int(time.time()),
        error=error,
        out=out
    )


def job_cmd_run(job_cmd_info, target=None):
    """
    执行命令
    :param job_cmd_info: 任务命令信息
    :param target: 目标(非salt命令不用传)
    :return:
    """
    job_cmd = job_cmd_info['model']
    if job_cmd.run_type != 'local' and target is None:
        job_cmd_failed(job_cmd, error="salt命令必须传入target参数", out=None)
        raise Exception("salt命令必须传入target参数")
    error = None
    out = None
    try:
        # 更新命令信息
        JobCmd.objects.filter(id=job_cmd.id).update(
            start_time=int(time.time()),
            status="running"
        )
        # 本地命令
        if job_cmd.run_type == 'local':
            res = cmd_run_local(job_cmd.cmd)
        # salt同步
        elif job_cmd.run_type == 'salt_sync':
            res = salt_sync_run(target, job_cmd.cmd)
        # salt异步
        else:
            jid = salt_async_run(target, job_cmd.cmd)
            JobCmd.objects.filter(id=job_cmd.id).update(jid=jid)
            # 15秒重试一次，重试30次
            for i in range(30):
                res = salt_get_result(target, jid)
                if res == '没有返回结果':
                    pass
                else:
                    break
            else:
                raise Exception("命令尝试多次查询没有返回结果,{jid}".format(jid=jid))
        out = res['out']
        # 错误处理
        if job_cmd_info.get('ignore_error') is None:
            error = res['err']
            if error:
                raise Exception("包含错误输出行")
        else:
            out += "\n{}".format(res['err'])
        # 状态码检查
        if res['status'] != 0:
            raise Exception("检查到命令执行状态码不为0")
        # 执行结果处理
        if job_cmd_info.get('out_check') is not None:
            job_cmd_info['check_params']['out'] = out
            if job_cmd_info['out_check'](**job_cmd_info['check_params']) is False:
                error = out
                raise Exception("未通过结果检查方法")
        # 更新命令执行状态
        job_cmd_success(job_cmd, out)
        print("err = {}".format(error))
    except Exception as e:
        if not error:
            error = traceback.format_exc()
        job_cmd_failed(job_cmd, error=error, out=out)
    finally:
        return out, error


# ------------------------------------------celery任务-----------------------------------------------
@app.task()
def task_runner_celery(job_task, job_cmd_infos, serial=None):
    """
    :param job_task: 任务队列模型
    :param job_cmd_infos: 任务命令信息
    :param serial: 串行
    :return: 错误信息或None
    """
    error = None
    # status = "success"
    serial = serial
    try:
        job_task_start(job_task)
        for job_cmd_info in job_cmd_infos:
            with allow_join_result():
                out, error = job_cmd_run(job_cmd_info)
            if error:
                print("shell_run_error：{}".format(error))
        job_task_finished(job_task)
    except Exception as e:
        if error is None:
            error = traceback.format_exc()
        job_task_interrupt(job_task, error)
        # status = "error"
    finally:
        async_runner.delay(job_task_confirm, job_task)
        status = select_runner_result(job_task)
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


@app.task()
def select_runner_result(job_task, time_check=15):
    """
    任务执行结果查询
    :param job_task: 任务队列模型
    :param time_check: 查询间隔
    :return:
    """
    # 每隔15秒查询一次，共查询12次，耗时3分钟
    status = "failed"
    for i in range(12):
        time.sleep(time_check)
        task = JobTask.objects.filter(id=job_task.id)[0]
        if task:
            j_cmd = JobCmd.objects.filter(job_task_id=job_task.id)[0]
            if str(task.status) == "finished" and str(j_cmd.status) == "success":
                status = "success"
            else:
                status = "failed"
            SCRIPT_LOGGER.info("task_status：{}\ncmd_status：{}".format(task.status, j_cmd.status))
            SCRIPT_LOGGER.info("任务执行结果：{}".format(status))
            break
    return status
