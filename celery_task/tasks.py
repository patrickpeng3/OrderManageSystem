import sys
sys.path.append("/data/gitlab/oam-admin/cmdb_hls")
from celery_task.celery_app import app


@app.task()
def my_task():
    print("输出：test")
    return "返回:test"


my_task.delay()
