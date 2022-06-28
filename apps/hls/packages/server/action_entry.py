from job_manager.packages.easy_tools import job_start_before, task_runner_celery


def update_entry(username, cmd_list):
    """
    更新
    :param username: 执行者
    :param cmd_list: 任务命令列表
    :return:
    """
    job_task, job_cmds = job_start_before("更新", username, update_entry, cmd_list)
    return task_runner_celery.delay(job_task, job_cmds)
