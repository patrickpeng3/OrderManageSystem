# -*- coding: utf-8 -*-
"""
cd /data/apps/cmdb_py3/ && /data/apps/cmdb_py3_env/bin/celery worker -A celery_task.celery_app -l info -E

cd /data/apps/cmdb_py3/ && /data/apps/cmdb_py3_env/bin/celery  worker -A  celery_task.celery_app -l info -E --logfile=/tmp/celerylog.log --pidfile=/tmp/celerypid.pid
"""

import os
from celery.task import Task
from celery import Celery, platforms

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cmdb_hls.settings")  # project_name 项目名称

platforms.C_FORCE_ROOT = True
# 创建实例
app = Celery()
# celery配置模块
app.config_from_object('celery_task.celeryconfig')
# 自动搜索任务
app.autodiscover_tasks(["job_manager.packages.easy_tools", "safety.tasks"])
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
# , "celery_task.tasks"


if __name__ == '__main__':
    app.start()
