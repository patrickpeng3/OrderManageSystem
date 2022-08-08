from celery.result import AsyncResult, allow_join_result
from celery_task import celery_app as app
import time
from cmdb_hls.cmdb_logger import SCRIPT_LOGGER


def get_result(celery_task):
    """
    单任务获取结果
    :param celery_task: celery异步任务
    :return:
    """
    pk = celery_task.task_id
    async = AsyncResult(id=pk, app=app)
    while True:
        if async.successful():
            result = async.get()
            return result
        elif async.failed():
            SCRIPT_LOGGER.info("{}任务执行失败！！！".format(celery_task.task_id))
            raise Exception("celery任务执行失败！")
        elif async.status == 'PENDING':
            pass
        elif async.sattus == 'STARTED':
            pass
        time.sleep(1)


def get_result_group(celery_group):
    """
    组任务获取结果
    :param celery_group: 组任务
    :return:
    """
    while True:
        if celery_group.ready():
            if celery_group.successful():
                while allow_join_result():
                    return celery_group.get()
            else:
                SCRIPT_LOGGER.info("组任务有执行失败的！！！")
                break
        else:
            pass
        time.sleep(1)









































